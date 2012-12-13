#-*- coding: utf-8 -*-

from PyQt4.QtCore import QRectF
from PyQt4.QtGui import QApplication, QGraphicsView, QGraphicsScene

from widgets.itens import ItemMovel


app = QApplication([])
view = QGraphicsView()
scene = QGraphicsScene()
view.setScene(scene)
a = ItemMovel()
scene.addItem(a)
view.show()
a.setTamanho(QRectF(0,0,100,100))
app.exec_()