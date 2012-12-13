#-*- coding: utf-8 -*-

from PyQt4.QtGui import QGraphicsScene, QGraphicsItem, QGraphicsWidget
from PyQt4.QtCore import QEvent, pyqtSignal, Qt, QRectF, QPointF

from widgets.itens import ItemMovel


class ListaScene(QGraphicsScene):
    TAM_ITENS = 40
    doubleClickItem = pyqtSignal(QGraphicsItem)
    def __init__(self, parent=None):
        super().__init__(parent)

        self._listaItens = []

    def eventFilter(self, item, event):
        if isinstance(item, QGraphicsWidget):
            if event.type() == QEvent.GraphicsSceneMouseDoubleClick:
                self.doubleClickItem.emit(item)
            if event.type() == QEvent.GraphicsSceneMouseRelease:
                self._analisarNovaPosicao(item)
        
        return super().eventFilter(item, event)

    def mouseMoveEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            item.update()

        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        val = - event.delta() / 120
        alturaTotal = self.alturaTotal()
        rect = self.sceneRect()
        ajustar = val * 10
        if rect.top() + ajustar < -1:
            ajustar = -rect.top()
        elif rect.bottom() + ajustar > alturaTotal:
            if rect.bottom() < alturaTotal:
                ajustar = alturaTotal-rect.bottom()+1
            else:
                ajustar = 0
        newRect = self.sceneRect().adjusted(0,ajustar,0,ajustar)

        self.setSceneRect(newRect)

    def setSceneRect(self, *args):
        if len(args) == 1:
            rect = args[0]
        else:
            left, top, width, height = args
            rect = QRectF(left, top, width, height)
            
        for item in self._listaItens:
            item.setTamanho(QRectF(0,0,rect.width(),item.altura()))
            
        super().setSceneRect(rect)

    def addItem(self, item):
        if isinstance(item, ItemMovel):
            item.installEventFilter(self)
            item.setMoveXY(False, True)
            
            item.rectChanged.connect(self.atualiza)
            
            item.goto(QPointF(0, self.calcularAlturaPosicao(self.quantItens())))
            self._listaItens.append(item)
            super().addItem(item)
        else:
            raise TypeError("O item deve ser um ItemMovel")

    def atualiza(self):
        pos = 0
        for item in self._listaItens:
            item.goto(QPointF(0,pos))
            pos += item.altura()

    def quantItens(self):
        return len(self._listaItens)

    def getItem(self, i):
        return self._listaItens[i]

    def calcularAlturaPosicao(self, pos):
        alt = 0
        for item in self._listaItens[:pos]:
            alt += item.altura()
        return alt

    def alturaTotal(self):
        return self.calcularAlturaPosicao(self.quantItens()-1)

    def posAltura(self, alt):
        altura = 0
        for i in range(self.quantItens()):
            altura += self.calcularAlturaPosicao(i) + (self.getItem(i).size().height() / 2)
            if alt < altura:
                return i

        return self.quantItens()

    def _analisarNovaPosicao(self, item):
        pos = self.posAltura(item.pos().y())

        self._listaItens.remove(item)
        item.goto(QPointF(0,self.calcularAlturaPosicao(pos)))
        self._listaItens.insert(pos, item)

        for i in range(pos+1, self.quantItens()):
            self._listaItens[i].goto(QPointF(0, self.calcularAlturaPosicao(i)))

        for i in range(0, pos):
            self._listaItens[i].goto(QPointF(0, self.calcularAlturaPosicao(i)))
