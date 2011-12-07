#!/usr/bin/python
# coding: utf-8

import sys
from math import sin, cos
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
	
	def __init__(self):
		super(MainWindow, self).__init__()
		
		self.initUI()
	
	def initUI(self):
		
		self.setWindowTitle(u'奥运五环')
		self.resize(700, 400)
		self.center()
	
	def center(self):
		
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	
	def paintEvent(self, e):
		
		qp = QtGui.QPainter()
		qp.begin(self)
		self.aywh(qp)
		qp.end()
	
	def aywh(self, qp):
		
		width = self.contentsRect().width()
		height = self.contentsRect().height()
		radius = height / 4
		center = (width / 2, height / 2 - radius / 2)
		
		circles = [
			(QtCore.QPoint(center[0] - 9 * radius / 4, center[1]), 
			QtGui.QColor(0, 0, 255)),
			(QtCore.QPoint(center[0], center[1]),
			QtGui.QColor(0, 0, 0)),
			(QtCore.QPoint(center[0] + 9 * radius / 4, center[1]),
			QtGui.QColor(255, 0, 0)),
			(QtCore.QPoint(center[0] - 9 * radius / 8, center[1] + radius),
			QtGui.QColor(255, 255, 0)),
			(QtCore.QPoint(center[0] + 9 * radius / 8, center[1] + radius),
			QtGui.QColor(0, 255, 0)),
			]
		
		pen = QtGui.QPen()
		qp.setPen(pen)
		
		for item in circles:
			qp.setPen(item[1])
			for i in range(7):
				r = radius - i
				qp.drawEllipse(item[0], r, r)
	
def main():
	
	app = QtGui.QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())
	

if __name__ == '__main__':
	main()