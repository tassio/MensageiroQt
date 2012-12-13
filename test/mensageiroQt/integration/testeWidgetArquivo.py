#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication

from widgets.widgetArquivo import WidgetArquivo


app = QApplication([])

a = WidgetArquivo()
a.setPorcentagem(30)
a.show()

app.exec_()