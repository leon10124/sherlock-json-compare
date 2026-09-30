"""Local file comparison. Exit 0 equal, 1 different, 2 invalid/error."""
import argparse
import json
from pathlib import Path
import sys
from json_compare import compare

def read_input(path):
    with Path(path).open('rb') as stream:raw=stream.read(262145)
    if len(raw)>262144:raise ValueError('Input exceeds 256 KiB')
    return raw.decode('utf-8-sig')

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('left');parser.add_argument('right')
    parser.add_argument('--ignore',action='append',default=[],help='Exact JSON Pointer; repeat for multiple paths')
    parser.add_argument('--unordered',action='store_true',help='Ignore ALL array order, preserving duplicates')
    args=parser.parse_args(argv)
    try:result=compare(read_input(args.left),read_input(args.right),args.ignore,args.unordered)
    except (OSError,ValueError,UnicodeError,RecursionError):
        print(json.dumps({'error':'Cannot compare: check UTF-8 JSON files, size, depth and exact ignore paths.'}))
        return 2
    # Summary avoids printing user values or file names into automation logs.
    print(json.dumps({'equal':result['equal'],'change_count':result['change_count'],'truncated':result['truncated']}))
    return 0 if result['equal'] else 1

if __name__=='__main__':sys.exit(main())
