"""
Audit Manuscript Quality, Anti-AI Markers, Burstiness, and Citation Integrity
"""

import re
import sys
import math
import statistics

BANNED_AI_CRUTCHES = [
    r'\bmoreover\b',
    r'\bfurthermore\b',
    r'\bin conclusion\b',
    r'\bit is crucial to note\b',
    r'\ba testament to\b',
    r'\bnavigating the\b',
    r'\bpivotal role\b',
    r'\bharnessing the\b',
    r'\btapestry\b',
    r'\bbeacon\b',
    r'\bdelve\b',
    r'\bdelving\b',
    r'\bdemystifying\b',
    r'\bin today\'s\b',
    r'\brapidly evolving\b',
    r'\bgame-changer\b',
    r'\bcornerstone\b',
    r'\bunderscores the need\b',
    r'\bplay a vital role\b',
    r'\bplays a crucial role\b'
]

def audit_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    print(f"=== Auditing {filepath} ===")
    print(f"Total characters: {len(text)}")
    words = re.findall(r'\b\w+\b', text)
    print(f"Total words: {len(words)}")

    # 1. Banned AI Crutches check
    found_crutches = {}
    for pattern in BANNED_AI_CRUTCHES:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            found_crutches[pattern] = len(matches)

    if found_crutches:
        print("\n[WARNING] Found banned AI formulaic phrases:")
        for pattern, count in found_crutches.items():
            print(f"  - {pattern}: {count} occurrences")
    else:
        print("\n[PASS] Zero banned AI formulaic phrases detected!")

    # 2. Sentence Length Variance (Syntactic Burstiness)
    # Exclude code blocks, tables, and headers
    clean_lines = []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code or line.strip().startswith(('#', '|', '---')):
            continue
        clean_lines.append(line)
    prose = ' '.join(clean_lines)

    sentences = re.split(r'(?<=[.!?])\s+', prose)
    sent_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences if len(re.findall(r'\b\w+\b', s)) > 2]

    if sent_lengths:
        mean_len = statistics.mean(sent_lengths)
        std_len = statistics.stdev(sent_lengths) if len(sent_lengths) > 1 else 0
        print(f"\n[SENTENCE BURSTINESS METRICS]")
        print(f"  Total prose sentences analyzed: {len(sent_lengths)}")
        print(f"  Mean sentence length: {mean_len:.1f} words")
        print(f"  Sentence length standard deviation: {std_len:.2f} words")
        if std_len >= 8.0:
            print("  [PASS] High syntactic burstiness (std dev >= 8.0) — human academic rhythm confirmed!")
        else:
            print("  [CAUTION] Sentence length is somewhat uniform; adjust cadence for higher burstiness.")

    # 3. Citation Check
    citations = re.findall(r'\[([0-9]+(?:,\s*[0-9]+)*)\]', text)
    cited_nums = set()
    for c in citations:
        for num in re.findall(r'\d+', c):
            cited_nums.add(int(num))
    print(f"\n[CITATIONS DETECTED]: {sorted(list(cited_nums))}")
    print(f"  Total distinct references cited: {len(cited_nums)}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        audit_text(sys.argv[1])
    else:
        print("Usage: python3 audit_manuscript.py <file.md>")
