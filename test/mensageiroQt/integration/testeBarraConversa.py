#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from barras.barraConversa import BarraConversa
from mensageiroCore.servicos.servicoMensageiro import ServicoClienteMensageiro,\
    ServicoServidorMensageiro
from mensageiroCore.servicos.informacao.informacaoMensageiro import Usuario

app = QApplication([])

cli = ServicoClienteMensageiro()
serv = ServicoServidorMensageiro()

b = BarraConversa(cli)
b.setUsuarioAtual(Usuario("ABS", "TESTE","127.0.0.1"))
b.show()
app.exec_()
