# ContextPerf Artifact

Public evidence-audit artifact for:

**ContextPerf: Context-Aware Performance Regression Reproduction for Database Systems**

Manuscript baseline: `8345496f3b258d0c26ada2831d734be2cddd6aa8`

Repository: `UpbeatH/ContextPerf-Artifacts`

## Status

**PUBLIC_EVIDENCE_AUDIT_RELEASE**

This repository exposes a bounded, reviewer-accessible subset of the evidence used by the manuscript. It is designed for evidence inspection and integrity checking, not for complete historical experiment reproduction.

## What this artifact supports

The release contains selected frozen E1--E5 evidence:

- all six Cassandra Figure 3 outcomes, including null/slower cases;
- the nine-setting PostgreSQL catalog curve and retained pair ratios;
- compact PostgreSQL and Cassandra native-work observations;
- direct-template/solver equivalence records;
- the frozen Figure 3 vector rendering and its input mapping;
- a provenance manifest, claim map, SHA-256 inventory, and read-only verification script.

Run from the repository root:

```bash
python3 scripts/verify_hashes.py
```

The verifier performs local hash and compact-record consistency checks only. It performs no network access, database execution, bootstrap rerun, or experiment.

## Deliberate boundary

This is **not a full raw-experiment reproduction artifact**. It does not contain historical raw roots, complete logs, private infrastructure, build trees, databases, launchers, full per-invocation receipts, or runtime environments. E6--E8 DuckDB source/result reports and the proposed common receipt-state-machine implementation are outside this minimal public subset.

No new experiment or statistical estimator was executed while preparing this release. The artifact supports audit of selected historical compact evidence; it does not establish prospective Context Receipt efficacy, a minimal sufficient context set, generic-planner superiority, reduced human effort, cross-system prevalence, or a measured C0/C1/C2 success rate.

## Contents

- `artifact/evidence/` — selected E1--E3 compact records.
- `artifact/figures/` — frozen Figure 3 and its input mapping.
- `artifact/tables/` — E3--E5 native-work/equivalence tables and claim map.
- `artifact/manifests/provenance.json` — source hashes, transformations, and evidence provenance.
- `docs/artifact_scope.md` — included/excluded evidence and interpretation limits.
- `docs/reproduction_boundary.md` — what this release can and cannot reproduce.
- `docs/public_release_checklist.md` — release and submission consistency status.
- `scripts/verify_hashes.py` — standard-library-only integrity/consistency checker.
- `SHA256SUMS` — inventory of every release file except itself.
- `LICENSE` — public-access notice; no general reuse license is granted.

## Access and reuse

The repository is public so reviewers can inspect the released files without access to the private ContextPerf research repository. Public visibility is an access mechanism, not a representation that the package is a complete experiment reproduction environment.

No general copyright/reuse license is granted by this repository. See `LICENSE`. Third-party rights, where any apply, remain with their respective rights holders.
