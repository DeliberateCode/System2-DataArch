# DataPipelineOverlay Development

This repo is a **System2 overlay** for data pipeline engineering with Apache Airflow
(ELT/ETL + labeled-data delivery for ML cycles). It does not run System2's agent pipeline
itself; it provides contribution content that System2's compose engine injects into pipeline
agents. Scaffolded from System2-OverlayTemplate — contribution content is being replaced with
domain guidance derived from `spec/context.md` (see `research/` and the README roadmap).

Use the contribution-ID prefix `dp-` (data-pipeline) for new contributions, replacing the
template's `tmpl-` prefix as files are rewritten.

## Project Structure

```
plugin/                              # Installable unit (referenced by marketplace.json)
├── .claude-plugin/plugin.json       # Plugin identity
├── system2.overlay.json             # Overlay manifest (contribution declarations)
├── contributions/                   # Content files referenced by the manifest
│   ├── orchestrator/                # Principles and gate consultations
│   │   ├── principle.md             # Operating principle injected into CLAUDE.md
│   │   └── gate1-consultation.md    # Gate 1 pre-delegation check
│   └── agents/                      # Prompt sections injected into pipeline agents
│       ├── executor-safety.md       # (inline: true — content inlined in CLAUDE.md)
│       ├── executor-discipline.md   # (inline: false — referenced as file pointer)
│       └── ...                      # One file per anchor point (22 total)
├── agents/                          # Auxiliary agent definitions
│   └── template-scout.md            # Non-pipeline agent with YAML frontmatter
└── hooks/                           # Hook scripts referenced by the manifest
    └── post-edit-check.py           # Example PostToolUse hook (stdlib only)
tests/                               # Smoke tests (compose against local System2)
```

## Testing

Smoke tests validate the manifest, content files, and dry-run composition against System2.
System2 must be cloned alongside this repo at `../System2`.

```bash
python3 tests/test_compose_smoke.py
```

Or with pytest:

```bash
pytest tests/
```

## Conventions

- Contribution content files are plain Markdown — no frontmatter, no YAML.
- Each file is self-contained guidance for a specific anchor point in a specific agent.
- Content should be prescriptive but scoped: tell the agent what to do, not how System2 works.
- Summaries in `system2.overlay.json` must accurately reflect the content file — the orchestrator
  reads the summary to decide whether to include the full content in a delegation.
- Contribution IDs use the `tmpl-` prefix (for "template"). Replace with your own prefix.
- All IDs must be unique across the manifest.

## Overlay Manifest Schema

The manifest (`plugin/system2.overlay.json`) is validated against System2's
`plugin/schemas/overlay.schema.json`. Valid contribution types: orchestrator principles,
gate consultations, agent prompt sections (keyed by anchor name), spec required sections,
delegation advisory sources, auxiliary agents, MCP servers, and permissions.

Valid anchor names per agent are defined in `plugin/schemas/anchor-map.json` in System2.

## Adding Contributions

1. Write the content file in `plugin/contributions/`.
2. Add the contribution declaration to `plugin/system2.overlay.json` with a unique prefixed ID.
3. Add the ID to `EXPECTED_CONTRIBUTION_IDS` in `tests/test_compose_smoke.py`.
4. Run smoke tests to validate.

## Inline vs. File-Pointer Contributions

Agent prompt sections support two modes via the `inline` field:

- **`inline: true`** — Content is inserted directly into the composed CLAUDE.md. Best for
  short, critical directives (safety rules, hard constraints). No `summary` field needed.
- **`inline: false`** (default) — Content is copied to `.system2/overlays/<name>/` and
  referenced as a file pointer. The `summary` field is required and must accurately describe
  the content, since the orchestrator reads the summary to decide relevance. Best for longer,
  domain-specific guidance.

This template uses `inline: true` for executor safety rules and `inline: false` for
everything else, demonstrating both patterns.
