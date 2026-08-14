"""Phase 1: 教則PDFの章番号チャンク化。

- source/kyosoku_v4.pdf をテキスト抽出(pdfplumber)
- 章番号(1.1 / 3.1.2 / 6.2 など)単位で分割
- 〔一等〕マーク付きチャンクは is_first_class_only=true(生成対象から除外)
- 原文中の数値を numbers_in_text に保持(Phase 5 の照合用)

冪等: 出力は chunks JSON の全置換なので再実行しても安全。
"""

from __future__ import annotations

import re
import sys

from common import (
    CHUNKS_PATH,
    KYOSOKU_VERSION,
    PDF_PATH,
    extract_numbers,
    save_json,
    setup_logging,
)

# 行頭の「3.1.2 タイトル」形式を章見出しとみなす(末尾ピリオドなし・4階層まで)
HEADING_RE = re.compile(r"^\s*(\d{1,2}(?:\.\d{1,2}){0,3})\s+(\S.*)$")
FIRST_CLASS_MARK = "〔一等〕"


def extract_pages() -> list[tuple[int, str]]:
    import pdfplumber

    pages = []
    with pdfplumber.open(PDF_PATH) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages.append((i, text))
    return pages


def looks_like_heading(num: str, title: str, prev_num: str | None) -> bool:
    """目次行やページ内の偶発的な数値行を見出しと誤認しないための緩い判定。"""
    if len(title) > 60 and not title.startswith(FIRST_CLASS_MARK):
        # 長すぎる「タイトル」は本文の折り返しの可能性が高い
        return False
    if re.search(r"[。、]\s*$", title):
        return False
    if prev_num is None:
        return True
    # 章番号は概ね単調に進む。大きく逆戻りする番号は目次等の混入とみなす
    try:
        prev_major = int(prev_num.split(".")[0])
        cur_major = int(num.split(".")[0])
        return cur_major >= prev_major - 1
    except ValueError:
        return True


def build_chunks(pages: list[tuple[int, str]]) -> list[dict]:
    chunks: list[dict] = []
    current: dict | None = None
    prev_num: str | None = None

    for page_no, text in pages:
        for line in text.splitlines():
            m = HEADING_RE.match(line)
            if m and looks_like_heading(m.group(1), m.group(2), prev_num):
                if current:
                    chunks.append(current)
                num, title = m.group(1), m.group(2).strip()
                prev_num = num
                current = {
                    "chunk_id": num,
                    "title": title,
                    "text": "",
                    "kyosoku_version": KYOSOKU_VERSION,
                    "page": page_no,
                    "is_first_class_only": FIRST_CLASS_MARK in title,
                    "numbers_in_text": [],
                }
            elif current is not None:
                current["text"] += line + "\n"
    if current:
        chunks.append(current)

    # 同一 chunk_id が複数回現れた場合(目次と本文など)は本文の長い方を採用
    merged: dict[str, dict] = {}
    for c in chunks:
        c["text"] = c["text"].strip()
        prev = merged.get(c["chunk_id"])
        if prev is None or len(c["text"]) > len(prev["text"]):
            merged[c["chunk_id"]] = c

    result = list(merged.values())
    for c in result:
        body = f"{c['title']}\n{c['text']}"
        c["numbers_in_text"] = extract_numbers(body)
        if FIRST_CLASS_MARK in c["text"] and not c["is_first_class_only"]:
            # 本文中にのみ〔一等〕が含まれる場合は部分的な一等項目。
            # 保守的に除外はせず、生成プロンプト側で該当箇所を無視させるため印を残す
            c["contains_first_class_mark"] = True
    return result


def main() -> None:
    logger = setup_logging("01_chunk")
    if not PDF_PATH.exists():
        logger.error("PDF not found: %s — 国交省サイトから取得して配置してください", PDF_PATH)
        sys.exit(1)

    pages = extract_pages()
    chunks = build_chunks(pages)
    save_json(CHUNKS_PATH, chunks)

    excluded = sum(1 for c in chunks if c["is_first_class_only"])
    total_chars = sum(len(c["text"]) for c in chunks)
    logger.info(
        "chunks=%d total_chars=%d first_class_excluded=%d -> %s",
        len(chunks), total_chars, excluded, CHUNKS_PATH,
    )


if __name__ == "__main__":
    main()
