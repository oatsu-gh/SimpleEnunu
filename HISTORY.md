# 更新履歴

## v0.0.1

- 初配布
- 2023年1月8日時点でのNNSVSのファイルを同梱

## v0.1.0

- 初回起動時のPyTorchのインストール方法を変更
  - [light-the-torch](https://github.com/pmeier/light-the-torch) を使って最適なバージョンを自動判別するようにした。
- SimpleEnunuのバージョンの標準出力をPythonスクリプトからバッチファイルに移動

## v0.2.0+TimingEditable (クローズド配布)

- タイミング加工ツールを使用できるようにした。
- torch を ltt ではなく pip で 通常通りインストールするように変更尾。
  - 環境によっては light-the-torch が狙い通り動かない場合があるため
- CUDA11 環境向けの PyTorch のバージョンを2.0.0に変更
- 音声出力を 32bit float に変更
- プログラム面の変更として、 SPSVS を継承して SimpleEnunu クラスを使うようにした。メンテしづらくなった。

## v0.2.1

- UST加工ツール と タイミング加工ツール を使用できるようにした。
  - 通常の ENUNU と違い、ust_editor や timing_editor をリスト指定できないことに注意。

```yaml
# sample of config.yaml to activate extensions
extensions:
    ust_editor: "%e/extensions/voicecolor_applier/voicecolor_applier.py"
    timing_editor: "%e/extensions/velocity_applier.py"
```

- PyTorch を再インストールするためのバッチファイルを追加
- [SiFiGAN](https://github.com/chomeyama/SiFiGAN), [uSFGAN](https://github.com/chomeyama/UnifiedSourceFilterGAN) に対応

## v0.2.2

- UST加工ツール (ust_editor) で加工した結果が反映されていない不具合を直した。
- UST加工ツール (ust_editor) と タイミング加工ツール (timing_editor) として、それぞれ複数の拡張機能を呼び出せるようにした。

```yaml
# sample of config.yaml to activate extensions
extensions:
  ust_editor:
    - "%e/extensions/voicecolor_applier/voicecolor_applier.py"
    - "%e/extensions/voicecolor_applier/lyric_nyaizer.py"
  timing_editor:
    - "%e/extensions/velocity_applier.py"
```

- 拡張機能に **lyric_nyaizer** を追加。
  - ust_editor に指定して使用してください。歌詞を `ny a` にします。

## v0.3.0

- 実行時に「名前を付けて保存」ダイアログを表示するように仕様変更。
  - LABなどの中間ファイルは変わらずustと同じフォルダに生成されます。
- 必要なライブラリのインストール元を下記に変更
  - SiFiGAN (https://github.com/nnsvs/SiFiGAN)
  - uSFGAN (https://github.com/nnsvs/HN-UnifiedSourceFilterGAN)
  - ParallelWaveGAN (https://github.com/nnsvs/ParallelWaveGAN)
- PyTorch のインストールに light-the-torch を使用するように変更。

## v0.3.1

- PyTorch のインストールに失敗する不具合を修正。
- 「名前を付けて保存」のタイミングを音声合成前ではなく音声合成後に変更。
  - 保存わすれで時間を無駄にするのを防ぐため。

## v0.4.0

- 拡張機能機能実行時に、UTAUにフィードバックするためのTMPファイルのパスを `--feedback` の引数で渡すようにした。
- ピッチ加工ツールやスタイルシフトツールなどの拡張機能を指定する、`acoustic_editor` を使えるようにした。
  - 拡張機能 f0_smoother を追加 (ENUNUからのコピー)
  - 拡張機能 f0_feedbacker を追加 (EnuPitchからコピーしてすこし改良)
  - 拡張機能 style_shifter を追加 (ENUNUからのコピー)

```yaml
# sample of config.yaml to activate extensions
extensions:
  ust_editor:
    - "%e/extensions/voicecolor_applier/voicecolor_applier.py"
    - "%e/extensions/voicecolor_applier/lyric_nyaizer.py"
    - "%e/extensions/style_shifter.py"
  timing_editor:
    - "%e/extensions/velocity_applier.py"
  acoustic_editor:
    - "%e/extensions/style_shifter.py"
    - "%e/extensions/f0_smoother.py"
```

## v0.5.0

- 同梱のpython を 3.12.10 に更新。

- 拡張機能 (extensions) を使用しないモデルが動作しない不具合を修正。

- repair_packages.bat を追加。torch と utaupy をユーザー側でアップグレードできる。

- 実行時のコマンドライン引数の取り扱いを変更

  - 第1引数 `ust` (必須): 入力ファイルのパス。USTまたはTMPファイル。
  - オプション引数 (任意) `--wav`: WAV出力パス。指定なしの場合は NULL として扱ってレンダリング後に「名前を付けて保存」する。
  - オプション `--play` (任意): 実行引数に含まれると TRUE として扱われて WAV合成後に再生 する。なければFALSE。

  ```cmd
  python.exe simple_enunu.py [-h] [--wav WAV] [--play] ust
  ```
