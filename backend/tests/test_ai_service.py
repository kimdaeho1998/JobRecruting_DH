import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.services.ai_service import AIService


class AIServiceTests(unittest.TestCase):
    def test_generate_response_uses_prompt_templates_for_supported_features(self) -> None:
        service = AIService()

        summary = service.generate_response("job_summary.prompt.md", company_name="TestCo", job_title="Backend Engineer", job_description="Build APIs")
        self.assertIn("summary", summary)
        self.assertIn("required_skills", summary)

        skill_result = service.generate_response("skill_extraction.prompt.md", company_name="TestCo", job_title="Backend Engineer", job_description="Build APIs")
        self.assertIn("technical_skills", skill_result)

        fit_result = service.generate_response("job_fit_analysis.prompt.md", company_name="TestCo", job_title="Backend Engineer", job_description="Build APIs", resume_text="Python experience")
        self.assertIn("fit_score", fit_result)

        resume_result = service.generate_response("resume_analysis.prompt.md", resume_text="Python experience")
        self.assertIn("experience_summary", resume_result)

        cover_letter = service.generate_response("cover_letter.prompt.md", company_name="TestCo", job_title="Backend Engineer", job_description="Build APIs", resume_text="Python experience")
        self.assertIn("cover_letter", cover_letter)

        interview = service.generate_response("interview_questions.prompt.md", company_name="TestCo", job_title="Backend Engineer", job_description="Build APIs")
        self.assertIn("technical_questions", interview)

        company = service.generate_response("company_analysis.prompt.md", company_name="TestCo")
        self.assertIn("industry", company)

        compare = service.generate_response("job_compare.prompt.md", job_a_title="A", job_a_description="A desc", job_b_title="B", job_b_description="B desc")
        self.assertIn("recommended_job", compare)


if __name__ == "__main__":
    unittest.main()
