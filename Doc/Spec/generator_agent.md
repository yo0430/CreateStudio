# Generator Agent 仕様書 (Generator Agent Spec)

## 1. 概要
Generator Agentは、Director Agentが作成した各カットの仕様に基づき、MiniMax Video-01 APIを非同期に呼び出し、動画クリップを生成・ダウンロード・キャッシュするエージェントです。

---

## 2. MiniMax API インターフェース仕様

### 2.1 タスク生成リクエスト
- **メソッド**: `POST`
- **エンドポイント**: `https://api.minimax.chat/v1/video_generation`
- **ヘッダー**:
  - `Authorization: Bearer <MINIMAX_API_KEY>`
  - `Content-Type: application/json`
- **リクエストボディ**:
  ```json
  {
    "prompt": "Cinematic shot of a cyberpunk city, 8k",
    "model": "video-01",
    "prompt_optimizer": true
  }
  ```
- **レスポンス**:
  ```json
  {
    "task_id": "1234567890",
    "base_resp": {
      "status_code": 0,
      "status_msg": "success"
    }
  }
  ```

### 2.2 ステータス照会（ポーリング）
- **メソッド**: `GET`
- **エンドポイント**: `https://api.minimax.chat/v1/query/video_generation?task_id={task_id}`
- **ステータス値**:
  - `Processing`: 生成中（待機して再照会）
  - `Success`: 生成完了（`file_id` またはダウンロードURL取得）
  - `Fail`: 生成失敗（エラーログ記録）

---

## 3. レートリミット & 並行数管理
- 同時生成リクエスト数: 最大2タスク（API制限およびコスト抑制）
- ポーリング間隔: 初回5秒、その後10秒、15秒、20秒と指数バックオフ
- タイムアウト: 最大300秒（5分）
