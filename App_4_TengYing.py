# coding=gbk
import configparser
import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMessageBox

from TengYing.NPathCreateDialog import NPathCreateDialog

if __name__ == '__main__':
    version = '1.0.0'
    app = QApplication(sys.argv)
    try:
        icon = QIcon()
        icon.addPixmap(QPixmap('MainApp.ico'), QIcon.Normal, QIcon.Off)

        config = configparser.ConfigParser()
        if not config.read('config.ini', encoding='GBK'):
            raise Exception('INI file not found.')
        chuck1_z_offset = config.getfloat('Chuck1', 'z_offset')
        chuck1_x_offset = config.getfloat('Chuck1', 'x_offset')
        probe_length = config.getfloat('Probe', 'length')

        dialog = NPathCreateDialog(chuck1_offset=(chuck1_x_offset, chuck1_z_offset), probe_length=probe_length)
        dialog.setWindowIcon(icon)
        title = dialog.windowTitle() + f' {version}'
        dialog.setWindowTitle(title)
        dialog.show()
    except Exception as e:
        QMessageBox.critical(None, 'Error', e.__str__())
    finally:
        sys.exit(app.exec_())
