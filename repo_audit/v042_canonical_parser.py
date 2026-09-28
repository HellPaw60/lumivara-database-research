#!/usr/bin/env python
"""V0.4.2 Phase 1: CANONICAL PARSER — satu parser untuk kedua bundle changelog.

Bukti Phase 3: raw slice entry 2026-09-28-kensei-twin-strike IDENTIK di kedua bundle
(karakter-per-karakter, termasuk lines[] lengkap). Perbedaan 613 lines sebelumnya
adalah PARSER_ERROR pada parser official lama (regex `lines:\[(.*?)\]\}` gagal saat
lines berisi `]` atau escape kompleks).

Parser canonical ini memakai bracket-matching untuk lines array — bukan regex lazy.
"""
import re, json, hashlib

LINE_STR = re.compile(r'"((?:[^"\\]|\\.)*)"')

def parse_bundle(path):
    """Parse changelog bundle dengan bracket-matching untuk lines[]."""
    src = open(path, encoding='utf-8').read()
    entries = []
    errors = []
    head_pat = re.compile(r'id:"([^"]+)",date:"([^"]+)",time:"([^"]*)",title:"((?:[^"\\]|\\.)*)"')
    for m in head_pat.finditer(src):
        eid, date, tm, title = m.groups()
        # posisi setelah title
        pos = m.end()
        lines = []
        # cari ',lines:[' tepat setelah title
        lm = re.match(r',lines:\[', src[pos:pos+10])
        if lm:
            # bracket-match dari '['
            start = pos + lm.end() - 1  # index of '['
            depth = 0
            end = None
            i = start
            in_str = False
            esc = False
            while i < len(src):
                c = src[i]
                if in_str:
                    if esc: esc = False
                    elif c == '\\': esc = True
                    elif c == '"': in_str = False
                else:
                    if c == '"': in_str = True
                    elif c == '[': depth += 1
                    elif c == ']':
                        depth -= 1
                        if depth == 0:
                            end = i
                            break
                i += 1
            if end is None:
                errors.append(f'{eid}: unterminated lines array')
            else:
                inner = src[start+1:end]
                # split string literals di dalam array
                lines = [s for s in LINE_STR.findall(inner)]
        else:
            errors.append(f'{eid}: no lines field found')
        entries.append({'id': eid, 'date': date, 'time': tm, 'title': title, 'lines': lines})
    return entries, errors, src

client_entries, client_errors, client_src = parse_bundle('web-v2/changelog-notice-BKeFrGHU.js')
official_entries, official_errors, official_src = parse_bundle('research/changelog/official_changelog_notice_bundle.js')

# dump canonical
for label, entries, errors, path in [
    ('CANONICAL_CLIENT', client_entries, client_errors, 'research/changelog/CANONICAL_CLIENT_CHANGELOG.json'),
    ('CANONICAL_OFFICIAL', official_entries, official_errors, 'research/changelog/CANONICAL_OFFICIAL_CHANGELOG.json'),
]:
    out = {
        '_meta': {
            'parser': 'canonical v1 (bracket-match lines)',
            'source': 'web-v2/changelog-notice-BKeFrGHU.js' if 'CLIENT' in label else 'research/changelog/official_changelog_notice_bundle.js (from https://lumivaraonline.com/changelog/)',
            'source_sha256': hashlib.sha256(open('web-v2/changelog-notice-BKeFrGHU.js' if 'CLIENT' in label else 'research/changelog/official_changelog_notice_bundle.js', 'rb').read()).hexdigest(),
            'entry_count': len(entries), 'parser_errors': errors,
        },
        'entries': entries,
    }
    json.dump(out, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{label}: {len(entries)} entries, {sum(len(e["lines"]) for e in entries)} total lines, {len(errors)} parser errors')

# statistik lines per sumber
c_with_lines = sum(1 for e in client_entries if e['lines'])
o_with_lines = sum(1 for e in official_entries if e['lines'])
print(f'\nclient entries with lines: {c_with_lines}/{len(client_entries)}')
print(f'official entries with lines: {o_with_lines}/{len(official_entries)}')
