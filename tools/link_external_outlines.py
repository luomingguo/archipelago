#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Link external course index.md files to the canonical Archipelago course notes.
Backs up original files into /private/tmp/archipelago-mgmt-outlines-backup/
"""

import os
import shutil
import tempfile
import time

BASE_REPO = '/Users/mac/Documents/MIT/archipelago'
DOCS_MGMT = os.path.join(BASE_REPO, 'docs/zh/management')
BASE_COURSES = '/Users/mac/Documents/courses'
BASE_MKT = '/Users/mac/Documents/MIT/15_Marketing'

# Import COURSES_SPEC from migrate_course15_stubs
import sys
sys.path.insert(0, os.path.join(BASE_REPO, 'tools'))
from migrate_course15_stubs import COURSES_SPEC

def main():
    backup_root = os.path.join(tempfile.gettempdir(), f'archipelago-mgmt-outlines-{int(time.time())}')
    os.makedirs(backup_root, exist_ok=True)
    print(f'Backup directory: {backup_root}')

    folder_mapping = {
        '会计学': 'acct',
        '信息技术': 'info_tech',
        '全球经济与管理': 'global_econ',
        '医疗卫生管理': 'ops_mngt',
        '工业关系与人力资源管理': 'org_studies',
        '工作与组织研究': 'org_studies',
        '战略管理': 'strat_mngt',
        '技术、创新与创业': 'tech_innov',
        '沟通与传播': 'comm',
        '法律': 'law',
        '管理经济学': 'managerial_econ',
        '运营管理': 'ops_mngt',
        '通识基础课程': 'or_stats',
        '金融学': 'finance',
        '高管工商管理硕士（EMBA）课程': 'emba'
    }

    source_dirs = {}
    for fld, grp in folder_mapping.items():
        p = os.path.join(BASE_COURSES, fld)
        if not os.path.exists(p): continue
        for sub in sorted(os.listdir(p)):
            subpath = os.path.join(p, sub)
            if not os.path.isdir(subpath) or sub.startswith('.'): continue
            if '15.301 Managerial Psychology Laboratory' in sub:
                source_dirs['15.301-ariely'] = subpath
            elif '15.301 Managerial Psychology' in sub:
                source_dirs['15.301-carroll'] = subpath
            else:
                import re
                m = re.search(r'15\.[0-9A-Z]+(?:\[?J\]?)?', sub, re.I)
                if m:
                    cid = m.group(0).upper().replace('[', '').replace(']', '')
                    source_dirs[cid] = subpath

    for sub in sorted(os.listdir(BASE_MKT)):
        subpath = os.path.join(BASE_MKT, sub)
        if not os.path.isdir(subpath) or sub.startswith('.') or 'Pricing' in sub or '15.810' in sub: continue
        import re
        m = re.search(r'15\.[0-9A-Z]+', sub, re.I)
        if m:
            cid = m.group(0).upper()
            source_dirs[cid] = subpath

    linked_count = 0
    already_linked = 0

    for cid_key, spec in COURSES_SPEC.items():
        src_path = source_dirs.get(cid_key)
        if not src_path:
            clean_k = cid_key.split('-')[0]
            src_path = source_dirs.get(clean_k)
        if not src_path:
            continue

        src_index = os.path.join(src_path, 'index.md')
        target_index = os.path.join(DOCS_MGMT, spec['group'], spec['dir_name'], 'index.md')

        if not os.path.exists(target_index):
            print(f'[SKIP] Missing canonical target: {target_index}')
            continue

        if os.path.islink(src_index):
            curr_target = os.path.realpath(src_index)
            if curr_target == os.path.realpath(target_index):
                already_linked += 1
                continue

        # Backup source file
        if os.path.exists(src_index):
            rel_bk = os.path.relpath(src_index, '/')
            bk_dest = os.path.join(backup_root, rel_bk)
            os.makedirs(os.path.dirname(bk_dest), exist_ok=True)
            shutil.copy2(src_index, bk_dest)
            os.remove(src_index)

        # Create symlink
        os.symlink(target_index, src_index)
        linked_count += 1

    print(f'Done! Successfully created {linked_count} symlinks. Already correct: {already_linked}')

if __name__ == '__main__':
    main()
