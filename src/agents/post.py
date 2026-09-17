import logging
from typing import List, Optional
from pydantic import BaseModel, Field
from src.core.models import ProjectPlan

logger = logging.getLogger(__name__)

class PublicationPackage(BaseModel):
    video_title: str = Field(..., description="クリック率を高めるフック付きタイトル")
    description: str = Field(..., description="動画の概要文")
    tags: List[str] = Field(default_factory=list, description="SEO・推薦アルゴリズム向けハッシュタグ")
    target_platform: str = Field(default="youtube_shorts", description="対象プラットフォーム")

class PostAgent:
    """完成したマスター動画の配信メタデータ最適化およびSNS投稿支援エージェント"""

    def generate_metadata(self, plan: ProjectPlan) -> PublicationPackage:
        """ProjectPlanから最適なSNS投稿用メタデータを自動生成する"""
        title = f"【衝撃】{plan.project_title}の真実 #Shorts"
        
        # ハッシュタグの選定
        tags = ["#AI", "#テクノロジー", "#Shorts", "#未来予測", "#最新AI"]
        if "都市" in plan.project_title or "city" in plan.project_title.lower():
            tags.extend(["#スマートシティ", "#未来都市"])

        # 概要文の構築
        description_lines = [
            f"🎬 今回のテーマ: {plan.project_title}",
            "",
            "AI動画生成マルチエージェントシステムによって完全自律制作された動画です。",
            "企画から動画生成、品質検閲、音声・テロップ編集まで完全自動化！",
            "",
            "チャンネル登録＆高評価よろしくお願いします！",
            "",
            " ".join(tags)
        ]
        description = "\n".join(description_lines)

        pkg = PublicationPackage(
            video_title=title,
            description=description,
            tags=tags,
            target_platform=plan.target_platform
        )
        logger.info(f"Generated publication package for: {plan.project_title}")
        return pkg
