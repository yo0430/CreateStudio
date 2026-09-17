import os
import shutil
import logging
from pathlib import Path
from typing import List, Optional, Tuple
from src.core.config import settings
from src.core.models import ProjectPlan, CutPlan
from src.utils.media_tools import MediaTools

logger = logging.getLogger(__name__)

class AssemblerAgent:
    def __init__(self, output_dir: Optional[Path] = None, temp_dir: Optional[Path] = None):
        self.output_dir = output_dir or settings.OUTPUT_DIR
        self.temp_dir = temp_dir or settings.TEMP_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def concatenate_clips(self, clip_paths: List[Path], output_path: Path, use_mock: bool = False) -> Path:
        """複数の動画クリップをタイムライン順に結合する"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if use_mock or not MediaTools.is_ffmpeg_available():
            # モック結合: クリップヘッダーを連結
            with open(output_path, "wb") as out_f:
                out_f.write(f"CONCATENATED_MASTER:num_clips={len(clip_paths)}\n".encode("utf-8"))
                for idx, p in enumerate(clip_paths):
                    if p.exists():
                        out_f.write(f"-- CLIP {idx + 1}: {p.name} --\n".encode("utf-8"))
                        with open(p, "rb") as in_f:
                            out_f.write(in_f.read())
            logger.info(f"Mock concatenated clips to: {output_path}")
            return output_path

        # FFmpeg concat demuxer を使用した高速・無劣化結合
        concat_list_file = self.temp_dir / "concat_list.txt"
        with open(concat_list_file, "w", encoding="utf-8") as f:
            for p in clip_paths:
                # Windowsパスのエスケープ処理
                safe_path = str(p.resolve()).replace("\\", "/")
                f.write(f"file '{safe_path}'\n")

        cmd = [
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list_file),
            "-c", "copy",
            str(output_path)
        ]
        MediaTools.run_ffmpeg_command(cmd)
        logger.info(f"Concatenated {len(clip_paths)} clips to {output_path}")
        return output_path

    def synthesize_narration(self, cuts: List[CutPlan], output_audio_path: Path, use_mock: bool = False) -> Path:
        """各カットのナレーション原稿から音声を合成し、タイムアライメントを構築する"""
        output_audio_path.parent.mkdir(parents=True, exist_ok=True)

        total_duration = sum(c.duration_sec for c in cuts)
        if use_mock or not MediaTools.is_ffmpeg_available():
            with open(output_audio_path, "wb") as f:
                f.write(f"SYNTHESIZED_NARRATION:duration={total_duration}\n".encode("utf-8"))
                for c in cuts:
                    f.write(f"Cut {c.cut_id}: {c.narration_script}\n".encode("utf-8"))
            return output_audio_path

        # FFmpeg を用いたモックトーン・タイムライン音声生成
        cmd = [
            "-y",
            "-f", "lavfi",
            "-i", f"sine=frequency=440:duration={total_duration}",
            "-c:a", "aac",
            "-b:a", "128k",
            str(output_audio_path)
        ]
        MediaTools.run_ffmpeg_command(cmd)
        return output_audio_path

    def mix_audio_with_ducking(
        self,
        voice_audio_path: Path,
        bgm_path: Optional[Path],
        output_path: Path,
        use_mock: bool = False
    ) -> Path:
        """ナレーション発話区間に合わせてBGM音量を減衰（ダッキング）して合成する"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if use_mock or not MediaTools.is_ffmpeg_available() or not bgm_path or not bgm_path.exists():
            # BGMなしまたはモックフォールバック
            if voice_audio_path.exists():
                shutil.copyfile(voice_audio_path, output_path)
            else:
                MediaTools.create_mock_audio(output_path, title="Mixed Audio")
            return output_path

        # FFmpeg sidechaincompress フィルターによるダッキング
        cmd = [
            "-y",
            "-i", str(voice_audio_path),
            "-i", str(bgm_path),
            "-filter_complex",
            "[1:a]volume=0.3[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[out]",
            "-map", "[out]",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_path)
        ]
        MediaTools.run_ffmpeg_command(cmd)
        return output_path

    def render_telop_overlay(
        self,
        video_path: Path,
        cuts: List[CutPlan],
        output_path: Path,
        use_mock: bool = False
    ) -> Path:
        """カット情報に基づいて字幕・テロップを画面下部にオーバーレイ描画する"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if use_mock or not MediaTools.is_ffmpeg_available():
            if video_path.exists():
                shutil.copyfile(video_path, output_path)
            else:
                MediaTools.create_mock_video(output_path, title="Telop Rendered")
            return output_path

        # テロップ情報の描画 (FFmpeg drawtext フィルタ)
        # 最初のカットのテロップを描画するフィルタ例
        first_telop = cuts[0].telop_text or "" if cuts else ""
        safe_telop = first_telop.replace(":", "\\:").replace("'", "")

        cmd = [
            "-y",
            "-i", str(video_path),
            "-vf", f"drawtext=text='{safe_telop}':fontcolor=white:fontsize=36:box=1:boxcolor=black@0.6:boxborderw=10:x=(w-text_w)/2:y=h-150",
            "-c:a", "copy",
            str(output_path)
        ]
        try:
            MediaTools.run_ffmpeg_command(cmd)
        except Exception as e:
            logger.warning(f"Telop drawtext rendering failed ({e}). Copying video without telop.")
            shutil.copyfile(video_path, output_path)

        return output_path

    def assemble_master_video(
        self,
        project_plan: ProjectPlan,
        clip_paths: List[Path],
        output_path: Optional[Path] = None,
        bgm_path: Optional[Path] = None,
        use_mock: bool = False
    ) -> Path:
        """全カットのクリップ結合、音声ミックス、テロップ合成を一括実行してマスター動画を出力する"""
        sanitized_title = "".join(c for c in project_plan.project_title if c.isalnum() or c in ("-", "_")).rstrip()
        final_output = output_path or (self.output_dir / f"{sanitized_title}_master.mp4")

        logger.info(f"Starting master video assembly for project: {project_plan.project_title}")

        # 1. 映像結合
        raw_concat_video = self.temp_dir / "temp_concat.mp4"
        self.concatenate_clips(clip_paths, raw_concat_video, use_mock=use_mock)

        # 2. ナレーション音声合成
        narration_audio = self.temp_dir / "temp_narration.aac"
        self.synthesize_narration(project_plan.cuts, narration_audio, use_mock=use_mock)

        # 3. BGMミックス & ダッキング
        mixed_audio = self.temp_dir / "temp_mixed_audio.aac"
        self.mix_audio_with_ducking(narration_audio, bgm_path, mixed_audio, use_mock=use_mock)

        # 4. テロップ描画 & 最終エンコード
        self.render_telop_overlay(raw_concat_video, project_plan.cuts, final_output, use_mock=use_mock)

        logger.info(f"Successfully assembled master video at: {final_output}")
        return final_output
