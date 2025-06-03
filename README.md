# discord-bot

## 概要

Discord 上で動作する AI アシスタントボットです。
ボットは特定のコンテキストに基づいてユーザーからのメッセージに返信します。

- Discord API を使ったチャット機能
- Google Generative AI（`google-genai`）の統合
- `.env` による環境変数の管理
- `ruff` による静的解析
- `ty` による型安全性の向上（WIP）

---

## 必要環境＆準備物

- [uv](https://github.com/astral-sh/uv)（依存関係管理・仮想環境の作成に使用）
- Discord 開発者アカウントとボットトークン
- Generative AI API キー

---

## セットアップ手順

### 1. リポジトリをクローン

```bash
git clone https://github.com/your-username/discord-bot.git
cd discord-bot
```

### 2. 依存関係のインストール

```bash
uv sync
```

### 3. 仮想環境に入る

```bash
. .venv/bin/activate
```

### 4. 環境変数を設定する

```bash
cp ./.env.sample ./.env
```

### 5. コードの実行

```bash
uv run main.py
```

---

## デプロイ用

以下のコマンドを実行して、requirements.txt を生成します。

```bash
uv pip compile pyproject.toml > requirements.txt
```
