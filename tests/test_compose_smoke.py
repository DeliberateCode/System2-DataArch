"""Smoke tests: validate that DataPipelineOverlay composes cleanly against System2.

The overlay intentionally targets 6 pipeline agents and 2 spec artifacts
(requirements + design); it ships no mcp_servers, permissions, hooks, or tools.
Total-coverage assertions from the template are therefore relaxed to scope checks.
"""

import json
import os
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OVERLAY_ROOT = os.path.join(REPO_ROOT, "plugin")
SYSTEM2_ROOT = os.environ.get(
    "SYSTEM2_ROOT", os.path.join(os.path.dirname(REPO_ROOT), "System2")
)
SYSTEM2_PLUGIN = os.path.join(SYSTEM2_ROOT, "plugin")
COMPOSER_DIR = os.path.join(SYSTEM2_PLUGIN, "scripts")

sys.path.insert(0, COMPOSER_DIR)

from composer import compose, validate_manifest, _scan_for_injection  # noqa: E402

MANIFEST_PATH = os.path.join(OVERLAY_ROOT, "system2.overlay.json")
CONTRIBUTIONS_DIR = os.path.join(OVERLAY_ROOT, "contributions")

EXPECTED_CONTRIBUTION_IDS = {
    # Orchestrator principles
    "dp-principle-orchestrate-not-compute",
    "dp-principle-data-aware-over-time-aware",
    "dp-principle-govern-the-interface",
    # Orchestrator gate consultations
    "dp-gate1-consultation",
    "dp-gate3-consultation",
    # design-architect
    "dp-architect-design-constraints",
    "dp-architect-required-sections",
    # requirements-engineer
    "dp-requirements-guardrails",
    "dp-requirements-req-sections",
    # executor
    "dp-executor-discipline",
    "dp-executor-verification",
    # test-engineer
    "dp-test-verification-workflow",
    "dp-test-authoring-rules",
    # code-reviewer
    "dp-reviewer-criteria",
    "dp-reviewer-surface-area",
    # security-sentinel
    "dp-security-threat-scope",
    # Spec required sections — requirements
    "dp-req-idempotency-backfill",
    "dp-req-compute-boundary",
    "dp-req-layered-dq",
    "dp-req-lineage-provenance",
    # Spec required sections — design
    "dp-design-ml-split-pit",
    "dp-design-eval-golden",
    "dp-design-reproducibility",
    "dp-design-skew-leakage",
    # Delegation advisory source
    "dp-airflow-facts",
    # Auxiliary agent
    "dp-pipeline-scout",
}

# The overlay targets these 6 pipeline agents by design (REQ-DP-008).
EXPECTED_AGENTS = {
    "design-architect",
    "requirements-engineer",
    "executor",
    "test-engineer",
    "code-reviewer",
    "security-sentinel",
}


def _load_schema_and_anchor_map():
    schema_path = os.path.join(SYSTEM2_PLUGIN, "schemas", "overlay.schema.json")
    anchor_path = os.path.join(SYSTEM2_PLUGIN, "schemas", "anchor-map.json")
    with open(schema_path) as f:
        schema = json.load(f)
    with open(anchor_path) as f:
        anchor_map = json.load(f)
    return schema, anchor_map


def _load_manifest():
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def test_manifest_validates():
    manifest = _load_manifest()
    schema, anchor_map = _load_schema_and_anchor_map()
    result = validate_manifest(manifest, schema, OVERLAY_ROOT, anchor_map)
    assert result.valid, f"Validation errors: {result.errors}"
    assert result.errors == []


def test_no_validation_warnings():
    manifest = _load_manifest()
    schema, anchor_map = _load_schema_and_anchor_map()
    result = validate_manifest(manifest, schema, OVERLAY_ROOT, anchor_map)
    assert result.warnings == [], f"Validation warnings: {result.warnings}"


def test_content_files_exist_and_nonempty():
    manifest = _load_manifest()
    contributions = manifest["contributions"]

    for principle in contributions.get("orchestrator", {}).get("principles", []):
        path = os.path.join(OVERLAY_ROOT, principle["content_file"])
        assert os.path.isfile(path), f"Missing: {principle['content_file']}"
        assert os.path.getsize(path) > 0, f"Empty: {principle['content_file']}"

    for gate_num, gate_data in contributions.get("orchestrator", {}).get("gates", {}).items():
        for consultation in gate_data.get("consultation", []):
            path = os.path.join(OVERLAY_ROOT, consultation["content_file"])
            assert os.path.isfile(path), f"Missing: {consultation['content_file']}"
            assert os.path.getsize(path) > 0, f"Empty: {consultation['content_file']}"

    for agent_name, agent_data in contributions.get("agents", {}).items():
        for anchor, sections in agent_data.get("prompt_sections", {}).items():
            for section in sections:
                path = os.path.join(OVERLAY_ROOT, section["content_file"])
                assert os.path.isfile(path), f"Missing: {section['content_file']}"
                assert os.path.getsize(path) > 0, f"Empty: {section['content_file']}"


def test_auxiliary_agent_files_exist():
    manifest = _load_manifest()
    for agent in manifest["contributions"].get("auxiliary_agents", []):
        path = os.path.join(OVERLAY_ROOT, agent["agent_file"])
        assert os.path.isfile(path), f"Missing auxiliary agent: {agent['agent_file']}"
        assert os.path.getsize(path) > 0, f"Empty auxiliary agent: {agent['agent_file']}"


def test_no_injection_patterns_in_content():
    """Content files must not trigger the composer's injection scanner."""
    issues = []
    for root, _dirs, files in os.walk(CONTRIBUTIONS_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath) as f:
                content = f.read()
            warnings = _scan_for_injection(content, fpath)
            issues.extend(warnings)
    assert issues == [], f"Injection patterns found: {issues}"


def test_targeted_agents_covered():
    """Exactly the 6 in-scope pipeline agents are targeted — no more, no fewer."""
    manifest = _load_manifest()
    covered = set(manifest["contributions"].get("agents", {}).keys())
    assert covered == EXPECTED_AGENTS, (
        f"Agent coverage mismatch. Expected {sorted(EXPECTED_AGENTS)}, "
        f"got {sorted(covered)}"
    )


def test_declared_anchors_are_valid():
    """Every declared prompt-section anchor is a real anchor for its agent.

    This is a subset/validity check, not a total-coverage check: the overlay
    intentionally contributes to only some anchors.
    """
    manifest = _load_manifest()
    _, anchor_map = _load_schema_and_anchor_map()
    agents_contrib = manifest["contributions"].get("agents", {})

    invalid = []
    for agent_name, agent_data in agents_contrib.items():
        valid_anchors = set(
            anchor_map["agents"].get(agent_name, {}).get("anchors", {}).keys()
        )
        for anchor_name in agent_data.get("prompt_sections", {}):
            if anchor_name not in valid_anchors:
                invalid.append(f"{agent_name}.{anchor_name}")
    assert not invalid, f"Invalid anchors declared: {invalid}"


def test_targeted_spec_artifacts_covered():
    """requirements + design carry sections; context + tasks intentionally do not."""
    manifest = _load_manifest()
    spec = manifest["contributions"].get("spec", {})
    for artifact in ["requirements", "design"]:
        sections = spec.get(artifact, {}).get("required_sections", [])
        assert len(sections) > 0, f"spec/{artifact}.md has no required sections"
    for artifact in ["context", "tasks"]:
        sections = spec.get(artifact, {}).get("required_sections", [])
        assert len(sections) == 0, (
            f"spec/{artifact}.md unexpectedly has sections; the overlay targets "
            f"only requirements + design by design"
        )


def test_dry_run_compose_succeeds():
    with tempfile.TemporaryDirectory() as tmp:
        result = compose(
            base_path=SYSTEM2_PLUGIN,
            overlay_paths=[OVERLAY_ROOT],
            project_path=tmp,
            dry_run=True,
        )
        assert result["errors"] == [], f"Compose errors: {result['errors']}"
        assert result["claude_md"], "Composed CLAUDE.md is empty"


def test_composed_output_contains_overlay_markers():
    """Composed CLAUDE.md must contain key overlay content markers."""
    with tempfile.TemporaryDirectory() as tmp:
        result = compose(
            base_path=SYSTEM2_PLUGIN,
            overlay_paths=[OVERLAY_ROOT],
            project_path=tmp,
            dry_run=True,
        )
        claude_md = result["claude_md"]

        markers = [
            "data-pipeline",
            "Orchestrate, don't compute",
        ]
        for marker in markers:
            assert marker in claude_md, (
                f"Composed CLAUDE.md missing expected marker: {marker!r}"
            )


def test_all_contribution_ids_applied():
    with tempfile.TemporaryDirectory() as tmp:
        result = compose(
            base_path=SYSTEM2_PLUGIN,
            overlay_paths=[OVERLAY_ROOT],
            project_path=tmp,
            dry_run=True,
        )
        lock = result.get("lock", {})
        applied_ids = set()
        for id_list in lock.get("contributions_applied", {}).values():
            applied_ids.update(id_list)

        missing = EXPECTED_CONTRIBUTION_IDS - applied_ids
        assert not missing, f"Contributions not applied: {missing}"


def test_contribution_id_prefix():
    """All contribution IDs use the dp- prefix."""
    manifest = _load_manifest()
    bad_ids = []

    def collect_ids(obj):
        if isinstance(obj, dict):
            if "id" in obj and isinstance(obj["id"], str):
                if not obj["id"].startswith("dp-"):
                    bad_ids.append(obj["id"])
            for v in obj.values():
                collect_ids(v)
        elif isinstance(obj, list):
            for item in obj:
                collect_ids(item)

    collect_ids(manifest["contributions"])
    assert not bad_ids, f"IDs without dp- prefix: {bad_ids}"


def test_summaries_present_for_non_inline():
    """Every non-inline prompt_section contribution has a summary."""
    manifest = _load_manifest()
    missing = []
    for agent_name, agent_data in manifest["contributions"].get("agents", {}).items():
        for anchor, sections in agent_data.get("prompt_sections", {}).items():
            for section in sections:
                if not section.get("inline", False) and "summary" not in section:
                    missing.append(f"{agent_name}.{anchor}.{section.get('id', '?')}")
    assert not missing, f"Missing summaries: {missing}"


def test_contribution_types_present():
    """The overlay ships exactly the contribution types it declares — and none
    of the runtime-surface types it deliberately omits (mcp_servers, permissions,
    hooks, tools)."""
    manifest = _load_manifest()
    contributions = manifest["contributions"]

    assert "orchestrator" in contributions, "Missing orchestrator contributions"
    assert "principles" in contributions["orchestrator"], "Missing orchestrator.principles"
    assert "gates" in contributions["orchestrator"], "Missing orchestrator.gates"
    assert "delegation" in contributions, "Missing delegation contributions"
    assert "advisory_sources" in contributions["delegation"], "Missing delegation.advisory_sources"
    assert "agents" in contributions, "Missing agents contributions"
    assert "spec" in contributions, "Missing spec contributions"
    assert "auxiliary_agents" in contributions, "Missing auxiliary_agents"

    # Deliberately-absent runtime-surface types (design Rejected Abstractions).
    assert "mcp_servers" not in contributions, "Overlay must not ship mcp_servers"
    assert "permissions" not in contributions, "Overlay must not ship permissions"
    for agent_name, agent_data in contributions["agents"].items():
        assert "tools" not in agent_data, f"{agent_name} must not declare tools"
        assert "hooks" not in agent_data, f"{agent_name} must not declare hooks"


ALL_TESTS = [
    test_manifest_validates,
    test_no_validation_warnings,
    test_content_files_exist_and_nonempty,
    test_auxiliary_agent_files_exist,
    test_no_injection_patterns_in_content,
    test_targeted_agents_covered,
    test_declared_anchors_are_valid,
    test_targeted_spec_artifacts_covered,
    test_dry_run_compose_succeeds,
    test_composed_output_contains_overlay_markers,
    test_all_contribution_ids_applied,
    test_contribution_id_prefix,
    test_summaries_present_for_non_inline,
    test_contribution_types_present,
]


if __name__ == "__main__":
    passed = 0
    failed = 0
    for test_fn in ALL_TESTS:
        try:
            test_fn()
            print(f"  [PASS] {test_fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {test_fn.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {test_fn.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed, {passed + failed} total")
    sys.exit(0 if failed == 0 else 1)
