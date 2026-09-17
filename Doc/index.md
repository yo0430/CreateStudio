# CreateStudio ドキュメンテーション & ナレッジポータル (Doc Hub)

ようこそ、**CreateStudio** の公式ドキュメンテーションポータルへ。  
本プロジェクトは、Andrej Karpathy氏が提唱した**「LLM Wiki」**の思想に基づき、プロジェクトの確定仕様（What & How）と設計判断・教訓（Why & Lessons）、および開発計画・進捗（Plan & Status）を構造化・相互リンクして運用されています。

---

## 🧭 ドキュメント体系 (Map of Content)

```text
Doc/
├── index.md                 # 【現在地】総合ポータル (MOC)
├── ARCHITECTURE.md          # 🏛️ 全体アーキテクチャ・データフロー・エージェント連携設計
│
├── Plan/                    # 🚀【計画・進捗管理】マイルストーン & 進捗ダッシュボード
│   ├── index.md             # 進捗管理ハブ（フェーズ別ステータス、完了タスク一覧）
│   ├── phase1_initial_setup.md # フェーズ1: 初期立ち上げ・サブモジュール設定（完了）
│   └── phase2_core_agents.md   # フェーズ2: コアエージェント実装計画
│
├── Spec/                    # 📐【確定仕様】現在の動作とインターフェース (Living Docs)
│   ├── index.md             # 仕様書ポータル (Spec MOC)
│   ├── content_pipeline.md  # 自律型動画生成パイプライン仕様
│   ├── director_agent.md    # 企画・カット割り・構造化JSON仕様
│   ├── generator_agent.md   # MiniMax Video-01 API連携・レート制限仕様
│   ├── critic_agent.md      # Vision LLM評価・自己修復リトライ仕様
│   └── assembler_agent.md   # FFmpeg結合・テロップ・BGM・エンコード仕様
│
└── Wiki/                    # 🧠【ナレッジ】意思決定理由・障害教訓・研究 (LLM Wiki)
    ├── index.md             # ナレッジポータル (Wiki MOC)
    ├── ADR/                 # 決定記録 (Architecture Decision Records)
    │   ├── ADR-001_llm_wiki_and_spec_driven_docs.md # ドキュメント管理アーキテクチャの採用
    │   └── ADR-002_minimax_and_ollama_hybrid.md     # MiniMax+Ollamaハイブリッド構成の決定
    ├── Troubleshooting/     # 過去の障害対応から抽出した教訓
    └── Research/            # 将来機能・API調査
        └── minimax_video_api_spec.md # MiniMax Video-01 API技術仕様・制約まとめ
```

---

## 🚀 クイックナビゲーション

### 1. 全体構造・エージェント連携を把握したい
* 👉 **[アーキテクチャ解説 (Doc/ARCHITECTURE.md)](./ARCHITECTURE.md)**: Director, Generator, Critic, Assembler の連携ループと非同期キュー設計。

### 2. 現在の開発進捗や次のマイルストーンを確認したい
* 👉 **[進捗管理ハブ (Doc/Plan/index.md)](./Plan/index.md)**: フェーズごとの進捗ステータス、完了タスク、現在進行中タスク。

### 3. 現在の「確定仕様（機能・API・データ構造）」を確認したい
* 👉 **[仕様書ハブ (Doc/Spec/index.md)](./Spec/index.md)**: 各エージェントおよびパイプラインのコードレベルの確定仕様（Living Docs）。

### 4. 「なぜその設計にしたのか」「API検証結果」を知りたい
* 👉 **[ナレッジWikiハブ (Doc/Wiki/index.md)](./Wiki/index.md)**: ADR（意思決定記録）、障害復旧の教訓、MiniMax API調査ナレッジ。

---

## 🛠️ ナレッジの運用・更新ルール

本プロジェクトでは、専用スキル [`.agent/skills/llm_wiki/SKILL.md`](../.agent/skills/llm_wiki/SKILL.md) を通じてドキュメントの整合性を維持しています。
* **仕様とナレッジの双方向リンク**: 仕様書には必ず背景となったADRへのリンクを貼り、Wikiには対象の仕様書へのリンクを記載します。
* **Living Documentation**: コードを変更する際は、必ず対応する `Doc/Spec/` を同期して更新します。
* **MOCの維持**: 新規ドキュメントを作成・変更した際は、本ファイルおよび各サブポータルの目次を直ちに更新します。
* **腐敗記述の排除**: 旧仕様書への未解決リンクや古い参照を残さないよう定期的に剪定（Pruning）します。
