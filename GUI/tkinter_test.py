#===================<<【危険】>>===================
#ファイル名が標準ライブラリと同じだと、自作ファイルが優先されてエラーになる
#Ex)tkinter.py, numpy.py, pandas.py, matplotlib.py, sklearn.py など

import tkinter as tk

#Pyhonの標準GUIライブラリ pipでインストール不要
import subprocess
import sys
from pathlib import Path






def run_script():
    # 実行したいPythonファイルのパス
    script_path = Path(r"C:\Users\hikar\Documents\VS_code\Python\Plan_αβ\Voice_input")
    
    if script_path.exists():
        # 現在のPython実行環境でファイルを実行
        subprocess.run([sys.executable, str(script_path)])
    else:
        print("指定されたファイルが存在しません。")
    
root = tk.Tk()

#rootはウィンドウ全体を指す変数
#こいつにいろいろぶら下げていくイメージ
#root: インスタンス（実物） Tk:クラス（設計図） Tk()はウィンドウを生成するクラス
#Pythonではクラスは慣習的に大文字で始まる

root.title("文字起こしAI") #ウィンドウのタイトルを設定
root.geometry("400x300") #ウィンドウのサイズを設定

label = tk.Label(
    root, 
    justify="center", 
    font=("KHドット道玄坂16", 20),
    text="文字起こしAIへようこそ\n")
label.place(x=50, y=10)#これを書くことでウィジェットが描写される

label = tk.Label(
    root, 
    justify="left",
    text="録音ボタンを押して話しかけると\n押してからの5秒間が文字起こしされます")
label.place(x=40, y=60)

button = tk.Button(
    root, 
    text="録音開始", 
    font=("けいふぉんと", 12),
    bd=5, 
    width=10,          # 幅（文字数）
    height=1,          # 高さ（行数）
    command=run_script)
button.place(x=250, y=60)

label = tk.Label(
    root, 
    justify="left",
    font=("けいふぉんと", 12),
    text="出力結果")
label.place(x=40, y=110)



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



root.mainloop()

#命令を実行し続ける（これがないとwindowが一瞬で閉じる）
#こいつがあることでウィンドウがユーザーの操作を待つことができる
#このloopの内側にいろいろ書いてく

