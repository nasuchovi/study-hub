# drone2-questions — 二等無人航空機操縦士 学科試験 問題生成パイプライン

「無人航空機の飛行の安全に関する教則(第4版)」(国土交通省, 令和7年2月1日)を唯一の
Ground Truth として、ファクトチェック済みの一問一答問題データベースを構築するパイプライン。

- 教則第4版 PDF: https://www.mlit.go.jp/koku/content/001860311.pdf
- 2025年4月17日以降の学科試験はこの第4版に準拠

## 絶対原則

1. 出典(章番号+根拠原文 `source_quote`)を持たない問題は存在してはならない → 自動リジェクト
2. 生成と検証は別モデル・別コンテキスト(独立APIリクエスト)で行う(自己追認の防止)
3. 数値(150m, 25kg, 100g, 80点 等)は言い換え時も原文から一切変更しない
4. 〔一等〕マーク付き項目は二等問題の生成対象から除外

## セットアップ

```bash
pip install anthropic pdfplumber
export ANTHROPIC_API_KEY=sk-ant-...   # または ant auth login

# 教則第4版の原本PDFを配置(改変禁止)
curl -L -o source/kyosoku_v4.pdf https://www.mlit.go.jp/koku/content/001860311.pdf
```

モデル分担(環境変数で上書き可):

| フェーズ | 既定モデル | 環境変数 |
|---|---|---|
| 生成 DRAFT | `claude-haiku-4-5`(コスト重視) | `DRONE2_GENERATE_MODEL` |
| FACT-CHECK / PROBE | `claude-sonnet-5`(精度重視) | `DRONE2_VERIFY_MODEL` |
| 最終 GATE | 人間のサンプリングレビュー | — |

## 実行順序

```bash
cd drone2-questions
python scripts/01_chunk.py          # PDF → source/kyosoku_v4_chunks.json
python scripts/02_generate.py       # チャンク → generated/draft/(Haiku)
python scripts/03_factcheck.py      # 3項目判定。不合格は generated/rejected/(Sonnet)
python scripts/04_probe.py          # 正解を伏せて逆解き。不一致は rejected(Sonnet)
python scripts/05_mechanical.py     # 数値照合/NGワード/重複/文字数(API不要)
python scripts/06_build_review.py   # review/gate_review.html を生成

# ブラウザで review/gate_review.html を開き承認/却下 → judgment.json を review/ に保存
python scripts/06_build_review.py apply review/judgment.json
# → final/questions_v4.json(却下率5%超の章は needs_reverify に戻る → Phase 3〜5 再実行)
```

各フェーズは冪等。`status` フィールド(draft → factchecked → verified → checked →
approved / rejected / needs_reverify)と `logs/generated_chunks.json` で管理しており、
再実行しても処理済みの問題は二重処理されない。

## ディレクトリ

```
source/      原本PDF(改変禁止)・章チャンク・NGワードホワイトリスト
generated/   draft(未検証)/ verified(FACT-CHECK+PROBE通過)/ rejected(理由付き)
final/       questions_v4.json(GATE通過済み本番データ)
review/      gate_review.html(人間レビュー用・単一ファイル)
logs/        各フェーズのログ・生成済みチャンクマーカー
```

## 検証パイプラインの内訳

- **Phase 3 FACT-CHECK**(新規コンテキストの Sonnet に問題+原文のみを渡す):
  1. `answer_entailment` — 正解が原文から導けるか(ENTAIL / CONTRADICT / NOT_FOUND)
  2. `distractor_check` — 誤答選択肢が本当に原文と矛盾しているか(偶然正しい誤答の排除)
  3. `no_extra_info` — 問題文が原文にない情報を含んでいないか

  通過率が90%を超える場合は検証が甘い可能性を疑い、プロンプトを厳格化する(ログに警告が出る)。
- **Phase 4 PROBE** — 別コンテキストで正解を伏せて解かせ、不一致は「問題が悪い」
  とみなして救済せずリジェクト(曖昧さ自体が欠陥)。
- **Phase 5 機械チェック** — 数値ドリフト/スコープ混入(NGワード)/○×比率45〜55%の
  監視/difflib類似度>0.85の重複除外/文字数(問題20〜120字・解説50〜200字)。
- **Phase 6 GATE** — 各章最低1問+全体の10%を抽出して人間がレビュー。却下が抽出数の
  5%を超えた章は全問題を再検証に回す。

## バージョン管理

- 全問題が `kyosoku_version: "v4"` を保持
- 教則第5版が出たら: 国交省の変更履歴(赤字版)から変更章リストを作成 → 該当
  `source_chapter` の問題の `status` を `"needs_reverify"` に変更して draft/ に戻す
  → Phase 3〜6 を再実行
- `final/questions_v4.json` は削除せず保持(差分検証の基準)

## アプリ側に必須の出典表記・免責

設定画面またはフッターに常設すること:

> 「無人航空機の飛行の安全に関する教則(第4版)」(国土交通省)(https://www.mlit.go.jp/koku/content/001860311.pdf)を加工して作成。
> 本アプリは国土交通省および指定試験機関とは無関係の非公式アプリです。収録問題は教則を基に独自に作成したものであり、実際の学科試験問題ではありません。

- 根拠: 国交省サイト利用ルール(政府標準利用規約準拠)— 出典記載/加工した旨の記載/国が作成したかのような態様の禁止
- `source_quote` はアプリに表示しない(内部検証用)。表示は章番号のみ
