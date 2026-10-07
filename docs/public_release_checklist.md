# Public release checklist

Status: **public bounded evidence-audit release prepared in `UpbeatH/ContextPerf-Artifacts`.**

## Completed

- [x] Destination confirmed as `UpbeatH/ContextPerf-Artifacts`.
- [x] Repository visibility is public.
- [x] Repository owner explicitly authorized publication of the bounded artifact.
- [x] Minimal allowlisted E1--E5 evidence selected; the broad private archive remains excluded.
- [x] All six Cassandra and nine PostgreSQL Figure 3 outcomes retained, including null/slower cells.
- [x] Private source-path fields replaced by documented opaque batch IDs.
- [x] Source and derived hashes recorded separately.
- [x] No upstream database source distribution, binary, credential, private host path, or cluster identifier is included in the selected payload.
- [x] Release boundaries document that this is evidence audit, not complete experiment reproduction.
- [x] Local verifier and complete SHA-256 inventory are included.

## License / rights status

- [x] The package does **not** invent an open-source license.
- [x] `LICENSE` explicitly grants no general reuse/redistribution permission.
- [ ] If the venue requires a specific reusable/open license rather than public reviewer access, authors must complete a separate rights review and replace the notice only with an authorized license.

## Submission consistency

- [x] The manuscript points to `https://github.com/UpbeatH/ContextPerf-Artifacts` as the artifact location.
- [ ] After the final artifact payload commit is frozen, update the manuscript artifact paragraph to describe the actually released E1--E5 subset and pin the release commit.
- [ ] Rebuild the final PDF after that source update.
- [ ] Confirm CMT/supplementary-material fields use the same public URL and scope wording.

## Access verification

- [x] GitHub repository metadata reports public visibility.
- [ ] Before final CMT submission, perform one independent retrieval test while signed out / without repository credentials and record the result.

No item in this checklist authorizes a new experiment or expands a scientific claim.
