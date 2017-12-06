import docx
import re

# TODO: execption handle

REG_SUMMARY_TABLE_IDENTIFY = '通用数据区'
IGNORE_REG_NAME = ['', '通用数据区', '保留']


class WordTable():

    def __init__(self, table):
        self.table = table

    def cell_text(self, idx_row, idx_col):
        return self.table.cell(idx_row, idx_col).text

    def has_text(self, str):
        for i in range(len(self.table.rows)):
            for j in range(len(self.table.columns)):
                if str == self.cell_text(i, j):
                    return True
        return False


class RegSummaryTable(WordTable):

    def __found_addr_range(self, text):
        # match like '188H - 18FH'
        if re.match('[0-9ABCDEF]+H – [0-9ABCDEF]+H', text):
            return True
        else:
            return False

    def __is_reg_list_row(self, idx_row):
        row_cells = self.table.row_cells(idx_row)
        first_cell_txt = row_cells[0].text
        if len(row_cells) == 9 and self.__found_addr_range(first_cell_txt):
            return True
        else:
            return False

    def __get_start_addr(self, idx_row):
        # row_cells = self.table.row_cells(idx_row)
        first_cell_txt = self.table.row_cells(idx_row)[0].text
        m = re.match('([0-9ABCDEF]+)H – [0-9ABCDEF]+H', first_cell_txt)
        start_addr_txt = m.group(1) if m else '0'
        return int('0x' + start_addr_txt, 16)

    def get_reg_list_row(self, idx_row):
        reg_lst = []
        row_cells = self.table.row_cells(idx_row)
        start_addr = self.__get_start_addr(idx_row)
        for i in range(1, len(row_cells)):
            if (row_cells[i].text not in IGNORE_REG_NAME):
                reg_lst.append((start_addr + i - 1, row_cells[i].text))
        return reg_lst

    def get_reg_list_all(self):
        all_reg_list = []
        for i_row in range(len(self.table.rows)):
            if self.__is_reg_list_row(i_row):
                all_reg_list.append(self.get_reg_list_row(i_row))
        return all_reg_list


def search_reg_summary_table(doc):
    for tab in doc.tables:
        wt = WordTable(tab)
        if wt.has_text(REG_SUMMARY_TABLE_IDENTIFY):
            return tab
    return None


def search_reg_bit_table(doc, reg_name):
    for tab in doc.tables:
        wt = WordTable(tab)
        if wt.cell_text(1, 0).strip() == reg_name:
            return tab
    return None


def do_all_reg(doc, all_reg_list):
    for reg_lst in all_reg_list:
        for (addr, reg_name) in reg_lst:
            reg_bit_tab = search_reg_bit_table(doc, reg_name)
            if reg_bit_tab:
                print(reg_name, 'found')
            else:
                print(reg_name, 'not')


def main():
    doc = docx.Document(r'E:\temp\jupyter\MC32P7510_UMAN_V1.5.docx')
    reg_sum_tab = RegSummaryTable(search_reg_summary_table(doc))
    if reg_sum_tab is None:
        print('Register summary table not found!')
        return -1
    else:
        all_reg_list = reg_sum_tab.get_reg_list_all()
        do_all_reg(doc, all_reg_list)
        return 0


if __name__ == '__main__':
    main()
