#!/usr/bin/python
# coding: utf-8

import sys
from math import sin, cos
from time import sleep
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
	
	def __init__(self):
		super(MainWindow, self).__init__()
		
		self.initUI()
	
	def initUI(self):
		
		self.setWindowTitle(u'点石成金')
		self.resize(600, 600)
		self.center()
	
	def center(self):
		
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	
	def paintEvent(self, e):
		
		qp = QtGui.QPainter()
		qp.begin(self)
		self.dscj(qp)
		qp.end()
	
	def dscj(self, qp):
		
		dvn = 30
		width = self.contentsRect().width()
		height = self.contentsRect().height()
		center = (width / 2, height / 2)
		if width > height:
			min = height
		else:
			min = width
		radius = min / 3
		
		
		points = []
		pi = 3.1415926
		theta = (2 * pi) / dvn
		
		for i in range(dvn):
			q = i * theta
			a = int(center[0] + radius * cos(q))
			b = int(center[1] + radius * sin(q))
			points.append((a, b))
		
		pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
		qp.setPen(pen)
		
		color = QtGui.QColor(255, 0, 0)
		qp.setPen(color)
		
		for i in range(dvn):
			for j in range(i + 1, dvn):
				qp.drawLine(points[i][0], points[i][1], 
					    points[j][0], points[j][1],)

def main():
	
	app = QtGui.QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())
	

if __name__ == '__main__':
	main()
