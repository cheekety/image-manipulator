import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PyQt5.QtWidgets import QShortcut
from MainWindow import Ui_MainWindow
import numpy as np
from matplotlib import pyplot as plt


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        QtGui.QWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.name = ' '

    def openfile(self):
        global img
        self.name = QtWidgets.QFileDialog.getOpenFileName(self,"Select Image")[0]
        img = cv2.imread(self.name)
        a = str(np.size(img, 0))
        b = str(np.size(img, 1))
        pixmap = QtGui.QPixmap(self.name)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap2)
        self.label_3.setText('Image Height: ' + a)
        self.label_4.setText('Image Width: ' + b)

    def save(self):
        global img
        img = cv2.imread(self.name)

        fname, fliter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', 'C:\\Users\\user\\Desktop\\', "Image Files (*.jpg)")
        if fname:
            cv2.imwrite(fname, img)
        else:
            print('Error')

    def reset(self):
        self.label_2.clear()

    def rotate(self):
        global img
        img = cv2.imread(self.name)
        rows, cols, ch = img.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
        c = cv2.warpAffine(img, M, (cols, rows))
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def translate(self):
        global img
        img = cv2.imread(self.name)
        rows, cols, ch = img.shape
        M = np.float32([[1, 0, 100], [0, 1, 50]])
        c = cv2.warpAffine(img, M, (cols, rows))
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def affinetransform(self):
        global img
        img = cv2.imread(self.name)
        rows, cols, ch = img.shape
        M = cv2.getAffineTransform(np.float32([[50, 50], [200, 50], [50, 200]]),
                                   np.float32([[10, 100], [200, 50], [100, 250]]))
        c = cv2.warpAffine(img, M, (cols, rows))
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def perspectivetransform(self):
        global img
        img = cv2.imread(self.name)
        rows, cols, ch = img.shape
        M = cv2.getPerspectiveTransform(np.float32([[56, 65], [368, 52], [28, 387], [389, 390]]),
                                        np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]]))
        c = cv2.warpPerspective(img, M, (cols, rows))
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def grid(self):
        if self.checkBox.isChecked():
            global img
            img = cv2.imread(self.name)
            width = np.size(img, 0)
            height = np.size(img, 1)
            j = int(height / 3)
            k = int(height * 2 / 3)
            w1 = int(width / 3)
            w2 = int(width * 2 / 3)
            cv2.line(img, (j, 0), (j, 5000), (0, 0, 0), 2)
            cv2.line(img, (k, 0), (k, 5000), (0, 0, 0), 2)
            cv2.line(img, (0, w1), (5000, w1), (0, 0, 0), 2)
            cv2.line(img, (0, w2), (5000, w2), (0, 0, 0), 2)
            qimg = QtGui.QImage(img, img.shape[1], img.shape[0], img.shape[1]*3, QtGui.QImage.Format_RGB888).rgbSwapped()
            pixmap = QtGui.QPixmap(qimg)
            pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
            self.label_2.setPixmap(pixmap2)
            img = pixmap2
        else:
            self.reset()

    def combo1(self):
        text = str(self.comboBox.currentText())
        if text == 'Grayscale':
            self.convert()
        elif text == 'HSV':
            self.hsv()

    def convert(self):
        global img
        img = cv2.imread(self.name)
        c = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1], QImage.Format_Grayscale8)
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def hsv(self):
        global img
        img = cv2.imread(self.name)
        c = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1]*3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def combo2(self):
        text = str(self.comboBox_2.currentText())
        if text == 'Convolution':
            self.convolution2D()
        elif text == 'Averaging':
            self.averaging_filter()
        elif text == 'Median':
            self.median_filter()
        elif text == 'Bilateral':
            self.bilateral_filter()
        elif text == 'Gaussian':
            self.gaussian_filter()

    def convolution2D(self):
        global img
        img = cv2.imread(self.name)
        kernel = np.ones((5, 5), np.float32) / 25
        c = cv2.filter2D(img, -1, kernel)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def averaging_filter(self):
        global img
        img = cv2.imread(self.name)
        c = cv2.blur(img, (5, 5))
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def median_filter(self):
        global img
        img = cv2.imread(self.name)
        c = cv2.medianBlur(img, 5)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def bilateral_filter(self):
        global img
        img = cv2.imread(self.name)
        c = cv2.bilateralFilter(img, 9, 75, 75)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def gaussian_filter(self):
        global img
        img = cv2.imread(self.name)
        c = cv2.GaussianBlur(img, (5, 5), 0)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def combo3(self):
        text = str(self.comboBox_3.currentText())
        if text == 'Binary':
            self.binary()
        elif text == 'Binary Inv':
            self.binary_inv()
        elif text == 'Trunc':
            self.trunc()
        elif text == 'Tozero':
            self.tozero()
        elif text == 'Tozero Inv':
            self.tozero_inv()

    def binary(self):
        global img
        img = cv2.imread(self.name)
        ret, c = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def binary_inv(self):
        global img
        img = cv2.imread(self.name)
        ret, c = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def trunc(self):
        global img
        img = cv2.imread(self.name)
        ret, c = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def tozero(self):
        global img
        img = cv2.imread(self.name)
        ret, c = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def tozero_inv(self):
        global img
        img = cv2.imread(self.name)
        ret, c = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def combo4(self):
        text = str(self.comboBox_4.currentText())
        if text == 'Laplacian':
            self.laplacian()
        elif text == 'SobelX':
            self.sobelx()
        elif text == 'SobelY':
            self.sobely()
        elif text == 'ROI':
            self.roi()

    def laplacian(self):
        global img
        img = cv2.imread(self.name)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_8U)
        c = cv2.cvtColor(laplacian, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def sobelx(self):
        global img
        img = cv2.imread(self.name)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=5)
        c = cv2.cvtColor(sobelx, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def sobely(self):
        global img
        img = cv2.imread(self.name)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        sobely = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=5)
        c = cv2.cvtColor(sobely, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2

    def roi(self):
        global img
        img = cv2.imread(self.name)
        r = cv2.selectROI("ROI", img)
        imgCrop = img[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])]
        c = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(c, c.shape[1], c.shape[0], c.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap(qimg)
        pixmap2 = pixmap.scaled(451, 471, QtCore.Qt.KeepAspectRatio)
        self.label_2.setPixmap(pixmap2)
        img = pixmap2


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())