# history:
# 2018/09/01  v1.0  initial


import os
import sys
import datetime
import re


VERSION = '1.0'
DF_LOG = r'e:\temp\df.log'
USEFUL_LOC = ['/home', '/bkup', '/loc']
K_TO_G_RATIO = 1024 * 1024


def ERR(abbrv):
    return '[Error] ' + {
        'no_file': 'no such file',
        'no_useful': 'cannot find useful location',
        'bkup_not_enough': 'bkup space not enough'
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


def read_log_file(file_name):
    try:
        with(open(file_name)) as f:
            txt = f.read()
    except FileNotFoundError:
        print_err('no_file', file_name)
        sys.exit(1)
    return txt


def get_all_info(log_txt):
    p = re.compile('(\d+)\s+(\d+)\s+\d+%\s+(.+?)\n', re.S)
    result = re.findall(p, log_txt)
    return result


def get_useful_info(log_txt):
    infos = get_all_info(log_txt)
    useful_info = {}
    for info in infos:
        if info[2] in USEFUL_LOC:
            location = info[2]
            used = int(info[0]) / K_TO_G_RATIO
            available = int(info[1]) / K_TO_G_RATIO
            # useful_info.append((location, used, available))
            useful_info[location] = (used, available)
    if len(useful_info) == 0:
        print_err('no_useful', '')
        sys.exit(1)
    return useful_info


def judge_info(useful_info):
    home_used = useful_info['/home'][0]
    bkup_available = useful_info['/bkup'][1]
    if(home_used * 1.1 > bkup_available):
        print_err('bkup_not_enough', '')
        sys.exit(1)


def print_info(useful_info):
    print('Location\tUsed\t\tAvailable\tTotal\t\tUsed%')
    for key in useful_info:
        used = useful_info[key][0]
        available = useful_info[key][1]
        total = used + available
        percent = 100 * used / total
        print('%s\t\t%1.1f\t\t%1.1f\t\t%1.1f\t\t%1.1f%%' %
              (key, used, available, total, percent))


def main():
    print_version(VERSION)
    log_txt = read_log_file(DF_LOG)
    useful_info = get_useful_info(log_txt)
    print_info(useful_info)
    judge_info(useful_info)


if __name__ == '__main__':
    main()
