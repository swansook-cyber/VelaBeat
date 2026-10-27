#!/usr/bin/env python3
"""Validate launcher entries in the *compiled* AndroidManifest via aapt xmltree."""
import re
import sys
from pathlib import Path


def nodes(text):
    roots, stack = [], []
    for line in text.splitlines():
        m = re.match(r'^(\s*)E: ([\w-]+)\b', line)
        if m:
            indent = len(m[1])
            node = {'tag': m[2], 'attrs': {}, 'children': []}
            while stack and stack[-1][0] >= indent:
                stack.pop()
            (stack[-1][1]['children'] if stack else roots).append(node)
            stack.append((indent, node))
        else:
            m = re.match(r'^\s*A: ([\w:]+)(?:\([^)]*\))?=(.*)$', line)
            if m and stack:
                v = re.search(r'^"([^"]*)"', m[2])
                stack[-1][1]['attrs'][m[1]] = v[1] if v else m[2].split(' (Raw:')[0]
    return roots


def walk(n):
    for a in n:
        yield a
        yield from walk(a['children'])


def name(n): return n['attrs'].get('android:name', '')
def enabled(n): return n['attrs'].get('android:enabled') != '(type 0x12)0x0'


def main_categories(n):
    categories = set()
    for f in n['children']:
        if f['tag'] != 'intent-filter':
            continue
        if not any(name(x) == 'android.intent.action.MAIN' for x in f['children'] if x['tag'] == 'action'):
            continue
        categories.update(name(x) for x in f['children'] if x['tag'] == 'category')
    return categories


def validate(text):
    components = [x for x in walk(nodes(text)) if x['tag'] in ('activity', 'activity-alias')]
    mobile = [x for x in components if enabled(x) and 'android.intent.category.LAUNCHER' in main_categories(x)]
    tv = [x for x in components if enabled(x) and 'android.intent.category.LEANBACK_LAUNCHER' in main_categories(x)]
    main = [x for x in components if x['tag'] == 'activity' and name(x).endswith('.MainActivity')]
    print('Active mobile:', [name(x) for x in mobile])
    print('Active TV:', [name(x) for x in tv])
    errors = []
    if len(mobile) != 1 or not name(mobile[0]).endswith('.LauncherDefault'):
        errors.append('Expected exactly one mobile/car launcher alias (LauncherDefault)')
    if len(tv) != 1 or not name(tv[0]).endswith('.TvActivity'):
        errors.append('Expected exactly one TV Leanback launcher (TvActivity)')
    if len(main) != 1 or main_categories(main[0]):
        errors.append('MainActivity has MAIN filters that may create a second car icon')
    if len(tv) == 1 and 'android:banner' not in tv[0]['attrs']:
        errors.append('TV activity is missing a banner')
    for e in errors:
        print('FAIL:', e, file=sys.stderr)
    if not errors:
        print('PASS: one phone/car and one TV entry without duplicated MAIN activity')
    return 1 if errors else 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: verify_universal_manifest.py <aapt-xmltree.txt>')
    sys.exit(validate(Path(sys.argv[1]).read_text(encoding='utf-8')))
