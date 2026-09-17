# Phase 6: エンドツーエンド自律実行パイプライン実装・統合

## 概要
全エージェント（Director, Generator, Critic, Assembler, Post）をオーケストレーターによって有機的に結合し、企画立案から動画生成、品質検査、編集結合、SNS投稿メタデータ生成までを完全自動で完走するパイプラインを構築・実機実証しました。

---

## 主な実装コンポーネント

1. **PostAgent (`src/agents/post.py`)**:
   - 企画内容・クリップ構成・トピックから最適なSNSタイトル、解説文、ハッシュタグを自動生成。
   - Ollama（`llama3.1:8b`）およびルールベースのフォールバックに対応。
2. **ContentPipeline (`src/pipeline/orchestrator.py`)**:
   - Director -> Generator -> Critic（自己修復ループ含む）-> Assembler -> Post の全フローを統括。
   - レートリミット、ファイルパスハンドリング、中間キャッシュを完備。
3. **CLIエントリーポイント (`main.py`)**:
   - コマンドライン実行インターフェース。
   - オプション: `--topic`, `--duration`, `--style`, `--output-dir`, `--mock`, `--live`。
   - Windows環境（CP932/UTF-8）におけるターミナル出力文字コード自動調整。
4. **単体・結合テスト (`tests/test_pipeline.py`)**:
   - 全11件の自動テスト（PostAgent、ContentPipeline、CLI引数解析）をパス。

---

## 実機検証実績
* コマンド: `python main.py --topic "未来の空飛ぶ車" --duration 10 --live`
* 実機モデル: `llama3.1:8b` (企画・構成立案・投稿文生成), `llava:7b` (Vision品質検査)
* 成果物: `output/AIVideoPlan_master.mp4` (結合・テロップ・BGM合成済みマスター動画)
