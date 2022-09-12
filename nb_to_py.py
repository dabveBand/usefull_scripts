#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# DESC : convert notebook files to markdown script
# -----------------------------------------------
import os.path


def parser_file(filename):
    with open(filename, 'rt', errors='ignore') as in_file:
        data = json.load(in_file)
        cells = data['cells']

        fileOut = os.path.splitext(filename)[0] + '.md'    # change extension from .ipynb to .md
        # fileOut = in_file.name[:-6] + '.md'             # change extension from .ipynb to .md
        with open(fileOut, 'wt') as out_file:
            for info in cells:
                # writing markdown cells
                if info['cell_type'] == 'markdown':
                    out_file.write(''.join(info['source']))
                    out_file.write('\n')

                elif info['cell_type'] == 'code':
                    # writing source as code
                    out_file.write('```python\n')
                    out_file.write(''.join(info['source']))
                    out_file.write('\n')
                    out_file.write('```')
                    out_file.write('\n\n')
    print('[+] Done Adding All Sources to: {}'.format(fileOut))


if __name__ == '__main__':
    import json
    import argparse
    parser = argparse.ArgumentParser(description='Convert notebook files to markdown files')
    parser.add_argument(dest='filename', metavar='filename')
    args = parser.parse_args()
    parser_file(args.filename)
