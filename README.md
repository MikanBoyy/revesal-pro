# 概要

Revesal Pro は TradingView Pine Script v6 に対応した ZigZag 算出および描画のサンプルプロジェクトです。
`src/main.pine` をエントリーポイントとし、ZigZag 計算ロジックを機能ごとの疑似モジュール（`core_math.pine` / `rendering.pine` / `sr_engine.pine` / `state_machine.pine`）に分割して管理しています。

# パッケージ構成

```
├── .github/
│   └── workflows/              # 将来的にビルドを自動化するためのGitHub Actions
├── dist/                       # ビルド（結合）後のコード出力先
│   └── compiled_script.pine    # これをTradingViewにコピペする
├── src/                        # ソースコード本体
│   ├── main.pine               # エントリーポイント（//@version宣言、indicator設定、モジュールのinclude宣言と実行）
│   ├── core_math.pine          # ZigZag の純粋計算ロジック（描画に依存しない）
│   ├── rendering.pine          # ラベル・ライン・テーブル等の描画ロジック
│   ├── sr_engine.pine          # レジサポライン（SRLine）管理・出来高集計・SR遷移評価
│   └── state_machine.pine      # ピボット確定・レジーム管理・SR遷移のオーケストレーション
├── scripts/
│   ├── build.py                # 分割したファイルを1つに結合するPythonスクリプト
│   └── phase_gate.py           # Phase7/8用のビルド同期・検証ゲート
├── .gitignore                  # dist/ やローカル設定を除外
└── README.md                   # プロジェクトの説明、ビルド手順
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

1. `src/` 配下の `.pine` ファイル更新後は必ず `scripts/build.py` を実行して `dist/compiled_script.pine` を再生成する。
2. TradingView貼り付け用の正本は常に `dist/compiled_script.pine` とする。
3. 次フェーズへ進む前に `scripts/phase_gate.py` を通し、表示の手動確認（短期足/長期足）を完了する。
4. `src/*.pine` は UTF-8 BOM なしで保存する（BOM 混入は `phase_gate.py` が検出する）。
