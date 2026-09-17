from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class CameraMotion(str, Enum):
    STATIC = "static"
    SLOW_ZOOM_IN = "slow_zoom_in"
    SLOW_ZOOM_OUT = "slow_zoom_out"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    ORBITAL = "orbital"

class AspectRatio(str, Enum):
    RATIO_9_16 = "9:16"
    RATIO_16_9 = "16:9"
    RATIO_1_1 = "1:1"

class CriticStatus(str, Enum):
    PASS_OK = "PASS"
    RETRY = "RETRY"
    REJECT = "REJECT"

from pydantic import BaseModel, Field, model_validator

class CutPlan(BaseModel):
    cut_id: int = Field(default=1, description="カット番号 (1-indexed)")
    duration_sec: float = Field(default=5.0, description="クリップ秒数")
    t2v_prompt: str = Field(..., description="動画生成モデル向け英語プロンプト")
    negative_prompt: str = Field(default="blurry, low quality, distorted, extra limbs, flickering", description="ネガティブプロンプト")
    camera_motion: CameraMotion = Field(default=CameraMotion.STATIC, description="カメラワーク")
    reference_image_path: Optional[str] = Field(default=None, description="I2V参照画像パス")
    narration_script: str = Field(default="", description="日本語ナレーション・セリフ")
    bgm_mood: str = Field(default="energetic", description="BGMの雰囲気")
    telop_text: Optional[str] = Field(default=None, description="テロップ表示テキスト")

    @model_validator(mode="before")
    @classmethod
    def normalize_cut(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "prompt" in data and "t2v_prompt" not in data:
                data["t2v_prompt"] = data["prompt"]
            if "t2v_prompt" not in data:
                data["t2v_prompt"] = data.get("description", "Cinematic scene")
            if "duration_sec" not in data:
                if "duration" in data:
                    data["duration_sec"] = float(data["duration"])
                elif "start_time" in data and "end_time" in data:
                    data["duration_sec"] = max(1.0, float(data["end_time"]) - float(data["start_time"]))
            if "camera_motion" in data and isinstance(data["camera_motion"], str):
                val = data["camera_motion"].lower().replace(" ", "_")
                valid_motions = {m.value for m in CameraMotion}
                data["camera_motion"] = val if val in valid_motions else CameraMotion.STATIC.value
        return data

class ProjectPlan(BaseModel):
    project_title: str = Field(default="Untitled Video", description="動画企画タイトル")
    target_platform: str = Field(default="youtube_shorts", description="対象プラットフォーム")
    aspect_ratio: AspectRatio = Field(default=AspectRatio.RATIO_9_16, description="画面比率")
    total_estimated_duration_sec: float = Field(default=30.0, description="目標総再生秒数")
    cuts: List[CutPlan] = Field(default_factory=list, description="カット割りのリスト")

    @model_validator(mode="before")
    @classmethod
    def normalize_project(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "project_title" not in data:
                data["project_title"] = data.get("project_name") or data.get("title") or "AI Video Plan"
            raw_cuts = data.get("cuts") or data.get("scenes") or []
            normalized_cuts = []
            for idx, c in enumerate(raw_cuts, start=1):
                if isinstance(c, dict):
                    if "cut_id" not in c and "id" not in c:
                        c["cut_id"] = idx
                    elif "id" in c and "cut_id" not in c:
                        c["cut_id"] = c["id"]
                    normalized_cuts.append(c)
                else:
                    normalized_cuts.append(c)
            data["cuts"] = normalized_cuts
        return data

class CutEvaluation(BaseModel):
    cut_id: int
    status: CriticStatus
    overall_score: float = Field(..., ge=1.0, le=10.0, description="総合評価スコア (1-10)")
    anatomical_fidelity: float = Field(..., ge=1.0, le=10.0, description="顔・身体・テクスチャの整合性")
    action_adherence: float = Field(..., ge=1.0, le=10.0, description="プロンプト・指示遵守度")
    temporal_consistency: float = Field(..., ge=1.0, le=10.0, description="時間的連続性・フリッカー")
    feedback_summary: str = Field(..., description="講評・改善理由")
    suggested_negative_prompt: Optional[str] = None
    suggested_prompt_refinement: Optional[str] = None
    retry_count: int = 0

class CriticReport(BaseModel):
    is_all_passed: bool
    cut_evaluations: Dict[int, CutEvaluation]
