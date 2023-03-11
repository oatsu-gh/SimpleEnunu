#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2023 oatsu
"""
1. UTAUプラグインのテキストファイルを読み取る。
2. LABファイル→WAVファイル
"""
import logging
import sys
import warnings
from datetime import datetime
from glob import glob
from os import chdir, listdir, makedirs, rename, startfile
from os.path import abspath, basename, dirname, exists, join, relpath, splitext
from pprint import pprint
from shutil import move
from tempfile import TemporaryDirectory, mkdtemp
from typing import List, Union

import colored_traceback.always  # pylint: disable=unused-import
import utaupy
import yaml
from nnmnkwii.io import hts
from scipy.io import wavfile
from utaupy.utils import ust2hts

# scikit-learn で警告が出るのを無視
warnings.simplefilter('ignore')

# my_package.my_moduleのみに絞ってsys.stderrにlogを出す
logging.basicConfig(stream=sys.stdout,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    level=logging.INFO)
logging.getLogger('simple_enunu')


# autopep8: off ----------------------------------

# ENUNUのフォルダ直下にあるフォルダやファイルをimportできるようにする
sys.path.append(dirname(__file__))
import enulib

try:
    import torch
except ModuleNotFoundError:
    print('----------------------------------------------------------')
    print('初回起動ですね。')
    print('PC環境に合わせてPyTorchを自動インストールします。')
    print('インストール完了までしばらくお待ちください。')
    print('----------------------------------------------------------')
#    enulib.install_torch.ltt_install_torch(sys.executable)
    enulib.install_torch.pip_install_torch(abspath(sys.executable))
    print('----------------------------------------------------------')
    print('インストール成功しました。')
    print('----------------------------------------------------------\n')
    import torch

# NNSVSをimportできるようにする
if exists(join(dirname(__file__), 'nnsvs-master')):
    sys.path.append(join(dirname(__file__), 'nnsvs-master'))
elif exists(join(dirname(__file__), 'nnsvs')):
    sys.path.append(join(dirname(__file__), 'nnsvs'))
else:
    logging.error('NNSVS directory is not found.')

import nnsvs  # pylint: disable=import-error
from nnsvs.svs import SPSVS
from utils import enunu2nnsvs  # pylint: disable=import-error

logging.debug(f'Imported NNSVS module: {nnsvs}')

# autopep8: on -------------------------------------


def get_project_path(path_utauplugin):
    """
    キャッシュパスとプロジェクトパスを取得する。
    """
    plugin = utaupy.utauplugin.load(path_utauplugin)
    setting = plugin.setting
    # ustのパス
    path_ust = setting.get('Project')
    # 音源フォルダ
    voice_dir = setting['VoiceDir']
    # 音声キャッシュのフォルダ(LABとJSONを設置する)
    cache_dir = setting['CacheDir']

    return path_ust, voice_dir, cache_dir


def wrapped_enunu2nnsvs(voice_dir, out_dir):
    """ENUNU用のディレクトリ構造のモデルをNNSVS用に再構築する。
    """
    # torch.save() の出力パスに日本語が含まれているとセーブできないので、一時フォルダを作ってそこに保存してから移動する。
    with TemporaryDirectory(prefix='.temp-enunu2nnsvs-', dir='.') as temp_dir:
        enunu2nnsvs.main(voice_dir, relpath(temp_dir))
        for path in listdir(temp_dir):
            move(join(temp_dir, path), join(out_dir, path))
    with open(join(voice_dir, 'enuconfig.yaml'), encoding='utf-8') as f:
        enuconfig = yaml.safe_load(f)
    rename(
        join(out_dir, 'kana2phonemes.table'),
        join(out_dir, basename(enuconfig['table_path'])))


def packed_model_exists(voice_dir: str) -> bool:
    """フォルダ内にNNSVSモデルがあるかどうかを返す

    Args:
        dir (str): Path of the directory
    """
    # SPSVSクラスを使う際に必要なNNSVSモデル用のファイル(の一部)
    required_files = {'config.yaml', 'qst.hed'}
    # 全ての要求ファイルがフォルダ内に存在するか調べて返す
    return all(map(exists, [join(voice_dir, p) for p in required_files]))


def find_table(model_dir: str) -> str:
    """ 歌詞→音素の変換テーブルを探す
    """
    table_files = glob(join(model_dir, '*.table'))
    if len(table_files) == 0:
        raise FileNotFoundError(f'Table file does not exist in {model_dir}.')
    elif len(table_files) > 1:
        logging.warn(f'Multiple table files are found. : {table_files}')
    logging.info(f'Using {basename(table_files[0])}')
    return table_files[0]


def main(path_plugin: str, path_wav: Union[str, None] = None, play_wav=True) -> str:
    """
    UTAUプラグインのファイルから音声を生成する
    """
    # USTの形式のファイルでなければエラー
    if not path_plugin.endswith('.tmp') or path_plugin.endswith('.ust'):
        raise ValueError('Input file must be UST or TMP(plugin).')
    # UTAUの一時ファイルに書いてある設定を読み取る
    logging.info('reading settings in TMP')
    path_ust, voice_dir, _ = get_project_path(path_plugin)
    path_enuconfig = join(voice_dir, 'enuconfig.yaml')

    # ENUNU=>1.0.0 または SimpleEnunu 用に作成されたNNSVSモデルの場合
    if packed_model_exists(join(voice_dir, 'model')):
        model_dir = join(voice_dir, 'model')
    # ENUNU 用ではない通常のNNSVSモデルの場合
    elif packed_model_exists(voice_dir):
        model_dir = voice_dir
        logging.warn(
            'NNSVS model is selected. This model might be not ready for ENUNU.')
    # ENUNU<1.0.0 向けの構成のモデルな場合
    elif exists(join(voice_dir, 'enuconfig.yaml')):
        logging.info(
            'Regacy ENUNU model is selected. Converting it for the compatibility...'
        )
        model_dir = join(voice_dir, 'model')
        makedirs(model_dir, exist_ok=True)
        print('----------------------------------------------')
        wrapped_enunu2nnsvs(voice_dir, model_dir)
        print('\n----------------------------------------------')
        logging.info('Converted.')
    # configファイルがあるか調べて、なければ例外処理
    else:
        raise Exception('UTAU音源選択でENUNU用モデルを指定してください。')
    assert model_dir

    # カレントディレクトリを音源フォルダに変更する
    chdir(voice_dir)

    # 日付時刻を取得
    str_now = datetime.now().strftime('%Y%m%d_%H%M%S')

    # wav出力パスが指定されていない(プラグインとして実行している)場合
    if path_wav is None:
        # 入出力パスを設定する
        if path_ust is not None:
            songname = splitext(basename(path_ust))[0]
            out_dir = dirname(path_ust)
            temp_dir = join(out_dir, f'{songname}_enutemp')
            path_wav = abspath(join(out_dir, f'{songname}__{str_now}.wav'))
        # WAV出力パス指定なしかつUST未保存の場合
        else:
            logging.info('USTが保存されていないので一時フォルダにWAV出力します。')
            songname = f'temp__{str_now}'
            out_dir = mkdtemp(prefix='enunu-')
            temp_dir = join(out_dir, f'{songname}_enutemp')
            path_wav = abspath(join(out_dir, f'{songname}__{str_now}.wav'))
    # WAV出力パスが指定されている場合
    else:
        songname = splitext(basename(path_wav))[0]
        out_dir = dirname(path_wav)
        temp_dir = join(out_dir, f'{songname}_enutemp')
        path_wav = abspath(path_wav)
    makedirs(temp_dir, exist_ok=True)
    path_full_score = join(temp_dir, f'{songname}.full')

    # モデルを読み取る
    logging.info('Loading models')
    engine = SPSVS(model_dir, device="cuda" if torch.cuda.is_available() else "cpu")
    config = engine.config

    # UST → LAB の変換をする
    logging.info('Converting UST -> LAB')
    enulib.utauplugin2score.utauplugin2score(
        path_plugin,
        find_table(model_dir),
        path_full_score,
        strict_sinsy_style=False
    )

    # フルラベルファイルを読み取る
    logging.info('Loading LAB')
    label = hts.load(path_full_score)

    # 音声を生成する
    logging.info('Generating WAV')
    wav_data, sample_rate = engine.svs(label, vocoder_type='auto')
    # TODO: float32で出力できるようにしたい。
    logging.debug(f'{wav_data.dtype}')
    wavfile.write(path_wav, rate=sample_rate, data=wav_data)

    # 音声を再生する。
    if exists(path_wav) and play_wav is True:
        startfile(path_wav)

    return path_wav


if __name__ == '__main__':
    logging.debug(f'sys.argv: {sys.argv}')
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1], None)
    elif len(sys.argv) == 1:
        main(input('Input file path of TMP(plugin)\n>>> ').strip('"'), None)
    else:
        raise Exception('引数が多すぎます。/ Too many arguments.')
