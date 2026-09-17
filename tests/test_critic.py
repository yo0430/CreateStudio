import unittest
import asyncio
from pathlib import Path
import shutil
from src.agents.critic import CriticAgent
from src.agents.generator import MiniMaxGenerator
from src.utils.frame_sampler import FrameSampler
from src.core.models import CutPlan, CameraMotion, CriticStatus

class TestCriticAgent(unittest.TestCase):
    def setUp(self):
        self.critic = CriticAgent()
        self.generator = MiniMaxGenerator()
        self.test_dir = Path("./temp/test_critic")
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_frame_sampler_mock(self):
        sampler = FrameSampler()
        dummy_video = self.test_dir / "dummy.mp4"
        frames = sampler.extract_frames(dummy_video, output_dir=self.test_dir)
        self.assertTrue(len(frames) > 0)
        self.assertTrue(frames[0].exists())

    def test_critic_evaluation_logic(self):
        async def run_test():
            cut = CutPlan(
                cut_id=1,
                t2v_prompt="Cinematic shot of neon street",
                camera_motion=CameraMotion.SLOW_ZOOM_IN
            )
            dummy_video = self.test_dir / "cut_1.mp4"

            # Attempt 0: RETRY
            eval_0 = await self.critic.evaluate_clip(cut, dummy_video, retry_count=0, use_mock=True)
            self.assertEqual(eval_0.status, CriticStatus.RETRY)
            self.assertTrue(bool(eval_0.suggested_negative_prompt))

            # Attempt 1: PASS
            eval_1 = await self.critic.evaluate_clip(cut, dummy_video, retry_count=1, use_mock=True)
            self.assertEqual(eval_1.status, CriticStatus.PASS_OK)
            self.assertGreaterEqual(eval_1.overall_score, 8.0)

        asyncio.run(run_test())

    def test_self_healing_loop(self):
        async def run_test():
            cut = CutPlan(
                cut_id=2,
                t2v_prompt="Portrait of cyber samurai",
                negative_prompt="blurry",
                camera_motion=CameraMotion.STATIC
            )
            final_clip, final_eval = await self.critic.run_self_healing_loop(
                cut=cut,
                generator=self.generator,
                max_retries=3,
                use_mock=True
            )
            self.assertEqual(final_eval.status, CriticStatus.PASS_OK)
            self.assertEqual(final_eval.retry_count, 1)  # 1回目のリトライで合格
            self.assertTrue(final_clip.exists())

        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()
