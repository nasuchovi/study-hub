"""drone2-questions パイプライン共通モジュール。

原則(仕様書 v1.0):
- 出典(章番号+根拠原文)を持たない問題は存在してはならない
- 生成と検証は別モデル・別コンテキスト(会話履歴を共有しない独立リクエスト)
- 数値は原文から一切変更しない
- 〔一等〕マーク付き項目は二等問題の生成対象から除外
- 各フェーズは冪等(status フィールドで管理。再実行しても二重処理しない)
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "source"
DRAFT_DIR = BASE_DIR / "generated" / "draft"
VERIFIED_DIR = BASE_DIR / "generated" / "verified"
REJECTED_DIR = BASE_DIR / "generated" / "rejected"
FINAL_DIR = BASE_DIR / "final"
REVIEW_DIR = BASE_DIR / "review"
LOGS_DIR = BASE_DIR / "logs"

PDF_PATH = SOURCE_DIR / "kyosoku_v4.pdf"
CHUNKS_PATH = SOURCE_DIR / "kyosoku_v4_chunks.json"
FINAL_PATH = FINAL_DIR / "questions_v4.json"

KYOSOKU_VERSION = "v4"

# モデル分担(仕様書 §0)。router.py 連携や変更は環境変数で上書き可。
GENERATE_MODEL = os.environ.get("DRONE2_GENERATE_MODEL", "claude-haiku-4-5")
VERIFY_MODEL = os.environ.get("DRONE2_VERIFY_MODEL", "claude-sonnet-5")

QUESTION_REQUIRED_FIELDS = [
    "question_id",
    "source_chapter",
    "source_quote",
    "kyosoku_version",
    "type",
    "angle",
    "question",
    "choices",
    "answer",
    "explanation",
    "status",
]

_NUM_RE = re.compile(r"\d+(?:\.\d+)?")


def setup_logging(phase: str) -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(phase)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        fh = logging.FileHandler(LOGS_DIR / f"{phase}.log", encoding="utf-8")
        fh.setFormatter(fmt)
        sh = logging.StreamHandler(sys.stderr)
        sh.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(sh)
    return logger


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")
    tmp.replace(path)


def normalize_text(text: str) -> str:
    """全角数字・英字を半角へ正規化(数値照合の前提を揃える)。"""
    return unicodedata.normalize("NFKC", text)


def extract_numbers(text: str) -> list[str]:
    """テキスト中の数値(小数含む)を文字列のまま抽出する。"""
    return sorted(set(_NUM_RE.findall(normalize_text(text))))


def load_chunks() -> dict[str, dict]:
    chunks = load_json(CHUNKS_PATH)
    return {c["chunk_id"]: c for c in chunks}


def iter_questions(directory: Path):
    for path in sorted(directory.glob("q_*.json")):
        yield path, load_json(path)


def reject_question(question: dict, reason: str, detail: str = "") -> Path:
    """問題を rejected/ へ理由付きで移動保存する。元ファイルは呼び出し側で削除。"""
    question = dict(question)
    question["status"] = "rejected"
    question["reject_reason"] = reason
    if detail:
        question["reject_detail"] = detail
    question["rejected_at"] = datetime.now(timezone.utc).isoformat()
    out = REJECTED_DIR / f"{question['question_id']}.json"
    save_json(out, question)
    return out


def validate_question_schema(q: dict) -> str | None:
    """スキーマ検証。問題があれば理由文字列、なければ None を返す。"""
    for field in QUESTION_REQUIRED_FIELDS:
        if field not in q:
            return f"missing_field:{field}"
    if not str(q.get("source_quote", "")).strip():
        return "missing_source"
    if not isinstance(q["choices"], list) or len(q["choices"]) < 2:
        return "invalid_choices"
    if not isinstance(q["answer"], int) or not (0 <= q["answer"] < len(q["choices"])):
        return "invalid_answer_index"
    if q["type"] not in ("ox", "multi4"):
        return "invalid_type"
    if q["angle"] not in ("A", "B", "C", "D"):
        return "invalid_angle"
    return None


def anthropic_client():
    import anthropic

    return anthropic.Anthropic()


def call_json(client, model: str, system: str, user_content: str, schema: dict,
              max_tokens: int = 4096):
    """構造化出力(JSON Schema 強制)で 1 リクエスト実行し、パース済み dict を返す。

    会話履歴は一切持たない独立リクエスト(自己追認防止のための別コンテキスト)。
    """
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user_content}],
        output_config={"format": {"type": "json_schema", "schema": schema}},
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("model refused the request")
    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)
