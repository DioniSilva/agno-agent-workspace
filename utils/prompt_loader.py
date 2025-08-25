from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml
from jinja2 import Template

try:
    import tiktoken
except Exception:
    tiktoken = None


def _read_yaml(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text())


def _render_template(template: str, ctx: Dict[str, Any]) -> str:
    return Template(template).render(**ctx)

def _count_tokens(prompts: List[Dict[str, str]], model: str | None = None) -> int:
    if model and tiktoken is not None:
        try:
            enc = tiktoken.encoding_for_model(model)
            return sum(len(enc.encode(m["content"])) for m in prompts)
        except Exception:
            pass
    return 0

class PromptKey(str, Enum):
    SYSTEM_MESSAGE = "system_message"
    INSTRUCTIONS = "instructions"
    DESCRIPTION = "description"
    GOAL = "goal"
    EXPECTED_OUTPUT = "expected_output"
    METADATA = "metadata"


def render_prompt(path: str, model: str | None = None, **ctx) -> Tuple[Dict[str, str], Dict[str, Any]]:
    """
    Load a prompt YAML, render prompts with the provided context and return (prompts, metadata).

    prompts: list of dicts with keys: role, content
    metadata: dict from YAML
    """
    p = Path(path)
    if not p.exists():
        p = Path.cwd() / path
        if not p.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")

    data = _read_yaml(p)
    metadata: Dict[str, Any] = data.get(PromptKey.METADATA, {})

    raw = data.get("prompt")
    if not isinstance(raw, dict):
        raise ValueError(f"Prompt file must contain a structured 'prompt' mapping: {path}")

    return raw, metadata
