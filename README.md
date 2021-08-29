# Ktuarto inside Tansu

## Ktuartoとは

https://github.com/keyhole0/Ktuarto 参照

## Ktuarto inside Tansuとは

QuartoのAI実装、及びモンテカルロ法等の汎用的なアルゴリズムの勉強のためKtuartoを改変したプロジェクト

## AI対戦方法

既にプロジェクト内に存在するAI同士で対戦する方法  

1. GitHubにサインインをする
1. [AI一覧](/ktuarto/AI)の各ファイルから、対戦させたい2つのAIのクラス名を選択。名前を控えておく
1. [GitHub Actionsのworkflow一覧](../..//actions)から `Buttle between AIs` を選択
    ![Image0](/docs/images/README.md/image0.png)
1. `Run workflow` をクリック
    ![Image1](/docs/images/README.md/image1.png)
1. 実行対象のBranch、1で控えた2つのAIの名前、試合回数を指定
1. `Run workflow` をクリック
1. F5等で画面を更新
1. 新規作成されたタスクの実行終了を待つ
1. 新規作成されたタスクをクリック
1. 出力されたログから実行結果を確認

## 開発環境構築方法

Requirements: Python >=3.9, Poetry >=1.1

1. Requirementsをインストール  
  インストール方法は各パッケージの公式ドキュメント参照
2. プロジェクトのルートディレクトリ直下で `poetry install` を実行
3. 同ディレクトリ直下で `poetry shell` を実行し開發用仮想環境へ入る

### コマンド実行例

``` sh
# Install Python >=3.9 if it doesn't exist
$ which python
$ which python3

# Install Poetry >=1.1 if it doesn't exist
$ which poetry

$ poetry install
$ poetry shell
```

作業終了後は `exit` で仮想環境から抜ける

## AI対戦方法 (開発用)

GitHub Actions上ではなくCLIから実行する方法

`poetry run COMMAND` 、もしくは仮想環境に入った状態で `COMMAND` を実行する  
詳しい実行方法は `poetry run ktuarto --help` もしくは[GitHub Actionsの設定ファイル](/.github/workflows/battle_between_AIs.yml)の `Run Ktuarto` で実行しているコマンドを参照

### コマンド実行例

``` sh
$ poetry shell
$ ktuarto --help
Usage: ktuarto [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  run
$ ktuarto run --help
Usage: ktuarto run [OPTIONS] YOUR_AI OPPONENT_AI

Options:
  --matches INTEGER  Number of matches (default: 1)
  --help             Show this message and exit.
```

## AI開発方法

新規AIは[`/ktuarto/AI`](/ktuarto/AI)に設置する

1. `base_ai.BaseAI` を継承したユニークな名前のclassを定義し、そのclassに `choice` メソッドと `put` メソッドを定義する  
  各メソッドの返り値は既に設置されているAI参考
2. [`/ktuarto/scripts/run.py`](/ktuarto/scripts/run.py)に `from ..AI.{新AIを書いたファイル名} import {新AIのclass名}` を追記
3. [`/ktuarto/AI/__init__.py`](/ktuarto/AI/__init__.py)に  `from .{新AIを書いたファイル名} import {新AIのclass名}` を追記

以上の作業終了後、各種AI対戦方法により対戦実行が可能
