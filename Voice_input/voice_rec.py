import numpy as np
import sounddevice as sd
import tempfile
import scipy.io.wavfile as wav
import whisper as wp
import os

#【numpy】
#行列やベクトルなど配列をつくれる
#数値計算やデータ分析に使われる

#【sounddevice】
#マイクから音声を録音したり、スピーカーから音声を再生したりできる
#リアルタイムの音声処理に使われる
#録音した音声データをnumpy配列として扱える

#【tempfile】
#Pythonの標準ライブラリ
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

#tempfile.NamedTemporaryFile(...)  tempfileモジュールのNamedTemporaryFile関数 
#一時ファイルを作って, ファイルオブジェクトを返す. ファイル名が一意に決まり, OSの一時ディレクトリ(temp)に作成される
#【withとは？】
#普通にファイルを作るプログラムを書いてみる↓

#f = open("test.txt", "w")
#f.write("hello")
#f.close()  　# ←自分で閉じないといけない

# f = open("test.txt", "w")　→ "test.txt" を「書き込みモード（w）」で開き,変数fに代入する（変数はfileやfpでもなんでもOK）
#f.write("hello")  → 変数f（test.txt）に, "hello"を書き込む
#f.close()  → fを閉じる（閉じないと, 他のプログラムから開けなかったり, データが保存されなかったりする）

#通常open()でファイルを開くと, 処理が終わった後にf.close()で閉じる必要がある
#withを使うと, ブロック(インデントで囲まれた部分. 後述する)を抜けるときに自動でclose()が呼ばれる
#つまり, 自分でclose()を書く必要がない
#先のコードをwithを使って書くと↓

#with open("test.txt", "w") as f:
#    f.write("hello")   # ←close()を書かなくてよい

#withブロックを抜けると自動でclose()が呼ばれる→→ファイルが開きっぱなしにならない
#【NamedTemporaryFile関数の引数説明】
#suffix=".wav"　→拡張子を指定（例：音声ファイル）
#delete=False　→ブロックを抜けても自動で削除しない
#as tmpfile → 変数tmpfileにファイルオブジェクトを代入する

    wav.write(tmpfile.name, sr, audio)
    print("保存先:", tmpfile.name)

#ブロックはこのインデントで囲まれている処理（wav.write(...)とprint(...）の部分）

#wav.write(...)  → scipy.io.wavfileモジュールのwrite関数で, データをwavファイルに書き込む(wavファイル専用の書き込み関数, その他.mp3などの圧縮形式には対応していない)
#.wavは非圧縮PCM形式の音声で, 単純なバイナリ構造だからPythonで簡単に書き込みができる
#【scipy.io.wavfile.write()関数の引数説明】
#tmpfile.name  → さっき作ったtempファイルの名前path
#sr  → サンプリングレート（16000Hz）
#audio  → 録音した音声データ（numpy配列）
# まとめると録音した音声 audio をNamedTemporaryFile関数で作った空の.wavに書き込み保存
#別に引数にサンプリングレートを指定しなくても, audio自体にサンプリングレートの情報は含まれているが, wav.write()関数は明示的に指定する必要がある
#なぜなら, 保存するときにサンプリングレートの情報がないと, 再生するときに正しい速度で再生できなくなるから（1秒あたりの測定回数ということを考えるとすぐわかる）

#print("保存先:", tmpfile.name)  → 保存先のファイルパスを表示


sd.play(audio, sr)      # 録音した音声を再生して確認, 引数にサンプリングレートを指定して正しい再生速度を設定
sd.wait()               # 非同期関数の処理
print("再生終了") 

#録音処理完了

print("Whisper(small)の読み込み中...")
# Whisperモデルの読み込み（軽量版なら "small" なども可）
model = wp.load_model("small")  # "tiny", "small", "medium", "large" も選べる
print("読み込み完了")

# 文字起こし
result = model.transcribe(tmpfile.name, language="ja")  # 日本語なら language="ja" tmpfile.name は音声ファイルのパスを引数に渡す



print("=== 文字起こし結果 ===")
print(result["text"])
# print(result) でもいいけど情報量が多いので, 文字おこしの結果のみ表示する場合は["text"]を指定する

for segment in result["segments"]:

#result["segments"]は音声ファイルを「時間ごとに小分けした区間」に分けた情報を持っている
#{
#  "id": 0,
#  "start": 0.0,
#  "end": 2.66,
#  "text": "いや、ノアライルズワンピース"
#}
#このように保存されている

    print(f"開始時間: {segment['start']:.2f}秒")
    print(f"終了時間: {segment['end']:.2f}秒")
    print(f"テキスト: {segment['text']}")
    print("---")



#音声ファイルを「時間ごとに小分けした区間」に分け、その区間の開始時間・終了時間・文字起こしテキストを順に表示している

