import unittest
import asyncio
from pathlib import Path
import shutil
from src.agents.generator import MiniMaxGenerator
from src.core.models import CutPlan, CameraMotion

class TestGeneratorAgent(unittest.TestCase):
    def setUp(self):
        self.generator = MiniMaxGenerator(api_key="test_key_dummy")
        self.test_output_dir = Path("./temp/test_clips")
        self.test_output_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.test_output_dir.exists():
            shutil.rmtree(self.test_output_dir, ignore_errors=True)

    def test_mock_clip_generation(self):
        async def run_test():
            cut = CutPlan(
                cut_id=1,
                duration_sec=5.0,
                t2v_prompt="Cinematic shot of flying drone",
                camera_motion=CameraMotion.SLOW_ZOOM_IN
            )
            output_file = self.test_output_dir / "test_cut_1.mp4"
            result_path = await self.generator.generate_clip(
                cut=cut,
                output_path=output_file,
                use_mock=True
            )
            self.assertTrue(result_path.exists())
            self.assertEqual(result_path, output_file)
            content = result_path.read_text(encoding="utf-8")
            self.assertIn("flying drone", content)

        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()
