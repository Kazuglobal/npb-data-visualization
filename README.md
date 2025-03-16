# NPB Data Visualization

NPB（日本野球機構）の選手データを収集し、可視化するプロジェクトです。

## 機能

- NPB全12球団の選手データをスクレイピング
- チーム別の選手一覧表示
- 選手詳細情報の表示
- リアルタイムデータ更新
- モダンなUI/UXデザイン

## 技術スタック

### バックエンド
- Python 3.11+
- FastAPI
- BeautifulSoup4
- aiohttp

### フロントエンド
- Next.js 14
- TypeScript
- Chakra UI
- React

## セットアップ

1. リポジトリのクローン:
```bash
git clone https://github.com/Kazuglobal/npb-data-visualization.git
cd npb-data-visualization
```

2. バックエンドのセットアップ:
```bash
# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# データの収集
python scraper/scraper.py

# APIサーバーの起動
cd api
uvicorn main:app --reload
```

3. フロントエンドのセットアップ:
```bash
cd frontend
npm install
npm run dev
```

## 使い方

1. ブラウザで http://localhost:3000 にアクセス
2. チーム選択タブでチームを選択
3. 選手一覧タブで選手データを確認

## API エンドポイント

- `GET /teams` - 全チームの一覧を取得
- `GET /players/{team_id}` - 指定チームの選手一覧を取得
- `GET /player/{player_id}` - 指定選手の詳細情報を取得
- `GET /statistics` - 全体の統計情報を取得

## 注意事項

- データは https://npb.jp/bis/players/ から取得しています
- 過度なリクエストを避けるため、適切な間隔でデータを更新してください
- スクレイピングの際は NPB公式サイトの利用規約を遵守してください

## ライセンス

MIT License