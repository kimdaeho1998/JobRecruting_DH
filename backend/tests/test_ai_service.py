import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.core.config import settings
from backend.app.services.ai_service import AIService


class AIServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_settings = {
            "ai_mode": settings.ai_mode,
            "ai_mock_mode": settings.ai_mock_mode,
            "openai_api_key": settings.openai_api_key,
            "openai_model": settings.openai_model,
            "openai_timeout": settings.openai_timeout,
            "openai_max_retries": settings.openai_max_retries,
            "ai_log_path": settings.ai_log_path,
        }
        settings.ai_mode = "mock"
        settings.ai_mock_mode = None
        settings.openai_api_key = ""
        settings.openai_model = "gpt-4o-mini"
        settings.openai_timeout = 3
        settings.openai_max_retries = 2
        settings.ai_log_path = str(Path(self.temp_dir.name) / "ai_calls.jsonl")

    def tearDown(self) -> None:
        for key, value in self.original_settings.items():
            setattr(settings, key, value)
        self.temp_dir.cleanup()

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

    def test_parse_json_response_handles_code_fences(self) -> None:
        service = AIService()
        parsed = service._parse_json_response('```json\n{"summary": "ok", "score": 1}\n```')
        self.assertEqual(parsed["summary"], "ok")
        self.assertEqual(parsed["score"], 1)

    def test_openai_mode_renders_prompt_parses_response_and_logs_call(self) -> None:
        settings.ai_mode = "openai"
        settings.openai_api_key = "test-key"
        settings.openai_max_retries = 1

        class FakeOpenAIService(AIService):
            def _call_openai(self, rendered_prompt: str) -> str:
                self.rendered_prompt = rendered_prompt
                return '{"summary": "real response", "required_skills": ["Python"]}'

        service = FakeOpenAIService()
        result = service.generate_response(
            "job_summary.prompt.md",
            company_name="TestCo",
            job_title="Backend Engineer",
            job_description="Build APIs",
        )

        self.assertEqual(result["summary"], "real response")
        self.assertIn("TestCo", service.rendered_prompt)
        self.assertIn("Backend Engineer", service.rendered_prompt)

        logs = Path(settings.ai_log_path).read_text(encoding="utf-8").strip().splitlines()
        log_payload = json.loads(logs[-1])
        self.assertTrue(log_payload["success"])
        self.assertEqual(log_payload["mode"], "openai")
        self.assertEqual(log_payload["details"]["model"], settings.openai_model)

    def test_openai_mode_retries_failed_calls(self) -> None:
        settings.ai_mode = "openai"
        settings.openai_api_key = "test-key"
        settings.openai_max_retries = 2

        class FlakyOpenAIService(AIService):
            def __init__(self) -> None:
                super().__init__()
                self.calls = 0

            def _call_openai(self, rendered_prompt: str) -> str:
                self.calls += 1
                if self.calls == 1:
                    raise TimeoutError("request timed out")
                return '{"summary": "retried"}'

        service = FlakyOpenAIService()
        with patch("backend.app.services.ai_service.time.sleep", return_value=None):
            result = service.generate_response(
                "job_summary.prompt.md",
                company_name="TestCo",
                job_title="Backend Engineer",
                job_description="Build APIs",
            )

        self.assertEqual(result["summary"], "retried")
        self.assertEqual(service.calls, 2)

    def test_openai_mode_requires_api_key(self) -> None:
        settings.ai_mode = "openai"
        settings.openai_api_key = ""

        service = AIService()
        result = service.generate_response(
            "job_summary.prompt.md",
            company_name="TestCo",
            job_title="Backend Engineer",
            job_description="Build APIs",
        )

        self.assertIn("error", result)
        self.assertIn("OPENAI_API_KEY", result["error"])

    def test_timeout_setting_is_applied_to_service(self) -> None:
        settings.ai_mode = "openai"
        settings.openai_api_key = "test-key"
        settings.openai_timeout = 7

        service = AIService()

        self.assertEqual(service.timeout, 7)


if __name__ == "__main__":
    unittest.main()
