#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from widgets.widgetNome import WidgetNome

app = QApplication([])
a = WidgetNome('Teste')
a.show()
app.exec_()