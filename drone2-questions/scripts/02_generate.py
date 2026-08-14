"""Phase 2: 問題生成 DRAFT(Haiku・コスト重視)。

- 1チャンクずつ渡す。渡すのは該当チャンクの原文のみ(他章の知識を混ぜさせない)
- 1チャンクから3〜5問、角度 A(定義)/B(適用場面)/C(例外)/D(誤り選択肢型)
- スキーマ不備・source_quote 欠落は即 rejected/(reason: "missing_source" 等)

冪等: チャンクごとに生成済みマーカー(logs/generated_chunks.json)で管理。
"""

from __future__ import annotations

import json

from common import (
    DRAFT_DIR,
    GENERATE_MODEL,
    KYOSOKU_VERSION,
    LOGS_DIR,
    REJECTED_DIR,
    VERIFIED_DIR,
    anthropic_client,
    call_json,
    load_chunks,
    load_json,
    reject_question,
    save_json,
    setup_logging,
    validate_question_schema,
)

MARKER_PATH = LOGS_DIR / "generated_chunks.json"

GENERATION_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source_quote": {"type": "string"},
                    "type": {"type": "string", "enum": ["ox", "multi4"]},
                    "angle": {"type": "string", "enum": ["A", "B", "C", "D"]},
                    "question": {"type": "string"},
                    "choices": {"type": "array", "items": {"type": "string"}},
                    "answer": {"type": "integer"},
                    "explanation": {"type": "string"},
                },
                "required": [
                    "source_quote", "type", "angle", "question",
                    "choices", "answer", "explanation",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["questions"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """あなたは二等無人航空機操縦士の学科試験対策問題を作成する出題者です。
与えられた「無人航空機の飛行の安全に関する教則(第4版)」の一章の原文だけを根拠に、一問一答問題を3〜5問作成してください。

厳守事項:
- 根拠は与えられた原文のみ。原文にない情報・一般知識での補完は禁止。
- 各問題に source_quote(根拠となる原文の一節をそのまま引用)を必ず付ける。source_quote は原文の連続した一節を一字一句そのまま抜き出すこと。
- 数値(150m, 25kg, 100g, 80点 等)は source_quote と一字一句同じものだけ使用可。言い換え時も数値は一切変更しない。
- 「〜できる/〜しなければならない/〜してはならない」の助動詞は、原文の義務・許可・禁止の区分を厳守する。
- 問題文は原文の丸写し禁止。言い換えで作成する。
- 〔一等〕マークが付いた箇所は一等無人航空機操縦士向けのため、出題対象にしない。
- 「一等」「レベル4」「カテゴリーIII」など二等の範囲外の語は、原文がその章で明示的に扱っている場合を除き使用しない。

出題角度(3〜5問の中で分散させる):
- A: 定義そのものを問う(○×)
- B: 適用場面・具体例を問う
- C: 例外・限定条件を問う
- D: 誤り選択肢型(4択。原文だけで明確に誤りと判断できる選択肢を作れる場合のみ)

形式:
- type "ox" の場合 choices は ["○", "×"] の2択。
- type "multi4" の場合 choices は4つ。
- answer は正解の choices 内インデックス(0始まり)。
- explanation は章番号を明記した解説(50〜200字)。
- question は20〜120字。"""


def load_marker() -> dict:
    if MARKER_PATH.exists():
        return load_json(MARKER_PATH)
    return {}


def existing_question_ids() -> set[str]:
    ids = set()
    for d in (DRAFT_DIR, VERIFIED_DIR, REJECTED_DIR):
        for p in d.glob("q_*.json"):
            ids.add(p.stem)
    return ids


def main() -> None:
    logger = setup_logging("02_generate")
    chunks = load_chunks()
    marker = load_marker()
    client = anthropic_client()

    targets = [
        c for c in chunks.values()
        if not c["is_first_class_only"] and len(c["text"]) >= 80
    ]
    logger.info("model=%s target_chunks=%d (skip generated=%d)",
                GENERATE_MODEL, len(targets),
                sum(1 for c in targets if marker.get(c["chunk_id"])))

    total_ok = total_rejected = 0
    for chunk in sorted(targets, key=lambda c: c["chunk_id"]):
        cid = chunk["chunk_id"]
        if marker.get(cid):
            continue

        user_content = (
            f"章番号: {cid}\n"
            f"タイトル: {chunk['title']}\n"
            f"--- 原文ここから ---\n{chunk['text']}\n--- 原文ここまで ---"
        )
        try:
            result = call_json(
                client, GENERATE_MODEL, SYSTEM_PROMPT, user_content,
                GENERATION_SCHEMA, max_tokens=8192,
            )
        except Exception as e:  # モデル拒否・パース失敗等はチャンク単位でスキップして続行
            logger.error("chunk %s: generation failed: %s", cid, e)
            continue

        seq = 0
        for raw in result.get("questions", []):
            seq += 1
            q = dict(raw)
            q["question_id"] = f"q_{cid}_{seq:03d}"
            q["source_chapter"] = cid
            q["kyosoku_version"] = KYOSOKU_VERSION
            q["status"] = "draft"

            error = validate_question_schema(q)
            if error is not None:
                reason = "missing_source" if error == "missing_source" else "schema_error"
                reject_question(q, reason, error)
                total_rejected += 1
                continue
            # source_quote が原文に実在するかの機械チェック(空白差は許容)
            quote = "".join(q["source_quote"].split())
            body = "".join((chunk["title"] + chunk["text"]).split())
            if quote not in body:
                reject_question(q, "quote_not_in_source")
                total_rejected += 1
                continue

            save_json(DRAFT_DIR / f"{q['question_id']}.json", q)
            total_ok += 1

        marker[cid] = {"questions": seq}
        save_json(MARKER_PATH, marker)
        logger.info("chunk %s: %d questions", cid, seq)

    logger.info("done: draft=%d rejected=%d", total_ok, total_rejected)


if __name__ == "__main__":
    main()
