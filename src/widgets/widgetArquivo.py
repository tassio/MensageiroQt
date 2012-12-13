#-*- coding: utf-8 -*-
from PyQt4.QtCore import QRectF, Qt, QTimer
from PyQt4.QtGui import QWidget, QPainter, QPen, QHBoxLayout, QVBoxLayout, QLabel, QPushButton


class WidgetProgresso(QWidget):
    def __init__(self, porcentagem=0, corFundo=Qt.white, corBarra=Qt.gray, parent=None):
        super().__init__(parent)

        self._porcentagem = porcentagem
        
        self._corFundo = corFundo
        self._corBarra = corBarra

    def setPorcentagem(self, porc):
        self._porcentagem = porc
        self.update()

    def getPorcentagem(self):
        return self._porcentagem

    def setCorFundo(self, cor):
        self._corFundo = cor
        self.update()

    def setCorBarra(self, cor):
        self._corBarra = cor
        self.update()

    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        rect = QRectF(self.rect())

        painter = QPainter(self)
        painter.setBrush(self._corFundo)

        pen = QPen()
        pen.setColor(Qt.gray)
        painter.setPen(pen)

        painter.drawRoundedRect(QRectF(2, 1, rect.width()-6, rect.height()-4), 8, 2)
        if self.getPorcentagem() > 0:
            painter.setBrush(self._corBarra)
            larguraBarra = self.getPorcentagem()*((rect.width()-6)/100.)
            painter.drawRoundedRect(QRectF(2, 1, larguraBarra, rect.height()-4), 8, 2)
            
        painter.end()


class WidgetArquivo(WidgetProgresso):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._configurarGui()

    def _configurarGui(self):
        layout = QHBoxLayout(self)
        layout.setMargin(5)

        lblLayout = QVBoxLayout()
        self._lblTexto = QLabel("Texto")
        self._lblInformacao = QLabel("Informacao")
        lblLayout.addWidget(self._lblTexto)
        lblLayout.addWidget(self._lblInformacao)

        self._btnEnviar = QPushButton('Enviar Arquivo')
        self._btnReceber = QPushButton('Receber Arquivo')
        self._btnReceber.setEnabled(False)
        self._btnCancelar = QPushButton('Cancelar')
        self._btnCancelar.setVisible(False)

        layout.addWidget(self._btnEnviar)
        layout.addLayout(lblLayout)
        layout.addWidget(self._btnReceber)
        layout.addWidget(self._btnCancelar)
        self.setLayout(layout)
        
    def _estadoCancelado(self):
        self.setTexto("Cancelado")
        self._btnCancelar.setEnabled(False)
        QTimer.singleShot(2000, lambda: self._estadoInicial())
        
    def _estadoFinalizado(self):
        self.setTexto("Finalizado")
        self._btnCancelar.setEnabled(False)
        QTimer.singleShot(2000, lambda: self._estadoInicial())

    def _estadoInicial(self):
        self.setPorcentagem(0)
        self.setTexto("Texto")
        self.setInformacao("Informacao")
        self._btnEnviar.setEnabled(True)
        self._btnReceber.setEnabled(False)
        self._btnCancelar.setVisible(False)
        self._btnCancelar.setEnabled(True)

    def setTexto(self, texto):
        self._lblTexto.setText(texto)

    def setInformacao(self, inf):
        self._lblInformacao.setText(inf)
