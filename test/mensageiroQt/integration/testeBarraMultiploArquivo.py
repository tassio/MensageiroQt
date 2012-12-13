#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication

from barras.barraArquivo import BarraMultiploArquivo
from mensageiroCore.servicos.informacao.informacaoMensageiro import Usuario


app = QApplication([])


b = BarraMultiploArquivo()
b.setUsuario(Usuario("Teste", "qwe", "127.0.0.1"))
b.show()

app.exec_()