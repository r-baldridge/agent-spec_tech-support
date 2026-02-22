"""Environment settings for the tech-support-agent system."""

import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    """Runtime settings loaded from environment variables with sensible defaults."""

    # LiteLLM proxy for Claude access
    litellm_proxy_url: str = field(
        default_factory=lambda: os.environ.get(
            "LITELLM_PROXY_URL", "http://localhost:4000/v1"
        )
    )
    litellm_api_key: str = field(
        default_factory=lambda: os.environ.get("LITELLM_API_KEY", "")
    )

    # OpenAI
    openai_api_key: str = field(
        default_factory=lambda: os.environ.get("OPENAI_API_KEY", "")
    )

    # Ollama (local)
    ollama_url: str = field(
        default_factory=lambda: os.environ.get(
            "OLLAMA_URL", "http://localhost:11434"
        )
    )

    # vLLM (on-prem)
    vllm_url: str = field(
        default_factory=lambda: os.environ.get(
            "VLLM_URL", "http://localhost:8000"
        )
    )

    # Swarm limits
    max_concurrent_swarms: int = field(
        default_factory=lambda: int(os.environ.get("MAX_CONCURRENT_SWARMS", "3"))
    )
    max_agents_per_swarm: int = field(
        default_factory=lambda: int(os.environ.get("MAX_AGENTS_PER_SWARM", "5"))
    )
    swarm_timeout_seconds: int = field(
        default_factory=lambda: int(os.environ.get("SWARM_TIMEOUT_SECONDS", "1800"))
    )

    # Logging / audit
    audit_log_dir: str = field(
        default_factory=lambda: os.environ.get("AUDIT_LOG_DIR", "./audit_logs")
    )
