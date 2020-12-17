# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myform.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(510, 115)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.txt_xls_file = QtWidgets.QLineEdit(Form)
        self.txt_xls_file.setObjectName("txt_xls_file")
        self.horizontalLayout.addWidget(self.txt_xls_file)
        self.tbt_load_file = QtWidgets.QToolButton(Form)
        self.tbt_load_file.setObjectName("tbt_load_file")
        self.horizontalLayout.addWidget(self.tbt_load_file)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(13, -1, 44, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.txt_lib_name = QtWidgets.QLineEdit(Form)
        self.txt_lib_name.setObjectName("txt_lib_name")
        self.horizontalLayout_2.addWidget(self.txt_lib_name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_confirm = QtWidgets.QPushButton(Form)
        self.btn_confirm.setObjectName("btn_confirm")
        self.horizontalLayout_3.addWidget(self.btn_confirm)
        self.btn_close = QtWidgets.QPushButton(Form)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_3.addWidget(self.btn_close)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        self.btn_confirm.clicked.connect(Form.confirm)
        self.btn_close.clicked.connect(Form.close_win)
        self.tbt_load_file.clicked.connect(Form.open_xls_file)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "IP列表Excel文件"))
        self.tbt_load_file.setText(_translate("Form", "..."))
        self.label_2.setText(_translate("Form", "输出lib/v文件名"))
        self.btn_confirm.setText(_translate("Form", "确定"))
        self.btn_close.setText(_translate("Form", "关闭"))
