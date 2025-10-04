import numpy as np
import sounddevice as sd
import tempfile
import scipy.io.wavfile as wav

#【numpy】
#行列やベクトルなど配列をつくれる
#数値計算やデータ分析に使われる

#【sounddevice】
#マイクから音声を録音したり、スピーカーから音声を再生したりできる
#リアルタイムの音声処理に使われる
#録音した音声データをnumpy配列として扱える

#【tempfile】
#一時的なファイルやディレクトリを作成するためのモジュール
#一時的なデータを保存するのに便利
#使い終わったら自動的に削除される

#【scipy.io.wavfile】
#WAV形式の音声ファイルを読み書きするためのモジュール
#音声データをnumpy配列として扱える
#音声データをWAVファイルとして保存するのに使われる

duration = 5  # 録音時間（秒） int型としてpythonが自動認識
sr = 16000  # wisperの推奨サンプリングレート 1秒間に16000回音を測定　上に同じ 

# 補足　PythonではC言語やJAVAなどのように型指定をしなくてもよい（宣言不要）

print("録音開始")

audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='int16')

#int(duration * sr)の理由
#duration = 5.0　だと duration * sr = 80000.0 となり、float型になってしまう
#sd.rec()の引数は整数でないといけない　→　int()で整数に変換

#channels=1 はモノラル録音を意味する　所謂チャンネル数（5.1chなど）

#dtype は データ型（Data Type） の指定
#int16 は 16ビットの符号付き整数という意味で、音声データの各サンプルを表すのに使われる
#0 000 0000 0000 0000 ～ 1 111 1111 1111 1111 の範囲の整数値を取る(10進数で言うと -32768 ～ 32767, 左の1bitで符号を表し, 残りの15bitで数値を表す)
#PCM（Pulse Code Modulation）方式での一般的な音声データ形式(パルス符号変調方式)
#PCM方式は、アナログ音声信号を一定の時間間隔でサンプリングし、その振幅を量子化(点で記録)してデジタル値に変換する方法
#wavファイルやCDなどの非圧縮音声フォーマットでよく使われる PCで扱う音声は 16bit が標準的（CD音質は16bit/44.1kHz）
#Whisper 用に録音するなら 16kHz, 16bit モノラルが推奨されてる

sd.wait()  # 録音終了まで待機

#待機が必要な理由
#sd.rec()は非同期関数であり、録音が完了する前に次のコードが実行される可能性がある

#同期関数
#タスク1 → 終わるまで待つ → タスク2

#非同期関数
#タスク1 → タスク2 → タスク1が終わるのを待つことなくタスク2が実行される
#つまり...録音が完了する前に次のコードが実行される可能性がある
#sd.wait() で同期化している

print("録音終了")


with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
    wav.write(tmpfile.name, sr, audio)
    print("保存先:", tmpfile.name)

# 録音した音声を再生して確認
sd.play(audio, sr)
sd.wait()
print("再生終了")

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#