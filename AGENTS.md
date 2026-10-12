# AGENTS.md - CreateStudio Root Single Source of Truth (SSOT)

<project_metadata>
  <name>CreateStudio</name>
  <type>Multi-Agent Content Generation Pipeline</type>
  <version>1.0.0</version>
  <specification_standard>Linux Foundation / Agentic AI Foundation (AAIF) AGENTS.md v1.0</specification_standard>
  <repository_url>https://github.com/yo0430/CreateStudio.git</repository_url>
  <default_branch>main</default_branch>
  <description>Gemini / AI プロンプト駆動型マルチエージェント制作・動画コンテンツ自動生成パイプライン。</description>
</project_metadata>

<system_architecture>
  <ssot_declaration>
    本ドキュメントは Linux Foundation / AAIF AGENTS.md 仕様に準拠した、CreateStudio ワークスペースの単一の真実源（Single Source of Truth / SSOT）である。
  </ssot_declaration>
  <design_principles>
    <principle name="Single Source of Truth">CLAUDE.md、copilot-instructions.md、.cursorrules は AGENTS.md を参照するポインタとして構成し、二重管理を排除する。</principle>
    <principle name="Progressive Disclosure">常時ロード指示は本 AGENTS.md（24KB / 20kトークン以内）に留め、詳細ロジックは .agent/skills/ および Doc/ へ段階的開示する。</principle>
    <principle name="Tri-Tier Safety">スキルを Autonomous（自律）、Controlled（計画承認）、Restricted（明示指示限定）の3階層で管理し、安全境界を担保する。</principle>
  </design_principles>
  <lifecycle_mapping>
    <phase name="調査 (Investigation)">
      <skills>fact_checker, llm_wiki, requirement_definition_master</skills>
      <mandate>客観的事実の検証、要件定義の事前確定、既存コードベースとドキュメントの照合。</mandate>
    </phase>
    <phase name="計画 (Planning)">
      <skills>structural_first, multi_reasoning_consensus, subagent_delegation</skills>
      <mandate>骨格・インターフェース先行設計、複数アプローチの合意形成、作業ブランチ作成計画。</mandate>
    </phase>
    <phase name="レビュー (Review)">
      <skills>iterative_review, devils_advocate, compliance</skills>
      <mandate>反復レビュー（RDD）、セキュリティ・境界値・クラッシュ耐性攻撃検証、ライセンス確認。</mandate>
    </phase>
    <phase name="実装 (Implementation)">
      <skills>coding_standards, refactoring_master</skills>
      <mandate>クリーンアーキテクチャ・型安全性の徹底、振る舞いを変えない安全なリファクタリング。</mandate>
    </phase>
    <phase name="テスト・検証 (Testing)">
      <skills>code_execution</skills>
      <mandate>数値計算・ロジックのコード実実行検証、自動テストスイートによる品質保証。</mandate>
    </phase>
  </lifecycle_mapping>
</system_architecture>

<precedence_policy>
  <rule priority="1" name="Subsystem Precedence">
    階層優先順位: [.agent/rules/ または 各サブディレクトリ規則] &gt; [ルート AGENTS.md]。
    特定サブシステム配下の編集時はそのディレクトリ配下の設定・ルールを最優先とする。
  </rule>
  <rule priority="2" name="SSOT Master Rule">
    ハーネス優先順位: [AGENTS.md (Root SSOT)] &gt; [ツール固有設定]。
    全エージェントハーネスは AGENTS.md の制約（トークン予算・Never-do）に完全拘束される。
  </rule>
  <rule priority="3" name="Clarification Mandate">
    暗黙の仮定禁止（No Implicit Assumptions）:
    仕様の不確実性や破壊的ファイル変更を検知した場合は、推測で進めず必ず事前にユーザーへ確認を行うこと。
  </rule>
</precedence_policy>

<subsystem_routing>
  <route path=".agent/skills/" role="Agent Skills Catalog">
    <description>本プロジェクト向けのエージェントスキル定義（SKILL.md）。</description>
  </route>
  <route path=".agent/workflows/" role="Standard Workflows &amp; Pipelines">
    <description>マルチエージェント協調手順および標準開発ワークフロー。</description>
  </route>
  <route path="Doc/" role="LLM Wiki Knowledge Base">
    <description>仕様書（Spec）、ナレッジ（Wiki）、計画（Plan）、運用（Operations）。</description>
  </route>
</subsystem_routing>

<development_standards>
  <commands>
    <command type="test">python -m unittest discover -s tests -v</command>
  </commands>
  <coding_principles>
    <principle name="Type Annotations">全関数・メソッドに厳格な型ヒントを義務付ける。</principle>
    <principle name="Single Responsibility">モジュール間の責務を明確に分離し、疎結合を保つ。</principle>
    <principle name="Size Budget Enforcement">常時ロード設定および SKILL.md は厳格に 24,576 bytes 以下を維持する。</principle>
      <principle name="Token Defense Test Execution">
      テスト・ビルド実行時の全量ログ出力を禁止し、標準出力・標準エラー出力を作業用ログファイル（例: .tmp/test_latest.log）へ集約すること。
      調査は末尾要約確認（15行以内）、エラーキーワード抽出を行い、1回の閲覧は最大30行以内に制限すること（rules/test_execution_policy.xml 準拠）。
    </principle>
  </coding_principles>
  <git_standards>
    <standard name="Branch Strategy">main ブランチへの直接コミット厳禁。必ず作業ブランチを作成して開発すること。</standard>
    <standard name="Pre-Commit Approval">コミット実行前に必ず変更サマリーを提示し、ユーザー承認を得ること。</standard>
    <standard name="Merge Mandate">ブランチのマージはユーザーの明示的な指示によってのみ実行すること。</standard>
  </git_standards>
</development_standards>

<safety_guardrails>
  <never_do>
    <item>ユーザーの明示的な承認なしに main ブランチへ直接コミット、またはプッシュを行わないこと。</item>
    <item>ユーザーの明示的な承認なしに .env、秘密鍵、認証情報をコミット・出力しないこと。</item>
    <item>ユーザーの明示的な事前承認なしに破壊的な一括ファイル削除を実行しないこと。</item>
    <item>同一エラー・調査課題に対して3回を超えて無意味なデバッグコマンドループを繰り返さないこと。</item>
    <item>Restricted スキルをユーザーの明示的なトリガーなしに自律的・暗黙的に実行しないこと。</item>
    <item>計画書内の複数タスク（例: T1, T2...）や大規模リファクタリングを単一エージェントセッションで抱え込んで連続実行しないこと（必ずサブエージェントへ分割委譲すること）。</item>
    <item>同一エージェント内でツール呼び出しを35回以上累積させてコンテキスト自動圧縮（Compaction）を無防備に誘発させないこと。</item>
      <item>テスト・ビルドの全量ログを直接出力へ垂れ流すこと、およびログファイルの無制限読み込み（cat等）を行わないこと（.tmp へのリダイレクトと最大30行制限を徹底）。</item>
  </never_do>
  <loop_prevention>
    <policy>
      同一アプローチでの試行は最大3回までとする。
      3回連続で失敗した場合は直ちにコマンド実行を停止し、問題点・試行結果・仮説をユーザーに報告して指示を仰ぐこと。
    </policy>
  </loop_prevention>
</safety_guardrails>

<restricted_skills_registry>
  <skill name="ops_workflow">
    <type>Restricted</type>
    <scope>workflows / deployment / release</scope>
    <trigger>ユーザーが「@ops_workflow」または「本番デプロイを実行」と明示指示した場合のみ</trigger>
    <default_action>自律実行を停止。実行確認プロンプトを提示し、明示的承認を待つ。</default_action>
    <guardrail>Frontmatter に disable-model-invocation: true および trigger: manual を付与</guardrail>
  </skill>
  <skill name="version_control">
    <type>Controlled / Restricted</type>
    <scope>git operations / release / branch merge</scope>
    <trigger>ブランチマージ、タグ発行、リモートプッシュ、ブランチ削除等のGit確定操作</trigger>
    <default_action>自律的なGit確定操作を停止。変更計画・コミット計画を提示し承認を待つ。</default_action>
    <guardrail>コミット前確認・マージ指示必須の二重承認プロセス</guardrail>
  </skill>
  <skill name="post_agent">
    <type>Restricted</type>
    <scope>social / external publication / webhook posting</scope>
    <trigger>ユーザーが明示的に投稿・パブリッシュを指示した場合のみ</trigger>
    <default_action>自律投稿を停止。投稿内容・送信先の確認を求め、明示的承認を待つ。</default_action>
    <guardrail>Frontmatter に disable-model-invocation: true および trigger: manual を付与</guardrail>
  </skill>
</restricted_skills_registry>
