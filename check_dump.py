# history:
# 2018/09/01  v1.0  initial


import os
import sys
import datetime
import re


VERSION = '1.0'
LOG_DIR = r'e:\temp'


def ERR(abbrv):
    return '[Error] ' + {
        'no_file': 'no such file',
        'split_err': 'cannot split log by day',
        'level_err': 'cannot extract valid level',
        'time_err': 'cannot extract valid completed time',
        'size_err': 'cannot extract valid file size',
        'no_level0': 'cannot find level0 info'
    }.get(abbrv, 'unknown error')


def print_err(abbrv, param):
    if param == '':
        print(ERR(abbrv))
    else:
        print('%s (%s)' % (ERR(abbrv), param))


def get_dump_file_name(log_dir):
    month_year_abbr = datetime.datetime.now().date().strftime('%b_%Y')
    file_name = 'dump_' + month_year_abbr + '.log'
    full_name = os.path.join(log_dir, file_name)
    # print(full_name)
    return full_name


def read_log_file(file_name):
    try:
        with(open(file_name)) as f:
            txt = f.read()
    except FileNotFoundError:
        print_err('no_file', file_name)
        sys.exit(1)

    return txt


def split_by_day(log_txt):
    p = re.compile('\*' * 55 + '(.*?)' + '\*' * 55, re.S)
    result = re.findall(p, log_txt)
    if len(result) == 0:
        print_err('split_err', '')
        sys.exit(1)
    return result


def get_a_day_level(log_a_day):
    p = re.compile('DUMP: Date of this level (\d) dump:', re.S)
    result = re.findall(p, log_a_day)
    if len(result) != 2:
        print_err('level_err', '')
        sys.exit(1)
    level = result[1]
    return level


def trans_time_format(time_txt):
    split_txt = time_txt.split()
    month = split_txt[1]
    date = split_txt[2]
    time = split_txt[3]
    year = split_txt[4]
    dt = datetime.datetime.strptime('%s %s %s %s' % (
        year, month, date, time), "%Y %b %d %H:%M:%S")
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def get_a_day_complete_time(log_a_day):
    p = re.compile('DUMP: Date this dump completed:(.*?)\n', re.S)
    result = re.findall(p, log_a_day)
    if len(result) != 1:
        print_err('time_err', '')
        sys.exit(1)
    complete_time = trans_time_format(result[0])
    return complete_time


def get_a_day_file_size(log_a_day):
    p = re.compile('DUMP: \d+ blocks \((.*?)\) on 1 volume\(s\)', re.S)
    result = re.findall(p, log_a_day)
    if len(result) != 1:
        print_err('size_err', '')
        sys.exit(1)
    file_size = result[0]
    return file_size


def get_a_day_info(log_a_day):
    level = get_a_day_level(log_a_day)
    complete_time = get_a_day_complete_time(log_a_day)
    file_size = get_a_day_file_size(log_a_day)
    return level, complete_time, file_size


def get_all_info(log_by_day):
    infos = []
    for alog in log_by_day:
        infos.append(get_a_day_info(alog))

    found_level0 = False
    print('level\tcompleted time\t\tfile size')
    for ainfo in infos:
        print('%s\t%s\t%s' % ainfo)
        if ainfo[0] == '0':
            found_level0 = True
    if not found_level0:
        print_err('no_level0', '')
        sys.exit(1)


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def main():
    print_version(VERSION)
    file_name = get_dump_file_name(LOG_DIR)
    # file_name = r'e:\temp\dump_Jun_2018.log'
    log_txt = read_log_file(file_name)
    log_by_day = split_by_day(log_txt)
    get_all_info(log_by_day)


if __name__ == '__main__':
    main()
