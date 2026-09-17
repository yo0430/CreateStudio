import unittest
import asyncio
from pathlib import Path
import shutil

from src.pipeline.orchestrator import ContentPipeline, PipelineResult

class TestContentPipeline(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("./temp/test_pipeline")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.pipeline = ContentPipeline()

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_pipeline_mock_run(self):
        async def run_test():
            out_video = self.test_dir / "master_test.mp4"
            result = await self.pipeline.run(
                topic="AIスマートシティ構想",
                duration_sec=10.0,
                target_platform="youtube_shorts",
                use_mock=True,
                output_path=out_video
            )
            self.assertIsInstance(result, PipelineResult)
            self.assertTrue(result.success)
            self.assertTrue(Path(result.master_video_path).exists())
            self.assertEqual(len(result.project_plan.cuts), 2)
            self.assertTrue(bool(result.publication_package.video_title))
            self.assertTrue(len(result.publication_package.tags) > 0)
            self.assertEqual(len(result.evaluations), 2)

        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()
