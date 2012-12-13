#-*- coding: utf-8 -*-
from PyQt4.QtGui import QGraphicsWidget, QColor
from PyQt4.QtCore import QObject, QEvent, pyqtSignal, QRectF, QRect, QTimeLine, QPointF


class Movel(QObject):
    def __init__(self, moveX=True, moveY=True, parent=None):
        super().__init__(parent)

        self._moveX = moveX
        self._moveY = moveY

    def setMoveXY(self, moveX, moveY):
        self._moveX = moveX
        self._moveY = moveY

    def eventFilter(self, obj, event):
        if isinstance(obj, QGraphicsWidget):
            if event.type() == QEvent.GraphicsSceneMouseMove:
                self.moverItem(obj, event)

        return True

    def moverItem(self, item, event):
        pos = item.scenePos()
        posX, posY = pos.x(), pos.y()
        if self._moveY:
            moveY = (event.lastScenePos().y() - event.scenePos().y())
            posY = posY - moveY
        if self._moveX:
            moveX = (event.lastScenePos().x() - event.scenePos().x())
            posX = posX - moveX

        item.setPos(posX, posY)


class ItemMovel(QGraphicsWidget):
    rectChanged = pyqtSignal()
    def __init__(self, moveX=True, moveY=True, rect=QRectF(0,0,30,30), parent=None):
        super().__init__(parent)

        self._movel = Movel(moveX, moveY, self)
        self.installEventFilter(self._movel)

        self._newPos = QPointF()
        self._oldPos = QPointF()

        self._rect = QRectF()
        self._newRect = QRectF()
        self._oldRect = QRectF()

        self._timePos = QTimeLine(1000)
        self._timePos.setCurveShape(QTimeLine.EaseInOutCurve)
        self._timePos.valueChanged.connect(self._atualizaPos)

        self._timeRect = QTimeLine(1000)
        self._timeRect.valueChanged.connect(self._atualizaRect)

        self.setTamanho(rect)

    def setMoveXY(self, x, y):
        self._movel.setMoveXY(x, y)
        
    def getRect(self):
        return self._rect
        
    def setRect(self, rect):
        self._rect = rect
        self._atualizaGeometria()
        
    def boundingRect(self):
        return self._rect.adjusted(-1,-1,1,1)

    def altura(self):
        return self._newRect.height()

    def _atualizaPos(self, t):
        #Funcao da curva que parametriza um segmento AB
        #C(t) = A + (B - A)*t
        pos = self._oldPos + (self._newPos - self._oldPos)*t

        self.setPos(pos)
        self._atualizaGeometria()

    def _atualizaRect(self, t):
        oldP1 = self._oldRect.topLeft()
        oldP2 = self._oldRect.bottomRight()

        newP1 = self._newRect.topLeft()
        newP2 = self._newRect.bottomRight()

        p1 = oldP1 + (newP1 - oldP1)*t
        p2 = oldP2 + (newP2 - oldP2)*t

        self.setRect(QRectF(p1, p2))
        
    def _atualizaGeometria(self):
        self.setGeometry(QRectF(self.pos(), self.pos() + self._rect.bottomRight()))

    def goto(self, pos):
        if self.pos() == pos:
            return

        if self._timePos.state() == QTimeLine.Running:
            self._timePos.stop()
        
        self._oldPos = self.pos()
        self._newPos = pos
        self._timePos.start()

    def setTamanho(self, tam):
        if self._rect == tam:
            return

        if self._timeRect.state() == QTimeLine.Running:
            self._timeRect.stop()
        
        self._oldRect = self._rect
        self._newRect = tam
        self._timeRect.start()
        self.rectChanged.emit()

    def resize(self, size):
        if isinstance(size, QRect):
            size = size.size()
            
        self.setTamanho(QRectF(0,0,size.width()-3,self._newRect.height()))

    def paint(self, painter, widget, option):
        if self._timePos.state() == QTimeLine.Running:
            currentValue = self._timePos.currentValue()
            nextValue = self._timePos.valueForTime(self._timePos.currentTime()+100)
            painter.setBrush(QColor(255,0,0,(nextValue-currentValue)*150))
            
        painter.drawRoundedRect(self._rect, 7, 5)
        