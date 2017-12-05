import docx


class WordTable():

    def __init__(self, table):
        self.table = table
        # self.n_row = len(table.rows)
        # self.n_col = len(table.columns)

    # TODO: execption handle
    def cell_text(self, idx_row, idx_col):
        return self.table.cell(idx_row, idx_col).text

    # TODO: change to exact compare
    def has_text(self, str):
        for i in range(len(self.table.rows)):
            for j in range(len(self.table.columns)):
                if str in self.cell_text(i, j):
                    return True
        return False


def main():
    doc = docx.Document(r'E:\temp\jupyter\MC32P7510_UMAN_V1.5.docx')
    wt = WordTable(doc.tables[3])
    print(wt.has_text('INDF01'))

if __name__ == '__main__':
    main()
