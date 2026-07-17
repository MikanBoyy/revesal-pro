# ZigZag 仕様メモ（リアルタイム高安値追従版）

## 目的
既存の `ta.pivothigh / ta.pivotlow` 由来の確定遅延を解消し、山谷の取りこぼしを抑えながら、ノイズに強いリアルタイム追従を実現する。

## 分割構成
`//#include` による疑似分割で以下を正本とする。

1. `src/zigzag/index.pine`
- ZigZag機能の集約エントリ。

2. `src/zigzag/core_math.pine`
- ER算出、反転閾値算出などの算出ロジックを集約。

3. `src/zigzag/rendering.pine`
- シグナルラベル管理とHUD描画を担当。

4. `src/zigzag/state_machine.pine`
- 高安値追従型の状態遷移本体。

5. `src/zigzag.pine`
- 旧include互換のラッパー。

## 新アルゴリズムの基準挙動
1. `rightBars` を使う挟み込み確定を廃止し、現在レッグの暫定高値/暫定安値を毎バー更新する。
2. 反転閾値は固定%ではなく、以下の価格幅を使う。
- `ThresholdPrice = (k × ATR) × (2.0 - ER)`
3. 上昇レッグでは `暫定高値 - ThresholdPrice` を下抜けたときに反転候補とする。
4. 下降レッグでは `暫定安値 + ThresholdPrice` を上抜けたときに反転候補とする。
5. 確定条件はERで切り替える。
- `ER >= ER強弱閾値`: 1本の終値ブレイクで即時確定
- `ER < ER強弱閾値`: 2本連続の終値ブレイクで確定
6. 確定した山谷のみを正規ピボットとしてS/Rライン管理へ引き渡す。
7. 未確定レッグは「最後の正規確定ピボット → 現在の暫定極値」を点線で1本だけ描画する。

## 入力項目（現行）
- ATR期間
- ATR乗数k
- ER期間
- ER強弱閾値
- HUDを表示
- シグナルを表示
- シグナル保持本数
- 表示ライン本数
- 未確定レッグを表示
- 上昇レッグ色
- 下降レッグ色
- ライン幅
- Max_Lines_Count
- Expiry_Bars_After_Break
- Res_Color / Sup_Color / Broken_Line_Color

## HUD表示（最小構成）
1. ER状態（強い/弱い + ER値）
2. 適用確定モード（1本抜け即時 / 2本連続確定）
3. 動的反転閾値（価格幅）
4. 最新確定方向（上方向 / 下方向 / 未確定）

## S/Rライン管理の仕様（維持）
1. 起点は `reversalConfirmSignal` で確定した正規ピボットのみ。
2. 状態は `Active(1) / Flipped(2) / Broken(3)`。
3. ブレイク確認は2段階。
- 足1: 終値でライン突破を検知し、足1高値/安値を記録
- 足2: 次バー終値で足1高値/安値更新時のみ確定
4. 遷移。
- Activeで成立: Flippedへ（役割反転）
- Flippedで成立: Brokenへ（グレー点線）
5. Brokenは `Expiry_Bars_After_Break` 経過で自動削除。

## 確認チェックリスト
1. 強い相場では1本目終値で反転確定する。
2. 弱い相場では2本連続終値でのみ反転確定する。
3. 右側バー待ちがなく、山谷確定の遅延が軽減されている。
4. 強トレンド中でも暫定極値の更新が継続し、山谷の取りこぼしが減る。
5. 反転確定時にS/Rラインが生成され、Active/Flipped/Brokenが正しく遷移する。
6. 未確定点線が常に1本で、暫定極値へ追従する。
7. 長時間表示でもライン・ラベル上限が機能し描画が破綻しない。

## 運用メモ
- リリース前に `python scripts/build.py` と `python scripts/phase_gate.py` を実行する。
- TradingView貼り付け用の正本は `dist/compiled_script.pine` を使う。
