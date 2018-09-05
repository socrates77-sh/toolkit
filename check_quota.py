# history:
# 2018/09/01  v1.0  initial


import os
import sys
import re


VERSION = '1.0'
SIZE_LOG = r'e:\temp\size.log'
K_TO_G_RATIO = 1024 * 1024
SKIP_LOC = ['/work', '/home', '/home/lost+found', '/home/data']
SIZE_LIMIT = 50


def ERR(abbrv):
    return '[Error] ' + {
        'no_file': 'no such file',
        'loc_err': 'location is not correct'
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
            lines = f.readlines()
    except FileNotFoundError:
        print_err('no_file', file_name)
        sys.exit(1)
    return lines


def loc_and_size(lines):
    list_work = []
    list_home = []
    for line in lines:
        size = line.split()[0]
        loc = line.split()[1]
        if loc not in SKIP_LOC:
            if loc.startswith('/home/'):
                list_home.append((loc, size))
            elif loc.startswith('/work/'):
                list_work.append((loc, size))
            else:
                print_err('loc_err', loc)
                sys.exit(1)
    return list_home, list_work


def dict_user_size(list_home, list_work):
    user_size = {}
    for l in list_home:
        user = l[0].split('/')[2]
        user_size[user] = [l[1], 0]

    for l in list_work:
        user = l[0].split('/')[2]
        if user in user_size:
            user_size[user][1] = l[1]
        else:
            user_size[user] = [0, l[1]]

    return user_size


def print_info(user_size):
    print('%10s%10s%10s%10s%10s' % ('user', 'home', 'work', 'sum', 'mark'))
    for key in user_size:
        home = int(user_size[key][0]) / K_TO_G_RATIO
        work = int(user_size[key][1]) / K_TO_G_RATIO
        sum = home + work
        if(sum > SIZE_LIMIT):
            print('%10s%10.2fG%10.2fG%10.2fG%5s' %
                  (key, home, work, sum, '*'))
        else:
            print('%10s%10.2fG%10.2fG%10.2fG' % (key, home, work, sum))


def main():
    print_version(VERSION)
    lines = read_log_file(SIZE_LOG)
    l1, l2 = loc_and_size(lines)
    user_size = dict_user_size(l1, l2)
    print_info(user_size)

if __name__ == '__main__':
    main()
