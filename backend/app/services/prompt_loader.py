from pathlib import Path
from typing import Optional


class PromptLoader:
    """Load prompt templates from the scripts/prompts directory."""

    def __init__(self, prompts_dir: Optional[str] = None) -> None:
        base_dir = Path(__file__).resolve().parents[3]
        self.prompts_dir = Path(prompts_dir) if prompts_dir else base_dir / "scripts" / "prompts"

    def load(self, file_name: str) -> str:
        prompt_path = self.prompts_dir / file_name
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        return prompt_path.read_text(encoding="utf-8")

    def render(self, file_name: str, **variables: str) -> str:
        template = self.load(file_name)
        rendered = template
        for key, value in variables.items():
            rendered = rendered.replace("{" + key + "}", str(value))
        return rendered
