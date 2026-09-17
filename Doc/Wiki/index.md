# ナレッジポータル (Wiki Hub)

本ディレクトリは、Andrej Karpathy氏提唱の「LLM Wiki」思想に基づき、プロジェクトの「設計判断理由 (ADR)」「障害と教訓 (Troubleshooting)」「技術調査 (Research)」を蓄積・管理するナレッジベースです。

---

## 🧭 ナレッジ一覧 (Wiki MOC)

### 1. アーキテクチャ意思決定記録 (ADR)
* **[ADR-001: LLM Wiki＋Spec駆動ドキュメント管理アーキテクチャの採用](./ADR/ADR-001_llm_wiki_and_spec_driven_docs.md)**
* **[ADR-002: MiniMax API ＋ ローカルOllamaのハイブリッド構成の決定](./ADR/ADR-002_minimax_and_ollama_hybrid.md)**

### 2. 障害対応 & トラブルシューティング知見 (Troubleshooting)
* 今後の開発・運用で得られた普遍的教訓をここに追加します。

### 3. 技術調査 & フィージビリティ (Research)
* **[MiniMax Video-01 API 技術仕様・制約まとめ](./Research/minimax_video_api_spec.md)**

---

## 🔗 仕様書 (Spec/) との双方向リンク
* 各ADRや知見は、対応する確定仕様書 [Doc/Spec/index.md](../Spec/index.md) とリンクし、なぜその仕様になったのかを常に追跡可能に保ちます。
