####!/bin/env python

# history:
# 2020/12/21  v1.0  initial

import os
import sys
import re

org_file = 'a910_SS_1p8v_125C_200917_simple.sdf'
out_file = 'a.sdf'

scale = 0.5

VERSION = '1.0'


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def usage():
    print('usage:')
    print('    %s in_sdf out_sdf scale' % os.path.basename(__file__))


def main():

    print_version(VERSION)
    if len(sys.argv) != 4:
        usage()
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    scale = float(sys.argv[3])

    with open(in_file, 'r',  errors='ignore') as f:
        l_lines = f.readlines()

    p = re.compile(r'\((-?\d+\.\d+)::(-?\d+\.\d+)\)', re.S)

    with open(out_file, 'w+') as f:
        for l in l_lines:
            def _scale_num(matched):
                # print(matched)
                first_num = scale * float(matched.group(1))
                second_num = scale * float(matched.group(2))
                result = '(%0.3f::%0.3f)' % (first_num, second_num)
                return result

            new_l = re.sub(p, _scale_num, l)
            f.write(new_l)

    print('=' * 70)

    print('<Input>  %s' % in_file)
    print('<Output> %s' % out_file)
    print('<Scale>  %0.3f' % scale)


if __name__ == '__main__':
    main()
