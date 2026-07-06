from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency for local env
    load_dotenv = None

try:
    from app.core.config import REPO_ROOT, settings
except ModuleNotFoundError:  # pragma: no cover - allows import from repo root during local checks
    from backend.app.core.config import REPO_ROOT, settings

try:
    from app.services.prompt_loader import PromptLoader
except ModuleNotFoundError:  # pragma: no cover - allows import from repo root during local checks
    from backend.app.services.prompt_loader import PromptLoader


class AIServiceError(RuntimeError):
    """Raised when the AI provider cannot produce a usable result."""


class AIService:
    """Service layer for AI prompt execution with mock and OpenAI modes."""

    def __init__(self, prompt_loader: Optional[PromptLoader] = None) -> None:
        if load_dotenv is not None:
            load_dotenv(REPO_ROOT / ".env", override=False)

        self.prompt_loader = prompt_loader or PromptLoader()
        self.logger = logging.getLogger("jobinsight.ai_service")
        self._configure_logging()

        self.mock_mode = self._resolve_mock_mode()
        self.api_key = settings.openai_api_key.strip()
        self.model = settings.openai_model.strip()
        self.timeout = settings.openai_timeout
        self.max_retries = max(1, settings.openai_max_retries)
        self.log_path = Path(settings.ai_log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _configure_logging(self) -> None:
        if self.logger.handlers:
            return
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _resolve_mock_mode(self) -> bool:
        ai_mode = settings.ai_mode.strip().lower()
        if ai_mode in {"mock", "test"}:
            return True
        if ai_mode in {"openai", "real", "api"}:
            return False

        if settings.ai_mock_mode is not None:
            normalized = settings.ai_mock_mode.strip().lower()
            if normalized in {"1", "true", "yes", "on"}:
                return True
            if normalized in {"0", "false", "no", "off"}:
                return False

        self.logger.warning("Unknown AI_MODE=%s. Falling back to mock mode.", settings.ai_mode)
        return True

    def generate_response(self, prompt_file: str, **variables: Any) -> dict[str, Any]:
        rendered_prompt = self.prompt_loader.render(prompt_file, **variables)

        if self.mock_mode:
            self._log_call(prompt_file=prompt_file, mode="mock", success=True, details={"mock_mode": True})
            return self._mock_response(prompt_file)

        if not self.api_key:
            message = "OPENAI_API_KEY is not configured. Set it in the environment or .env file."
            self._log_call(prompt_file=prompt_file, mode="openai", success=False, details={"error": message})
            return {"error": message}

        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info("Calling OpenAI for %s (attempt %s)", prompt_file, attempt)
                started_at = time.perf_counter()
                response_text = self._call_openai(rendered_prompt)
                parsed_response = self._parse_json_response(response_text)
                self._log_call(
                    prompt_file=prompt_file,
                    mode="openai",
                    success=True,
                    details={
                        "attempt": attempt,
                        "model": self.model,
                        "duration_ms": int((time.perf_counter() - started_at) * 1000),
                    },
                )
                return parsed_response
            except Exception as exc:  # pragma: no cover - exercised in runtime, covered by logging path
                last_error = exc
                self.logger.warning("OpenAI request failed for %s (attempt %s): %s", prompt_file, attempt, exc)
                self._log_call(
                    prompt_file=prompt_file,
                    mode="openai",
                    success=False,
                    details={"attempt": attempt, "error": str(exc), "model": self.model},
                )
                if attempt < self.max_retries:
                    time.sleep(min(2 ** (attempt - 1), 4))

        return {
            "error": "AI provider request failed",
            "details": str(last_error) if last_error else "Unknown error",
            "provider": "openai",
        }

    def _call_openai(self, rendered_prompt: str) -> str:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - depends on package installation
            raise AIServiceError("The openai package is not installed. Install it with pip.") from exc

        client = OpenAI(api_key=self.api_key, timeout=self.timeout)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": rendered_prompt}],
            temperature=0,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        if not content:
            raise AIServiceError("OpenAI returned an empty response")
        return content

    def _parse_json_response(self, response_text: str | dict[str, Any]) -> dict[str, Any]:
        if isinstance(response_text, dict):
            return response_text

        text = str(response_text).strip()
        if not text:
            raise AIServiceError("OpenAI returned an empty payload")

        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text).strip()

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                raise AIServiceError("Unable to parse OpenAI JSON response") from None
            parsed = json.loads(match.group(0))

        if not isinstance(parsed, dict):
            raise AIServiceError("OpenAI JSON response must be an object")

        return parsed

    def _log_call(
        self,
        *,
        prompt_file: str,
        mode: str,
        success: bool,
        details: dict[str, Any],
    ) -> None:
        payload = {
            "prompt_file": prompt_file,
            "mode": mode,
            "success": success,
            "timestamp": time.time(),
            "details": details,
        }
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def _mock_response(self, prompt_file: str) -> dict[str, Any]:
        if prompt_file == "job_summary.prompt.md":
            return {
                "summary": "Mock summary for the job posting.",
                "key_responsibilities": ["Backend development", "System design"],
                "required_skills": ["Python", "FastAPI"],
            }

        if prompt_file == "skill_extraction.prompt.md":
            return {
                "technical_skills": ["Python", "FastAPI", "PostgreSQL"],
                "preferred_skills": ["Docker", "CI/CD"],
            }

        if prompt_file == "job_fit_analysis.prompt.md":
            return {
                "fit_score": 84,
                "summary": "The candidate appears well matched to the role.",
                "strengths": ["Relevant backend experience", "Strong Python skills"],
                "gaps": ["Additional cloud experience"],
            }

        if prompt_file == "resume_analysis.prompt.md":
            return {
                "experience_summary": "Candidate has strong backend engineering experience.",
                "skills": ["Python", "SQLAlchemy", "Docker"],
                "strengths": ["Problem solving", "System design"],
            }

        if prompt_file == "cover_letter.prompt.md":
            return {"cover_letter": "Mock cover letter draft."}

        if prompt_file == "interview_questions.prompt.md":
            return {
                "technical_questions": ["Explain your experience with API design."],
                "behavioral_questions": ["Describe a challenging project you led."],
            }

        if prompt_file == "company_analysis.prompt.md":
            return {
                "industry": "Software Development",
                "strengths": ["Innovation", "Engineering quality"],
                "summary": "Mock company analysis.",
            }

        if prompt_file == "job_compare.prompt.md":
            return {
                "comparison": {
                    "strengths_a": ["Broader scope"],
                    "strengths_b": ["More focused role"],
                    "differences": ["One emphasizes backend scale", "Another focuses on product delivery"],
                },
                "recommended_job": "Job A",
            }

        return {"result": "mock response"}
