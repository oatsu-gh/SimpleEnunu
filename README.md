# SimpleEnunu

メンテしやすく、最新のNNSVSが使いやすいようにしたENUNUです。

Another ENUNU for enthusiasts and developers, easy to catch up with NNSVS.


## How to install / インストール方法

UTAU を起動し、**SimpleEnunu-{version}.zip** をUTAUのウィンドウにドラッグアンドドロップしてください。 

Launch UTAU and D&D SimpleEnunu-{version}.zip into the window.

## How to use / 使い方
1. UTAUを起動 / Launch UTAU
2. UTAU音源としてENUNU用のモデルを指定、またはNNSVS用のモデルを含むフォルダを選択 / Select the model on UTAU as voicebank
3. USTファイルを保存 / Save UST
4. ノートを2つ以上選択してプラグイン一覧からSimpleEnunuを起動 / Launch SimpleEnunu as a UTAU plugin

## How to use the latest NNSVS (development version) / 同梱NNSVSの更新方法

1. Download the latest nnsvs from https://github.com/nnsvs/nnsvs
2. Replace local nnsvs-master directory

## How to activate extensions / 拡張機能の使い方

- `%e` : SimpleEnunu のフォルダ / The directory "simple_enunu.py" exists in
- `%v` : SimpleEnunu 用モデルのフォルダ / The directory voicebank and "config.yaml" exist in
- `%u` : UTAU のフォルダ / The directory "utau.exe" exists in

```yaml
# sample of config.yaml to activate extensions
extensions:
	- ust_editor: "%e/voicecolor_applier/voicecolor_applier.py"
    - timing_editor: "%e/velocity_applier.py"
```
## Bundled extensions / 同梱の拡張機能一覧

- voicecolor_applier (ust_editor)
  - `あ強` などの表情サフィックスを使用可能にします。（例：`強` が含まれる場合は `Power` をフラグ欄に追記します。）

- dummy (-)
  - とくに何もしません。デバッグ用です。

- timing_repairer (timing_editor)
  - ラベル内の音素の発声時間に不具合がある場合に自動修正を試みます。

- velocity_applier (timing_editor)
  - USTの子音速度をもとに子音の長さを調節します。


## Development environment / 開発環境

- Windows 10
- Python 3.9
  - utaupy 1.18.3
  - numpy 1.23.5
  - torch  2.0.0+cu118
  - nnsvs (dev)
  - scikit-learn 1.1.3
- CUDA 11.7
