# 概要

Revesal Pro は TradingView Pine Script v6 に対応した ZigZag 算出および描画のサンプルプロジェクトです。
`src/zigzag.pine` に描画に依存しない ZigZag 計算ロジックを保持し、`src/main.pine` でインジケーター設定と描画ロジックを実装しています。

# パッケージ構成

```
├── .github/
│   └── workflows/              # 将来的にビルドを自動化する用のGitHub Actions
├── dist/                     # ビルド（結合）後のコード出力先
│   └── compiled_script.pine    # これをTradingViewにコピペする
├── src/                      # ソースコード本体
│   ├── main.pine               # 本処理（//@version宣言、indicator/strategy設定、およびエントリーポイント）
│   ├── zigzag.pine             # ZigZag の純粋計算ロジック（描画に依存しない）
│   ├── zigzag.md               # ZigZag の仕様書
├── scripts/
│   └── build.py                # 分割したファイルを1つに結合するPythonスクリプト
│   └── phase_gate.py           # Phase7/8用のビルド同期・検証ゲート
├── .gitignore                # dist/ やローカル設定を除外
└── README.md                 # プロジェクトの説明、ビルド手順
```

# ビルド手順

1. 通常ビルド

```bash
python scripts/build.py
```

2. Phase7/8ゲート（ビルド同期 + 静的検証 + 手動確認項目の表示）

```bash
python scripts/phase_gate.py
```

3. 既にビルド済みで検証だけ行う場合

```bash
python scripts/phase_gate.py --skip-build
```

# Phase7/8 運用ルール

1. `src/zigzag.pine` 更新後は必ず `scripts/build.py` を実行して `dist/compiled_script.pine` を再生成する。
2. TradingView貼り付け用の正本は常に `dist/compiled_script.pine` とする。
3. 次フェーズへ進む前に `scripts/phase_gate.py` を通し、表示の手動確認（短期足/長期足）を完了する。
