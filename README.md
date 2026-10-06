# ContextPerf Artifact Package

Artifact package for:

**ContextPerf: Context-Aware Performance Regression Reproduction for Database Systems**

This repository provides a reviewer-oriented evidence audit package for the EDBT 2027 submission.

## Scope

This artifact supports:

- audit of compact evidence records;
- verification of manuscript-linked figures/tables;
- provenance checking through manifests and hashes.

This artifact does **not** claim:

- complete reproduction of all historical experiments;
- redistribution of private experiment environments;
- availability of original cluster/storage environments;
- rerunning of historical experiments.

## Structure

```
artifact/
  evidence/
  figures/
  tables/
  manifests/

docs/
  artifact_scope.md
  reproduction_boundary.md

scripts/
  verify_hashes.py
```

## Status

Initial public artifact structure prepared. Evidence files are added only after source, license, and distribution checks are completed.
