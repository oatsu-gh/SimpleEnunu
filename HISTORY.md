# 更新履歴

## v0.0.1

- 初配布
- 2023年1月8日時点でのNNSVSのファイルを同梱

## v0.1.0

- 初回起動時のPyTorchのインストール方法を変更
  - [light-the-torch](https://github.com/pmeier/light-the-torch) を使って最適なバージョンを自動判別するようにした。
- SimpleEnunuのバージョンの標準出力をPythonスクリプトからバッチファイルに移動

## v0.2.0+TimingEditable

- タイミング補正ツールを使用できるようにした。
- torch を ltt ではなく pip で 通常通りインストールするように変更尾。
  - 環境によっては light-the-torch が狙い通り動かない場合があるため
- CUDA11 環境向けの PyTorch のバージョンを2.0.0に変更
- 音声出力を 32bit float に変更
- プログラム面の変更として、 SPSVS を継承して SimpleEnunu クラスを使うようにした。メンテしづらくなった。
