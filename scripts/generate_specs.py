"""Generate YAML specs from Python definitions into the specs/ directory."""

import os
import sys

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyagentspec.serialization import AgentSpecSerializer

from config.llm_profiles import LLMProfile, get_llm_config
from agents.base_agent import create_base_agent
from agents.triage_manager import create_triage_manager
from agents.expert_reviewer import create_expert_reviewer
from agents.specialist_registry import SpecialistRegistry
from modes.manager_mode import build_manager_workers
from modes.orchestrator import build_orchestrator
from tools.tool_registry import ToolRegistry

SPECS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "specs")


def _write_spec(category: str, name: str, yaml_str: str) -> None:
    out_dir = os.path.join(SPECS_DIR, category)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.yaml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(yaml_str)
    print(f"  -> {path}")


def main() -> None:
    serializer = AgentSpecSerializer()

    # LLM configs for construction
    specialist_llm = get_llm_config(LLMProfile.OPENAI_DEFAULT, role="specialist")
    manager_llm = get_llm_config(LLMProfile.CLAUDE_DEFAULT, role="manager")
    reviewer_llm = get_llm_config(LLMProfile.CLAUDE_DEFAULT, role="reviewer")

    # -- Tools --
    print("Generating tool specs...")
    for name, tool in ToolRegistry.all_tools().items():
        _write_spec("tools", name, serializer.to_yaml(tool))

    # -- Agents --
    print("Generating agent specs...")
    base_agent = create_base_agent(specialist_llm)
    _write_spec("agents", "base_agent", serializer.to_yaml(base_agent))

    specialists = SpecialistRegistry.build_all(base_agent)
    for domain, specialist in specialists.items():
        _write_spec("agents", f"specialist_{domain}", serializer.to_yaml(specialist))

    triage_manager = create_triage_manager(manager_llm)
    _write_spec("agents", "triage_manager", serializer.to_yaml(triage_manager))

    expert_reviewer = create_expert_reviewer(reviewer_llm)
    _write_spec("agents", "expert_reviewer", serializer.to_yaml(expert_reviewer))

    # -- Modes --
    print("Generating mode specs...")
    manager_workers = build_manager_workers(triage_manager, base_agent)
    _write_spec("modes", "manager_workers", serializer.to_yaml(manager_workers))

    orchestrator = build_orchestrator(manager_workers, expert_reviewer, manager_llm)
    _write_spec("modes", "orchestrator", serializer.to_yaml(orchestrator))

    print("Done.")


if __name__ == "__main__":
    main()
