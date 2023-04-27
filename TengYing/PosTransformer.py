# coding=gbk
import math

import numpy as np


class Workpiece:

    def __init__(self, wp_name: str):
        """
        代表一个工件
        :param wp_name:
        """
        self.WpName = wp_name
        self.ElList = []

    def add_electrode(self, el_name):
        self.ElList.append(Electrode(el_name))

    def __eq__(self, other):
        return self.WpName == other.WpName


class Electrode:

    def __init__(self, el_name: str):
        """
        代表一个电极，具有以下数据：名称，偏移值，加工路径列表
        :param el_name:
        """
        self.ElName = el_name
        self.Offset = [0.0, 0.0, 0.0]
        self.Paths = []

    def __eq__(self, other):
        return self.ElName == other.ElName

    def add_path(self, start_pt, end_pt, nr):
        self.Paths.append(Path(start_pt, end_pt, nr))

    def __str__(self):
        return self.ElName + f' (X{self.Offset[0]:.3f},Y{self.Offset[1]:.3f}, Z{self.Offset[2]:.3f})'


class Path:

    def __init__(self, start_pt, end_pt, order_index):
        """
        代表一个电极在一个工件中，加工的某一个路径
        :param start_pt:
        :param end_pt:
        :param order_index:
        """
        # Vector from start point to end point
        self.vector = [end_pt[0] - start_pt[0], end_pt[1] - start_pt[1], end_pt[2] - start_pt[2]]
        self.angel = (start_pt[3] + end_pt[3]) / 2.0
        self.depth = math.sqrt(((end_pt[0] - start_pt[0]) ** 2) + ((end_pt[1] - start_pt[1]) ** 2) +
                               ((end_pt[2] - start_pt[2]) ** 2))
        self.vector[0] = self.vector[0] / self.depth
        self.vector[1] = self.vector[1] / self.depth
        self.vector[2] = self.vector[2] / self.depth
        self.start_point = start_pt[:-1]
        self.end_point = end_pt[:-1]
        # output to the nc program finally
        self.do_real_sparking = True
        # order in the segment mold
        self.position_index = order_index
        # machining order
        self.machining_order = order_index
        # small offset
        self.target_point_offset = None

    def set_end_point_offset(self, offset):
        pass

    def __gt__(self, other):
        return self.machining_order < other.machining_order

    def to_table_display(self):
        display_list = [self.position_index,
                        self.machining_order,
                        'X{0:>10.3f}\nY{1:>10.3f}\nZ{2:>10.3f}\nB{3:>10.3f}'.format(self.start_point[0],
                                                                                    self.start_point[1],
                                                                                    self.start_point[2], self.angel),
                        'X{0:>10.3f}\nY{1:>10.3f}\nZ{2:>10.3f}\nB{3:>10.3f}'.format(self.end_point[0],
                                                                                    self.end_point[1],
                                                                                    self.end_point[2], self.angel),
                        f'{self.depth:>10.3f}']
        return display_list

    def __str__(self):
        t1 = 'X{0:.3f},Y{1:.3f},Z{2:.3f},B{3:.3f}'.format(self.start_point[0], self.start_point[1], self.start_point[2],
                                                          self.angel)
        t2 = 'X{0:.3f},Y{1:.3f},Z{2:.3f},B{3:.3f}'.format(self.end_point[0], self.end_point[1], self.end_point[2],
                                                          self.angel)
        return t1 + '->' + t2

    def do_small_offset(self):
        """
        根据偏置值，计算新的点
        :return:
        """
        if self.target_point_offset is None:
            return self.start_point, self.end_point, self.angel
        else:
            the_vector = np.array(self.vector)
            the_vector = -1.0 * the_vector
            if math.fabs(self.target_point_offset.B) <= 0.001:
                new_vector = the_vector
            else:
                r_matrix = Path.__rodrigues_rotation_vec_to_r(
                    np.array([0.0, self.target_point_offset.B / 180.0 * np.pi, 0.0]))
                new_vector = np.matmul(r_matrix[:3, :3], the_vector)
            spx = self.end_point[0] + self.depth * new_vector[0]
            spy = self.end_point[1] + self.depth * new_vector[1]
            spz = self.end_point[2] + self.depth * new_vector[2]
            return [spx, spy, spz], self.end_point, self.angel + self.target_point_offset.B

    @staticmethod
    def __rodrigues_rotation(r, theta):
        """
        生成旋转矩阵
        :param r:
        :param theta: 旋转角度
        :return:
        """
        r = np.array(r).reshape(3, 1)
        rx, ry, rz = r[:, 0]
        m = np.array([
            [0, -rz, ry],
            [rz, 0, -rx],
            [-ry, rx, 0]
        ])
        rr = np.eye(4)
        rr[:3, :3] = np.cos(theta) * np.eye(3) + (1 - np.cos(theta)) * r @ r.T + np.sin(theta) * m
        return rr

    @staticmethod
    def __rodrigues_rotation_vec_to_r(v):
        """
        生成旋转矢量的旋转矩阵
        :param v:
        :return:
        """
        theta = np.linalg.norm(v)
        r = np.array(v).reshape(3, 1) / theta
        return Path.__rodrigues_rotation(r, theta)


class SmallOffset:

    def __init__(self, name):
        """
        代表电极在某一加工路径的轻微调整
        :param name:
        """
        self.name = name
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.B = 0.0

    def __str__(self):
        return f'{self.name} X{self.X:.3f},Y{self.Y:.3f},Z{self.Z:.3f},B{self.B:.3f}'
