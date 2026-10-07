#!/usr/bin/env python3
"""Read-only inventory and selected compact-record checks; no experiments."""
import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(root, name, delimiter=','):
    with (root / name).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def check_inventory(root):
    inventory = root / 'SHA256SUMS'
    require(inventory.is_file() and not inventory.is_symlink(), 'Missing or linked SHA256SUMS')
    listed = {}
    for line in inventory.read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, 'Malformed SHA256SUMS line')
        digest, name = match.groups()
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts and '.' not in path.parts
                and '\\' not in name and str(path) == name, 'Unsafe manifest path')
        require(name != 'SHA256SUMS' and name not in listed and '.git' not in path.parts,
                'Duplicate or reserved manifest entry')
        listed[name] = digest
    actual = set()
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if '.git' in relative.parts:
            continue  # Version-control metadata is not artifact payload.
        require(not path.is_symlink(), 'Symlink present: ' + relative.as_posix())
        if path.is_file() and relative.as_posix() != 'SHA256SUMS':
            actual.add(relative.as_posix())
    require(actual == set(listed), 'Inventory mismatch: missing=' + str(sorted(set(listed) - actual))
            + '; unlisted=' + str(sorted(actual - set(listed))))
    for name, expected in listed.items():
        require(sha256(root / name) == expected, 'SHA-256 mismatch: ' + name)
    return len(listed)


def check_records(root):
    summary = json.loads((root / 'artifact/evidence/e1-preload-summary.json').read_text())
    expected_keys = {s + ':' + m for s in ('one_small', 'one_large', 'four_small')
                     for m in ('bounded', 'chunked')}
    require(set(summary['paired_summaries']) == expected_keys, 'E1 outcome coverage mismatch')
    require(summary['samples'] == 108, 'E1 historical sample count mismatch')
    for record in summary['paired_summaries'].values():
        require(0 < record['ci95_low'] <= record['median'] <= record['ci95_high'], 'E1 interval mismatch')
    pairs = read_csv(root, 'artifact/evidence/e1-preload-pairs.tsv', '\t')
    require(len(pairs) == 72, 'E1 pair-row count mismatch')
    require(Counter(p['scenario'] + ':' + p['candidate'] for p in pairs) == Counter({k: 12 for k in expected_keys}),
            'E1 pair coverage mismatch')
    # Arithmetic checks are not recomputation of the source medians or intervals.
    for p in pairs:
        ratio = float(p['base_elapsed_ms']) / float(p['candidate_elapsed_ms'])
        require(abs(ratio - float(p['base_over_candidate'])) < 1e-12, 'E1 pair arithmetic mismatch')
    construction = read_csv(root, 'artifact/evidence/e1-preload-construction.tsv', '\t')
    require(len(construction) == 18, 'E1 construction-row count mismatch')
    for r in construction:
        require(int(r['file_count']) * int(r['partitions_per_file']) == int(r['total_partitions']),
                'E1 partition arithmetic mismatch')
        if r['scenario'] in ('one_large', 'four_small'):
            require(int(r['total_partitions']) == 4800000
                    and r['logical_input_sha256'] == summary['equal_work_logical_input_sha256'],
                    'E1 equal-logical-input witness mismatch')
    curve = read_csv(root, 'artifact/evidence/e2-catalog-curve.csv')
    require([int(r['distractor_tables']) for r in curve] == [0, 10, 50, 100, 250, 500, 1000, 2000, 4000],
            'E2 setting coverage mismatch')
    for r in curve:
        ratios = [float(x) for x in r['pair_runtime_ratios'].split(';')]
        require(int(r['pairs']) == len(ratios) == 10, 'E2 pair count mismatch')
        require(sum(v > 2 for v in ratios) == int(r['pairs_above_illustrative_2x']),
                'E2 illustrative policy count mismatch')
        require((float(r['median_runtime_ratio']) > 2) == (r['illustrative_median_signal'] == 'True'),
                'E2 illustrative policy point mismatch')
        require(0 < float(r['bootstrap95_low_ratio']) <= float(r['median_runtime_ratio'])
                <= float(r['bootstrap95_high_ratio']), 'E2 interval mismatch')
        expected_batch = 'B001' if int(r['distractor_tables']) in (0, 4000) else 'B002'
        require(r['source_batch'] == expected_batch, 'E2 source-batch membership mismatch')
    for name, n, count_field in [('e3-native-work-calibration.csv', 6, 'carrier_count'),
                                  ('e3-native-work-targets.csv', 4, 'target_count')]:
        rows = read_csv(root, 'artifact/tables/' + name)
        require(len(rows) == n, 'E3 row coverage mismatch')
        for r in rows:
            require(r['timing_fields_present'] == 'false', 'E3 timing-disabled boundary mismatch')
            work = 1 if r['role'] == 'parent' else 421 + 5 * int(r[count_field])
            require(int(r['rows_visited']) == work, 'E3 native-work law mismatch')
    result = json.loads((root / 'artifact/evidence/e3-template-result.json').read_text())
    require(result['closed_form_template_matches_solver'] is True, 'E3 template tie missing')
    rows = read_csv(root, 'artifact/tables/e4-native-work-counts.csv')
    require(len(rows) == 18, 'E4 row count mismatch')
    require({(r['role'], int(r['sstables']), int(r['cache_entries'])) for r in rows}
            == {(role, n, k) for role in ('parent', 'child') for n in (8, 16, 32) for k in (2, 4, 8)},
            'E4 cell coverage mismatch')
    for r in rows:
        n, k = int(r['sstables']), int(r['cache_entries'])
        expected = (k * n, 0, 0, 0) if r['role'] == 'parent' else (0, 1, n, k)
        observed = tuple(int(r[f]) for f in ('generation_comparisons', 'map_builds', 'map_insertions', 'map_lookups'))
        require(observed == expected and r['work_model_matches'] == 'true', 'E4 work-law mismatch')
    rows = read_csv(root, 'artifact/tables/e5-constructor-equivalence.csv')
    require(len(rows) == 9, 'E5 target count mismatch')
    for r in rows:
        require(r['same_native_action'] == 'True', 'E5 negative/tie result missing')
        for suffix in ('sstables', 'cache_entries'):
            require(r['measured_' + suffix] == r['template_' + suffix] == r['solver_' + suffix],
                    'E5 constructor equivalence mismatch')
    manifest = json.loads((root / 'artifact/manifests/provenance.json').read_text())
    require(len(manifest['records']) == 10, 'Source-selection inventory mismatch')
    for record in manifest['records']:
        require(sha256(root / record['artifact_path']) == record['artifact_sha256'],
                'Derived-provenance digest mismatch')
        if record['transformation'].startswith('Exact byte copy'):
            require(record['artifact_sha256'] == record['source_sha256'], 'Exact-copy identity mismatch')
    return {'e1_plot_outcomes': 6, 'e1_pair_rows': 72, 'e1_construction_rows': 18,
            'e2_plot_settings': 9, 'e2_pairs_per_setting': 10, 'e3_cells': 10,
            'e4_cells': 18, 'e5_analytical_targets': 9, 'source_records': 10}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args().root.resolve()
    count = check_inventory(root)
    checks = check_records(root)
    print(json.dumps({'status': 'PASS', 'hashed_files': count, 'compact_record_checks': checks,
                      'boundary': 'Local file integrity and selected consistency only; no experiment, bootstrap, license, privacy, public-access, or venue-readiness certification.'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, ZeroDivisionError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
