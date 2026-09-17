import json
import logging
from typing import Optional, Dict, Any
import httpx
from src.core.config import settings
from src.core.models import ProjectPlan, CutPlan, CameraMotion, AspectRatio

logger = logging.getLogger(__name__)

DIRECTOR_SYSTEM_PROMPT = """
You are an expert film director and AI video producer for viral short-form and cinematic content.
Your task is to plan a video production by generating a structured JSON object according to the specified schema.

Guidelines:
1. Divide the video into sequential cuts (each 4-6 seconds duration).
2. For each cut, write a descriptive English prompt ('t2v_prompt') optimized for modern AI video generation (e.g., MiniMax Video-01). Focus on lighting, subject action, camera movement, and aesthetic details.
3. Keep 'negative_prompt' focused on preventing distortions, blur, and extra limbs.
4. Specify appropriate 'camera_motion' from: static, slow_zoom_in, slow_zoom_out, pan_left, pan_right, tilt_up, tilt_down, orbital.
5. Provide a compelling Japanese narration line ('narration_script') and an engaging on-screen subtitle ('telop_text').
6. The first cut MUST have a strong hook (dynamic camera, striking visual, intriguing telop) to maximize audience retention.

Output format:
You MUST respond with valid JSON ONLY matching the ProjectPlan schema. Do not enclose in markdown ticks if possible, or use standard ```json blocks.
"""

class DirectorAgent:
    def __init__(self, base_url: Optional[str] = None, model_name: Optional[str] = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model_name = model_name or settings.OLLAMA_MODEL_DIRECTOR

    async def generate_plan(
        self,
        topic: str,
        duration_sec: float = 30.0,
        target_platform: str = "youtube_shorts",
        aspect_ratio: AspectRatio = AspectRatio.RATIO_9_16,
        style_preset: str = "cinematic_realism",
        use_mock: bool = False
    ) -> ProjectPlan:
        """動画企画全体のカット割り計画 (ProjectPlan) を生成する"""
        if use_mock:
            return self._create_mock_plan(topic, duration_sec, target_platform, aspect_ratio, style_preset)

        user_prompt = f"""
Topic: {topic}
Target Duration: {duration_sec} seconds
Target Platform: {target_platform}
Aspect Ratio: {aspect_ratio.value}
Style: {style_preset}

Generate a complete production plan JSON with approximately {int(duration_sec // 5)} cuts.
"""

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": user_prompt,
                        "system": DIRECTOR_SYSTEM_PROMPT,
                        "stream": False,
                        "format": "json"
                    }
                )
                response.raise_for_status()
                data = response.json()
                raw_text = data.get("response", "{}")
                
                # JSONパースとPydanticバリデーション
                parsed_json = json.loads(raw_text)
                return ProjectPlan.model_validate(parsed_json)
        except Exception as e:
            logger.warning(f"Ollama generation failed ({e}). Falling back to mock plan.")
            return self._create_mock_plan(topic, duration_sec, target_platform, aspect_ratio, style_preset)

    def _create_mock_plan(
        self,
        topic: str,
        duration_sec: float,
        target_platform: str,
        aspect_ratio: AspectRatio,
        style_preset: str
    ) -> ProjectPlan:
        """テストおよびフォールバック用モック計画"""
        num_cuts = max(1, int(duration_sec // 5))
        cuts = []
        for i in range(1, num_cuts + 1):
            if i == 1:
                motion = CameraMotion.SLOW_ZOOM_IN
                prompt = f"Cinematic opening hook of {topic}, dramatic lighting, hyper-realistic, 8k resolution"
                telop = f"衝撃の事実: {topic}"
                narration = f"知っていましたか？{topic}の驚くべき真実を解説します。"
            elif i == num_cuts:
                motion = CameraMotion.SLOW_ZOOM_OUT
                prompt = f"Cinematic grand finale revealing the conclusion of {topic}, cinematic 8k, bokeh"
                telop = "チャンネル登録よろしくお願いします"
                narration = f"これが{topic}の未来です。次回もお楽しみに！"
            else:
                motion = CameraMotion.PAN_RIGHT if i % 2 == 0 else CameraMotion.STATIC
                prompt = f"Detailed shot demonstrating key mechanism of {topic}, dynamic camera motion, photorealistic"
                telop = f"ポイント {i}: {topic}の深層"
                narration = f"さらに重要なのは、この技術が急速に進化している点です。"

            cuts.append(CutPlan(
                cut_id=i,
                duration_sec=5.0,
                t2v_prompt=prompt,
                camera_motion=motion,
                narration_script=narration,
                telop_text=telop,
                bgm_mood="energetic" if i == 1 else "tension"
            ))

        return ProjectPlan(
            project_title=f"{topic} 徹底解説",
            target_platform=target_platform,
            aspect_ratio=aspect_ratio,
            total_estimated_duration_sec=float(num_cuts * 5),
            cuts=cuts
        )
