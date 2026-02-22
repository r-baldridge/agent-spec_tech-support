"""Shared test fixtures."""

import sys
import os

import pytest

# Ensure the project root is on sys.path so all imports resolve.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyagentspec.agent import Agent
from pyagentspec.llms import OpenAiCompatibleConfig, LlmGenerationConfig

from config.settings import Settings


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def dummy_llm_config():
    """A lightweight LLM config for unit tests (no real endpoint needed)."""
    return OpenAiCompatibleConfig(
        name="test_llm",
        url="http://localhost:9999/v1",
        model_id="test-model",
        default_generation_parameters=LlmGenerationConfig(
            temperature=0.1, max_tokens=256
        ),
    )


@pytest.fixture
def base_agent(dummy_llm_config):
    from agents.base_agent import create_base_agent
    return create_base_agent(dummy_llm_config)


@pytest.fixture
def triage_manager(dummy_llm_config):
    from agents.triage_manager import create_triage_manager
    return create_triage_manager(dummy_llm_config)


@pytest.fixture
def expert_reviewer(dummy_llm_config):
    from agents.expert_reviewer import create_expert_reviewer
    return create_expert_reviewer(dummy_llm_config)
