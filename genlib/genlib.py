# history:
# 2020/4/18  v1.0  initial
# 2020/4/21  v1.1  MAX_BUS_NUM = 16; header first line delete a '/'
# 2020/4/24  v1.2  add AIO, DIO pin type
# 2020/10/4  v2.0  add verilog output function
# 2022/4/20  v3.0  change verilog format, and power info

import os
import sys
import re
import msvcrt
import datetime
import pandas as pd

from PyQt5 import QtWidgets
from myform import Ui_Form

VERSION = '3.0'

VALID_COLS = ['管脚方向', '管脚名']
VALID_PIN_TYPE = ['PR', 'GD', 'PR_IO', 'GD_IO',
                  'AI', 'AO', 'AIO', 'DI', 'DO', 'DIO']
MAX_BUS_NUM = 16


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

    def confirm(self):
        xls_file_name = self.txt_xls_file.text()
        lib_name = self.txt_lib_name.text()

        if xls_file_name == '':
            info = 'excel文件名为空'
            QtWidgets.QMessageBox.warning(self, '出错', info)
            return

        if lib_name == '':
            info = 'Lib名为空'
            QtWidgets.QMessageBox.warning(self, '出错', info)
            return

        ret = xls_to_lib(xls_file_name, lib_name)
        ret1 = xls_to_v(xls_file_name, lib_name)
        ret2 = xls_to_pg(xls_file_name, lib_name)

        if isinstance(ret, str):
            info = '生成文件: %s.lib' % ret
            QtWidgets.QMessageBox.information(self, '信息', info)
        if isinstance(ret1, str):
            info = '生成文件: %s.v' % ret
            QtWidgets.QMessageBox.information(self, '信息', info)
        if isinstance(ret2, str):
            info = '生成文件: %s.[pg*]' % ret
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


def write_header(f, lib_name):
    f.write('/*******************************************************************************\n')
    f.write('// Library Name    : %s\n' % lib_name)
    f.write('// Modified Date   : %s\n' %
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    f.write('//*******************************************************************************\n')

    f.write('/**************************\n')
    f.write('Unit :\n')
    f.write('\ttime : ns\n')
    f.write('\tcapacitance : pf\n')
    f.write('\tvoltage : V\n')
    f.write('\tcurrent : mA\n')
    f.write('\tpower   : mW\n')
    f.write('**************************/\n\n')

    f.write('/* ******************************* */\n')
    f.write('/* ****  Library Description  **** */\n')
    f.write('/* ******************************* */\n\n')

    f.write('library (%s)  {\n\n' % lib_name)
    f.write('/* General Library Attributes */\n\n')
    f.write('\ttechnology (cmos) ;\n')
    f.write('\tdelay_model      : table_lookup;\n')
    f.write('\tbus_naming_style : "%s[%d]";\n')
    f.write('\tsimulation  : true;\n\n\n')

    f.write('/* Unit Definition */\n\n')
    f.write('\ttime_unit               : "1ns";\n')
    f.write('\tvoltage_unit            : "1V";\n')
    f.write('\tcurrent_unit            : "1mA";\n')
    f.write('\tcapacitive_load_unit (1,pf);\n')
    f.write('\tpulling_resistance_unit : "1kohm";\n\n\n')

    f.write('/* Added for DesignPower (Power Estimation). */\n')
    f.write('\tleakage_power_unit : 1pW;\n')
    f.write('\tdefault_cell_leakage_power : 1;\n\n')
    f.write('slew_lower_threshold_pct_rise :  30 ;\n')
    f.write('slew_upper_threshold_pct_rise :  70 ;\n')
    f.write('input_threshold_pct_fall      :  50 ;\n')
    f.write('output_threshold_pct_fall     :  50 ;\n')
    f.write('input_threshold_pct_rise      :  50 ;\n')
    f.write('output_threshold_pct_rise     :  50 ;\n')
    f.write('slew_lower_threshold_pct_fall :  30 ;\n')
    f.write('slew_upper_threshold_pct_fall :  70 ;\n')
    f.write('slew_derate_from_library      :  0.4 ;\n\n\n')

    f.write('/****************************/\n')
    f.write('/** user supplied nominals **/\n')
    f.write('/****************************/\n\n')
    f.write('nom_voltage     : 1.5;\n')
    f.write('nom_temperature : 25 ;\n')
    f.write('nom_process     : 1.0 ;\n\n\n')

    f.write('operating_conditions("typ"){\n')
    f.write('process :   1.0 ;\n')
    f.write('temperature :  25 ;\n')
    f.write('voltage :      1.5 ;\n')
    f.write('tree_type : "balanced_tree" ;\n')
    f.write('}\n\n')

    f.write('default_operating_conditions  : typ ;\n\n\n\n')

    f.write('/****************************/\n')
    f.write('/** user supplied defaults **/\n')
    f.write('/****************************/\n\n')
    f.write('default_inout_pin_cap           :       0.0200;\n')
    f.write('default_input_pin_cap           :       0.0200;\n')
    f.write('default_output_pin_cap          :       0.0000;\n')
    f.write('default_fanout_load             :       1.0000;\n\n\n')

    f.write('/* Type declarations */\n\n')

    for i in range(2, MAX_BUS_NUM+1):
        bus_type_define(f, i)


def write_tail(f, lib_name):
    f.write('}  /* end of library %s*/\n' % lib_name)


# def is_valid_pin(pin_type):
#     return (pin_type in VALID_PIN_TYPE)


def pin_type_to_txt(pin_type):
    if pin_type in ['AI', 'DI']:
        type_txt = 'input'
    elif pin_type in ['AO', 'DO']:
        type_txt = 'output'
    else:
        type_txt = 'inout'
    return type_txt


def write_norm_pin(f, pin_type, pin_name):
    type_txt = pin_type_to_txt(pin_type)
    f.write('   pin (%s) {\n' % pin_name)
    f.write('           direction : %s;\n' % type_txt)
    f.write('           capacitance : 0.1;\n')
    f.write('   }\n')
    f.write('\n')


def write_bus_pin(f, pin_type, pin_main_name, i_max, i_min):
    type_txt = pin_type_to_txt(pin_type)
    f.write('  bus (%s) {\n' % pin_main_name)
    # f.write('        bus_type       : "bus%d";\n' % (eval(i_max)+1))
    f.write('        bus_type       : "bus%d";\n' % (i_max+1))
    for i in range(i_max, i_min-1, -1):
        # f.write('%s[%d]\n' % (pin_main_name, i))
        f.write('        pin (%s[%d]) {\n' % (pin_main_name, i))
        f.write('           direction : %s;\n' % type_txt)
        f.write('           capacitance : 0.1;\n')
        f.write('        }\n')
    f.write('   } /* end of bus %s */\n' % pin_main_name)

    f.write('\n')


def write_pin(f, item):
    pin_type = item[0]
    pin_name = item[1]

    # f.write('%s\n' % ({pin_type} & {'DI1', 'DO1'}))
    # f.write('%s\n' % is_valid_pin(pin_type))
    # if is_valid_pin(pin_type):
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
    # print(lib_name)
    f.write('cell (%s) {\n\n' % cell_name)
    f.write('   area            : 0;\n')
    f.write('   dont_touch      : true;\n')
    f.write('   dont_use        : true;\n')
    f.write('   map_only        : true;\n\n')
    # print(df)
    for _, row in df.iterrows():
        # f.write(row.tolist())
        write_pin(f, row.tolist())
    f.write('}  /* end of cell %s */\n\n' % cell_name)


def is_valid_sheet(df):
    n_cols = len(VALID_COLS)
    return df.columns.tolist()[1:n_cols+1] == VALID_COLS


def clean_df(df):
    df = df[VALID_COLS]
    df = df.dropna()
    df = df.loc[df[VALID_COLS[0]].isin(VALID_PIN_TYPE)]
    # test.loc[test["所属区域"]=="苏州"]
    return df


def xls_to_lib(xls_file_name, lib_name):
    try:
        xlsx = pd.ExcelFile(xls_file_name)
        lib_file = '%s.lib' % lib_name

        f = open(lib_file, 'w+')
        write_header(f, lib_name)
        for sheet_name in xlsx.sheet_names:
            df = pd.read_excel(xlsx, sheet_name=sheet_name, header=2)
            if is_valid_sheet(df):
                df = clean_df(df)
                write_cell(f, cell_name=sheet_name, df=df)
        write_tail(f, lib_name)
        f.close()
    except Exception as e:
        return e
    return(lib_name)


def write_norm_pin_v(f, pin_type, pin_name):
    type_txt = pin_type_to_txt(pin_type)
    f.write('    %-10s %s;\n' % (type_txt, pin_name))


def write_bus_pin_v(f, pin_type, pin_main_name, i_max, i_min):
    type_txt = pin_type_to_txt(pin_type)
    f.write('    %-10s [%s:%s]%s;\n' %
            (type_txt, i_max, i_min, pin_main_name))


def write_pin_v_1(f, item):
    pin_type = item[0]
    pin_name = item[1]

    p = re.compile(r'(.+?)<(\d+):(\d+)>', re.S)
    m = re.match(p, pin_name)
    if m:
        pin_main_name = m.group(1)
        # i_max = int(m.group(2))
        # i_min = int(m.group(3))
        # write_bus_pin_v(f, pin_type, pin_main_name, i_max, i_min)
    else:
        # write_norm_pin_v(f, pin_type, pin_name)
        pin_main_name = pin_name

    f.write('    %s' % pin_main_name)


def write_pin_v_2(f, item):
    pin_type = item[0]
    pin_name = item[1]

    p = re.compile(r'(.+?)<(\d+):(\d+)>', re.S)
    m = re.match(p, pin_name)
    if m:
        pin_main_name = m.group(1)
        i_max = int(m.group(2))
        i_min = int(m.group(3))
        write_bus_pin_v(f, pin_type, pin_main_name, i_max, i_min)
    else:
        write_norm_pin_v(f, pin_type, pin_name)


def write_cell_v(f, cell_name, df):
    # print(lib_name)
    f.write('module %s (\n' % cell_name)
    num = df.shape[0]
    i = 0
    for _, row in df.iterrows():
        i += 1
        write_pin_v_1(f, row.tolist())

        if i < num:
            f.write(',\n')
        # else:
        #     f.write('\n')
    f.write(');\n\n')

    for _, row in df.iterrows():
        write_pin_v_2(f, row.tolist())

    f.write('endmodule\n\n')


def write_pg(filename, pin_list):
    with open(filename, 'w+') as f:
        for pin in pin_list:
            f.write('%s ' % pin)


def xls_to_v(xls_file_name, lib_name):
    try:
        xlsx = pd.ExcelFile(xls_file_name)
        v_file = '%s.v' % lib_name

        f = open(v_file, 'w+')
        # write_header(f, lib_name)
        for sheet_name in xlsx.sheet_names:
            df = pd.read_excel(xlsx, sheet_name=sheet_name, header=2)
            if is_valid_sheet(df):
                df = clean_df(df)
                write_cell_v(f, cell_name=sheet_name, df=df)
        # write_tail(f, lib_name)
        f.close()
    except Exception as e:
        return e
    return(lib_name)


def xls_to_pg(xls_file_name, lib_name):
    try:
        xlsx = pd.ExcelFile(xls_file_name)

        # f = open(v_file, 'w+')
        # write_header(f, lib_name)
        all_p = []
        all_g = []
        all_pio = []
        all_gio = []
        for sheet_name in xlsx.sheet_names:
            df = pd.read_excel(xlsx, sheet_name=sheet_name, header=2)
            if is_valid_sheet(df):
                df = clean_df(df)
                df_p = df.loc[df[VALID_COLS[0]] == VALID_PIN_TYPE[0]]
                l_df = df_p[VALID_COLS[1]].tolist()
                all_p = all_p+l_df

                df_g = df.loc[df[VALID_COLS[0]] == VALID_PIN_TYPE[1]]
                l_df = df_g[VALID_COLS[1]].tolist()
                all_g = all_g+l_df

                df_pio = df.loc[df[VALID_COLS[0]] == VALID_PIN_TYPE[2]]
                l_df = df_pio[VALID_COLS[1]].tolist()
                all_pio = all_pio+l_df

                df_gio = df.loc[df[VALID_COLS[0]] == VALID_PIN_TYPE[3]]
                l_df = df_gio[VALID_COLS[1]].tolist()
                all_gio = all_gio+l_df

        all_p = list(set(all_p))
        all_g = list(set(all_g))
        all_pio = list(set(all_pio))
        all_gio = list(set(all_gio))

        filename = '%s.p' % lib_name
        write_pg(filename, all_p)

        filename = '%s.g' % lib_name
        write_pg(filename, all_g)

        filename = '%s.pio' % lib_name
        write_pg(filename, all_pio)

        filename = '%s.gio' % lib_name
        write_pg(filename, all_gio)

        # write_tail(f, lib_name)
        # f.close()
    except Exception as e:
        return e
    return(lib_name)


def main():
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.setWindowTitle('genlib v%s' % VERSION)
    myshow.show()
    sys.exit(app.exec_())

# def main():
#     xls_file_name = 'A801_IP列表.xlsx'
#     lib_name = 'A800_ALL'
#     xls_to_lib(xls_file_name, lib_name)


if __name__ == '__main__':
    main()
