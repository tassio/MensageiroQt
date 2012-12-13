#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication, QGraphicsView
from PyQt4.QtCore import QTimer, QRectF

from widgets.lista import ListaScene
from widgets.itens import ItemMovel


app = QApplication([])
w = QGraphicsView()
a = ListaScene(w)
a.setSceneRect(0,0,300,300)

i = ItemMovel()
a.addItem(i)
i2 = ItemMovel()
a.addItem(i2)

QTimer.singleShot(2000, lambda: (i.setTamanho(QRectF(0,0,10,10)), i2.setTamanho(QRectF(0,0,40,20))))
QTimer.singleShot(4000, lambda: i.setTamanho(QRectF(0,0,60,50)))

q = ItemMovel()
QTimer.singleShot(6000, lambda: (a.addItem(q), q.setTamanho(QRectF(0,0,60,60))))

QTimer.singleShot(8000, lambda: (q.setTamanho(QRectF(0,0,30,20)), i.setTamanho(QRectF(0,0,10,50)), i2.setTamanho(QRectF(0,0,30,10))))

a.addItem(ItemMovel())
w.setScene(a)
w.show()

app.exec_()