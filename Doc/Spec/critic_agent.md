# Critic Agent 仕様書 (Critic Agent Spec)

## 1. 概要
Critic Agentは、生成された動画クリップからフレーム画像を抽出し、Vision LLMを用いて品質、解剖学的整合性、指示遵守度を評価・採点し、必要に応じて自己修復リトライパラメータを生成するエージェントです。

---

## 2. 評価基準 & スコアリングマトリクス (各1〜10点)

| 評価項目 | 評価内容 | 合格基準 |
| :--- | :--- | :---: |
| **解剖学的整合性 (anatomical_fidelity)** | 人物の顔、指、四肢の崩れや歪み、不自然な変形がないか | 7.0点以上 |
| **指示遵守度 (action_adherence)** | プロンプトで指定された被写体、動作、カメラワークが表現されているか | 7.0点以上 |
| **時間的連続性 (temporal_consistency)** | フレーム間のフリッカー（チラつき）、物体の突如の消失・変形がないか | 7.0点以上 |
| **総合スコア (overall_score)** | 全項目の加重平均 | 8.0点以上 |

---

## 3. 自己修復ループ（リトライ補正）ロジック
総合スコアが8.0未満の場合、Critic Agentは以下の調整パラメータを出力する。
1. **ネガティブプロンプトの強化**:
   - 顔崩れ時: `distorted face, poorly drawn eyes, asymmetry`
   - 指崩れ時: `extra fingers, mutated hands, missing fingers`
2. **プロンプトの微調整**:
   - 複雑すぎる描写を簡潔化し、モデルが破綻しにくい表現へ置換
3. **シード値の変更**:
   - 異なるシード値での再生成を指示

---

## 4. 実装インターフェース (`src/agents/critic.py`)

### 4.1 メソッド定義
```python
class CriticAgent:
    async def evaluate_clip(
        self,
        cut: CutPlan,
        video_path: Path,
        retry_count: int = 0,
        max_retries: int = 3,
        use_mock: bool = False
    ) -> CutEvaluation:
        """フレーム抽出（FrameSampler）および Vision LLM (llava:7b) による品質検閲"""
        ...

    async def run_self_healing_loop(
        self,
        cut: CutPlan,
        generator: MiniMaxGenerator,
        max_retries: int = 3,
        use_mock: bool = False
    ) -> Tuple[Path, CutEvaluation]:
        """合格（PASS）するまでプロンプトを補正して再生成を繰り返す自律修復ループ"""
        ...
```
