# Phase 2: コアエージェント実装計画 & 進捗管理

## 概要
- **目標**: Director Agent（企画・カット割りJSON生成）および Generator Agent（MiniMax Video-01 API非同期クライアント）の実装と単体検証。
- **ステータス**: ⏳ 準備完了（Phase 1およびドキュメント基盤完了後に着手）

---

## タスクブレイクダウン

### 1. Director Agent の実装
- [ ] **プロンプトテンプレート & スキーマ策定**:
  - `src/agents/director.py` の作成
  - Ollama APIクライアント経由で `ProjectPlan` JSONを確実に出力させるシステムプロンプトの設計
- [ ] **単体テスト & モック検証**:
  - トレンドキーワード入力から正常なカット割りJSONが生成されるかのテスト

### 2. Generator Agent の実装
- [ ] **MiniMax Video-01 APIクライアント**:
  - `src/agents/generator.py` の作成
  - 非同期タスク登録 (`POST /v1/video_generation`)
  - ポーリング (`GET /v1/query/video_generation`) と指数バックオフ
  - ダウンロード処理（一時ディレクトリ `temp/clips/` への保存）
- [ ] **APIレートリミット & Semaphore制御**:
  - 同時生成リクエスト数の制限ロジック

### 3. モック / オフライン検証モードの導入
- [ ] APIキー未設定時やテスト環境で動画生成をシミュレートするモッククライアントの実装
