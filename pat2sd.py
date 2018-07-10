import re
import glob
import os


# pat_file = './pat/Rom_P0_driver_Write_170817.pat'


def read_pat_lines(pat_file):
    lines = open(pat_file).readlines()
    return lines


def get_element_from_pat_line(line):
    result = {'p04': '', 'p10': '', 'p12': '',
              'p11': '', 'comment': '', 'repeat': ''}
    p = re.compile('\*(.*?)\*', re.S)
    m = re.search(p, line)
    if m:
        all_pin = m.group(1)
        result['p04'] = all_pin[0]
        result['p10'] = all_pin[2]
        result['p12'] = all_pin[3]
        result['p11'] = all_pin[4]

    p = re.compile('//(.*?)$', re.S)
    m = re.search(p, line)
    if m:
        result['comment'] = m.group(1)

    p = re.compile('RPT(.*?);', re.S)
    m = re.search(p, line)
    if m:
        result['repeat'] = m.group(1)
    return result


def init_write(out_file_name):
    return open(out_file_name, 'w+')


def write_head(f):
    f.write(
        '//HEAD[PIN_NAME]: P14,P15,P16,P04,P02,P03,P07,P06,P05,P23,P24,P01,P00,P10,P11,P12,P13\n')
    f.write('//END_HEAD;\n')
    f.write('@@PATTERN_DEFINE\n')
    f.write('\n')


def write_line(f, element_dict):
    p04 = element_dict['p04']
    p10 = element_dict['p10']
    p12 = element_dict['p12']
    p11 = element_dict['p11']
    if(p04 != '' and p10 != '' and p12 != '' and p11 != ''):
        # P14, P15, P16, P04, P02, P03, P07, P06, P05, P23, P24, P01, P00, P10, P11, P12, P13
        f.write('        XXX%sXXXXXXXXX%s%s%sX;' % (p04, p10, p11, p12))

    repeat = element_dict['repeat']
    if(repeat != ''):
        f.write('RPT%s' % repeat)

    comment = element_dict['comment']
    if(comment != ''):
        f.write('//%s' % comment)

    f.write('\n')


def do_one_file(pat_file):
    sd_name = pat_file.replace('.pat', '.sd')
    f = init_write(sd_name)
    write_head(f)
    pat_lines = read_pat_lines(pat_file)
    for l in pat_lines:
        element_dict = get_element_from_pat_line(l)
        write_line(f, element_dict)
    print('%s -> %s' % (pat_file, sd_name))
    f.close()


def main():
    file_list = glob.glob('.\pat\*.pat')
    for fl in file_list:
        # print(os.path.normpath(fl))
        do_one_file(os.path.normpath(fl))


if __name__ == '__main__':
    main()
