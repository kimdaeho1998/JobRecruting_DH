from typing import Any, Optional

try:
    from app.services.prompt_loader import PromptLoader
except ModuleNotFoundError:  # pragma: no cover - allows import from repo root during local checks
    from backend.app.services.prompt_loader import PromptLoader


class AIService:
    """Service layer for AI prompt execution.

    The current implementation returns mock responses so the application can be
    developed without calling the OpenAI API. It is structured so the logic can
    be swapped for a real provider later.
    """

    def __init__(self, prompt_loader: Optional[PromptLoader] = None) -> None:
        self.prompt_loader = prompt_loader or PromptLoader()

    def generate_response(self, prompt_file: str, **variables: Any) -> dict[str, Any]:
        rendered_prompt = self.prompt_loader.render(prompt_file, **variables)

        # Placeholder for future OpenAI integration.
        # Example: client.responses.create(model="gpt-4o", input=rendered_prompt)
        return self._mock_response(prompt_file)

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
