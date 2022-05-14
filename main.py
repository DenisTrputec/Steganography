import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5 import QtGui

from steganography import Steganography


# Load ui files
uiMainWindow = "steganography.ui"
formMainWindow, baseMainWindow = uic.loadUiType(uiMainWindow)


class MainWindow(baseMainWindow, formMainWindow):
    def __init__(self):
        super(baseMainWindow, self).__init__()
        self.setupUi(self)
        self.steganography = Steganography()

        self.pushButton_hide_source.clicked.connect(self.browse_hide_source)
        self.pushButton_hide_destination.clicked.connect(self.browse_hide_destination)
        self.pushButton_hide_text.clicked.connect(self.hide)
        self.pushButton_reveal_source.clicked.connect(self.browse_reveal_source)
        self.pushButton_reveal_text.clicked.connect(self.reveal)

    def browse_hide_source(self):
        img_path, _ = QFileDialog.getOpenFileName(self, "Odaberi sliku")
        self.lineEdit_hide_source.setText(img_path)
        self.label_hide_image.setPixmap(QtGui.QPixmap(img_path))

    def browse_hide_destination(self):
        # Dohvati odredišni direktorij
        dest_folder = QFileDialog.getExistingDirectory(self, "Odaberi odredišni direktorij!")

        # Uzmi ime odabrane slike bez putanje i ekstenzije
        source_file = os.path.splitext(self.lineEdit_hide_source.text())[0]
        self.lineEdit_hide_destination.setText(os.path.join(dest_folder, source_file + "_s_tajnom.png"))

    def browse_reveal_source(self):
        img_path, _ = QFileDialog.getOpenFileName(self, "Odaberi sliku")
        self.lineEdit_reveal_source.setText(img_path)
        self.label_reveal_image.setPixmap(QtGui.QPixmap(img_path))

    def hide(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Obavijest")
        try:
            self.steganography.hide(self.lineEdit_hide_text.text(),
                                    self.lineEdit_hide_source.text(),
                                    self.lineEdit_hide_destination.text())
            message_box.setText("Uspješno je kreirana slika sa skrivenom porukom!")
        except Exception as e:
            message_box.setText("Dogodio se problem: " + e.args[0])
        finally:
            message_box.exec_()

    def reveal(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Obavijest")
        try:
            text = self.steganography.reveal(self.lineEdit_reveal_source.text())
            self.lineEdit_reveal_text.setText(text if text is not None else "")
            message_box.setText("Uspješno je pročitana skrivena poruka sa slike!")
        except Exception as e:
            message_box.setText("Dogodio se problem: " + e.args[0])
        finally:
            message_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

