"""教材一冊分または二冊分を共通ルールで生成・照合・合冊する。"""
import argparse
import json

from build import ROOT,build
from assemble import assemble


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--collection',choices=['all','textbook','exercise'],default='all')
    parser.add_argument('--mode',choices=['all','flow'],default='all')
    args=parser.parse_args()
    collections=json.loads((ROOT/'docs/textbook/collections.json').read_text(encoding='utf-8'))
    for name,collection in collections.items():
        if args.collection not in ('all',name):continue
        for chapter in collection['parts']:build(chapter,args.mode)
        assemble(name,collection)
