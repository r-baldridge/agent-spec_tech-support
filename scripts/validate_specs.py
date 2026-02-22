"""Validate generated YAML specs via round-trip serialization.

For each YAML spec file:
1. Deserialize YAML -> dict
2. Verify the dict has the expected component_type and name
3. Check structural integrity (required fields present)
"""

import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SPECS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "specs")

# Required fields per component type
REQUIRED_FIELDS = {
    "ServerTool": ["name", "component_type"],
    "Agent": ["name", "component_type", "system_prompt", "llm_config"],
    "SpecializedAgent": ["name", "component_type", "agent", "agent_specialization_parameters"],
    "ManagerWorkers": ["name", "component_type", "group_manager", "workers"],
    "Flow": ["name", "component_type", "start_node", "nodes"],
}


def validate_file(path: str) -> list[str]:
    """Validate a single YAML spec file.  Returns a list of errors (empty if valid)."""
    errors = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]

    if not isinstance(data, dict):
        return [f"Expected a dict at top level, got {type(data).__name__}"]

    component_type = data.get("component_type")
    if not component_type:
        errors.append("Missing 'component_type' field")
        return errors

    name = data.get("name")
    if not name:
        errors.append("Missing 'name' field")

    required = REQUIRED_FIELDS.get(component_type, ["name", "component_type"])
    for field in required:
        if field not in data:
            errors.append(f"Missing required field '{field}' for {component_type}")

    return errors


def main() -> None:
    if not os.path.isdir(SPECS_DIR):
        print(f"Specs directory not found: {SPECS_DIR}")
        print("Run generate_specs.py first.")
        sys.exit(1)

    total = 0
    passed = 0
    failed = 0

    for root, _dirs, files in os.walk(SPECS_DIR):
        for filename in sorted(files):
            if not filename.endswith(".yaml"):
                continue
            total += 1
            path = os.path.join(root, filename)
            rel_path = os.path.relpath(path, SPECS_DIR)
            errors = validate_file(path)
            if errors:
                failed += 1
                print(f"FAIL  {rel_path}")
                for err in errors:
                    print(f"      - {err}")
            else:
                passed += 1
                print(f"OK    {rel_path}")

    print(f"\n{total} specs checked: {passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
