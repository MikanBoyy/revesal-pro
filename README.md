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
├── .gitignore                # dist/ やローカル設定を除外
└── README.md                 # プロジェクトの説明、ビルド手順
```
