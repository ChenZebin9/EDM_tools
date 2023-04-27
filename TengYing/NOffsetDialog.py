# coding=gbk
from PyQt5.QtWidgets import QDialog, QLineEdit, QMessageBox

from TengYing.ElectrodeOffsetDialog import Ui_Dialog
from TengYing.PosTransformer import Electrode, SmallOffset


class NOffsetDialog(QDialog, Ui_Dialog):

    def __init__(self, parent, electrode, chuck=None, probe_length=0.0, small_offset=None, mode=0):
        """
        偏置值修改对话框
        :param parent:
        :param electrode:
        :param mode: 0 -> 电极偏置值；1 -> 卡盘偏置值； 2 -> 微调偏置值
        """
        self.__parent = parent
        self.__mode = mode
        self.__el: Electrode = electrode
        self.__chuck: list = chuck
        self.__probe_length = probe_length
        self.__small_offset: SmallOffset = small_offset
        super(NOffsetDialog, self).__init__(parent=parent)
        self.__x_offset_lineEdit = QLineEdit()
        self.__y_offset_lineEdit = QLineEdit()
        self.__z_offset_lineEdit = QLineEdit()
        self.__b_offset_lineEdit = QLineEdit()
        self.__probe_length_lineEdit = QLineEdit()
        self.__setup_ui()

    def __setup_ui(self):
        super(NOffsetDialog, self).setupUi(self)
        self.setLayout(self.mVLayout)
        self.dataFormLayout.addRow('X', self.__x_offset_lineEdit)
        self.dataFormLayout.addRow('Y', self.__y_offset_lineEdit)
        self.dataFormLayout.addRow('Z', self.__z_offset_lineEdit)
        self.dataFormLayout.addRow('B', self.__b_offset_lineEdit)
        if self.__mode == 0:
            self.__x_offset_lineEdit.setText(f'{self.__el.Offset[0]:.3f}')
            self.__y_offset_lineEdit.setText(f'{self.__el.Offset[1]:.3f}')
            self.__z_offset_lineEdit.setText(f'{self.__el.Offset[2]:.3f}')
            self.__b_offset_lineEdit.setEnabled(False)
            self.setWindowTitle(f'{self.__el.ElName} 偏置值')
        elif self.__mode == 1:
            self.__x_offset_lineEdit.setText(f'{self.__chuck[0]:.3f}')
            self.__y_offset_lineEdit.setEnabled(False)
            self.__z_offset_lineEdit.setText(f'{self.__chuck[1]:.3f}')
            self.__b_offset_lineEdit.setEnabled(False)
            self.dataFormLayout.addRow('探针长度', self.__probe_length_lineEdit)
            self.__probe_length_lineEdit.setText(f'{self.__probe_length:.3f}')
            self.setWindowTitle('卡盘的偏置值 & 探针')
        elif self.__mode == 2:
            self.__x_offset_lineEdit.setText(f'{self.__small_offset.X:.3f}')
            self.__y_offset_lineEdit.setText(f'{self.__small_offset.Y:.3f}')
            self.__z_offset_lineEdit.setText(f'{self.__small_offset.Z:.3f}')
            self.__b_offset_lineEdit.setText(f'{self.__small_offset.B:.3f}')
            self.setWindowTitle('路径微小调整')
        self.setFixedWidth(200)
        self.setFixedHeight(160)

    def get_chuck_offset(self):
        """
        获取机床卡盘的偏置值
        :return:
        """
        return self.__chuck, self.__probe_length

    def accept(self) -> None:
        try:
            if self.__mode == 0:
                x = float(self.__x_offset_lineEdit.text())
                y = float(self.__y_offset_lineEdit.text())
                z = float(self.__z_offset_lineEdit.text())
                self.__el.Offset = [x, y, z]
            elif self.__mode == 1:
                x = float(self.__x_offset_lineEdit.text())
                z = float(self.__z_offset_lineEdit.text())
                self.__chuck = [x, z]
                l = float(self.__probe_length_lineEdit.text())
                self.__probe_length = l
            elif self.__mode == 2:
                x = float(self.__x_offset_lineEdit.text())
                y = float(self.__y_offset_lineEdit.text())
                z = float(self.__z_offset_lineEdit.text())
                b = float(self.__b_offset_lineEdit.text())
                self.__small_offset.X = x
                self.__small_offset.Y = y
                self.__small_offset.Z = z
                self.__small_offset.B = b
            super(NOffsetDialog, self).accept()
        except Exception as e:
            QMessageBox.warning(self, '异常', str(e))
