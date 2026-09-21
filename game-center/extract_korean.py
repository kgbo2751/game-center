import os
import re
import glob

def extract():
    korean_pattern = re.compile(r'[\'"]([^\'"]*[가-힣]+[^\'"]*)[\'"]')
    found = set()
    files = glob.glob('games/**/*.py', recursive=True)
    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                matches = korean_pattern.findall(line)
                for m in matches:
                    found.add(m)
    for s in sorted(list(found)):
        print(s)

extract()
