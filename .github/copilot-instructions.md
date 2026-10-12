# GitHub Copilot Custom Instructions — CreateStudio

## 1. Single Source of Truth (SSOT)
- **Primary Directive**: You MUST strictly adhere to `AGENTS.md` at the repository root as the authoritative Single Source of Truth (SSOT) for this workspace.
- **Specification Compliance**: Follow the Linux Foundation / Agentic AI Foundation (AAIF) `AGENTS.md` standard.
- **Subsystem Scope**: If working within a subdirectory, check for local `AGENTS.md` files and apply local rules with precedence over global rules (`<precedence_policy>`).

## 2. 5 Core Development Lifecycle Standards
Adhere to the 5 development lifecycle elements defined in `AGENTS.md`:
1. **調査 (Research)**: Verify facts with objective sources (`fact_checker`), maintain documentation (`llm_wiki`), clarify ambiguous requirements (`requirement_definition_master`).
2. **計画 (Planning)**: Design interfaces first (`structural_first`), evaluate algorithmic trade-offs (`multi_reasoning_consensus`), delegate tasks to subagents (`subagent_delegation`).
3. **レビュー (Review)**: Execute review loops (`iterative_review`), aggressively test edge cases (`devils_advocate`), ensure license compliance (`compliance`).
4. **実装 (Implementation)**: Enforce clean architecture and strict typing (`coding_standards`), refactor safely (`refactoring_master`).
5. **テスト・運用 (Testing & Ops)**: Validate all changes with project test suites, respect branch rules (`version_control`), execute restricted ops safely (`ops_workflow`).

## 3. Strict Safety Guardrails
- **Never Commit to Main**: NEVER commit directly to `main` branch. Always work on designated feature branches.
- **Never Expose Secrets**: Never read, output, or commit `.env` files, API keys, or credentials.
- **Max 3 Debug Iterations**: If an error or command fails 3 times, STOP immediately and summarize findings for user instruction.
- **Restricted Operations**: Operations registered in `<restricted_skills_registry>` MUST NEVER be invoked autonomously. Require explicit user trigger.
- **Language**: All explanations, progress updates, and code comments to the user MUST be in Japanese.
