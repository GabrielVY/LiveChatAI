# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(816, 529)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.keyLayout = QtWidgets.QHBoxLayout()
        self.keyLayout.setObjectName("keyLayout")
        self.apiKeyInput = QtWidgets.QLineEdit(self.centralwidget)
        self.apiKeyInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.apiKeyInput.setPlaceholderText("")
        self.apiKeyInput.setObjectName("apiKeyInput")
        self.keyLayout.addWidget(self.apiKeyInput)
        self.confirmKeyBtn = QtWidgets.QPushButton(self.centralwidget)
        self.confirmKeyBtn.setObjectName("confirmKeyBtn")
        self.keyLayout.addWidget(self.confirmKeyBtn)
        self.envUseButton = QtWidgets.QPushButton(self.centralwidget)
        self.envUseButton.setObjectName("envUseButton")
        self.keyLayout.addWidget(self.envUseButton)
        self.verticalLayout.addLayout(self.keyLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.promptLayout = QtWidgets.QVBoxLayout()
        self.promptLayout.setObjectName("promptLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.promptLayout.addWidget(self.label_2)
        self.promptInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.promptInput.setBackgroundVisible(False)
        self.promptInput.setCenterOnScroll(False)
        self.promptInput.setObjectName("promptInput")
        self.promptLayout.addWidget(self.promptInput)
        self.verticalLayout_2.addLayout(self.promptLayout)
        self.settingsLayout = QtWidgets.QVBoxLayout()
        self.settingsLayout.setObjectName("settingsLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.settingsLayout.addWidget(self.label_3)
        self.enableVoiceBox = QtWidgets.QCheckBox(self.centralwidget)
        self.enableVoiceBox.setEnabled(True)
        self.enableVoiceBox.setChecked(True)
        self.enableVoiceBox.setTristate(False)
        self.enableVoiceBox.setObjectName("enableVoiceBox")
        self.settingsLayout.addWidget(self.enableVoiceBox)
        self.enableSafetyBox = QtWidgets.QCheckBox(self.centralwidget)
        self.enableSafetyBox.setChecked(True)
        self.enableSafetyBox.setObjectName("enableSafetyBox")
        self.settingsLayout.addWidget(self.enableSafetyBox)
        self.verticalLayout_2.addLayout(self.settingsLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.startRecordButton = QtWidgets.QPushButton(self.centralwidget)
        self.startRecordButton.setEnabled(False)
        self.startRecordButton.setObjectName("startRecordButton")
        self.horizontalLayout.addWidget(self.startRecordButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 816, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "WARNING: Please note that using the Google Gemini API may result in charges."))
        self.label.setText(_translate("MainWindow", "Insert your Gemini API key below."))
        self.confirmKeyBtn.setText(_translate("MainWindow", "Confirm"))
        self.envUseButton.setText(_translate("MainWindow", "Use .env"))
        self.label_2.setText(_translate("MainWindow", "AI PROMPT"))
        self.label_3.setText(_translate("MainWindow", "Settings"))
        self.enableVoiceBox.setText(_translate("MainWindow", "Enable Voice Recording"))
        self.enableSafetyBox.setText(_translate("MainWindow", "Safe Messages"))
        self.label_5.setText(_translate("MainWindow", "After pressing \'Start Recording\' you will start sending live video and audio (If enabled) to Google Gemini."))
        self.startRecordButton.setText(_translate("MainWindow", " Start Recording"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
