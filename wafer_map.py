import re
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import msvcrt

# from PyInstaller import log as logging
# from PyInstaller import compat
# from os import listdir


cp_file = 'FA7Y-726810-161604.CP3'


def trans_bin(x):
    if x == '1':
        return 0
    elif x == '.':
        return 2
    elif x == ' ':
        return 3
    else:
        return 1


def get_map_data(cp_file):
    with(open(cp_file)) as f:
        try:
            lines = f.readlines()
        except Exception as e:
            print('Wrong format: %s' % cp_file)
            return None
    p = re.compile('^\d{3}(.*?)$', re.S)
    l_map = []
    for l in lines:
        m = re.match(p, l)
        if m:
            l_map.append(list(map(trans_bin, list(m.group(1)))))
            # l_map.append(list(m.group(1)))
    if l_map == []:
        print('Wrong format: %s' % cp_file)
        return None
    else:
        return np.array(l_map)


def save_map_png(cp_file, array_data):
    x, y = array_data.shape
    # plt.figure(figsize=(6, 6), dpi=500)
    plt.figure(figsize=(6, 6))
    colors = ['green', 'red', 'yellow', 'white']
    cmap = mpl.colors.ListedColormap(colors)
    plt.imshow(array_data, cmap=cmap, aspect=y / x)
    plt.axis('off')
    # plt.show()
    plt.savefig(cp_file + '.png')
    plt.close()
    print('[F] %s' % cp_file + '.png')


def do_one_map(cp_file):
    array_data = get_map_data(cp_file)
    if array_data is None:
        return None
    save_map_png(cp_file, array_data)
    return array_data


def main():
    # do_one_map(cp_file)

    file_list = glob.glob('*')
    data_array_list = []
    for f in file_list:
        print('[P] %s' % f)
        da = do_one_map(f)
        if da is not None:
            data_array_list.append(da)

    # print(len(file_list))
    # print(len(data_array_list))

    first = data_array_list[0]
    i = 0
    for da in data_array_list[1:-1]:
        second = da
        first = np.maximum(first, second)

    first = np.maximum(first, data_array_list[-1])
    save_map_png('all_wafer', first)

    print('Press any key to exit ...')
    msvcrt.getch()

if __name__ == '__main__':
    main()
