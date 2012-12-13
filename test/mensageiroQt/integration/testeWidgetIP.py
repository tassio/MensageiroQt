#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from widgets.widgetIP import WidgetIP
app = QApplication([])
a = WidgetIP('Teste')
a.show()
app.exec_()