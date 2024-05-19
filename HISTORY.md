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
	- ust_editor: "%e/extensions/voicecolor_applier/voicecolor_applier.py"
    - timing_editor: "%e/extensions/velocity_applier.py"
```

- PyTorch を再インストールするためのバッチファイルを追加
- [SiFiGAN](https://github.com/chomeyama/SiFiGAN), [uSFGAN](https://github.com/chomeyama/UnifiedSourceFilterGAN) に対応

## v0.2.2

- UST加工ツール (ust_editor) で加工した結果が反映されていない不具合を直した。
- UST加工ツール (ust_editor) と タイミング加工ツール (timing_editor) として、それぞれ複数の拡張機能を呼び出せるようにした。

```yaml
# sample of config.yaml to activate extensions
extensions:
  - ust_editor:
    - "%e/extensions/voicecolor_applier/voicecolor_applier.py"
    - "%e/extensions/voicecolor_applier/lyric_nyaizer.py"
  - timing_editor:
    - "%e/extensions/velocity_applier.py"
```

- 拡張機能に **lyric_nyaizer** を追加。
  - ust_editor に指定して使用してください。歌詞を `ny a` にします。
