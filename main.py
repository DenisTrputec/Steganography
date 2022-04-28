from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5 import QtGui
from stegano import lsb

import os
import sys


# Load ui files
uiMainWindow = "steganography.ui"
formMainWindow, baseMainWindow = uic.loadUiType(uiMainWindow)


class MainWindow(baseMainWindow, formMainWindow):
    def __init__(self):
        super(baseMainWindow, self).__init__()
        self.setupUi(self)

        self.img_path = None

        self.pushButton_hide_browse.clicked.connect(self.browse_hide)
        self.pushButton_hide.clicked.connect(self.hide)
        self.pushButton_reveal_browse.clicked.connect(self.browse_reveal)
        self.pushButton_reveal.clicked.connect(self.reveal)

    def browse_hide(self):
        self.img_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()")
        self.lineEdit_hide_browse.setText(self.img_path)
        self.label_hide_image.setPixmap(QtGui.QPixmap(self.img_path))

    def hide(self):
        secret = lsb.hide(self.img_path, self.lineEdit_hide.text())
        secret.save("secret.png")

    def browse_reveal(self):
        self.img_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()")
        self.lineEdit_reveal_browse.setText(self.img_path)
        self.label_reveal_image.setPixmap(QtGui.QPixmap(self.img_path))

    def reveal(self):
        self.lineEdit_reveal.setText(lsb.reveal(self.img_path))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

