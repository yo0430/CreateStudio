# 自律型動画生成パイプライン仕様 (Content Pipeline Spec)

## 1. 概要
本仕様は、企画テーマの入力から各エージェント（Director, Generator, Critic, Assembler, Post）が協調して1本の動画を完成させるパイプラインの動作仕様を定めます。

---

## 2. 実行シーケンス

```mermaid
sequenceDiagram
    autonumber
    participant User as ユーザー / トリガー
    participant Pipe as Pipeline Orchestrator
    participant Dir as Director Agent
    participant Gen as Generator Agent
    participant Crit as Critic Agent
    participant Asm as Assembler Agent
    participant Post as Post Agent

    User->>Pipe: 企画テーマ / キーワード入力
    Pipe->>Dir: 企画・脚本・カット割り生成要求
    Dir-->>Pipe: ProjectPlan (JSON)
    
    loop 各カットの生成 (並行 / 順次)
        Pipe->>Gen: CutPlan 生成リクエスト
        Gen-->>Pipe: クリップダウンロード完了 (cut_X.mp4)
        
        loop 自己修復ループ (最大3回)
            Pipe->>Crit: クリップ評価要求 (フレーム画像抽出)
            Crit-->>Pipe: CutEvaluation (PASS / RETRY)
            alt RETRY
                Pipe->>Gen: 修正プロンプト・シード値で再生成
                Gen-->>Pipe: 再生成クリップ
            else PASS
                Note over Pipe,Crit: 当該カット合格
            end
        end
    end
    
    Pipe->>Asm: 全合格クリップ結合 & ポスプロ要求
    Asm-->>Pipe: 完成動画 (master.mp4)
    Pipe->>Post: メタデータ生成 & 配信要求
    Post-->>Pipe: 投稿完了 (URL / ログ)
    Pipe-->>User: 完了報告
```

---

## 3. エラーハンドリング & フォールバック
1. **リトライ上限到達**:
   - 3回リトライしても Critic Agent の基準点（8.0点以上）に達しないカットがある場合、最高スコアのクリップを採用するか、人間への通知フラグ（`NeedsReview`）を付与してパイプラインを一時停止する。
2. **APIレートリミット到達 (HTTP 429)**:
   - 指数バックオフ（初期5秒、最大60秒）で自動待機・再試行。
3. **ディスク空き容量チェック**:
   - 生成開始前に `temp/` および `output/` に最低2GBの空き容量があるか検証。
