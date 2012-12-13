#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from widgets.editConversa import EditEnviar
from utilTeste import printt

app = QApplication([])
a = EditEnviar()
a.textoDigitado.connect(printt)
a.show()
app.exec_()