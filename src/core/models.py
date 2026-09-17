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

class CutPlan(BaseModel):
    cut_id: int = Field(..., description="カット番号 (1-indexed)")
    duration_sec: float = Field(default=5.0, description="クリップ秒数")
    t2v_prompt: str = Field(..., description="動画生成モデル向け英語プロンプト")
    negative_prompt: str = Field(default="blurry, low quality, distorted, extra limbs, flickering", description="ネガティブプロンプト")
    camera_motion: CameraMotion = Field(default=CameraMotion.STATIC, description="カメラワーク")
    reference_image_path: Optional[str] = Field(default=None, description="I2V参照画像パス")
    narration_script: str = Field(default="", description="日本語ナレーション・セリフ")
    bgm_mood: str = Field(default="energetic", description="BGMの雰囲気")
    telop_text: Optional[str] = Field(default=None, description="テロップ表示テキスト")

class ProjectPlan(BaseModel):
    project_title: str = Field(..., description="動画企画タイトル")
    target_platform: str = Field(default="youtube_shorts", description="対象プラットフォーム")
    aspect_ratio: AspectRatio = Field(default=AspectRatio.RATIO_9_16, description="画面比率")
    total_estimated_duration_sec: float = Field(default=30.0, description="目標総再生秒数")
    cuts: List[CutPlan] = Field(..., description="カット割りのリスト")

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
