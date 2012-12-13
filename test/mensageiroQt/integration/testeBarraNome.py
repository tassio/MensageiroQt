#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from barras.barraNome import BarraNome
from mensageiroCore.servicos.servicoMensageiro import ServicoClienteMensageiro

app = QApplication([])
a = ServicoClienteMensageiro()
b = BarraNome(a)
b.show()
app.exec_()