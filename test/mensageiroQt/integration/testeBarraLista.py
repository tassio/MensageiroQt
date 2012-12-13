#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from barras.barraLista import BarraLista, ItemUsuario
from mensageiroCore.servicos.servicoMensageiro import ServicoClienteMensageiro,\
    ServicoServidorMensageiro
from mensageiroCore.servicos.informacao.informacaoMensageiro import Usuario

app = QApplication([])
s = ServicoClienteMensageiro()
ss = ServicoServidorMensageiro()

w = BarraLista(s)
w.setSceneRect(0,0,300,300)

q = ItemUsuario(Usuario('QNome','AUSENTE','12333'))
w.addItem(q)
i = ItemUsuario(Usuario('Localhost','ONLINE','127.0.0.1'))
w.addItem(i)
z = ItemUsuario(Usuario('QNome','AUSENTE','12333'))
w.addItem(z)

w.show()
w.usuarioSelecionado.connect(lambda u: print(u))
app.exec_()