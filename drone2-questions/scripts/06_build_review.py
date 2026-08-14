"""Phase 6: GATE 人間レビュー。

build(既定): verified/(status=checked)から各章最低1問+全体の10%をランダム抽出し、
  問題/正解/解説/根拠原文/章番号/教則ページ番号 を1画面に並べた単一ファイルの
  レビューHTMLを生成。承認・却下ボタンで judgment.json をダウンロードできる。

apply <judgment.json>: レビュー結果を反映。
  - 却下された問題は rejected/ へ(reason: "gate_rejected")
  - 却下が抽出数の5%を超えた章は、その章の全問題を status=needs_reverify に戻し
    draft/ へ移動(Phase 3〜5 を再実行)
  - 残った status=checked の全問題を final/questions_v4.json に出力
"""

from __future__ import annotations

import json
import random
import sys
from collections import defaultdict

from common import (
    DRAFT_DIR,
    FINAL_PATH,
    REVIEW_DIR,
    VERIFIED_DIR,
    iter_questions,
    load_chunks,
    load_json,
    reject_question,
    save_json,
    setup_logging,
)

SAMPLE_RATE = 0.10
REJECT_THRESHOLD = 0.05

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>drone2 GATE レビュー</title>
<style>
  body {{ font-family: sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; background: #fafafa; color: #222; }}
  .card {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 1rem 1.5rem; margin-bottom: 1.5rem; }}
  .card.approved {{ border-color: #2a2; background: #f3fbf3; }}
  .card.rejected {{ border-color: #c33; background: #fbf3f3; }}
  .meta {{ color: #666; font-size: 0.85rem; }}
  .quote {{ background: #f5f5ef; border-left: 4px solid #cc9; padding: 0.5rem 1rem; margin: 0.5rem 0; white-space: pre-wrap; font-size: 0.9rem; }}
  .choices li.correct {{ font-weight: bold; color: #161; }}
  button {{ padding: 0.4rem 1.2rem; margin-right: 0.5rem; cursor: pointer; border-radius: 4px; border: 1px solid #999; background: #fff; }}
  button.approve {{ border-color: #2a2; color: #2a2; }}
  button.reject {{ border-color: #c33; color: #c33; }}
  #export {{ position: fixed; bottom: 1rem; right: 1rem; background: #246; color: #fff; border: none; padding: 0.8rem 1.5rem; font-size: 1rem; }}
  #progress {{ position: fixed; bottom: 1rem; left: 1rem; background: #fff; border: 1px solid #ccc; padding: 0.5rem 1rem; border-radius: 4px; }}
</style>
</head>
<body>
<h1>二等無人航空機 問題GATEレビュー</h1>
<p>抽出 {count} 問(各章最低1問+全体の10%)。全問判定後「judgment.json を保存」を押し、
<code>python scripts/06_build_review.py apply review/judgment.json</code> で反映してください。</p>
<div id="cards"></div>
<div id="progress">0 / {count}</div>
<button id="export">judgment.json を保存</button>
<script>
const QUESTIONS = {questions_json};
const judgments = {{}};
const cards = document.getElementById("cards");

for (const q of QUESTIONS) {{
  const div = document.createElement("div");
  div.className = "card";
  div.id = "card-" + q.question_id;
  const choices = q.choices.map((c, i) =>
    `<li class="${{i === q.answer ? 'correct' : ''}}">[${{i}}] ${{esc(c)}}${{i === q.answer ? ' ← 正解' : ''}}</li>`).join("");
  div.innerHTML = `
    <div class="meta">${{esc(q.question_id)}} | 教則 ${{esc(q.source_chapter)}} ${{esc(q.chunk_title)}} | p.${{q.page}} | 角度${{esc(q.angle)}}</div>
    <h3>${{esc(q.question)}}</h3>
    <ul class="choices">${{choices}}</ul>
    <p><b>解説:</b> ${{esc(q.explanation)}}</p>
    <div class="quote"><b>根拠原文:</b>\n${{esc(q.source_quote)}}</div>
    <button class="approve">承認</button>
    <button class="reject">却下</button>`;
  div.querySelector(".approve").onclick = () => judge(q.question_id, "approved");
  div.querySelector(".reject").onclick = () => judge(q.question_id, "rejected");
  cards.appendChild(div);
}}

function esc(s) {{
  const d = document.createElement("div");
  d.textContent = String(s);
  return d.innerHTML;
}}

function judge(id, verdict) {{
  judgments[id] = verdict;
  const card = document.getElementById("card-" + id);
  card.className = "card " + verdict;
  document.getElementById("progress").textContent =
    Object.keys(judgments).length + " / " + QUESTIONS.length;
}}

document.getElementById("export").onclick = () => {{
  const blob = new Blob(
    [JSON.stringify({{judgments: judgments, sampled: QUESTIONS.map(q => q.question_id)}}, null, 2)],
    {{type: "application/json"}});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "judgment.json";
  a.click();
}};
</script>
</body>
</html>
"""


def collect_checked() -> list[tuple]:
    return [(p, q) for p, q in iter_questions(VERIFIED_DIR) if q["status"] == "checked"]


def build() -> None:
    logger = setup_logging("06_build_review")
    chunks = load_chunks()
    questions = collect_checked()
    if not questions:
        logger.error("status=checked の問題がありません。Phase 5 まで実行してください。")
        sys.exit(1)

    by_chapter: dict[str, list[dict]] = defaultdict(list)
    for _, q in questions:
        by_chapter[q["source_chapter"]].append(q)

    rng = random.Random(42)
    sampled: dict[str, dict] = {}
    for chapter_questions in by_chapter.values():
        pick = rng.choice(chapter_questions)
        sampled[pick["question_id"]] = pick
    target = max(len(sampled), round(len(questions) * SAMPLE_RATE))
    remaining = [q for _, q in questions if q["question_id"] not in sampled]
    rng.shuffle(remaining)
    for q in remaining[: max(0, target - len(sampled))]:
        sampled[q["question_id"]] = q

    payload = []
    for q in sampled.values():
        chunk = chunks[q["source_chapter"]]
        payload.append({
            "question_id": q["question_id"],
            "source_chapter": q["source_chapter"],
            "chunk_title": chunk["title"],
            "page": chunk["page"],
            "angle": q["angle"],
            "question": q["question"],
            "choices": q["choices"],
            "answer": q["answer"],
            "explanation": q["explanation"],
            "source_quote": q["source_quote"],
        })
    payload.sort(key=lambda q: q["question_id"])

    page = PAGE_TEMPLATE.format(
        count=len(payload),
        questions_json=json.dumps(payload, ensure_ascii=False),
    )
    out = REVIEW_DIR / "gate_review.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    logger.info("total=%d sampled=%d -> %s", len(questions), len(payload), out)


def apply_judgment(judgment_path: str) -> None:
    logger = setup_logging("06_apply_gate")
    data = load_json(judgment_path if judgment_path.startswith("/")
                     else (REVIEW_DIR.parent / judgment_path))
    judgments: dict[str, str] = data["judgments"]
    sampled: list[str] = data.get("sampled", list(judgments))
    missing = [qid for qid in sampled if qid not in judgments]
    if missing:
        logger.error("未判定の問題があります: %s", missing)
        sys.exit(1)

    questions = {q["question_id"]: (p, q) for p, q in collect_checked()}

    # 章ごとの却下率を集計
    sampled_by_ch: dict[str, list[str]] = defaultdict(list)
    for qid in sampled:
        if qid in questions:
            sampled_by_ch[questions[qid][1]["source_chapter"]].append(qid)

    reverify_chapters = set()
    rejected_count = 0
    for qid, verdict in judgments.items():
        if qid not in questions or verdict != "rejected":
            continue
        path, q = questions.pop(qid)
        reject_question(q, "gate_rejected")
        path.unlink()
        rejected_count += 1

    for chapter, qids in sampled_by_ch.items():
        n_rejected = sum(1 for qid in qids if judgments.get(qid) == "rejected")
        if qids and n_rejected / len(qids) > REJECT_THRESHOLD:
            reverify_chapters.add(chapter)

    reverified = 0
    for qid, (path, q) in list(questions.items()):
        if q["source_chapter"] in reverify_chapters:
            q["status"] = "needs_reverify"
            save_json(DRAFT_DIR / path.name, q)
            path.unlink()
            questions.pop(qid)
            reverified += 1
    if reverify_chapters:
        logger.warning(
            "却下率が5%%を超えた章 %s の全%d問を needs_reverify に戻しました。"
            "Phase 3〜5 を再実行してください。",
            sorted(reverify_chapters), reverified,
        )

    final = sorted((q for _, q in questions.values()), key=lambda q: q["question_id"])
    for q in final:
        q["status"] = "approved"
    save_json(FINAL_PATH, final)
    for path, q in questions.values():
        save_json(path, q)
    logger.info(
        "gate applied: rejected=%d reverify=%d final=%d -> %s",
        rejected_count, reverified, len(final), FINAL_PATH,
    )


def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] == "apply":
        if len(sys.argv) < 3:
            print("usage: 06_build_review.py apply <judgment.json>", file=sys.stderr)
            sys.exit(2)
        apply_judgment(sys.argv[2])
    else:
        build()


if __name__ == "__main__":
    main()
