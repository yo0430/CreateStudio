import unittest
from pathlib import Path
import shutil
from src.agents.assembler import AssemblerAgent
from src.utils.media_tools import MediaTools
from src.core.models import ProjectPlan, CutPlan, CameraMotion, AspectRatio

class TestAssemblerAgent(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("./temp/test_assembler")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.assembler = AssemblerAgent(output_dir=self.test_dir, temp_dir=self.test_dir)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_media_tools_mock(self):
        mock_vid = self.test_dir / "mock_vid.mp4"
        mock_aud = self.test_dir / "mock_aud.aac"
        MediaTools.create_mock_video(mock_vid, duration_sec=3.0)
        MediaTools.create_mock_audio(mock_aud, duration_sec=3.0)
        self.assertTrue(mock_vid.exists())
        self.assertTrue(mock_aud.exists())

    def test_concatenate_clips(self):
        clip1 = self.test_dir / "clip1.mp4"
        clip2 = self.test_dir / "clip2.mp4"
        MediaTools.create_mock_video(clip1, duration_sec=2.0, title="Clip 1")
        MediaTools.create_mock_video(clip2, duration_sec=2.0, title="Clip 2")

        out_concat = self.test_dir / "concat.mp4"
        res = self.assembler.concatenate_clips([clip1, clip2], out_concat, use_mock=True)
        self.assertTrue(res.exists())
        content = res.read_text(encoding="utf-8", errors="ignore")
        self.assertIn("CONCATENATED_MASTER", content)

    def test_assemble_master_video(self):
        plan = ProjectPlan(
            project_title="Tokyo Cyberpunk",
            target_platform="youtube_shorts",
            aspect_ratio=AspectRatio.RATIO_9_16,
            total_estimated_duration_sec=10.0,
            cuts=[
                CutPlan(
                    cut_id=1,
                    duration_sec=5.0,
                    t2v_prompt="Neon street",
                    camera_motion=CameraMotion.SLOW_ZOOM_IN,
                    telop_text="サイバーパンクの夜",
                    narration_script="未来の東京へようこそ。"
                ),
                CutPlan(
                    cut_id=2,
                    duration_sec=5.0,
                    t2v_prompt="Flying drone",
                    camera_motion=CameraMotion.PAN_RIGHT,
                    telop_text="空飛ぶドローン",
                    narration_script="AIが街を自動監視します。"
                )
            ]
        )
        clip1 = self.test_dir / "cut_1.mp4"
        clip2 = self.test_dir / "cut_2.mp4"
        MediaTools.create_mock_video(clip1, duration_sec=5.0)
        MediaTools.create_mock_video(clip2, duration_sec=5.0)

        master_out = self.test_dir / "master.mp4"
        final_video = self.assembler.assemble_master_video(
            project_plan=plan,
            clip_paths=[clip1, clip2],
            output_path=master_out,
            use_mock=True
        )
        self.assertTrue(final_video.exists())
        self.assertEqual(final_video, master_out)

if __name__ == "__main__":
    unittest.main()
