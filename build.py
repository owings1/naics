from __future__ import annotations

import csv
import json
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Iterator

dirs = dict(
    base=Path(__file__).parent,
    build=Path(__file__).parent/'build')

files = dict(
    csv = dirs['base']/'2022.csv',
    json = dirs['build']/'2022.json',
    min = dirs['build']/'2022.min.json')

columns = [
    'seq',
    'code',
    'title',
    'description']

def rows() -> Iterator[dict[str, str]]:
    with files['csv'].open() as file:
        reader = csv.reader(file)
        next(reader)
        for values in reader:
            yield dict(zip(columns, values))

def entries(row: dict[str, str]) -> Iterator[dict[str, Any]]:
    seq = int(row['seq'])
    code_raw = row['code']
    title = row['title'].rstrip('T')
    description = row['description']
    if description == 'NULL':
        description = None
    codes = list(map(int, code_raw.split('-')))
    if len(codes) == 2:
        codes = range(codes[0], codes[1] + 1)
    for code in codes:
        yield dict(
            seq=seq,
            code=code,
            code_raw=code_raw,
            title=title,
            description=description)

def build() -> None:
    dirs['build'].mkdir(parents=True, exist_ok=True)
    data = [entry for row in rows() for entry in entries(row)]
    with files['json'].open('w') as file:
        json.dump(data, file, indent=2)
    with files['min'].open('w') as file:
        json.dump(data, file)

parser = ArgumentParser(description='Build JSON files')

if __name__ == '__main__':
    parser.parse_args()
    build()
