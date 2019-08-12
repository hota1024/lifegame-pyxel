# ダウンロード
「Clone or download」をクリックするか[こちら](https://github.com/hota1024/lifegame-pyxel/archive/master.zip)からリポジトリをダウンロードしてください。

# 環境の用意
このライフゲームはPythonのライブラリ[pyxel](https://github.com/kitao/pyxel/blob/master/README.ja.md)を使って開発しています。
pyxelを実行するには依存関係を解決してあげる必要があります。
インストールする依存パッケージは以下のとおりです。

## Windowsの場合
pyxelをインストールします。
```
pip3 install pyxel
```

## Mac OSの場合
pyxelとpython3とglfw,sdl2,sdl2_imageをインストールします。
python3とglfwなどのインストールには[Homebrew](https://brew.sh/index_ja)を使うため予めインストールしておいてください。
```
pip3 install pyxel
brew install python3 glfw sdl2 sdl2_image
```

# 使い方
ダウンロードしたファイルを解凍して、フォルダの中の`lifegame.py'をPython3で実行してください。

実行方法の例：
```
$ python3 lifegame.py
```

実行するとグリッドが出てきます。

クリックでセルを配置。
右クリックでセルを削除。
Rキーでランダム生成。
Cキーでクリア。
スペースキーで再生とポーズ切り替え。
右矢印キーで１世代進む。

