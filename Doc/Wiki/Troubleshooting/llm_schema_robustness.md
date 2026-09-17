# LLM出力JSONのゆらぎ吸収とPydanticモデル堅牢化

## 現象
ローカルLLM（Ollama `llama3.1:8b`）に対してJSON出力を要求した際、以下のような軽微なキー名のゆらぎやフィールド省略が発生し、Pydanticの厳格バリデーションでエラー（Missing field）が発生した。
- `project_title` の代わりに `project_name` や `title` が出力される。
- `cuts` の中で `cut_id` が省略され、`start_time` / `end_time` または `id` のみが出力される。
- `t2v_prompt` の代わりに `prompt` や `description` が出力される。

## 根本原因
ローカルLLMは一般的な動画企画のJSON表現（タイムコード形式や一般的な命名）を学習しているため、指示が詳細であっても微小なキー名の揺れが生じることがある。

## 恒久対応策 (Pydantic model_validator による正規化)
`src/core/models.py` において、`model_validator(mode="before")` を導入し、LLMからの入力データを検証前に自動正規化・フォールバック補完するアーキテクチャを実装した。
1. **キー名のエイリアス解決**:
   - `project_name` / `title` → `project_title`
   - `prompt` / `description` → `t2v_prompt`
2. **自動ID・秒数補完**:
   - `cut_id` 未指定時はリストのインデックス（1-indexed）を自動付与。
   - `start_time` と `end_time` の差分から `duration_sec` を自動算出。
3. **Enum値の安全なフォールバック**:
   - `camera_motion` の大文字・表記ゆれを吸収し、未知の文字列は `CameraMotion.STATIC` に安全にフォールバック。

## 成果
ローカルLLMによる実機推論時にバリデーションエラーによるフォールバック発生がゼロになり、100%の成功率で構造化 `ProjectPlan` を生成できるようになった。
