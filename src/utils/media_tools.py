import os
import shutil
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class MediaTools:
    """動画・音声処理におけるFFmpegバイナリ解決およびメタデータ操作ユーティリティ"""

    @staticmethod
    def get_ffmpeg_path() -> Optional[str]:
        """システムまたは環境変数からFFmpegバイナリのパスを検出する"""
        # 1. 環境変数設定
        env_path = os.getenv("FFMPEG_PATH")
        if env_path and shutil.which(env_path):
            return env_path

        # 2. システムPATH上の 'ffmpeg'
        if shutil.which("ffmpeg"):
            return "ffmpeg"

        # 3. imageio_ffmpeg がインストールされている場合
        try:
            import imageio_ffmpeg
            exe = imageio_ffmpeg.get_ffmpeg_exe()
            if exe and os.path.exists(exe):
                return exe
        except ImportError:
            pass

        return None

    @classmethod
    def is_ffmpeg_available(cls) -> bool:
        return cls.get_ffmpeg_path() is not None

    @classmethod
    def run_ffmpeg_command(cls, args: list, check: bool = True) -> subprocess.CompletedProcess:
        """FFmpegコマンドを実行する"""
        ffmpeg_bin = cls.get_ffmpeg_path()
        if not ffmpeg_bin:
            raise RuntimeError("FFmpeg executable is not found in system or environment.")

        cmd = [ffmpeg_bin] + args
        logger.debug(f"Executing FFmpeg command: {' '.join(cmd)}")
        return subprocess.run(cmd, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @classmethod
    def create_mock_video(cls, output_path: Path, duration_sec: float = 5.0, title: str = "Mock Video") -> Path:
        """テスト用の軽量モック動画ファイルを生成する"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        ffmpeg_bin = cls.get_ffmpeg_path()

        if ffmpeg_bin:
            # FFmpegが利用可能な場合は本物の最小限動画（テスト用カラーバー/単色）を生成
            cmd = [
                "-y",
                "-f", "lavfi",
                "-i", f"color=c=navy:s=720x1280:d={duration_sec}:r=25",
                "-f", "lavfi",
                "-i", f"anullsrc=r=44100:cl=stereo",
                "-c:v", "libx264",
                "-t", str(duration_sec),
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-shortest",
                str(output_path)
            ]
            try:
                cls.run_ffmpeg_command(cmd)
                return output_path
            except Exception as e:
                logger.warning(f"FFmpeg mock video generation failed ({e}). Falling back to dummy file.")

        # フォールバック: メタデータ付きダミーMP4バイナリ
        with open(output_path, "wb") as f:
            header = f"MOCK_MP4_HEADER:{title}:duration={duration_sec}\n"
            f.write(header.encode("utf-8") + b"\x00" * 1024)
        return output_path

    @classmethod
    def create_mock_audio(cls, output_path: Path, duration_sec: float = 5.0, title: str = "Mock Audio") -> Path:
        """テスト用の軽量モック音声ファイルを生成する"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            header = f"MOCK_AUDIO_HEADER:{title}:duration={duration_sec}\n"
            f.write(header.encode("utf-8") + b"\x00" * 512)
        return output_path
