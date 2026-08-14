"""Phase 5: 機械チェック(Python のみ・API 不要)。

1. 数値照合: 問題文・選択肢・解説中の数値が chunk の numbers_in_text に全て
   含まれるか(章番号の構成数値は許容)。逸脱 → reject(number_drift)
2. スコープ混入: 「一等」「レベル4」「カテゴリーIII」等の NG ワード照合。
   章ごとのホワイトリストは source/ngword_whitelist.json で管理
3. 正解分布: ○× 比率を集計し 45〜55% を外れたら警告(生成段階の角度指定で調整)
4. 重複検出: difflib ratio > 0.85 で実質同一問題を検出し後発を除外
5. 文字数: 問題文 20〜120 字、解説 50〜200 字

冪等: verified/ の status=verified のみ判定し、通過は status=checked に更新。
"""

from __future__ import annotations

import difflib

from common import (
    SOURCE_DIR,
    VERIFIED_DIR,
    extract_numbers,
    iter_questions,
    load_chunks,
    load_json,
    reject_question,
    save_json,
    setup_logging,
)

NG_WORDS = ["一等", "レベル4", "カテゴリーIII", "カテゴリーⅢ", "カテゴリー3"]
WHITELIST_PATH = SOURCE_DIR / "ngword_whitelist.json"

DUP_THRESHOLD = 0.85
QUESTION_LEN = (20, 120)
EXPLANATION_LEN = (50, 200)


def load_whitelist() -> dict[str, list[str]]:
    if WHITELIST_PATH.exists():
        return load_json(WHITELIST_PATH)
    return {}


def allowed_numbers(chunk: dict) -> set[str]:
    allowed = set(chunk["numbers_in_text"])
    # 解説の「教則3.1.2参照」等で章番号の構成数値が現れるのは正当
    allowed.update(chunk["chunk_id"].split("."))
    allowed.add(chunk["chunk_id"])
    for i in range(1, chunk["chunk_id"].count(".") + 1):
        allowed.add(".".join(chunk["chunk_id"].split(".")[: i + 1]))
    # 選択肢インデックス由来の 0〜4 は数値ドリフトとみなさない
    allowed.update({"0", "1", "2", "3", "4"})
    return allowed


def check_numbers(q: dict, chunk: dict) -> str | None:
    text = q["question"] + " ".join(q["choices"]) + q["explanation"]
    found = set(extract_numbers(text))
    drift = found - allowed_numbers(chunk)
    if drift:
        return f"numbers not in source: {sorted(drift)}"
    return None


def check_ng_words(q: dict, whitelist: dict[str, list[str]]) -> str | None:
    allowed = set(whitelist.get(q["source_chapter"], []))
    text = q["question"] + " ".join(q["choices"]) + q["explanation"]
    hits = [w for w in NG_WORDS if w in text and w not in allowed]
    if hits:
        return f"ng words: {hits}"
    return None


def check_length(q: dict) -> str | None:
    ql, el = len(q["question"]), len(q["explanation"])
    if not (QUESTION_LEN[0] <= ql <= QUESTION_LEN[1]):
        return f"question length {ql} not in {QUESTION_LEN}"
    if not (EXPLANATION_LEN[0] <= el <= EXPLANATION_LEN[1]):
        return f"explanation length {el} not in {EXPLANATION_LEN}"
    return None


def main() -> None:
    logger = setup_logging("05_mechanical")
    chunks = load_chunks()
    whitelist = load_whitelist()

    kept: list[tuple] = []  # (path, question) 既存 checked + 今回通過分(重複判定用)
    checked = rejected = 0

    for path, q in iter_questions(VERIFIED_DIR):
        if q["status"] == "checked":
            kept.append((path, q))

    for path, q in iter_questions(VERIFIED_DIR):
        if q["status"] != "verified":
            continue
        checked += 1
        chunk = chunks[q["source_chapter"]]

        reason = None
        for name, res in (
            ("number_drift", check_numbers(q, chunk)),
            ("scope_violation", check_ng_words(q, whitelist)),
            ("length_violation", check_length(q)),
        ):
            if res is not None:
                reason = (name, res)
                break
        if reason is None:
            for _, other in kept:
                ratio = difflib.SequenceMatcher(
                    None, q["question"], other["question"]
                ).ratio()
                if ratio > DUP_THRESHOLD:
                    reason = ("duplicate", f"similar to {other['question_id']} ({ratio:.2f})")
                    break

        if reason is not None:
            reject_question(q, reason[0], reason[1])
            path.unlink()
            rejected += 1
            logger.info("%s: rejected (%s: %s)", q["question_id"], *reason)
        else:
            q["status"] = "checked"
            save_json(path, q)
            kept.append((path, q))

    # 正解分布(○× 比率)の集計
    ox = [q for _, q in kept if q["type"] == "ox"]
    if ox:
        maru = sum(1 for q in ox if q["choices"][q["answer"]] == "○")
        ratio = maru / len(ox)
        logger.info("ox questions=%d maru_ratio=%.1f%%", len(ox), ratio * 100)
        if not (0.45 <= ratio <= 0.55):
            logger.warning(
                "○×比率が45〜55%%を外れています(○=%.1f%%)。"
                "生成段階の角度指定で偏り側を調整してください。", ratio * 100,
            )

    logger.info("checked=%d rejected=%d kept_total=%d", checked, rejected, len(kept))


if __name__ == "__main__":
    main()
