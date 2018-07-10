#!/bin/env python

# history:
# 2018/07/01  v1.0  initial

import re
import os
import sys

VERSION = '1.0'


# class ERR():

#     def __init__(self, abbrv):
#         self.__abbrv = abbrv

#     @property
#     def message(self):
#         return {
#             'no_file': 'file not found',
#             'no_inst': 'instance not found'
#         }.get(self.__abbrv, 'unknown error')

NO_RIGHT = 1
NOT_SAME = 2
CORRECT = 0


def ERR(abbrv):
    return '[Error] ' + {
        'no_file': 'no such file',
        'no_inst': 'no such instance',
        'format_err': 'file format not supported'
    }.get(abbrv, 'unknown error')


def WARN(abbrv):
    return '[Warning] ' + {
        'not_same': 'index not same',
        'no_right': 'right part has no index'
    }.get(abbrv, 'unknown warning')


def print_err(abbrv, param):
    print('%s (%s)' % (ERR(abbrv), param))


def print_warn(abbrv, param):
    print('%s (%s)' % (WARN(abbrv), param), end=', ')


def read_cdl(file_name):
    lines = []
    try:
        with(open(file_name)) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print_err('no_file', file_name)
        sys.exit(1)
    except Exception as e:
        print_err('format_err', file_name)
        sys.exit(1)

    return lines


def add_line_no(txt_as_list):
    txt_with_lineno_as_list = []
    for i in range(len(txt_as_list)):
        txt_with_lineno_as_list.append(
            '%10s: %s' % (str(i + 1), txt_as_list[i]))
    return txt_with_lineno_as_list


def match_start(a_line, keyword):
    p = re.compile('[\s\d]{10}:\s+?\.SUBCKT\s+?%s\s+?' % keyword, re.S)
    if re.match(p, a_line):
        return True
    else:
        return False


def match_end(a_line):
    p = re.compile('[\s\d]{10}:\s+?\.ENDS\s*$', re.S)
    if re.match(p, a_line):
        return True
    else:
        return False


def extract_instance(whole_cdl_as_list, instance):
    for i in range(len(whole_cdl_as_list)):
        if match_start(whole_cdl_as_list[i], instance):
            start = i
            for i in range(i, len(whole_cdl_as_list)):
                if match_end(whole_cdl_as_list[i]):
                    end = i
                    return whole_cdl_as_list[start:end + 1]

    print_err('no_inst', instance)
    sys.exit(1)


def find_bus(a_line):
    found_bus = []
    split_line = a_line.split(' ')
    p = re.compile('\s*?\S+?\[\d+?\]=\S+?\s*?', re.S)
    for a_net in split_line:
        if(re.search(p, a_net)):
            found_bus.append(a_net)
    return found_bus


def check_bus(a_bus):
    p = re.compile('.+?\[(\d+?)\]=.+?\[(\d+?)\]', re.S)
    m = re.match(p, a_bus)
    if m:
        if m.group(1) == m.group(2):
            return CORRECT
        else:
            return NOT_SAME
    else:
        return NO_RIGHT


def get_lineno(line):
    return line[:10]


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def usage():
    print('usage:')
    print('    %s cdl_netlist_file instance_name' % os.path.basename(__file__))


def main():
    print_version(VERSION)
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    cdl_name = sys.argv[1]
    inst_name = sys.argv[2]

    txt_as_list = read_cdl(cdl_name)
    whole_cdl_as_list = add_line_no(txt_as_list)
    instance_as_list = extract_instance(whole_cdl_as_list, inst_name)

    for line in instance_as_list:
        found_bus_in_a_line = find_bus(line)
        for bus in found_bus_in_a_line:
            check_result = check_bus(bus)
            if(check_result == NOT_SAME):
                print_warn('not_same', bus.strip())
                print('line %s' % get_lineno(line).strip())
            elif(check_result == NO_RIGHT):
                print_warn('no_right', bus.strip())
                print('line %s' % get_lineno(line).strip())


if __name__ == '__main__':
    main()
