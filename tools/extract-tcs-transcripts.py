#!/usr/bin/env python3
"""
Extract clean English transcripts from MIT OCW WebVTT/SRT files into docs/zh/cs/tcs/<course>/transcripts/en/lecXX.txt
"""

import os
import json
import re

def clean_vtt_text(vtt_path, title):
    with open(vtt_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    blocks = content.split('\n\n')
    paragraphs = []
    current_speaker = None
    current_sentences = []
    word_count_in_block = 0

    noise_re = re.compile(r'\[(SQUEAKING|RUSTLING|CLICKING|CHUCKLING|COUGHING|SNICKERING|LAUGHTER|APPLAUSE)\]', re.IGNORECASE)
    disclaimer_re = re.compile(r'The following content is provided under a Creative Commons license.*?(visit MIT OpenCourseWare at ocw\.mit\.edu|ocw\.mit\.edu\.)', re.DOTALL | re.IGNORECASE)

    # remove disclaimer if at the very beginning
    content = disclaimer_re.sub('', content)
    blocks = content.split('\n\n')

    for block in blocks:
        lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
        if not lines or lines[0].startswith('WEBVTT') or lines[0].startswith('NOTE'):
            continue
        text_lines = [l for l in lines if '-->' not in l]
        if not text_lines:
            continue
        raw_text = ' '.join(text_lines)
        
        cleaned = noise_re.sub('', raw_text).strip()
        if not cleaned:
            continue

        # Check speaker tag
        m = re.match(r'^([A-Z][a-zA-Z\s\.\-]+):\s*(.*)', cleaned)
        if m:
            speaker = m.group(1).strip()
            rest = m.group(2).strip()
            if current_sentences:
                paragraphs.append((current_speaker, ' '.join(current_sentences)))
                current_sentences = []
                word_count_in_block = 0
            current_speaker = speaker
            if rest:
                current_sentences.append(rest)
                word_count_in_block += len(rest.split())
        else:
            current_sentences.append(cleaned)
            word_count_in_block += len(cleaned.split())
            if word_count_in_block > 140 and (cleaned.endswith('.') or cleaned.endswith('?') or cleaned.endswith('!')):
                paragraphs.append((current_speaker, ' '.join(current_sentences)))
                current_sentences = []
                word_count_in_block = 0

    if current_sentences:
        paragraphs.append((current_speaker, ' '.join(current_sentences)))

    out = [f'# {title}\n']
    prev_speaker = None
    for spk, text in paragraphs:
        clean_p = re.sub(r'\s+', ' ', text).strip()
        if not clean_p:
            continue
        if spk and spk != prev_speaker:
            out.append(f'{spk}:\n\n{clean_p}\n')
            prev_speaker = spk
        else:
            out.append(f'{clean_p}\n')

    return '\n'.join(out)


def extract_course(name, base_dir, out_dir):
    res_dir = os.path.join(base_dir, 'resources')
    static_dir = os.path.join(base_dir, 'static_resources')
    os.makedirs(out_dir, exist_ok=True)

    lectures = []
    if os.path.exists(res_dir):
        for item in os.listdir(res_dir):
            dj = os.path.join(res_dir, item, 'data.json')
            if os.path.exists(dj):
                with open(dj) as f:
                    data = json.load(f)
                if data.get('resource_type') == 'Video':
                    title = data.get('title')
                    m = re.search(r'Lecture\s+(\d+):\s*(.*)', title)
                    if m:
                        num = int(m.group(1))
                        cap = data.get('captions_file', '')
                        cap_base = os.path.basename(cap)
                        vtt_path = os.path.join(static_dir, cap_base)
                        if os.path.exists(vtt_path):
                            lectures.append((num, title, vtt_path))

    lectures.sort(key=lambda x: x[0])
    print(f'Extracting {len(lectures)} lectures for {name}...')
    for num, title, vtt_path in lectures:
        out_file = os.path.join(out_dir, f'lec{num:02d}.txt')
        text = clean_vtt_text(vtt_path, title)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'  [OK] Lec {num:02d}: {title} -> {out_file} ({len(text)} chars)')


if __name__ == '__main__':
    print('=== 6.1200 ===')
    extract_course(
        '6.1200 Mathematics for Computer Science',
        '/Users/mac/Documents/MIT/6_ComputerScience/Theoretical Computer Science/6.1200 Mathematics for Computer Science/resources/6.1200j-spring-2024',
        '/Users/mac/Documents/MIT/archipelago/docs/zh/cs/tcs/61200_maths_for_cs/transcripts/en'
    )
    print('\n=== 6.1210 ===')
    extract_course(
        '6.1210 Introduction to Algorithms',
        '/Users/mac/Documents/MIT/6_ComputerScience/Theoretical Computer Science/6.1210 Introduction to Algorithms/6.006-spring-2020',
        '/Users/mac/Documents/MIT/archipelago/docs/zh/cs/tcs/61210_introduction_to_algorithms/transcripts/en'
    )
    print('\n=== 6.1220 ===')
    extract_course(
        '6.1220 Design and Analysis of Algorithms',
        '/Users/mac/Documents/MIT/6_ComputerScience/Theoretical Computer Science/6.1220 Design and Analysis of Algorithms/6.046j-spring-2015',
        '/Users/mac/Documents/MIT/archipelago/docs/zh/cs/tcs/61220_design_and_analysis_of_algos/transcripts/en'
    )
