#!/uer/bin/python
# -*- coding: utf-8 -*-

import sys
from math import sin, cos, atan, sqrt
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
	
	def __init__(self):
		super(MainWindow, self).__init__()
		
		self.initUI()
	
	def initUI(self):
		
		self.setWindowTitle(u'上机实验五')
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
		self.five(qp)
		qp.end()
	
	def getBaseP(self, startP, endP, n, i):
		
		return (((n - i) * startP[0] + i * endP[0]) / n,
				((n - i) * startP[1] + i * endP[1]) / n, )
	
	def getAngle(self, startP, endP):
		
		PI = 3.141592653
		if endP[1] == startP[1]:
			if endP[0] > startP[0]:
				return PI / 2
			else:
				return 3 * PI / 2
		if (endP[1] - startP[1]) > 0:
			return atan((startP[0] - endP[0]) / (endP[1] - startP[1])) + PI
		else:
			return atan((startP[0] - endP[0]) / (endP[1] - startP[1]))
	
	def getP(self, startP, endP, baseP, len):
		
		angle = self.getAngle(startP, endP)
		return (baseP[0] + len * cos(angle), baseP[1] + len * sin(angle))
	
	def drawTriangle(self, qp, radius, n, points):
		
		ps = []
		high = sqrt(3) / 8 * radius
		for i in range(3):
			p = []
			middlePoint = self.getP(points[(i + 1) % 3], points[i],
				self.getBaseP(points[(i + 1) % 3], points[i], 2, 1),
				high )
			high_row = high / 3
			high_row_n = 0
			if n % 2 == 0:
				startP = points[i]
				endP = middlePoint
			else:
				startP = middlePoint
				endP = points[(i + 1) % 3]
			p.append(startP)
			for j in range(1, 9):
				if j <= 4:
					high_row_n += 1.0 / (2 + j) * high_row
				point = self.getP(startP, endP,
					self.getBaseP(startP, endP, 9, j),
					high_row_n )
				if j > 4:
					high_row_n -= 1.0 / (2 + (9 - j)) * high_row
				p.append(point)
			p.append(endP)
			ps.append(p)
		pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
		qp.setPen(pen)
		color = QtGui.QColor(128, 0, 128)
		qp.setPen(color)
		for i in range(3):
			for j in range(10):
				startP = ps[i][j]
				endP = ps[(i + 1) % 3][j]
				if j != 9:
					qp.drawLine(startP[0], startP[1],
						ps[i][j + 1][0], ps[i][j + 1][1] )
					qp.drawLine(endP[0], endP[1],
						ps[(i + 1) % 3][j + 1][0], ps[(i + 1) % 3][j + 1][1] )
				qp.drawLine(startP[0], startP[1], endP[0], endP[1])
		
	
	def five(self, qp):
		
		width = self.contentsRect().width()
		height = self.contentsRect().height()
		center = (width / 2, height / 2)
		if width > height:
			min = height
		else:
			min = width
		radius = float(min) / 3
		keyPoints = [
			(center[0] - radius, center[1]),
			(center[0] - radius / 2, center[1] - radius * sqrt(3) / 2),
			(center[0] + radius / 2, center[1] - radius * sqrt(3) / 2),
			(center[0] + radius, center[1]),
			(center[0] + radius / 2, center[1] + radius * sqrt(3) / 2),
			(center[0] - radius / 2, center[1] + radius * sqrt(3) / 2),
		]
		for i in range(6):
			self.drawTriangle(qp, radius, i,
				[keyPoints[i], center, keyPoints[(i + 1) % 6]] )
	
def main():
	
	app = QtGui.QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())
	

if __name__ == '__main__':
	main()