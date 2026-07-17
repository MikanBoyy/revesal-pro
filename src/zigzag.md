# ZigZag 仕様書

このドキュメントは、`src/zigzag.pine` に実装された ZigZag 計算ロジックの仕様と設計意図を説明します。

## 概要
`src/zigzag.pine` は描画に依存しない純粋計算モジュールです。`main.pine` から `zigzag_core(...)` を呼び出し、計算結果を `zigzag_draw(...)` などの描画ロジックに渡します。

内部では `enum ZigZagAnchorType` を用いてアンカー状態を明確にし、処理を小さな補助関数に分離しています。

## API

### zigzag_core(high, low, left, right, threshold, thresholdIsPercent)

- 説明
  - 高値と安値の系列から現在確定中の ZigZag アンカー価格を算出します。
  - 既存アンカーの延長、極値追跡、反転判定を行います。

- 引数
  - `high` (float): 高値系列
  - `low` (float): 安値系列
  - `left` (int): ピボット判定の左側バー数
  - `right` (int): ピボット判定の右側バー数
  - `threshold` (float): 反転に必要な値幅。`thresholdIsPercent=false` の場合は価格単位。
  - `thresholdIsPercent` (bool): `threshold` を直近アンカー価格のパーセント比として扱うかどうか

- 戻り値
  - `float` 系列: 現在確定中の ZigZag アンカー価格。アンカー未確定期間は `na`。

### 補助関数

`zigzag.pine` は内部に以下のような小さなメソッドを持ち、処理を分離しています。

- `find_pivot_high(...)` / `find_pivot_low(...)` - ピボット検出を抽象化
- `resolve_threshold(...)` - パーセント基準と価格単位のしきい値計算
- `update_extreme_val(...)` - 現在レッグの極値追跡
- `should_extend_high(...)`, `should_extend_low(...)` - 延長判定
- `should_reverse_to_low(...)`, `should_reverse_to_high(...)` - 反転判定

## 設計

`zigzag_core()` は `ta.pivothigh` / `ta.pivotlow` の確定バーのみを利用し、
描画ロジックと切り離した計算専用の API を提供します。

### 処理フロー

1. `ta.pivothigh` / `ta.pivotlow` で高値/安値ピボットを検出
2. 現在のスイング方向に応じて極値（高値アンカー時は最安値、安値アンカー時は最高値）を追跡
3. 逆方向ピボットとしきい値の両方が成立した場合に反転を確定
4. 反転時には現在の極値を次のアンカーとして採用

## 使用例

`src/main.pine` では以下のように利用します。

```pine
//#include "zigzag.pine"

left = input.int(5, "Left", minval=1)
right = input.int(5, "Right", minval=1)
zigzagWidth = input.int(2, "ZigZag Line Width")
threshold = input.float(1.5, "Threshold", minval=0.0)
thresholdIsPercent = input.bool(true, "Threshold is Percent")
upColor = input.color(color.new(color.lime, 0), "Up ZigZag Color")
downColor = input.color(color.new(color.red, 0), "Down ZigZag Color")

zigzagValue = zigzag_core(high, low, left, right, threshold, thresholdIsPercent)
zigzag_draw(zigzagValue, zigzagWidth, upColor, downColor, right)
```
