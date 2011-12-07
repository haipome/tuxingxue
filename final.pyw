#!/uer/bin/python
# -*- coding: utf-8 -*-

import sys
from math import sin, cos, atan, sqrt
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
	
	PI = 3.141592653
	n = 1
	speed = 100
	colors = [
		QtGui.QColor(0, 0, 255),
		QtGui.QColor(255, 255, 0),
		QtGui.QColor(255, 0, 0),
		QtGui.QColor(255, 255, 255),
	]
	def __init__(self):
		
		super(MainWindow, self).__init__()
		self.timer = QtCore.QBasicTimer()
		self.timer.start(self.speed, self)
		self.initUI()
	
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			if self.n < 60:
				self.n += 1
				self.update()
			else:
				self.timer.stop()
		else:
			QtGui.QFrame.timerEvent(self, event)
	
	def initUI(self):
		
		self.setWindowTitle(u'李宁  一切皆有可能')
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
		self.final(qp)
		qp.end()
	
	def getBaseP(self, startP, endP, n, i):
		
		return (((n - i) * startP[0] + i * endP[0]) / n,
				((n - i) * startP[1] + i * endP[1]) / n, )
	
	def getAngle(self, startP, endP):
		
		if endP[1] == startP[1]:
			if endP[0] > startP[0]:
				return self.PI / 2
			else:
				return 3 * self.PI / 2
		if (endP[1] - startP[1]) > 0:
			return atan((startP[0] - endP[0]) / (endP[1] - startP[1])) + self.PI
		else:
			return atan((startP[0] - endP[0]) / (endP[1] - startP[1]))
	
	def getP(self, startP, endP, baseP, len):
		
		angle = self.getAngle(startP, endP)
		return (baseP[0] + len * cos(angle), baseP[1] + len * sin(angle))
	
	def lenOf(self, x, y):
		
		return sqrt((y[1] - x[1]) ** 2 + (y[0] - x[0]) ** 2)
	
	def absolute(self, point, center):
		
		return (center[0] + point[0], center[1] - point[1])
	
	def myLine(slef, qp, x, y):
		
		qp.drawLine(x[0], x[1], y[0], y[1])
	
	def getPs(self, x, y, high):
		
		p = []
		high_n = 0
		p.append(x)
		for i in range(1, 9):
			if i <= 4:
				high_n += 1.0 / (2 + i) * high
			p.append(self.getP(x, y, self.getBaseP(x, y, 9, i), high_n ))
			if i > 4:
				high_n -= 1.0 / (2 + (9 - i)) * high
		p.append(y)
		return p
	
	def myCurve(self, qp, x, y, high, color = False):
		
		p = self.getPs(x, y, high)
		for i in range(9):
			self.myLine(qp, p[i], p[i + 1])
			if color:
				qp.setBrush(color)
				qp.setPen(color)
				p1 = self.getBaseP(x, y, 9, i)
				p2 = self.getBaseP(x, y, 9, i + 1)
				qp.drawPolygon(
					QtCore.QPointF(p1[0], p1[1]),
					QtCore.QPointF(p2[0], p2[1]),
					QtCore.QPointF(p[i + 1][0], p[i + 1][1]),
					QtCore.QPointF(p[i][0], p[i][1]), )
				
	
	def drawLiNing(self, qp, points, color = False):
		
		if color:
			qp.setBrush(self.colors[2])
			qp.setPen(self.colors[2])
			qp.drawPolygon(
				QtCore.QPointF(points[0][0], points[0][1]),
				QtCore.QPointF(points[1][0], points[1][1]),
				QtCore.QPointF(points[2][0], points[2][1]),
				QtCore.QPointF(points[4][0], points[4][1]),
				QtCore.QPointF(points[5][0], points[5][1]), )
			qp.drawPolygon(
				QtCore.QPointF(points[2][0], points[2][1]),
				QtCore.QPointF(points[3][0], points[3][1]),
				QtCore.QPointF(points[4][0], points[4][1]), )
		self.myLine(qp, points[0], points[1])
		self.myLine(qp, points[1], points[2])
		middleP1 = self.getBaseP(points[2], points[3], 4, 3)
		middleP2 = self.getBaseP(points[3], points[4], 2, 1)
		self.myCurve(qp,  middleP1, points[2], 
			3 * self.lenOf(points[2], middleP1) / 16, color and self.colors[2] or color)
		self.myCurve(qp, middleP2, points[3],
			2 * self.lenOf(middleP2, points[3]) / 9, color and self.colors[2] or color)
		self.myCurve(qp, middleP2, points[4],
			3 * self.lenOf(middleP2, points[4]) / 16, color and self.colors[0] or color)
		self.myCurve(qp, middleP1, points[3],
			3 * self.lenOf(middleP1, points[3]) / 16, color and self.colors[0] or color)
		self.myLine(qp, points[4], points[5])
		self.myLine(qp, points[5], points[0])
	
	def drawLiNingN(self, qp, center, points, n):
		
		rad = 180.0 / self.PI
		degree = 0
		zeroP = (0, 0)
		for i in range(n):
			absolutePs = []
			degree += 6.0
			angle = degree / rad
			rate = (100 - i) / 100.0
			for point in points:
				angle_a = angle + atan(point[1] / float(point[0]))
				len = self.lenOf(zeroP, point) * rate
				absolutePs.append(
				self.absolute((len * cos(angle_a), len * sin(angle_a)), center))
			qp.setPen(self.colors[1])
			if i == 0:
				self.drawLiNing(qp, absolutePs, color = True)
			else:
				self.drawLiNing(qp, absolutePs, color = False)
	
	def final(self, qp):
		
		width = self.contentsRect().width()
		height = self.contentsRect().height()
		center = (width / 2, height / 2)
		
		pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
		qp.setBrush(self.colors[0])
		qp.drawRect(0, 0, width, height)
		qp.setPen(pen)
		qp.setPen(self.colors[3])
		self.myLine(qp, (20, center[1]), (width - 20, center[1]))
		self.myLine(qp, (center[0], 20), (center[0], center[1] + 220))
		qp.drawText(center[0] - 210, center[1] + 250, 
		u"姓名: 杨海坡    班级: 11010802    学号: 2008302699    日期: 2011.12.07")
		
		A = [(54, 88), (68, 88), (50, 52), (256, 54), (25, 20), (20, 20),]
		self.drawLiNingN(qp, center, A, self.n)
	
def main():
	
	app = QtGui.QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())
	

if __name__ == '__main__':
	main()