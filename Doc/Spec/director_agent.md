# Director Agent 仕様書 (Director Agent Spec)

## 1. 概要
Director Agentは、動画の企画立案、脚本作成、カット割り、カメラワーク・演出策定、および構造化JSON出力を行うエージェントです。

---

## 2. 入力と出力

### 入力
- `topic`: 動画のテーマ（例: 「2026年最新AIトレンド」）
- `duration_sec`: 目標総再生秒数（デフォルト: 30秒）
- `target_platform`: プラットフォーム（`youtube_shorts`, `tiktok`, `x`）
- `style_preset`: スタイル（`cinematic_realism`, `anime`, `3d_animation`）

### 出力: `ProjectPlan`
```json
{
  "project_title": "string",
  "target_platform": "youtube_shorts",
  "aspect_ratio": "9:16",
  "total_estimated_duration_sec": 30.0,
  "cuts": [
    {
      "cut_id": 1,
      "duration_sec": 5.0,
      "t2v_prompt": "Cinematic shot of ..., 8k resolution, photorealistic",
      "negative_prompt": "blurry, low quality, distorted hands",
      "camera_motion": "slow_zoom_in",
      "reference_image_path": null,
      "narration_script": "未来の都市ではAIが...",
      "bgm_mood": "energetic",
      "telop_text": "未来都市のリアル"
    }
  ]
}
```

---

## 3. 演出ガイドライン
- **フック (冒頭1〜3秒)**: カット1は視聴維持率を左右するため、動きのダイナミックなカメラワーク（`slow_zoom_in` や急速な追従）と興味を惹くテロップを必ず配置する。
- **カメラモーション**: `static`, `slow_zoom_in`, `slow_zoom_out`, `pan_left`, `pan_right`, `tilt_up`, `tilt_down`, `orbital` から最適なものを指定。
- **プロンプト**: MiniMaxのT2V性能を最大限引き出すため、英語で具体的・写実的に記述する。
