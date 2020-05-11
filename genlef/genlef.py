# history:
# 2020/4/28  v1.0  initial


import os
import sys
import re
import msvcrt
import datetime
import pandas as pd

from PyQt5 import QtWidgets
from myform import Ui_Form

VERSION = '1.0'

VALID_COLS = ['管脚方向', '管脚名']
VALID_PIN_TYPE = ['POWER', 'AI', 'AO', 'AIO', 'DI', 'DO', 'DIO']
MAX_BUS_NUM = 16

PAD_SIZE = (1, 0.3)
pt_left_bottom = (0, 0)


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

    def confirm(self):
        xls_file_name = self.txt_xls_file.text()
        lef_name = self.txt_lef_name.text()

        if xls_file_name == '':
            info = 'excel文件名为空'
            QtWidgets.QMessageBox.warning(self, '出错', info)
            return

        if lef_name == '':
            info = 'LEF名为空'
            QtWidgets.QMessageBox.warning(self, '出错', info)
            return

        ret = xls_to_lef(xls_file_name, lef_name)

        if isinstance(ret, str):
            info = '生成文件: %s.lef' % ret
            QtWidgets.QMessageBox.information(self, '信息', info)
        else:
            info = repr(ret)
            QtWidgets.QMessageBox.warning(self, '出错', info)

    def close_win(self):
        self.close()

    def open_xls_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件', '.')
        if file_name:
            self.txt_xls_file.setText(file_name)


def bus_type_define(f, num):
    f.write('  type (bus%d)  {\n' % num)
    f.write('    base_type : array;\n')
    f.write('    data_type : bit;\n')
    f.write('    bit_width : %d;\n' % num)
    f.write('    bit_from  : %d\n' % (num-1))
    f.write('    bit_to    : 0;\n')
    f.write('    downto    : true;\n')
    f.write('  }\n')
    f.write('\n')


def write_header(f, lef_name):
    f.write('#'*70 + '\n')
    f.write('# LEF Name        : %s\n' % lef_name)
    f.write('# Modified Date   : %s\n' %
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    f.write('#'*70 + '\n\n')

    f.write('VERSION 5.5 ;\n\n')
    f.write('NAMESCASESENSITIVE ON ;\n\n')
    f.write('DIVIDERCHAR "/" ;\n')
    f.write('BUSBITCHARS "[]" ;\n\n')
    f.write(' USEMINSPACING OBS OFF  ;\n')
    f.write('UNITS\n')
    f.write('    DATABASE MICRONS 2000  ;\n')
    f.write('END UNITS\n\n')

    f.write(' MANUFACTURINGGRID    0.005000 ;\n')
    f.write('SITE IOSite\n')
    f.write('    SYMMETRY Y  ;\n')
    f.write('    CLASS PAD  ;\n')
    f.write('    SIZE 80.8400 BY 144.0000 ;\n')
    f.write('END IOSite\n\n')

    f.write('SITE CoreSite\n')
    f.write('    SYMMETRY Y   ;\n')
    f.write('    CLASS CORE  ;\n')
    f.write('    SIZE 0.3700 BY 2.2200 ;\n')
    f.write('END CoreSite\n\n')


def write_tail(f):
    f.write('\nEND LIBRARY\n')


def is_valid_pin(pin_type):
    return (pin_type in VALID_PIN_TYPE)


def pin_type_to_txt(pin_type):
    if pin_type in ['AI', 'DI']:
        type_txt = 'INPUT'
    elif pin_type in ['AO', 'DO']:
        type_txt = 'OUTPUT'
    else:
        type_txt = 'INOUT'
    return type_txt


def write_norm_pin(f, pin_type, pin_name):
    global pt_left_bottom
    x0, y0 = pt_left_bottom
    x1, y1 = (x0+PAD_SIZE[0], y0+PAD_SIZE[1])
    pt_left_bottom = (x0, y0+0.6)

    type_txt = pin_type_to_txt(pin_type)
    f.write('    PIN %s\n' % pin_name)
    f.write('        DIRECTION %s ;\n' % type_txt)
    f.write('        ANTENNAPARTIALMETALSIDEAREA 10  LAYER M3 ;\n')
    f.write('        PORT\n')
    f.write('        LAYER M3 ;\n')
    f.write('        RECT  %0.4f %0.4f %0.4f %0.4f ;\n' % (x0, y0, x1, y1))
    f.write('        END\n')
    f.write('    END %s\n' % pin_name)


def write_bus_pin(f, pin_type, pin_main_name, i_max, i_min):
    for i in range(i_max, i_min-1, -1):
        pin_name = '%s[%d]' % (pin_main_name, i)
        write_norm_pin(f, pin_type, pin_name)


def write_pin(f, item):
    pin_type = item[0]
    pin_name = item[1]

    if is_valid_pin(pin_type):
        p = re.compile(r'(.+?)<(\d+):(\d+)>', re.S)
        m = re.match(p, pin_name)
        if m:
            pin_main_name = m.group(1)
            i_max = int(m.group(2))
            i_min = int(m.group(3))
            write_bus_pin(f, pin_type, pin_main_name, i_max, i_min)
        else:
            write_norm_pin(f, pin_type, pin_name)


def write_cell(f, cell_name, df):
    f.write('MACRO %s\n' % cell_name)
    f.write('    CLASS PAD ;\n')
    f.write('    FOREIGN %s 0 0 ;\n' % cell_name)
    f.write('    ORIGIN 0.0000 0.0000 ;\n')
    f.write('    SIZE 1000.0000 BY 1000.0000 ;\n')
    f.write('    SYMMETRY R0 ;\n')
    f.write('    SITE IOSite ;\n')
    # print(df)
    for _, row in df.iterrows():
        write_pin(f, row.tolist())
    f.write('END %s\n\n' % cell_name)


def is_valid_sheet(df):
    n_cols = len(VALID_COLS)
    return df.columns.tolist()[1:n_cols+1] == VALID_COLS


def clean_df(df):
    df = df[VALID_COLS]
    df = df.dropna()
    return df


def xls_to_lef(xls_file_name, lef_name):
    try:
        xlsx = pd.ExcelFile(xls_file_name)
        lef_file = '%s.lef' % lef_name

        f = open(lef_file, 'w+')
        write_header(f, lef_name)
        for sheet_name in xlsx.sheet_names:
            df = pd.read_excel(xlsx, sheet_name=sheet_name, header=2)
            if is_valid_sheet(df):
                df = clean_df(df)
                write_cell(f, cell_name=sheet_name, df=df)
        write_tail(f)
        f.close()
    except Exception as e:
        return e
    return(lef_name)


def main():
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.setWindowTitle('genlef v%s' % VERSION)
    myshow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
