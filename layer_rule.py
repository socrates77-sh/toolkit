# history:
# 2018/09/10  v1.0  initial


import os
import sys

VERSION = '1.0'
LAYER_FILE = r'E:\py\toolkit\lay_list.txt'
RULE_FILE = 'rule'


def ERR(abbrv):
    return '[Error] ' + {
        'no_file': 'no such file'
    }.get(abbrv, 'unknown error')


def print_err(abbrv, param):
    if param == '':
        print(ERR(abbrv))
    else:
        print('%s (%s)' % (ERR(abbrv), param))


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def read_file(file_name):
    try:
        with(open(file_name)) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print_err('no_file', file_name)
        sys.exit(1)
    return lines


def lay_info(lines):
    infos = []
    for line in lines:
        result = line.split()
        print(result)
        name = result[0]
        layer = result[1]
        datatype = result[2]
        infos.append((name, layer, datatype))
    return infos


def init_write(out_file_name):
    return open(out_file_name, 'w+')


def write_head(f):
    print('LAYOUT PRIMARY "TOPCELL"', file=f)
    print('LAYOUT PATH "TOPCELL.gds"', file=f)
    print('LAYOUT SYSTEM GDSII\n', file=f)
    print('DRC RESULTS DATABASE "jdv.gds" GDSII', file=f)
    print('DRC SUMMARY REPORT "jdv.sum"', file=f)
    print('DRC MAXIMUM RESULTS ALL\n', file=f)


def layer_define(f, layers):
    for l in layers:
        print('LAYER MAP %s DATATYPE %s' % (l[1], l[2]), file=f)
        print('LAYER %s_0\n' % l[0], file=f)


def layer_operation(f, layers):
    for l in layers:
        print('%s { COPY %s_0 }' % (l[0], l[0]), file=f)
        print('DRC CHECK MAP %s GDSII %s %s\n' % l, file=f)


def main():
    print_version(VERSION)
    lines = read_file(LAYER_FILE)
    layer_inofs = lay_info(lines)
    f = init_write(RULE_FILE)
    write_head(f)
    layer_define(f, layer_inofs)
    layer_operation(f, layer_inofs)

if __name__ == '__main__':
    main()
