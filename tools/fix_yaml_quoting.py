#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

base = '/Users/mac/Documents/MIT/archipelago/docs/zh/management'
fixed = 0

for root, _, files in os.walk(base):
    for f in files:
        if f.endswith('.md'):
            fpath = os.path.join(root, f)
            text = open(fpath, 'r', encoding='utf-8').read()
            if not text.startswith('---'):
                continue
            parts = text.split('---', 2)
            if len(parts) < 3:
                continue
            fm_raw = parts[1]
            lines = fm_raw.split('\n')
            changed = False
            new_lines = []
            for line in lines:
                if line.startswith('title: '):
                    val = line[7:].strip()
                    if not (val.startswith("'") and val.endswith("'")) and not (val.startswith('"') and val.endswith('"')):
                        # Wrap in single quotes, escaping internal single quotes
                        escaped = val.replace("'", "''")
                        line = f"title: '{escaped}'"
                        changed = True
                elif line.startswith('course: '):
                    val = line[8:].strip()
                    if not (val.startswith("'") and val.endswith("'")) and not (val.startswith('"') and val.endswith('"')):
                        escaped = val.replace("'", "''")
                        line = f"course: '{escaped}'"
                        changed = True
                new_lines.append(line)
            if changed:
                new_text = '---' + '\n'.join(new_lines) + '---' + parts[2]
                with open(fpath, 'w', encoding='utf-8') as out:
                    out.write(new_text)
                fixed += 1

print(f'Total YAML files with updated quotes: {fixed}')
