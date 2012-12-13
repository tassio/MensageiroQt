#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication

from barras.barraConexao import BarraConexao
from mensageiroCore.servicos.servicoMensageiro import ServicoClienteMensageiro,\
    ServicoServidorMensageiro


app = QApplication([])

b = ServicoServidorMensageiro()

a = BarraConexao(ServicoClienteMensageiro())
a.show()

app.exec_()