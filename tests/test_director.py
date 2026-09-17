import unittest
import asyncio
from src.agents.director import DirectorAgent
from src.core.models import AspectRatio, ProjectPlan

class TestDirectorAgent(unittest.TestCase):
    def setUp(self):
        self.agent = DirectorAgent()

    def test_mock_plan_generation(self):
        async def run_test():
            plan = await self.agent.generate_plan(
                topic="AIロボットの未来",
                duration_sec=15.0,
                target_platform="youtube_shorts",
                aspect_ratio=AspectRatio.RATIO_9_16,
                use_mock=True
            )
            self.assertIsInstance(plan, ProjectPlan)
            self.assertEqual(len(plan.cuts), 3)
            self.assertEqual(plan.cuts[0].cut_id, 1)
            self.assertTrue("AIロボットの未来" in plan.cuts[0].t2v_prompt)
            self.assertTrue(bool(plan.cuts[0].telop_text))
            self.assertTrue(bool(plan.cuts[0].narration_script))

        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()
