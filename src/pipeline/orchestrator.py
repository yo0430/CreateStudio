import asyncio
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from src.core.config import settings
from src.core.models import ProjectPlan, CutPlan, CutEvaluation, CriticReport
from src.agents.director import DirectorAgent
from src.agents.generator import MiniMaxGenerator
from src.agents.critic import CriticAgent
from src.agents.assembler import AssemblerAgent
from src.agents.post import PostAgent, PublicationPackage

logger = logging.getLogger(__name__)

class PipelineResult(BaseModel):
    success: bool
    project_plan: ProjectPlan
    master_video_path: str
    publication_package: PublicationPackage
    evaluations: Dict[int, CutEvaluation]
    summary_report: str

class ContentPipeline:
    """マルチエージェント型・自律コンテンツ生成パイプラインオーケストレーター"""

    def __init__(
        self,
        director: Optional[DirectorAgent] = None,
        generator: Optional[MiniMaxGenerator] = None,
        critic: Optional[CriticAgent] = None,
        assembler: Optional[AssemblerAgent] = None,
        post: Optional[PostAgent] = None
    ):
        self.director = director or DirectorAgent()
        self.generator = generator or MiniMaxGenerator()
        self.critic = critic or CriticAgent()
        self.assembler = assembler or AssemblerAgent()
        self.post = post or PostAgent()

    async def run(
        self,
        topic: str,
        duration_sec: float = 30.0,
        style_preset: str = "cinematic_realism",
        target_platform: str = "youtube_shorts",
        use_mock: bool = False,
        output_path: Optional[Path] = None
    ) -> PipelineResult:
        """企画から動画生成、自己修復ループ、編集、投稿パッケージ生成までを一括自動実行する"""
        logger.info(f"=== Starting Autonomous Content Pipeline for topic: '{topic}' ===")

        # Step 1: Director Agent による企画立案 & カット割り策定
        logger.info("Step 1: Planning and scripting with Director Agent...")
        plan = await self.director.generate_plan(
            topic=topic,
            duration_sec=duration_sec,
            target_platform=target_platform,
            style_preset=style_preset,
            use_mock=use_mock
        )
        logger.info(f"Generated plan '{plan.project_title}' with {len(plan.cuts)} cuts.")

        # Step 2: 各カットの自律生成 & Critic Agent による自己修復ループ
        logger.info("Step 2: Generating clips with Critic inspection and self-healing loops...")
        passed_clips: List[Path] = []
        evaluations: Dict[int, CutEvaluation] = {}

        for cut in plan.cuts:
            clip_path, eval_res = await self.critic.run_self_healing_loop(
                cut=cut,
                generator=self.generator,
                max_retries=3,
                use_mock=use_mock
            )
            passed_clips.append(clip_path)
            evaluations[cut.cut_id] = eval_res

        # Step 3: Assembler Agent によるポスプロ合成
        logger.info("Step 3: Assembling master video (concatenation, ducking, telop)...")
        master_video = self.assembler.assemble_master_video(
            project_plan=plan,
            clip_paths=passed_clips,
            output_path=output_path,
            use_mock=use_mock
        )

        # Step 4: Post Agent による配信メタデータ生成
        logger.info("Step 4: Generating publication package with Post Agent...")
        pub_pkg = self.post.generate_metadata(plan)

        # 最終サマリー構築
        summary_lines = [
            f"🎬 タイトル: {plan.project_title}",
            f"⏱️ 総再生時間: {plan.total_estimated_duration_sec}秒 ({len(plan.cuts)}カット)",
            f"📁 マスター動画: {master_video.resolve()}",
            "📊 品質審査スコア:",
        ]
        for cid, ev in evaluations.items():
            summary_lines.append(f"   Cut {cid}: {ev.status.value} (Score: {ev.overall_score}/10) - {ev.feedback_summary}")

        summary_report = "\n".join(summary_lines)
        logger.info(f"=== Autonomous Pipeline Completed Successfully! ===\n{summary_report}")

        return PipelineResult(
            success=True,
            project_plan=plan,
            master_video_path=str(master_video.resolve()),
            publication_package=pub_pkg,
            evaluations=evaluations,
            summary_report=summary_report
        )
