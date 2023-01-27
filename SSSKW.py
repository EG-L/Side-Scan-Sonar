# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SSSKW1.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pyqtgraph import PlotWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1095, 710)
        icon = QIcon()
        icon.addFile(u"kyungwon.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: rgb(75, 75, 75);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QSize(0, 120))
        self.tabWidget.setMaximumSize(QSize(16777215, 120))
        self.tabWidget.setStyleSheet(u"QTabBar::tab{\n"
"background-color: rgb(97, 97, 97);\n"
"border-color: rgb(97, 97, 97);\n"
"min-height: 20px; \n"
"border-color: rgb(0, 0, 0);\n"
"border-style:solid;\n"
"border-width:1px;\n"
"padding : 2px 12px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"	border-color: rgb(97, 97, 97);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QTabBar::tab:!selected{\n"
"	color: gray;\n"
"	background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover {\n"
"	color: white;\n"
"	background-color: rgb(97, 97, 97);\n"
"}                                          \n"
"QWidget{\n"
"	background-color: rgb(97, 97, 97);\n"
"}\n"
"QTabWidget::pane{\n"
"border-width: 1px;\n"
"border-style : solid;\n"
"border-color :rgb(97, 97, 97);\n"
"}")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout = QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setStyleSheet(u"QPushButton:hover {\n"
"	border-color: rgb(0, 0, 0);\n"
"	border-style:solid;\n"
"	border-width:1px;\n"
"	background-color: rgb(172, 172, 172);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"color:rgb(255,255,255);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"icons8-wi-fi-24.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QSize(20, 20))
        self.pushButton.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)
        self.pushButton_2.setStyleSheet(u"QPushButton:hover {\n"
"	border-color: rgb(0, 0, 0);\n"
"	border-style:solid;\n"
"	border-width:1px;\n"
"	background-color: rgb(172, 172, 172);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"color:rgb(255,255,255);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u"icons8-wi-fi-disconnected-24.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QSize(20, 20))
        self.pushButton_2.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 5)
        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy2)
        self.label_9.setMinimumSize(QSize(65, 0))
        self.label_9.setStyleSheet(u"color:rgb(255,255,255);")
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_9)

        self.lineEdit_2 = QLineEdit(self.tab)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy3)
        self.lineEdit_2.setMinimumSize(QSize(100, 0))
        self.lineEdit_2.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"border-style:solid;\n"
"border-width:1px;")

        self.horizontalLayout_7.addWidget(self.lineEdit_2)


        self.verticalLayout_10.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")
        sizePolicy2.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy2)
        self.label_8.setMinimumSize(QSize(65, 0))
        self.label_8.setStyleSheet(u"color:rgb(255,255,255);")
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_8)

        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy3.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy3)
        self.lineEdit.setMaximumSize(QSize(100, 16777215))
        self.lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"border-style:solid;\n"
"border-width:1px;")

        self.horizontalLayout_6.addWidget(self.lineEdit)


        self.verticalLayout_10.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_2.addLayout(self.verticalLayout_10)


        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        self.label_5.setMaximumSize(QSize(345, 16777215))
        self.label_5.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_5)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)
        self.label_10.setMaximumSize(QSize(1, 16777215))
        self.label_10.setStyleSheet(u"border-left-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-width:1px;")

        self.horizontalLayout.addWidget(self.label_10)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(-1, -1, -1, 3)
        self.label_20 = QLabel(self.tab)
        self.label_20.setObjectName(u"label_20")
        sizePolicy2.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy2)
        self.label_20.setMinimumSize(QSize(70, 0))
        self.label_20.setMaximumSize(QSize(70, 16777215))
        self.label_20.setStyleSheet(u"color:rgb(255,255,255);")

        self.horizontalLayout_17.addWidget(self.label_20)

        self.lineEdit_5 = QLineEdit(self.tab)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        sizePolicy1.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy1)
        self.lineEdit_5.setMinimumSize(QSize(60, 0))
        self.lineEdit_5.setMaximumSize(QSize(40, 16777215))
        self.lineEdit_5.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"border-style:solid;\n"
"border-width:1px;")

        self.horizontalLayout_17.addWidget(self.lineEdit_5)


        self.verticalLayout_15.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(-1, -1, -1, 3)
        self.label_21 = QLabel(self.tab)
        self.label_21.setObjectName(u"label_21")
        sizePolicy2.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy2)
        self.label_21.setMinimumSize(QSize(70, 0))
        self.label_21.setMaximumSize(QSize(70, 16777215))
        self.label_21.setStyleSheet(u"color:rgb(255,255,255);")

        self.horizontalLayout_15.addWidget(self.label_21)

        self.lineEdit_6 = QLineEdit(self.tab)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        sizePolicy1.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy1)
        self.lineEdit_6.setMinimumSize(QSize(60, 0))
        self.lineEdit_6.setMaximumSize(QSize(40, 16777215))
        self.lineEdit_6.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"border-style:solid;\n"
"border-width:1px;")

        self.horizontalLayout_15.addWidget(self.lineEdit_6)


        self.verticalLayout_15.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_22 = QLabel(self.tab)
        self.label_22.setObjectName(u"label_22")
        sizePolicy2.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy2)
        self.label_22.setMinimumSize(QSize(70, 0))
        self.label_22.setMaximumSize(QSize(70, 16777215))
        self.label_22.setStyleSheet(u"color:rgb(255,255,255);")

        self.horizontalLayout_16.addWidget(self.label_22)

        self.comboBox = QComboBox(self.tab)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy1.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy1)
        self.comboBox.setMinimumSize(QSize(60, 0))
        self.comboBox.setMaximumSize(QSize(40, 16777215))
        self.comboBox.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_16.addWidget(self.comboBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_16)


        self.horizontalLayout_14.addLayout(self.verticalLayout_15)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")

        self.verticalLayout_16.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(-1, -1, -1, 3)
        self.label_23 = QLabel(self.tab)
        self.label_23.setObjectName(u"label_23")
        sizePolicy2.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy2)
        self.label_23.setMinimumSize(QSize(70, 0))
        self.label_23.setMaximumSize(QSize(70, 16777215))
        self.label_23.setStyleSheet(u"color:rgb(255,255,255);")

        self.horizontalLayout_18.addWidget(self.label_23)

        self.comboBox_2 = QComboBox(self.tab)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy3.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy3)
        self.comboBox_2.setMinimumSize(QSize(60, 0))
        self.comboBox_2.setMaximumSize(QSize(40, 16777215))
        self.comboBox_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_18.addWidget(self.comboBox_2)


        self.verticalLayout_16.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")

        self.verticalLayout_16.addLayout(self.horizontalLayout_19)


        self.horizontalLayout_14.addLayout(self.verticalLayout_16)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_14)


        self.verticalLayout_8.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)

        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")
        sizePolicy3.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy3)
        self.label_6.setMinimumSize(QSize(273, 0))
        self.label_6.setMaximumSize(QSize(120, 16777215))
        self.label_6.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_6)


        self.horizontalLayout.addLayout(self.verticalLayout_8)

        self.label_11 = QLabel(self.tab)
        self.label_11.setObjectName(u"label_11")
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)
        self.label_11.setMaximumSize(QSize(1, 16777215))
        self.label_11.setStyleSheet(u"border-left-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-width:1px;")

        self.horizontalLayout.addWidget(self.label_11)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.pushButton_6 = QPushButton(self.tab)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy1.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy1)
        self.pushButton_6.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_6.setBaseSize(QSize(0, 0))
        self.pushButton_6.setStyleSheet(u"QPushButton:hover {\n"
"	border-color: rgb(0, 0, 0);\n"
"	border-style:solid;\n"
"	border-width:1px;\n"
"	background-color: rgb(172, 172, 172);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"color:rgb(255,255,255);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u"icons8-play-64.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_6.setIcon(icon3)
        self.pushButton_6.setIconSize(QSize(20, 20))
        self.pushButton_6.setFlat(True)

        self.horizontalLayout_13.addWidget(self.pushButton_6)

        self.pushButton_5 = QPushButton(self.tab)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy1.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy1)
        self.pushButton_5.setStyleSheet(u"QPushButton:hover {\n"
"	border-color: rgb(0, 0, 0);\n"
"	border-style:solid;\n"
"	border-width:1px;\n"
"	background-color: rgb(172, 172, 172);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"color:rgb(255,255,255);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u"icons8-pause-squared-50.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_5.setIcon(icon4)
        self.pushButton_5.setIconSize(QSize(20, 20))
        self.pushButton_5.setFlat(True)

        self.horizontalLayout_13.addWidget(self.pushButton_5)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_13)


        self.verticalLayout_9.addLayout(self.horizontalLayout_4)

        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")
        sizePolicy3.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy3)
        self.label_7.setMinimumSize(QSize(155, 0))
        self.label_7.setMaximumSize(QSize(155, 16777215))
        self.label_7.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_7)


        self.horizontalLayout.addLayout(self.verticalLayout_9)

        self.label_19 = QLabel(self.tab)
        self.label_19.setObjectName(u"label_19")
        sizePolicy1.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy1)
        self.label_19.setMaximumSize(QSize(1, 16777215))
        self.label_19.setStyleSheet(u"border-left-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-width:1px;")

        self.horizontalLayout.addWidget(self.label_19)

        self.horizontalSpacer = QSpacerItem(400, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_10 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.pushButton_3 = QPushButton(self.tab_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy4)
        self.pushButton_3.setStyleSheet(u"QPushButton:hover {\n"
"	border-color: rgb(0, 0, 0);\n"
"	border-style:solid;\n"
"	border-width:1px;\n"
"	background-color: rgb(172, 172, 172);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"color:rgb(255,255,255);\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u"../../Downloads/icons8-opened-folder-50.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon5)
        self.pushButton_3.setFlat(True)

        self.verticalLayout_13.addWidget(self.pushButton_3)

        self.label_40 = QLabel(self.tab_2)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_40.setAlignment(Qt.AlignCenter)

        self.verticalLayout_13.addWidget(self.label_40)


        self.verticalLayout_17.addLayout(self.verticalLayout_13)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_16 = QLabel(self.tab_2)
        self.label_16.setObjectName(u"label_16")
        sizePolicy2.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy2)
        self.label_16.setMaximumSize(QSize(100, 16777215))
        self.label_16.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_16.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.label_16)


        self.verticalLayout_17.addLayout(self.verticalLayout_14)


        self.horizontalLayout_10.addLayout(self.verticalLayout_17)

        self.label_17 = QLabel(self.tab_2)
        self.label_17.setObjectName(u"label_17")
        sizePolicy2.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy2)
        self.label_17.setMaximumSize(QSize(1, 16777215))
        self.label_17.setStyleSheet(u"border-left-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-width:1px;")

        self.horizontalLayout_10.addWidget(self.label_17)

        self.horizontalSpacer_3 = QSpacerItem(980, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_3)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.horizontalLayout_5 = QHBoxLayout(self.tab_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_13 = QLabel(self.tab_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_13.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_13)

        self.comboBox_3 = QComboBox(self.tab_3)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_8.addWidget(self.comboBox_3)


        self.verticalLayout_11.addLayout(self.horizontalLayout_8)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_3)

        self.label_12 = QLabel(self.tab_3)
        self.label_12.setObjectName(u"label_12")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy5)
        self.label_12.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_12.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.label_12)


        self.horizontalLayout_5.addLayout(self.verticalLayout_11)

        self.label_14 = QLabel(self.tab_3)
        self.label_14.setObjectName(u"label_14")
        sizePolicy2.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy2)
        self.label_14.setMaximumSize(QSize(1, 16777215))
        self.label_14.setStyleSheet(u"border-left-color: rgb(255, 255, 255);\n"
"border-style:solid;\n"
"border-width:1px;")
        self.label_14.setLineWidth(0)

        self.horizontalLayout_5.addWidget(self.label_14)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        self.splitter_3 = QSplitter(self.centralwidget)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.splitter_3.setOpaqueResize(False)
        self.splitter = QSplitter(self.splitter_3)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.setOpaqueResize(False)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy5.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy5)
        self.label.setMinimumSize(QSize(0, 20))
        self.label.setMaximumSize(QSize(16777215, 20))
        self.label.setStyleSheet(u"background-color: rgb(97, 97, 97);\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout.addWidget(self.label)

        self.widget = PlotWidget(self.verticalLayoutWidget)
        self.widget.setObjectName(u"widget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy6)
        self.widget.setMinimumSize(QSize(0, 40))
        self.widget.setMaximumSize(QSize(16777215, 16777215))
        self.widget.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        self.verticalLayout.addWidget(self.widget)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy5.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy5)
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setMaximumSize(QSize(16777215, 16777215))
        self.label_2.setStyleSheet(u"background-color: rgb(97, 97, 97);\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.label_2)

        self.widget_2 = QWidget(self.verticalLayoutWidget_2)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy6.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy6)
        self.widget_2.setMinimumSize(QSize(600, 400))
        self.widget_2.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.verticalLayout_12 = QVBoxLayout(self.widget_2)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_15 = QLabel(self.widget_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setScaledContents(True)

        self.verticalLayout_12.addWidget(self.label_15)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_4)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setSpacing(1)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.pushButton_11 = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setStyleSheet(u"QPushButton:hover {\n"
"	border-color: rgb(0, 0, 0);\n"
"	border-style:solid;\n"
"	border-width:1px;\n"
"	background-color: rgb(172, 172, 172);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"color:rgb(255,255,255);\n"
"}")
        self.pushButton_11.setIcon(icon3)
        self.pushButton_11.setFlat(True)

        self.horizontalLayout_36.addWidget(self.pushButton_11)

        self.pushButton_12 = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setStyleSheet(u"QPushButton:hover {\n"
"	border-color: rgb(0, 0, 0);\n"
"	border-style:solid;\n"
"	border-width:1px;\n"
"	background-color: rgb(172, 172, 172);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"color:rgb(255,255,255);\n"
"}")
        self.pushButton_12.setIcon(icon4)
        self.pushButton_12.setFlat(True)

        self.horizontalLayout_36.addWidget(self.pushButton_12)

        self.comboBox_4 = QComboBox(self.verticalLayoutWidget_2)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_36.addWidget(self.comboBox_4)

        self.horizontalSlider = QSlider(self.verticalLayoutWidget_2)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setStyleSheet(u"QSlider::groove:horizontal {\n"
"    border: 1px solid #565a5e;\n"
"    height: 10px;\n"
"    background: #eee;\n"
"    margin: 0px;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background: blue;\n"
"    border: 1px solid #565a5e;\n"
"    width: 24px;\n"
"    height: 8px;\n"
"    border-radius: 4px;\n"
"}")
        self.horizontalSlider.setMaximum(99)
        self.horizontalSlider.setPageStep(0)
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_36.addWidget(self.horizontalSlider)

        self.label_18 = QLabel(self.verticalLayoutWidget_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_36.addWidget(self.label_18)


        self.verticalLayout_2.addLayout(self.horizontalLayout_36)

        self.splitter.addWidget(self.verticalLayoutWidget_2)
        self.splitter_3.addWidget(self.splitter)
        self.splitter_2 = QSplitter(self.splitter_3)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.verticalLayoutWidget_3 = QWidget(self.splitter_2)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget_3)
        self.label_3.setObjectName(u"label_3")
        sizePolicy5.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy5)
        self.label_3.setMinimumSize(QSize(0, 20))
        self.label_3.setMaximumSize(QSize(16777215, 20))
        self.label_3.setStyleSheet(u"QLabel{\n"
"background-color: rgb(97, 97, 97);\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"QLabel:clicked{\n"
"background-color:white;\n"
"}")

        self.verticalLayout_3.addWidget(self.label_3)

        self.widget_3 = QWidget(self.verticalLayoutWidget_3)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy6.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy6)
        self.widget_3.setMinimumSize(QSize(150, 300))
        self.widget_3.setStyleSheet(u"border-color: rgb(255, 255, 255);\n"
"border-width: 1 px;\n"
"border-style:solid;\n"
"background-color: rgb(0, 0, 0);")

        self.verticalLayout_3.addWidget(self.widget_3)

        self.splitter_2.addWidget(self.verticalLayoutWidget_3)
        self.verticalLayoutWidget_4 = QWidget(self.splitter_2)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.verticalLayoutWidget_4)
        self.label_4.setObjectName(u"label_4")
        sizePolicy5.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy5)
        self.label_4.setMinimumSize(QSize(0, 20))
        self.label_4.setMaximumSize(QSize(16777215, 20))
        self.label_4.setStyleSheet(u"background-color:rgb(97, 97, 97);\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_4.addWidget(self.label_4)

        self.textBrowser = QTextBrowser(self.verticalLayoutWidget_4)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy6.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy6)
        self.textBrowser.setMinimumSize(QSize(0, 100))
        self.textBrowser.setStyleSheet(u"border-color: rgb(255, 255, 255);\n"
"border-width: 1 px;\n"
"border-style:solid;\n"
"color: white;\n"
"background-color: rgb(0, 0, 0);")

        self.verticalLayout_4.addWidget(self.textBrowser)

        self.splitter_2.addWidget(self.verticalLayoutWidget_4)
        self.splitter_3.addWidget(self.splitter_2)

        self.verticalLayout_5.addWidget(self.splitter_3)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        MainWindow.setCentralWidget(self.centralwidget)

        self.MessageBox = QMessageBox()

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"KW_SSS", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"CONNECT", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"DISCONNECT", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u" HW IP", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u" HW PORT", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"9090", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Connecction Control", None))
        self.label_10.setText("")
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Range[m]", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Gain", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"TVG", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Step 0", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Step 1", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Step 2", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Step 3", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Step 4", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"Step 5", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"Step 6", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"Step 7", None))

        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Pulse Width", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Step 0", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"Step 1", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"Step 2", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("MainWindow", u"Step 3", None))
        self.comboBox_2.setItemText(4, QCoreApplication.translate("MainWindow", u"Step 4", None))
        self.comboBox_2.setItemText(5, QCoreApplication.translate("MainWindow", u"Step 5", None))
        self.comboBox_2.setItemText(6, QCoreApplication.translate("MainWindow", u"Step 6", None))
        self.comboBox_2.setItemText(7, QCoreApplication.translate("MainWindow", u"Step 7", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"System Setting", None))
        self.label_11.setText("")
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Scanning Control", None))
        self.label_19.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Real Time", None))
        self.pushButton_3.setText("")
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"OPEN", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"File Mode", None))
        self.label_17.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"File Mode", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Color Set", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("MainWindow", u"Color", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("MainWindow", u"Gray", None))

        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.label_14.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Filter", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u" Signal", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u" Main", None))
        self.label_15.setText("")
        self.pushButton_11.setText("")
        self.pushButton_12.setText("")
        self.comboBox_4.setItemText(0, QCoreApplication.translate("MainWindow", u"Step1", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("MainWindow", u"Step2", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("MainWindow", u"Step3", None))

        self.label_18.setText(QCoreApplication.translate("MainWindow", u"0/100", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u" Navigation", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u" Event Log", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Gulim'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Gulim';\"><br /></p></body></html>", None))
    # retranslateUi

