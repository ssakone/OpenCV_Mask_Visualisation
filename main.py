from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import cv2
import numpy as np
from threading import Thread
import qimage2ndarray

class QVSlider(QFrame):
	def __init__(self):
		QFrame.__init__(self)
		row = QHBoxLayout()
		self.sl = QSlider()
		self.label = QLabel()
		row.addWidget(self.sl)
		row.addWidget(self.label)
		self.sl.valueChanged.connect(lambda: self.label.setText(str(self.sl.value())))
		self.setLayout(row)
	def value(self):
		return self.sl.value()
	def setMaximum(self, value):
		self.sl.setMaximum(value)
	def setValue(self, value):
		self.sl.setValue(value)
	def setOrientation(self, orient):
		self.sl.setOrientation(orient)
class Widget(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.mask = QLabel()
		self.masked = QLabel()
		self.maskAplly = QLabel()
		self.masked.setMaximumHeight(250)
		self.mask.setMaximumHeight(250)
		self.maskAplly.setMaximumHeight(250)
		self.control = QFrame()
		self.control.setMinimumWidth(250)
		self.control.setMaximumWidth(250)

		frameCol = QVBoxLayout()
		self.h_min = QVSlider();self.h_min.setMaximum(179);self.h_min.setOrientation(Qt.Horizontal);self.h_min.setValue(0)
		self.h_max = QVSlider();self.h_max.setMaximum(179);self.h_max.setOrientation(Qt.Horizontal);self.h_max.setValue(179)
		self.sat_min = QVSlider();self.sat_min.setMaximum(255);self.sat_min.setOrientation(Qt.Horizontal);self.sat_min.setValue(0)
		self.sat_max = QVSlider();self.sat_max.setMaximum(255);self.sat_max.setOrientation(Qt.Horizontal);self.sat_max.setValue(255)
		self.val_min = QVSlider();self.val_min.setMaximum(255);self.val_min.setOrientation(Qt.Horizontal);self.val_min.setValue(0)
		self.val_max = QVSlider();self.val_max.setMaximum(255);self.val_max.setOrientation(Qt.Horizontal);self.val_max.setValue(104)

		frameCol.addWidget(QLabel("Mask HUE CONFIGURATIOn"))
		frameCol.addWidget(QLabel("HUE MIN"))
		frameCol.addWidget(self.h_min)

		frameCol.addWidget(QLabel("HUE MAX"))
		frameCol.addWidget(self.h_max)

		frameCol.addWidget(QLabel("SAT MIN"))
		frameCol.addWidget(self.sat_min)

		frameCol.addWidget(QLabel("SAT MAX"))
		frameCol.addWidget(self.sat_max)

		frameCol.addWidget(QLabel("VAL MIN"))
		frameCol.addWidget(self.val_min)

		frameCol.addWidget(QLabel("SAT MAX"))
		frameCol.addWidget(self.val_max)

		self.control.setLayout(frameCol)
		row = QHBoxLayout()
		col = QVBoxLayout()
		row.addLayout(col)
		col.addWidget(self.mask)
		col.addWidget(self.masked)
		col.addWidget(self.maskAplly)
		row.addWidget(self.control)
		self.setLayout(row)
		self.resize(700,600)
		self.im = cv2.imread("mask.png")
		tr = Thread(target=self.getMask)
		tr.start()
	def imOperation(self):
		self.timer3 = QTimer()
		self.timer3.timeout.connect(lambda: self.getMask())
		self.timer3.start(15)
	def getImage(self):
		#print("video capturing")
		video = cv2.VideoCapture(0)
		#success, self.im = video.read()
		video = cv2.VideoCapture(0)
	def getMask(self):
		video = cv2.VideoCapture(0)
		
		while 1:
			success, self.im = video.read()
			video = cv2.VideoCapture(0)
			im = self.im
			self.mask.setPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(im)))
			#cv2.imwrite("mask.png",im)
			imHSV = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
			lower = np.array([self.h_min.value(),self.sat_min.value(),self.val_min.value()])
			upper = np.array([self.h_max.value(),self.sat_max.value(),self.val_max.value()])
			mask = cv2.inRange(imHSV,lower,upper)
			imR = cv2.bitwise_and(im,im,mask=mask)
			self.masked.setPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(mask)))
			
			imm = cv2.imread("office.jpg")
			imm = cv2.cvtColor(imm, cv2.COLOR_BGR2RGB)
			imme = cv2.resize(imm, (imR.shape[1],imR.shape[0]),interpolation = cv2.INTER_AREA)
			#imr = cv2.addWeighted(imR,0.8,imme,0.2,0)
			background = np.full(imm.shape, 255, dtype=np.uint8)
			mask = cv2.bitwise_not(mask)
			bk = cv2.bitwise_or(imme, imme, mask=mask)
			final = cv2.bitwise_or(imR, bk)
			#imr = cv2.add(imR,imme)
			self.maskAplly.setPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(final)))



application = QApplication([])
w = Widget()
w.show()
application.exec_()