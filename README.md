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

## Development environment / 開発環境

- Windows 10
- Python 3.9
  - utaupy 1.18.0
  - numpy 1.23.5
  - torch  1.13.1+cu117
  - nnsvs (dev)
  - scikit-learn 1.1.3
- CUDA 11.7
