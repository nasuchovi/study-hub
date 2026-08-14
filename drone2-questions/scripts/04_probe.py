"""Phase 4: PROBE 逆解き(Sonnet・別コンテキスト)。

- 正解を伏せて「問題+選択肢+該当チャンク原文」を渡し解答させる
- 生成時の answer と不一致 → 曖昧問題として rejected/(reason: "probe_mismatch")
- 不一致は「問題が悪い」とみなす。モデル側の誤答と判断して救済しない

冪等: status が factchecked の問題のみ処理。通過は verified/ へ移動(status: verified)。
"""

from __future__ import annotations

from common import (
    DRAFT_DIR,
    VERIFIED_DIR,
    VERIFY_MODEL,
    anthropic_client,
    call_json,
    iter_questions,
    load_chunks,
    reject_question,
    save_json,
    setup_logging,
)

PROBE_SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "integer"},
        "reasoning": {"type": "string"},
    },
    "required": ["answer", "reasoning"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """あなたは無人航空機の学科試験の受験者です。
与えられた原文だけを根拠に問題を解き、正解の選択肢インデックス(0始まり)を答えてください。
原文以外の知識は使わないこと。reasoning には根拠を簡潔に記すこと。"""


def build_user_content(q: dict, chunk: dict) -> str:
    choices = "\n".join(f"  [{i}] {c}" for i, c in enumerate(q["choices"]))
    return (
        f"--- 原文(教則 {chunk['chunk_id']} {chunk['title']})ここから ---\n"
        f"{chunk['text']}\n"
        f"--- 原文ここまで ---\n\n"
        f"問題文: {q['question']}\n"
        f"選択肢:\n{choices}"
    )


def main() -> None:
    logger = setup_logging("04_probe")
    chunks = load_chunks()
    client = anthropic_client()

    probed = passed = 0
    for path, q in iter_questions(DRAFT_DIR):
        if q["status"] != "factchecked":
            continue
        chunk = chunks[q["source_chapter"]]

        try:
            result = call_json(
                client, VERIFY_MODEL, SYSTEM_PROMPT,
                build_user_content(q, chunk), PROBE_SCHEMA, max_tokens=2048,
            )
        except Exception as e:
            logger.error("%s: probe call failed: %s", q["question_id"], e)
            continue

        probed += 1
        if result["answer"] == q["answer"]:
            q["status"] = "verified"
            q["probe"] = {"answer": result["answer"]}
            save_json(VERIFIED_DIR / path.name, q)
            path.unlink()
            passed += 1
        else:
            detail = (
                f"probe answered [{result['answer']}], "
                f"expected [{q['answer']}]: {result['reasoning']}"
            )
            reject_question(q, "probe_mismatch", detail)
            path.unlink()
            logger.info("%s: rejected (probe_mismatch)", q["question_id"])

    logger.info("probed=%d passed=%d", probed, passed)


if __name__ == "__main__":
    main()
