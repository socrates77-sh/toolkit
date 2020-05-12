# history:
# 2020/4/12  v1.0  initial
# 2020/4/13  v1.1  output 2 sheets
# 2020/5/11  v1.2  add exception check
# 2020/5/11  v2.0  change output scheme


import os
import sys
import msvcrt
import datetime
# import xlwt
# import xlrd
import pandas as pd
import numpy as np

import openpyxl
from openpyxl.styles import colors, Font, Color, Border, Side, Alignment, PatternFill

from PyQt5 import QtWidgets
from myform import Ui_Form

VERSION = '2.0'
# IS_FAMILY = True

INX_NAME_WORK_LOAD = 3
INX_NAME_DETAIL_COST = 1


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def wait_any_key():
    print('press any key to exit...')
    msvcrt.getch()


def clean_work_load(df_work_load):
    valid_columns = df_work_load.columns.values[INX_NAME_WORK_LOAD:-2]
    df = df_work_load[valid_columns]
    df = df.set_index(valid_columns[0])
    df = df.fillna(0)
    return df


def clean_detail_cost(df_detail_cost):
    # valid_columns = df_detail_cost.columns.values[INX_NAME_DETAIL_COST:-1]
    valid_columns = df_detail_cost.columns.values[INX_NAME_DETAIL_COST:]
    df = df_detail_cost[valid_columns]
    df = df.fillna(0)
    return df


class ExcelDataException(Exception):
    pass
    # def __init__(self, msg):
    #     self.msg = msg

    # def __str__(self):
    #     msg = '费用明细表的人员未出现在人员分摊表中: %s' % self.msg
    #     return(str)


def sum_cost(df_work_load, df_detail_cost):
    colunms = df_work_load.columns
    df_used_work_load = df_work_load.loc[df_detail_cost.index.values]
    person_in_cost = set(df_detail_cost.index.values)
    person_in_load = set(df_work_load.index.values)
    person_missed = person_in_cost-(person_in_cost & person_in_load)
    if len(person_missed) > 0:
        msg = '费用明细表的人员未出现在人员分摊表中: %s' % person_missed
        raise ExcelDataException(msg)

    df_used_work_load_classified = df_used_work_load.sum(
        level=0, axis=1).T.unstack()

    valid_columns = df_detail_cost.columns.values[2:]
    info_colunms = df_detail_cost.columns.values[0:2]
    # df_detail_valid_cost = df_detail_cost[valid_columns]

    narray1 = []
    narray2 = []
    narray3 = []
    narray4 = []
    for item in df_used_work_load_classified.index.values:
        # print(item)
        name = item[0]
        department = df_detail_cost.loc[name, info_colunms[0]]
        loc = df_detail_cost.loc[name, info_colunms[1]]
        family = item[1]
        narray1.append(name)
        narray2.append(department)
        narray3.append(loc)
        narray4.append(family)

    new_index = [np.array(narray1), np.array(narray2),
                 np.array(narray3), np.array(narray4)]
    df = pd.DataFrame(columns=valid_columns,
                      index=new_index)

    df.index.names = ['员工', info_colunms[0], info_colunms[1], '分类']

    for item in df.index.values:
        name = item[0]
        family = item[3]
        value = df_used_work_load_classified.loc[(name, family)]
        df.loc[item] = value*df_detail_cost[valid_columns].loc[name]

    return df


def format_xls(xls_file_name, sheet_name, is_family):
    workbook = openpyxl.load_workbook(xls_file_name)
    ws = workbook[sheet_name]

    if is_family:
        header_row = 1
    else:
        header_row = 2
        ws.delete_rows(3)

    header_col = 4

    nrows = ws.max_row
    ncols = ws.max_column

    font = Font(name='Arial', size=10, color=colors.BLACK)
    hd_font = Font(name='Arial', size=10, color=colors.BLACK, bold=True)

    thin = Side(border_style="thin")
    border = Border(top=thin, left=thin, right=thin, bottom=thin)

    alignment = Alignment(horizontal="center", vertical="center")

    fill = PatternFill(fill_type="solid", fgColor="C1CDC1")

    for row in ws.rows:
        for cell in row:
            cell.font = font
            cell.border = border
            cell.alignment = alignment

    for i in range(header_row):
        for cell in list(ws.rows)[i]:
            cell.font = hd_font
            cell.fill = fill

    for i in range(header_col):
        for cell in list(ws.columns)[i]:
            cell.font = hd_font
            cell.fill = fill

    for i in range(header_row, nrows):
        for j in range(header_col, ncols):
            ws.cell(i+1, j+1).number_format = '0.00'

    ws.column_dimensions['B'].width = 20.0
    ws.column_dimensions['D'].width = 15.0

    workbook.save(filename=xls_file_name)


def report_xls(xls_file_name, sheet_name, df_sum_cost):
    sheet_name_family = '%s-大类' % sheet_name
    # sheet_name_proj = '%s-项目' % sheet_name

    with pd.ExcelWriter(xls_file_name) as xlsx:
        # df = df_sum_cost.sum(level=0, axis=1)
        df = df_sum_cost
        df.to_excel(xlsx, sheet_name=sheet_name_family, merge_cells=False)
        # df = df_sum_cost
        # df.to_excel(xlsx, sheet_name=sheet_name_proj)

    format_xls(xls_file_name, sheet_name_family, is_family=True)
    # format_xls(xls_file_name, sheet_name_proj, is_family=False)


def backend_proc(work_load_file, work_load_sheet, detail_cost_file, detail_cost_sheet):
    try:
        df_work_load = pd.read_excel(
            work_load_file, sheet_name=work_load_sheet,  header=[0, 1])
        df_detail_cost = pd.read_excel(
            detail_cost_file, sheet_name=detail_cost_sheet,
            index_col=INX_NAME_DETAIL_COST)

        df_work_load = clean_work_load(df_work_load)
        df_detail_cost = clean_detail_cost(df_detail_cost)

        df_sum_cost = sum_cost(df_work_load, df_detail_cost)

        xls_file_name = '%s汇总_%s.xlsx' % (
            detail_cost_sheet, datetime.datetime.now().date().strftime('%y%m%d'))
        report_xls(xls_file_name, work_load_sheet,
                   df_sum_cost)
    except Exception as e:
        return e
    return(xls_file_name)


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

    def confirm(self):
        work_load_file = self.txt_work_load.text()
        work_load_sheet = self.txt_work_load_sheet.text()
        detail_cost_file = self.txt_detail_cost.text()
        detail_cost_sheet = self.txt_detail_txt_sheet.text()

        # work_load_file = r'E:\py\toolkit\cost\人员费用分摊.xlsx'
        # work_load_sheet = '4月'
        # detail_cost_file = r'E:\py\toolkit\cost\4月工时分摊表 - 副本(1).xlsx'
        # # detail_cost_sheet = '社保'
        # detail_cost_sheet = '公积金'
        # detail_cost_sheet = '工资'

        ret = backend_proc(work_load_file, work_load_sheet,
                           detail_cost_file, detail_cost_sheet)

        if isinstance(ret, str):
            info = '生成文件: %s' % ret
            QtWidgets.QMessageBox.information(self, '信息', info)
        else:
            info = repr(ret)
            QtWidgets.QMessageBox.warning(self, '出错', info)

    def close_win(self):
        self.close()

    def open_work_load(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件', '.')
        if file_name:
            self.txt_work_load.setText(file_name)

    def open_detail_cost(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件', '.')
        if file_name:
            self.txt_detail_cost.setText(file_name)


def main():
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.setWindowTitle('cal_cost v%s' % VERSION)
    myshow.show()
    sys.exit(app.exec_())


def main1():
    work_load_file = r'E:\py\toolkit\cost\人员费用分摊.xlsx'
    work_load_sheet = '4月'
    detail_cost_file = r'E:\py\toolkit\cost\4月工时分摊表 - 副本(1).xlsx'
    # detail_cost_sheet = '社保'
    detail_cost_sheet = '公积金'
    detail_cost_sheet = '工资'

    # ret = backend_proc(work_load_file, work_load_sheet,
    #    detail_cost_file, detail_cost_sheet)

    df_work_load = pd.read_excel(
        work_load_file, sheet_name=work_load_sheet,  header=[0, 1])
    df_detail_cost = pd.read_excel(
        detail_cost_file, sheet_name=detail_cost_sheet,
        index_col=INX_NAME_DETAIL_COST)

    print(df_detail_cost)

    df_work_load = clean_work_load(df_work_load)
    df_detail_cost = clean_detail_cost(df_detail_cost)

    df_sum_cost = sum_cost(df_work_load, df_detail_cost)

    xls_file_name = '%s汇总_%s.xlsx' % (
        detail_cost_sheet, datetime.datetime.now().date().strftime('%y%m%d'))
    report_xls(xls_file_name, work_load_sheet,
               df_sum_cost)


if __name__ == '__main__':
    main()
