import unittest
from src.core.models import ProjectPlan, CutPlan, CameraMotion, AspectRatio, CutEvaluation, CriticStatus

class TestModels(unittest.TestCase):
    def test_project_plan_validation(self):
        cut1 = CutPlan(
            cut_id=1,
            duration_sec=5.0,
            t2v_prompt="Cinematic shot of a futuristic cyberpunk city at dusk, neon lights, 8k",
            camera_motion=CameraMotion.SLOW_ZOOM_IN,
            narration_script="未来の都市ではAIが日常を変革しています。",
            telop_text="未来都市のリアル"
        )
        
        plan = ProjectPlan(
            project_title="AI Future",
            target_platform="youtube_shorts",
            aspect_ratio=AspectRatio.RATIO_9_16,
            total_estimated_duration_sec=30.0,
            cuts=[cut1]
        )
        
        self.assertEqual(plan.project_title, "AI Future")
        self.assertEqual(len(plan.cuts), 1)
        self.assertEqual(plan.cuts[0].camera_motion, CameraMotion.SLOW_ZOOM_IN)

    def test_critic_evaluation_validation(self):
        eval_result = CutEvaluation(
            cut_id=1,
            status=CriticStatus.PASS_OK,
            overall_score=8.5,
            anatomical_fidelity=8.0,
            action_adherence=9.0,
            temporal_consistency=8.5,
            feedback_summary="破綻なく高品質"
        )
        self.assertEqual(eval_result.status, CriticStatus.PASS_OK)
        self.assertEqual(eval_result.overall_score, 8.5)

if __name__ == "__main__":
    unittest.main()
