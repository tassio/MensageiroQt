#-*- coding: utf-8 -*-
#import sys
#sys.path.append(r"/media/376E9CF27352AA77/Users/Tassio/Downloads/base mensageiro/src")

from PyQt4.QtGui import QWidget, QHBoxLayout, QVBoxLayout, QApplication, \
    QPainter
from barras.barraArquivo import BarraArquivo
from barras.barraConexao import BarraConexao
from barras.barraConversa import BarraConversa
from barras.barraLista import BarraLista, NoteLista
from barras.barraNome import BarraNome
from mensageiroCore.servicos.servicoMensageiro import ServicoClienteMensageiro
from util.resourceUtil import ResourceUtil


class Mensageiro(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._servico = ServicoClienteMensageiro()

        self._configurarGui()
        self._noteLista.barraLista.usuarioSelecionado.connect(self._selecionarUsuario)
        self._barraConversa.conversasNaoVisualizadas.connect(self._noteLista.barraLista.atualizarNumConversasNaoVisualizadas)
        self.background = ResourceUtil.getImage("images/background4.jpg")

    def _configurarGui(self):
        mainLayout = QHBoxLayout()

        layoutUsuario = QVBoxLayout()
        layoutNomeConexao = QHBoxLayout()
        self._barraNome = BarraNome(self._servico)
        self._barraConexao = BarraConexao(self._servico)
        layoutNomeConexao.addWidget(self._barraNome)
        layoutNomeConexao.addWidget(self._barraConexao)

        self._noteLista = NoteLista(self._servico)

        layoutUsuario.addLayout(layoutNomeConexao)
        layoutUsuario.addWidget(self._barraNome)
        layoutUsuario.addWidget(self._noteLista)

        layoutConversa = QVBoxLayout()
        #self._barraArquivo = BarraMultiploArquivo()
        self._barraArquivo = BarraArquivo()
        self._barraConversa = BarraConversa(self._servico)
        layoutConversa.addWidget(self._barraArquivo)
        layoutConversa.addWidget(self._barraConversa)

        mainLayout.addLayout(layoutUsuario, 1)
        mainLayout.addLayout(layoutConversa, 2)
        self.setLayout(mainLayout)

    def _selecionarUsuario(self, usuario):
        self._barraArquivo.setUsuario(usuario)
        self._barraConversa.setUsuarioAtual(usuario)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.background)


if __name__ == '__main__':
    app = QApplication([])
    mens = Mensageiro()
    mens.show()
    app.exec_()
