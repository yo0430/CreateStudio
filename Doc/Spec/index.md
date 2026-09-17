# 仕様書ポータル (Spec Hub)

本ディレクトリは、CreateStudioシステムの現在の確定仕様（What & How: Living Documentation）を管理します。  
コードの変更と仕様書の記述は常に完全に同期され、陳腐化を防ぎます。

---

## 🧭 仕様書一覧 (Spec MOC)

| 仕様書 | 対象コンポーネント | 概要 | 状態 | 関連実装 |
| :--- | :--- | :--- | :---: | :--- |
| **[content_pipeline.md](./content_pipeline.md)** | 全体パイプライン | 企画から投稿までのオーケストレーション仕様・非同期キュー | 確定 | `src/pipeline/` |
| **[director_agent.md](./director_agent.md)** | Director Agent | 企画・プロット・カット割り・構造化JSONスキーマ仕様 | 確定 | `src/agents/director.py`, `src/core/models.py` |
| **[generator_agent.md](./generator_agent.md)** | Generator Agent | MiniMax Video-01 API連携・非同期タスク・レート制限仕様 | 確定 | `src/agents/generator.py` |
| **[critic_agent.md](./critic_agent.md)** | Critic Agent | Vision LLM評価・フレームサンプリング・自己修復リトライ仕様 | 確定 | `src/agents/critic.py` |
| **[assembler_agent.md](./assembler_agent.md)** | Assembler Agent | FFmpegクリップ結合・テロップ・BGM・エンコード仕様 | 確定 | `src/agents/assembler.py` |

---

## 🔗 ナレッジ・ADRとの対応
* 全体設計方針: [ADR-001: LLM Wiki＋Spec駆動運用の採用](../Wiki/ADR/ADR-001_llm_wiki_and_spec_driven_docs.md)
* モデル選定: [ADR-002: MiniMax＋Ollamaハイブリッド構成](../Wiki/ADR/ADR-002_minimax_and_ollama_hybrid.md)
