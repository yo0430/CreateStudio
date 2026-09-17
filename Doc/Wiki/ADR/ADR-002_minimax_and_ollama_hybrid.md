# ADR-002: MiniMax API ＋ ローカルOllamaのハイブリッド構成の決定

## ステータス
**承認済 (Accepted)** - 2026-09-18

## コンテキスト
動画生成パイプラインにおいて、すべての推論（企画、カット割り、動画生成、フレーム評価）をクラウドAPI（例: GPT-4o + Runway/Pika）に依存すると、API利用料金が高騰し、レート制限やプライバシーの制約を受けます。  
一方、動画生成そのものはローカルGPU（一般家庭環境）では計算負荷が高すぎるため、高品質な動画生成APIの活用が不可欠です。

## 決定事項
以下のハイブリッド構成を採用する。
1. **企画・演出 (Director Agent)**: ローカルLLM（Ollama Llama 3.1等）または低コストLLM。
2. **動画生成 (Generator Agent)**: **MiniMax Video-01 API**（Hailuo AI）。高品質な720p/25fpsシネマティック映像を低コスト・高速度で非同期生成可能。
3. **フレーム検閲・スコアリング (Critic Agent)**: ローカルVision LLM（Ollama LLaVA / Llama-Vision等）を活用。動画フレームを大量にサンプリングして評価しても外部API費用が発生しない。
4. **編集・合成 (Assembler Agent)**: ローカルのFFmpeg / MoviePyで高速レンダリング。

## トレードオフ & 影響
- **メリット**: 運用コストを最小化しつつ、業界トップクラスの生成映像品質と自律検閲ループを実現。
- **留意点**: MiniMax APIの非同期ポーリングおよびOllamaのローカル起動状態監視を堅牢に実装する必要がある。

## 関連ドキュメント
- 👉 アーキテクチャ解説: [Doc/ARCHITECTURE.md](../../ARCHITECTURE.md)
- 👉 Generator仕様: [Doc/Spec/generator_agent.md](../../Spec/generator_agent.md)
