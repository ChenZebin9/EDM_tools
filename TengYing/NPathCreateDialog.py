# coding=gbk
import configparser
import math
import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog, QCheckBox, QTableWidgetItem, QListWidgetItem, \
    QInputDialog

from TengYing.NOffsetDialog import NOffsetDialog
from TengYing.PathCreateDialog import Ui_Dialog
from TengYing.PosTransformer import Workpiece, Path, Electrode, SmallOffset


class NPathCreateDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None, chuck1_offset=(0.0, 0.0), probe_length=0.0):
        self.__parent = parent
        # path data list, and dict
        self.__wp_name_list = []
        self.__wp_dict = {}
        # offset list, and dict
        self.__offset_name_list = []
        self.__offset_dict = {}
        # 机床卡盘的偏置值，(x_offset, z_offset)
        self.__chuck_offset = chuck1_offset[:]
        # 探针长度
        self.__probe_length = probe_length
        # 电极列表的默认表头列表
        self.__table_default_header = ['加工顺序', '起始点', '结束点', '深度']
        # 偏置值的对应表
        self.__offset_check_box_dict = {}
        # checkbox 的锁定标志
        self.__lock_check_box_change_2 = False
        super(NPathCreateDialog, self).__init__(parent=parent)
        self.__setup_ui()

    def __setup_ui(self):
        super(NPathCreateDialog, self).setupUi(self)
        self.setLayout(self.mVerticalLayout)
        self.setMinimumWidth(600)

        self.elTableWidget.setColumnCount(len(self.__table_default_header))
        self.elTableWidget.setHorizontalHeaderLabels(self.__table_default_header)

        self.__first_check_box_dict = {}

        # handler methods
        self.selectPathFileButton.clicked.connect(self.__select_file)
        self.selectNcPrgButton.clicked.connect(self.__select_file)
        self.editElOffsetPushButton.clicked.connect(self.__edit_el_offset)
        self.chuckOffsetPushButton.clicked.connect(self.__edit_chuck_offset)
        self.generatePushButton.clicked.connect(self.__generate)
        self.addOffsetButton.clicked.connect(self.__add_small_offset)
        self.editOffsetButton.clicked.connect(self.__edit_small_offset)
        self.removeOffsetButton.clicked.connect(self.__remove_small_offset)

        self.chuckOffsetPushButton.setText(self.__machining_data_str())

    def __machining_data_str(self):
        return f'卡盘偏置值：X{self.__chuck_offset[0]:.3f}, Z{self.__chuck_offset[1]:.3f}\n探针长度：{self.__probe_length:.3f}'

    def __add_small_offset(self):
        """
        添加一个电极的微小偏移
        :return:
        """
        txt, ok = QInputDialog.getText(self, '输入', '代号')
        if not ok or len(txt) < 1:
            return
        if txt in self.__offset_name_list:
            QMessageBox.warning(self, '', '代号已存在')
            return
        neu_offset = SmallOffset(txt)
        self.__offset_name_list.append(txt)
        self.__offset_dict[txt] = neu_offset

        list_item = QListWidgetItem(neu_offset.__str__())
        list_item.setData(Qt.UserRole, neu_offset)
        self.offsetListWidget.addItem(list_item)

        if len(self.__offset_name_list) < 1:
            return
        header = self.__table_default_header[:]
        header.extend(self.__offset_name_list)
        self.elTableWidget.setColumnCount(len(header))
        self.elTableWidget.setHorizontalHeaderLabels(header)
        column_index = len(header) - 1
        for r in range(0, self.elTableWidget.rowCount()):
            check_box = QCheckBox()
            self.elTableWidget.setCellWidget(r, column_index, check_box)
            check_box.stateChanged.connect(self.__offset_check_box_changed)
            self.__offset_check_box_dict[check_box] = (r, column_index)
        self.elTableWidget.resizeColumnsToContents()
        self.elTableWidget.resizeRowsToContents()

    # noinspection PyTypeChecker
    def __offset_check_box_changed(self, state):
        t: QCheckBox = self.sender()
        row_index, column_index = self.__offset_check_box_dict[t]
        offset_name = self.__offset_name_list[column_index - len(self.__table_default_header)]
        offset_obj = self.__offset_dict[offset_name]
        path_obj: Path = (self.elTableWidget.item(row_index, 0)).data(Qt.UserRole)
        if state == 0 and not self.__lock_check_box_change_2:
            path_obj.target_point_offset = None
            self.__lock_check_box_change_2 = False
        elif state == 2:
            if path_obj.target_point_offset is not None:
                QMessageBox.warning(self, '', '该路径已设定了偏置值。')
                self.__lock_check_box_change_2 = True
                t.setChecked(False)
                return
            path_obj.target_point_offset = offset_obj

    def __edit_small_offset(self):
        """
        编辑一个电极的微小偏移
        :return:
        """
        item = self.offsetListWidget.currentItem()
        if item is None:
            return
        offset_obj: SmallOffset = item.data(Qt.UserRole)
        dialog = NOffsetDialog(self, electrode=None, chuck=None, small_offset=offset_obj, mode=2)
        dialog.exec_()
        item.setText(offset_obj.__str__())

    def __remove_small_offset(self):
        """
        删除一个电极的微小偏移
        :return:
        """
        pass

    def __generate(self):
        """
        生成新的NC程序。对于偏置值的规定：
        1、所有偏置值，均是在机床的机械坐标系下的数值！
        :return:
        """
        try:
            # 更新加工顺序
            for r in range(0, self.elTableWidget.rowCount()):
                first_item = self.elTableWidget.item(r, 0)
                m_order = int(first_item.text())
                the_path:Path = first_item.data(Qt.UserRole)
                the_path.machining_order = m_order

            the_el_general_offset = [0.0, 0.0, 0.0]
            wp_name = self.__wp_name_list[0]
            wp_obj = self.__wp_dict[wp_name]
            el_obj: Electrode = wp_obj.ElList[0]
            the_el_general_offset[0] = self.__chuck_offset[0] + el_obj.Offset[0]
            the_el_general_offset[1] = el_obj.Offset[1]
            the_el_general_offset[2] = self.__chuck_offset[1] + el_obj.Offset[2]

            # 根据排列顺序，对各个路径进行排序
            el_obj.Paths.sort(reverse=True)

            output_path = []
            for p in el_obj.Paths:
                pp: Path = p
                if pp.machining_order < 1:
                    continue
                neu_offset = the_el_general_offset[:]
                s_p, e_p, a = pp.do_small_offset()
                if pp.target_point_offset is not None:
                    o: SmallOffset = pp.target_point_offset
                    neu_offset[0] -= o.X
                    neu_offset[1] -= o.Y
                    neu_offset[2] -= o.Z
                # print(math.sqrt((s_p[0]-e_p[0])**2+(s_p[1]-e_p[1])**2+(s_p[2]-e_p[2])**2))
                neu_s_pt = list(NPathCreateDialog.__neu_pt(s_p, a, neu_offset))
                neu_e_pt = list(NPathCreateDialog.__neu_pt(e_p, a, neu_offset))
                neu_s_pt.append(a)
                neu_e_pt.append(a)
                # calculate about offsets from chuck1 and probe
                neu_s_pt[0] += self.__chuck_offset[0]
                neu_e_pt[0] += self.__chuck_offset[0]
                zt = self.__chuck_offset[1] - self.__probe_length
                neu_s_pt[2] += zt
                neu_e_pt[2] += zt
                output_path.append([neu_s_pt, neu_e_pt])

            tt = self.ncPrgFilelineEdit.text()
            nc_file_short_name = os.path.basename(tt)
            nc_folder = os.path.dirname(tt)
            neu_file_name = os.path.join(nc_folder, f'{wp_name}_{el_obj.ElName}_{nc_file_short_name}')

            original_pre_lines = []
            original_post_lines = []
            with open(tt, 'r') as f:
                all_lines = f.readlines()
                f.close()
            is_pre = True
            for l in all_lines:
                if l.startswith('##'):
                    is_pre = False
                    continue
                if is_pre:
                    original_pre_lines.append(l)
                else:
                    original_post_lines.append(l)

            with open(neu_file_name, 'w') as f:
                f.writelines(original_pre_lines)
                for p in output_path:
                    h661 = NPathCreateDialog.__get_format_number(p[0][0])
                    h662 = NPathCreateDialog.__get_format_number(p[0][1])
                    h663 = NPathCreateDialog.__get_format_number(p[0][2])
                    h664 = NPathCreateDialog.__get_format_number(p[0][3])
                    h771 = NPathCreateDialog.__get_format_number(p[1][0])
                    h772 = NPathCreateDialog.__get_format_number(p[1][1])
                    h773 = NPathCreateDialog.__get_format_number(p[1][2])
                    h774 = NPathCreateDialog.__get_format_number(p[1][3])
                    p_line = f'H661 = {h661} H662 = {h662} H663 = {h663} H664 = {h664} H771 = {h771} H772 = {h772} H773 = {h773} H774 = {h774};\n'
                    c_line = r'/G054 M98P0000;' + '\n'
                    f.writelines((p_line, c_line))
                f.writelines(original_post_lines)
                f.close()

            QMessageBox.information(self, '', '生成成功。')
        except Exception as e:
            QMessageBox.warning(self, '生成时异常', str(e))

    @staticmethod
    def __get_format_number(n) -> str:
        """
        获取规范的数值表达式，例如：+003.456。
        :param n:
        :return:
        """
        t = '{0:+.3f}'.format(n)
        i = t.find('.')
        if i == 2:
            return t[0] + '00' + t[1:]
        elif i == 3:
            return t[0] + '0' + t[1:]
        else:
            return t

    @staticmethod
    def __pt_offset(af, offset) -> tuple:
        """
        calculate to new offset by rotate angle and offset
        :param af: angle
        :param offset: point offset
        :return:
        """
        a = af / 180.0 * math.pi
        x = offset[0]
        z = offset[2]
        x_n = z * math.sin(a) + x * math.cos(a)
        z_n = z * math.cos(a) - x * math.sin(a)
        return x_n, offset[1], z_n

    @staticmethod
    def __neu_pt(pt, af, offset) -> tuple:
        """
        get new point in WCS
        :param pt:
        :param af:
        :param offset:
        :return:
        """
        neu_offset = NPathCreateDialog.__pt_offset(af, offset)
        x = pt[0] - neu_offset[0]
        y = pt[1] - neu_offset[1]
        z = pt[2] - neu_offset[2]
        return x, y, z

    def __edit_el_offset(self):
        item = self.elListWidget.currentItem()
        if item is None:
            return
        el_obj = item.data(Qt.UserRole)
        dialog = NOffsetDialog(self, el_obj)
        dialog.exec_()
        item.setText(el_obj.__str__())

    def __edit_chuck_offset(self):
        dialog = NOffsetDialog(self, None, chuck=self.__chuck_offset, mode=1, probe_length=self.__probe_length)
        dialog.exec_()
        self.__chuck_offset, self.__probe_length = dialog.get_chuck_offset()
        self.chuckOffsetPushButton.setText(self.__machining_data_str())
        config = configparser.ConfigParser()
        config['Chuck1'] = {
            'z_offset': f'{self.__chuck_offset[1]:.3f}',
            'x_offset': f'{self.__chuck_offset[0]:.3f}'
        }
        config['Probe'] = {
            'length': f'{self.__probe_length:.3f}'
        }
        with open('config.ini', 'w') as config_file:
            config.write(config_file)

    def reject(self) -> bool:
        resp = QMessageBox.question(self, '', '确定要退出？', defaultButton=QMessageBox.No)
        if resp == QMessageBox.No:
            return False
        super(NPathCreateDialog, self).reject()

    def __select_file(self):
        if self.sender() is self.selectPathFileButton:
            file_name, file_type = QFileDialog.getOpenFileName(self, '选择路径文件', '', 'Path Files(*.dat)')
            if file_name is not None and len(file_name) > 0:
                # do clearing
                self.elListWidget.clear()
                self.offsetListWidget.clear()
                self.elTableWidget.clear()
                self.__offset_name_list.clear()
                self.__offset_dict.clear()
                self.__offset_check_box_dict.clear()
                self.__wp_name_list.clear()
                self.__wp_dict.clear()
                self.__analysis_path_file(file_name)
                self.pathFileLineEdit.setText(file_name)
                self.__display_table_list()
        elif self.sender() is self.selectNcPrgButton:
            file_name, file_type = QFileDialog.getOpenFileName(self, '选择NC文件', '', 'Nc Files(*.nc)')
            if file_name is not None and len(file_name) > 0:
                self.ncPrgFilelineEdit.setText(file_name)

    def __analysis_path_file(self, file_name: str):
        all_lines = []
        with open(file_name) as f:
            all_lines.extend(f.readlines())
            f.close()
        temp = []
        for l in all_lines:
            ll = l.strip()
            if len(ll) > 1:
                temp.append(ll)
        all_lines.clear()
        all_lines.extend(temp)
        line_count = len(all_lines)
        i = 0
        el_index = 1
        while i < line_count:
            l = all_lines[i]
            index1 = l.find(':')
            wp_name = l[index1 + 1:-1]
            i += 1
            l = all_lines[i]
            index1 = l.find(':')
            el_name = l[index1 + 1:-1]
            i += 1
            l = all_lines[i]
            tt = l.split(';')
            s_pt = [0.0, 0.0, 0.0, 0.0]
            e_pt = [0.0, 0.0, 0.0, 0.0]
            for t in tt:
                if t.startswith('SX='):
                    s_pt[0] = float(t[3:])
                elif t.startswith('SY='):
                    s_pt[1] = float(t[3:])
                elif t.startswith('SZ='):
                    s_pt[2] = float(t[3:])
                elif t.startswith('SC='):
                    s_pt[3] = float(t[3:])
                elif t.startswith('DX='):
                    e_pt[0] = float(t[3:])
                elif t.startswith('DY='):
                    e_pt[1] = float(t[3:])
                elif t.startswith('DZ='):
                    e_pt[2] = float(t[3:])
                elif t.startswith('DC='):
                    e_pt[3] = float(t[3:])
            i += 2
            if wp_name in self.__wp_name_list:
                wp_obj: Workpiece = self.__wp_dict[wp_name]
                try:
                    ii = wp_obj.ElList.index(Electrode(el_name))
                    el_obj = wp_obj.ElList[ii]
                    el_obj.add_path(s_pt, e_pt, el_index)
                except ValueError:
                    el_obj = Electrode(el_name)
                    el_obj.add_path(s_pt, e_pt, el_index)
                    wp_obj.ElList.append(el_obj)
                el_index += 1
            else:
                wp_obj = Workpiece(wp_name)
                el_obj = Electrode(el_name)
                wp_obj.ElList.append(el_obj)
                el_obj.add_path(s_pt, e_pt, el_index)
                el_index += 1
                self.__wp_name_list.append(wp_name)
                self.__wp_dict[wp_name] = wp_obj

    def __display_table_list(self):
        self.elTableWidget.setColumnCount(len(self.__table_default_header))
        self.elTableWidget.setHorizontalHeaderLabels(self.__table_default_header)

        wp_obj: Workpiece = self.__wp_dict[self.__wp_name_list[0]]
        el_obj = wp_obj.ElList[0]
        all_paths = el_obj.Paths

        self.elListWidget.clear()
        el_item = QListWidgetItem(el_obj.__str__())
        el_item.setData(Qt.UserRole, el_obj)
        self.elListWidget.addItem(el_item)

        self.elTableWidget.setRowCount(0)
        row_index = 0
        self.elTableWidget.setRowCount(len(all_paths))
        for p in all_paths:
            p_obj: Path = p
            data_s = p_obj.to_table_display()
            machining_order_item = QTableWidgetItem(f'{data_s[1]}')
            machining_order_item.setData(Qt.UserRole, p_obj)
            self.elTableWidget.setItem(row_index, 0, machining_order_item)
            item2 = QTableWidgetItem(data_s[2])
            item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.elTableWidget.setItem(row_index, 1, item2)
            item3 = QTableWidgetItem(data_s[3])
            item3.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.elTableWidget.setItem(row_index, 2, item3)
            item4 = QTableWidgetItem(data_s[4])
            item4.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.elTableWidget.setItem(row_index, 3, item4)
            row_index += 1
        self.elTableWidget.resizeColumnsToContents()
        self.elTableWidget.resizeRowsToContents()
