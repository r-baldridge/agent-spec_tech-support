"""LLM configuration factory for multiple providers."""

from enum import Enum
from typing import Optional

from pyagentspec.llms import (
    LlmGenerationConfig,
    OllamaConfig,
    OpenAiCompatibleConfig,
    VllmConfig,
)

from config.settings import Settings


class LLMProfile(str, Enum):
    """Available LLM profiles, each mapping to a provider + model + generation params."""

    CLAUDE_DEFAULT = "claude/default"
    OPENAI_DEFAULT = "openai/default"
    OLLAMA_FAST = "ollama/fast"
    VLLM_LARGE = "vllm/large"


# Generation parameter presets tuned per agent role.
_GENERATION_PRESETS = {
    "manager": LlmGenerationConfig(temperature=0.3, max_tokens=4096),
    "specialist": LlmGenerationConfig(temperature=0.2, max_tokens=8192),
    "reviewer": LlmGenerationConfig(temperature=0.1, max_tokens=16384),
}


def get_llm_config(
    profile: LLMProfile,
    role: str = "specialist",
    settings: Optional[Settings] = None,
) -> OpenAiCompatibleConfig:
    """Build an LLM config for the given profile and agent role.

    Parameters
    ----------
    profile:
        Which provider / model combination to use.
    role:
        One of ``"manager"``, ``"specialist"``, or ``"reviewer"``.
        Controls temperature and token limits.
    settings:
        Runtime settings (URLs, API keys).  Falls back to defaults when ``None``.
    """
    if settings is None:
        settings = Settings()

    generation_params = _GENERATION_PRESETS.get(
        role, _GENERATION_PRESETS["specialist"]
    )

    if profile == LLMProfile.CLAUDE_DEFAULT:
        return OpenAiCompatibleConfig(
            name=f"claude_{role}",
            url=settings.litellm_proxy_url,
            model_id="claude-sonnet-4-20250514",
            api_key=settings.litellm_api_key,
            default_generation_parameters=generation_params,
        )

    if profile == LLMProfile.OPENAI_DEFAULT:
        return OpenAiCompatibleConfig(
            name=f"openai_{role}",
            url="https://api.openai.com/v1",
            model_id="gpt-4o",
            api_key=settings.openai_api_key,
            default_generation_parameters=generation_params,
        )

    if profile == LLMProfile.OLLAMA_FAST:
        return OllamaConfig(
            name=f"ollama_{role}",
            url=settings.ollama_url,
            model_id="llama3.1:70b",
            default_generation_parameters=generation_params,
        )

    if profile == LLMProfile.VLLM_LARGE:
        return VllmConfig(
            name=f"vllm_{role}",
            url=settings.vllm_url,
            model_id="Qwen2.5-72B",
            default_generation_parameters=generation_params,
        )

    raise ValueError(f"Unknown LLM profile: {profile}")
