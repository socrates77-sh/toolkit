# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myform.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(409, 155)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.txt_work_load = QtWidgets.QLineEdit(Form)
        self.txt_work_load.setObjectName("txt_work_load")
        self.horizontalLayout.addWidget(self.txt_work_load)
        self.tbt_work_load_file = QtWidgets.QToolButton(Form)
        self.tbt_work_load_file.setObjectName("tbt_work_load_file")
        self.horizontalLayout.addWidget(self.tbt_work_load_file)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(37, -1, 44, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.txt_work_load_sheet = QtWidgets.QLineEdit(Form)
        self.txt_work_load_sheet.setObjectName("txt_work_load_sheet")
        self.horizontalLayout_2.addWidget(self.txt_work_load_sheet)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.txt_detail_cost = QtWidgets.QLineEdit(Form)
        self.txt_detail_cost.setObjectName("txt_detail_cost")
        self.horizontalLayout_3.addWidget(self.txt_detail_cost)
        self.tbt_detail_cost_file = QtWidgets.QToolButton(Form)
        self.tbt_detail_cost_file.setObjectName("tbt_detail_cost_file")
        self.horizontalLayout_3.addWidget(self.tbt_detail_cost_file)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(37, -1, 44, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.txt_detail_txt_sheet = QtWidgets.QLineEdit(Form)
        self.txt_detail_txt_sheet.setObjectName("txt_detail_txt_sheet")
        self.horizontalLayout_4.addWidget(self.txt_detail_txt_sheet)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_confirm = QtWidgets.QPushButton(Form)
        self.btn_confirm.setObjectName("btn_confirm")
        self.horizontalLayout_5.addWidget(self.btn_confirm)
        self.btn_close = QtWidgets.QPushButton(Form)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_5.addWidget(self.btn_close)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        self.btn_confirm.clicked.connect(Form.confirm)
        self.btn_close.clicked.connect(Form.close_win)
        self.tbt_work_load_file.clicked.connect(Form.open_work_load)
        self.tbt_detail_cost_file.clicked.connect(Form.open_detail_cost)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "工作分配文件"))
        self.tbt_work_load_file.setText(_translate("Form", "..."))
        self.label_2.setText(_translate("Form", "表单名"))
        self.label_3.setText(_translate("Form", "费用明细文件"))
        self.tbt_detail_cost_file.setText(_translate("Form", "..."))
        self.label_4.setText(_translate("Form", "表单名"))
        self.btn_confirm.setText(_translate("Form", "确定"))
        self.btn_close.setText(_translate("Form", "关闭"))
