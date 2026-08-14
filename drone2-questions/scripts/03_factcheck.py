"""Phase 3: FACT-CHECK(Sonnet・精度重視)。

- 新規コンテキストで「問題+選択肢+正解+該当チャンク原文」だけを渡す
  (生成時のやり取りは一切見せない → 自己追認の防止)
- 3項目判定: answer_entailment / distractor_check / no_extra_info
- 全項目パスのみ通過(status: factchecked)。失敗は rejected/ へ判定理由付き
- 通過率が90%超の場合は検証が甘い可能性を警告

冪等: status が draft / needs_reverify の問題のみ処理。
"""

from __future__ import annotations

from common import (
    DRAFT_DIR,
    VERIFY_MODEL,
    anthropic_client,
    call_json,
    iter_questions,
    load_chunks,
    reject_question,
    save_json,
    setup_logging,
)

FACTCHECK_SCHEMA = {
    "type": "object",
    "properties": {
        "answer_entailment": {
            "type": "string",
            "enum": ["ENTAIL", "CONTRADICT", "NOT_FOUND"],
        },
        "distractor_check": {"type": "boolean"},
        "no_extra_info": {"type": "boolean"},
        "reason": {"type": "string"},
    },
    "required": ["answer_entailment", "distractor_check", "no_extra_info", "reason"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """あなたは無人航空機の学科試験問題のファクトチェック担当者です。
与えられた原文(Ground Truth)だけを根拠に、問題を厳格に検証してください。原文以外の知識・常識による補完は判定に使わないこと。

判定項目:
1. answer_entailment: 提示された正解が原文から論理的に導けるか。
   - ENTAIL: 原文から正解が確実に導ける
   - CONTRADICT: 原文と矛盾する
   - NOT_FOUND: 原文に根拠が見つからない
2. distractor_check: 全ての誤答選択肢が原文と本当に矛盾している(=偶然正しい誤答が1つもない)場合のみ true。
3. no_extra_info: 問題文・選択肢が原文にない情報を含んでいない場合のみ true。

疑わしい場合は不合格側に倒すこと。曖昧さを許容しない。
reason には判定の根拠を簡潔に記す。"""


def build_user_content(q: dict, chunk: dict) -> str:
    choices = "\n".join(f"  [{i}] {c}" for i, c in enumerate(q["choices"]))
    return (
        f"--- 原文(教則 {chunk['chunk_id']} {chunk['title']})ここから ---\n"
        f"{chunk['text']}\n"
        f"--- 原文ここまで ---\n\n"
        f"問題文: {q['question']}\n"
        f"選択肢:\n{choices}\n"
        f"正解: [{q['answer']}] {q['choices'][q['answer']]}\n"
        f"解説: {q['explanation']}"
    )


def main() -> None:
    logger = setup_logging("03_factcheck")
    chunks = load_chunks()
    client = anthropic_client()

    checked = passed = 0
    for path, q in iter_questions(DRAFT_DIR):
        if q["status"] not in ("draft", "needs_reverify"):
            continue
        chunk = chunks.get(q["source_chapter"])
        if chunk is None:
            reject_question(q, "chunk_not_found", q["source_chapter"])
            path.unlink()
            continue

        try:
            verdict = call_json(
                client, VERIFY_MODEL, SYSTEM_PROMPT,
                build_user_content(q, chunk), FACTCHECK_SCHEMA, max_tokens=2048,
            )
        except Exception as e:
            logger.error("%s: factcheck call failed: %s", q["question_id"], e)
            continue

        checked += 1
        ok = (
            verdict["answer_entailment"] == "ENTAIL"
            and verdict["distractor_check"]
            and verdict["no_extra_info"]
        )
        if ok:
            q["status"] = "factchecked"
            q["factcheck"] = verdict
            save_json(path, q)
            passed += 1
        else:
            reject_question(q, "factcheck_failed", verdict["reason"])
            path.unlink()
            logger.info("%s: rejected (%s)", q["question_id"], verdict["reason"])

    rate = passed / checked if checked else 0.0
    logger.info("checked=%d passed=%d rate=%.1f%%", checked, passed, rate * 100)
    if checked >= 20 and rate > 0.9:
        logger.warning(
            "通過率が90%%を超えています(%.1f%%)。検証が甘い可能性があります。"
            "プロンプトの厳格化を検討してください。", rate * 100,
        )


if __name__ == "__main__":
    main()
