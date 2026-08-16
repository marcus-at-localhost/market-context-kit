# Market Context Kit Search Context Consumer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let Market Context Kit safely consume a validated `SEARCH-CONTEXT.v1.json` artifact during orchestrator synthesis without exposing analytics to scoring subagents or changing independent audit scores.

**Architecture:** A shared reference defines artifact discovery, domain and freshness checks, provenance rules, and failure behavior. The audit, report, and SEO skills load that reference only when the user explicitly supplies an artifact or an exact-domain artifact is found in the current client's Search Context output. Static tests protect the Data Manifest exclusion and orchestrator-only boundary.

**Tech Stack:** Markdown Claude Code skills and pytest static contract tests.

**Spec:** `E:/WEB/GEO/.claude/skills/search-context-kit/docs/superpowers/specs/2026-08-16-search-context-kit-design.md`

## Global Constraints

- Keep all five audit subagents independent of analytics exports.
- Never put `SEARCH-CONTEXT.v1.json` on a subagent Data Manifest.
- Require schema version `1.0`, exact target domain, a valid reporting period, and visible source status.
- Use analytics for prioritization and evidence, not for retroactive audit scoring.
- Reject cross-client, malformed, unsupported, or silently stale artifacts.
- Preserve UTF-8 and existing Market Context Kit terminology and output-location rules.
- Keep changes in branch `codex/search-mcp-integration` inside the isolated worktree.

---

### Task 1: Shared artifact-consumer contract

**Files:**
- Create: `references/search-context-integration.md`
- Create: `tests/test_search_context_integration.py`

**Interfaces:**
- Produces: one shared instruction contract for artifact discovery, validation, provenance, and synthesis.
- Produces: static test helper `read(relative_path: str) -> str`.

- [ ] **Step 1: Write failing static contract tests**

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_reference_requires_schema_domain_period_and_source_validation():
    text = read("references/search-context-integration.md")
    for phrase in ("schema_version", "exact target domain", "reporting period", "source status"):
        assert phrase in text


def test_reference_keeps_artifact_out_of_data_manifest():
    text = read("references/search-context-integration.md")
    assert "never goes on the Data Manifest" in text
    assert "must not change an audit score" in text
```

- [ ] **Step 2: Run the new test and confirm failure**

Run: `python -m pytest tests/test_search_context_integration.py -q`

Expected: failure because the reference does not exist.

- [ ] **Step 3: Write the shared integration reference**

Define explicit-path precedence, exact-domain auto-discovery under `YYYY-MM-DD - Search Context/<domain>/SEARCH-CONTEXT.v1.json`, freshness disclosure, schema validation, source-state handling, and orchestrator-only synthesis. Require a visible limitation for invalid or partial sources. State that search estimates remain estimates and that supplied supplemental context retains its own provenance.

- [ ] **Step 4: Run the static tests**

Run: `python -m pytest tests/test_search_context_integration.py -q`

Expected: all tests pass.

- [ ] **Step 5: Commit the shared contract**

```text
git add references/search-context-integration.md tests/test_search_context_integration.py
git commit -m "docs: define search context artifact contract"
```

### Task 2: Audit orchestrator integration

**Files:**
- Modify: `skills/audit/SKILL.md`
- Modify: `tests/test_search_context_integration.py`

**Interfaces:**
- Consumes: `references/search-context-integration.md` from Task 1.
- Produces: optional validated Search Context evidence in Phase 3 synthesis.

- [ ] **Step 1: Extend the test with audit boundary assertions**

```python
def test_audit_loads_search_context_only_for_orchestrator_synthesis():
    text = read("skills/audit/SKILL.md")
    assert "references/search-context-integration.md" in text
    assert "orchestrator-only" in text
    assert "Do not paste Search Context data into any subagent prompt" in text
    assert "do not change the six audit scores" in text
```

- [ ] **Step 2: Run the audit assertion and confirm failure**

Run: `python -m pytest tests/test_search_context_integration.py::test_audit_loads_search_context_only_for_orchestrator_synthesis -q`

Expected: failure because the audit skill has no Search Context integration.

- [ ] **Step 3: Add Phase 0 artifact resolution**

After grounding and output-location resolution, instruct the orchestrator to read the shared reference, resolve only an explicit user path or exact-domain artifact, validate it, and retain it for Phase 3. Reaffirm that analytics exports remain excluded from the Data Manifest.

- [ ] **Step 4: Add Cross-Skill Integration synthesis rules**

Add Search Context as orchestrator-only evidence after independent subagents return. Require report citations to name period and sources, distinguish measured values from estimates, disclose partial sources, prioritize recommendations where evidence supports them, and leave all six scores unchanged.

- [ ] **Step 5: Run audit integration and full tests**

Run: `python -m pytest tests/test_search_context_integration.py -q`

Expected: all Search Context assertions pass.

Run: `python -m pytest -q`

Expected: the existing 23 tests plus new tests pass.

- [ ] **Step 6: Commit audit integration**

```text
git add skills/audit/SKILL.md tests/test_search_context_integration.py
git commit -m "feat: add search context to audit synthesis"
```

### Task 3: Report and SEO integration plus user documentation

**Files:**
- Modify: `skills/report/SKILL.md`
- Modify: `skills/seo/SKILL.md`
- Modify: `README.md`
- Modify: `tests/test_search_context_integration.py`

**Interfaces:**
- Consumes: the shared reference from Task 1.
- Produces: explicit Search Context data-source sections in reports and measured query/page evidence in SEO recommendations.

- [ ] **Step 1: Add report, SEO, and README assertions**

```python
def test_report_and_seo_use_shared_reference():
    for path in ("skills/report/SKILL.md", "skills/seo/SKILL.md"):
        text = read(path)
        assert "references/search-context-integration.md" in text
        assert "SEARCH-CONTEXT.v1.json" in text


def test_readme_documents_optional_companion():
    text = read("README.md")
    assert "Search Context Kit" in text
    assert "optional companion" in text
    assert "does not change audit scores" in text
```

- [ ] **Step 2: Run the new assertions and confirm failure**

Run: `python -m pytest tests/test_search_context_integration.py -q`

Expected: report, SEO, and README assertions fail.

- [ ] **Step 3: Integrate the report skill**

During data collection, resolve and validate an explicitly supplied Search Context artifact. Use measured traffic, query, page, and engagement fields in the appropriate deep dives and data-source appendix. Do not substitute absent analytics with invented values and do not convert search estimates into revenue facts.

- [ ] **Step 4: Integrate the SEO skill**

Use validated query, landing-page, CTR, position, and indexing evidence to prioritize SEO recommendations. Preserve the existing live-site structural evidence rules and label the artifact period. Reject domain mismatches.

- [ ] **Step 5: Document the optional companion**

Add installation-neutral documentation explaining that Search Context Kit is separate, supplies a versioned artifact, remains optional, and is consumed only after validation. Include one natural-language example with an explicit artifact path.

- [ ] **Step 6: Run full tests and formatting checks**

Run: `python -m pytest -q`

Expected: all tests pass.

Run: `git diff --check`

Expected: no whitespace errors.

- [ ] **Step 7: Commit report, SEO, and README integration**

```text
git add skills/report/SKILL.md skills/seo/SKILL.md README.md tests/test_search_context_integration.py
git commit -m "docs: integrate optional search context evidence"
```

### Task 4: Final worktree verification

**Files:**
- Modify only exact files implicated by a failing verification command.

**Interfaces:**
- Verifies the worktree branch without changing the `main` checkout.

- [ ] **Step 1: Run the complete suite**

Run: `python -m pytest -q`

Expected: all tests pass.

- [ ] **Step 2: Confirm worktree and branch isolation**

Run: `git branch --show-current && git worktree list && git status --short`

Expected: current branch is `codex/search-mcp-integration`, the original checkout remains on `main`, and only intentional changes are present.

- [ ] **Step 3: Inspect the complete branch diff**

Run: `git diff main...HEAD --check && git diff --stat main...HEAD`

Expected: no whitespace errors and only the integration reference, three skills, README, tests, and plan are changed.
