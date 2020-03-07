# -*- coding: utf-8 -*-
"""
@Describe: some tools
@Time    : 2019/7/16 22:05
@Author  : Alone Mr.Yang
@Email   : w1053904672@163.com
@File    : Utils.py
@Software: PyCharm
"""
from PyQt5 import sip
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage
import sys
import numpy as np


class Array(np.ndarray):
    def setTag(self, tag):
        setattr(self, "__tag", tag)


def qImage2array(image, share_memory=False):
    assert isinstance(image, QImage), "img must be a QtGui.QImage object"
    assert image.format() == QImage.Format.Format_RGB32, \
        "img format must be QImage.Format.Format_RGB32, got: {}".format(image.format())
    img_size = image.size()
    buffer: sip.voidptr = image.constBits()
    depth = (image.depth() // 8)
    buffer.setsize(image.width() * image.height() * depth)
    arr = Array(shape=(img_size.height(), img_size.width(), depth),
                buffer=buffer,
                dtype=np.uint8)
    if share_memory:
        arr.setTag(image)
        return arr
    else:
        return arr.copy()


app = QApplication(sys.argv)
screen = QApplication.primaryScreen()


def get_screen(x=0, y=0, width=-1, height=-1, isQImg=False) -> (Array, QImage):
    image = screen.grabWindow(0, x, y, width, height).toImage()
    arr = qImage2array(image, share_memory=True)
    if isQImg:
        return image
    return arr


if __name__ == '__main__':
    import cv2

    # img = get_screen(100, 100, 100, 100)
    img = get_screen()
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
