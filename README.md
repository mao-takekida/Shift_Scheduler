# この python スクリプトについて
シフトを計算するための python スクリプトです。

# 使い方

## 1. 事前準備

### 1.1. python 仮想環境の作成
python の仮想環境を作成し、必要なライブラリをインストールしてください。
以下のコマンドを実行してください。

#### macOS の場合
```bash
# この README.md があるディレクトリに移動.
cd path/to/this/directory # 各自の環境に合わせてください

# 仮想環境を作成 python3
python3 -m venv venv

# 仮想環境を有効化 (有効化されると、プロンプトに (venv) が表示されます。)
source venv/bin/activate

# ライブラリをインストール
pip install -r requirements.txt
```

#### Windows (Git Bash) の場合
```bash
# この README.md があるディレクトリに移動.
cd path/to/this/directory # 各自の環境に合わせてください

# 仮想環境を作成 python3
python3 -m venv venv

# 仮想環境を有効化 (有効化されると、プロンプトに (venv) が表示されます。)
source venv/Scripts/activate

# ライブラリをインストール
pip install -r requirements.txt
```

## 2. python スクリプトを実行


例として, 以下のコマンドを実行してください。
```bash
python src/run_gui.py
```

ログレベルを指定してログを出力することもできます。
```bash
python src/run_gui.py -l DEBUG
```

詳しくは
```bash
python src/run_gui.py --help
```
を確認してください。

## 3. 実行ファイルの作成 (macOS, Windows)
pyinstaller を使って、実行ファイルを作成することができます。

以下のコマンドを実行してください。
```bash
pyinstaller --noconsole --add-data "config/config.json:config" --name shift_scheduler --icon=icon/feather_pen.ico src/run_gui.py
```

アプリケーションは `dist/shift_scheduler.app` に作成されます。
ダブルクリックで実行することができます。


# 以下は、開発者向けの情報です。

## pre-commit によるコードフォーマットと静的解析を行うことができます。
```bash
pre-commit install
```
