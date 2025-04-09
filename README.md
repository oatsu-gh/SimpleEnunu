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

## How to activate extensions / 拡張機能の使い方

- `%e` : SimpleEnunu のフォルダ / The directory "simple_enunu.py" exists in
- `%v` : SimpleEnunu 用モデルのフォルダ / The directory voicebank and "config.yaml" exist in
- `%u` : UTAU のフォルダ / The directory "utau.exe" exists in

```yaml
# sample of config.yaml to activate extensions
extensions:
    ust_editor: "%e/extensions/voicecolor_applier/voicecolor_applier.py"
    timing_editor: "%e/extensions/velocity_applier.py"
```

## Bundled extensions / 同梱の拡張機能一覧

- voicecolor_applier (ust_editor)
  - `あ強` などの表情サフィックスを使用可能にします。（例：`強` が含まれる場合は `Power` をフラグ欄に追記します。）
- dummy (-)
  - とくに何もしません。デバッグ用です。
- f0_feedbacker (acoustic_editor)
  - ENUNUモデルで合成したピッチ線を UST のピッチにフィードバックします。EnuPitch のようなことができます。

- f0_smoother (acoustic_editor)
  - 急峻なピッチ変化を滑らかにします。

- lyric_nyaizer (ust_editor)
  - 歌詞を `ny a` にします。主にデバッグ用です。
- score_myaizer (score_editor)
  - 歌詞を `my a` にします。主にデバッグ用です。

- style_shifter (ust_editor, acoustic_editor)
  - USTのフラグ に `S5` や `S-3` のように記入することで、スタイルシフトのようなことができます。

- timing_repairer (timing_editor)
  - ラベル内の音素の発声時間に不具合がある場合に自動修正を試みます。
- velocity_applier (timing_editor)
  - USTの子音速度をもとに子音の長さを調節します。


## Development environment / 開発環境

- Windows 10
- Python 3.12.10
  - utaupy 1.19.1
  - numpy 1.26.4
  - torch   2.4.1+cu118
  - nnsvs (dev)
  - scikit-learn 1.4.2
- CUDA 12.6

## How to use the latest NNSVS (development version) / 同梱NNSVSの更新方法

1. Download the latest nnsvs from https://github.com/nnsvs/nnsvs
2. Replace local nnsvs-master directory

## 環境構築メモ

### python-3.12.7-embed-amd64 での環境構築手順

- pysptk をインストールするときに dll とか h ファイルとかが必要なので、インストール版の Python からコピーする。(2025/04/09)

  - python/include/  → python-embeddable/include/
  - python/libs/  → python-embeddable/libs/

- pysptk をインストールするときと uSFGAN を使うときに tcl/tk が必要なので、インストール版の Python から下記内容でコピーして対処。(2025/04/09)

  - python/tcl/  → python-embeddable/tcl/
  - python/Lib/tkinter/ → python/tkinter/
  - python/DLLs/\_tkinter.pyd → python-embeddable/\_tkinter.pyd 
  - python/DLLs/tcl86t.dll → python-embeddable/tcl86t.dll
  - python/DLLs/tk86t.dll→ python-embeddable/tk86t.dll 
  - python/DLLs/zlib1.dll → python-embeddable/zlib1.dll

- ```python
  python-3.12.10-embed-amd64\get-pip.py --no-warn-script-location
  python-3.12.10-embed-amd64\python.exe -m pip install -r requirements.txt --no-warn-script-location
  python-3.12.10-embed-amd64\python.exe -m pip install nnsvs
  python-3.12.10-embed-amd64\python.exe -m pip uninstall nnsvs torch torchaudio torchvision -y
  ```

- nnsvs をダウンロード (https://github.com/nnsvs/nnsvs)

- uSFGAN は HN-UnifiedSourceFilterGAN-nnsvs を DL

- ParallelWaveGAN は ParallelWaveGAN-nnsvs をDL (https://github.com/nnsvs/ParallelWaveGAN)

- SiFiGAN は SiFiGAN-nnsvs を DL (https://github.com/nnsvs/SiFiGAN)

  - pip で python embeddable に SiFiGAN をインストールする場合は docopt が無いとエラーが出るので、インストール版の Python から docopt をコピーして対処。(2024/05/19)
