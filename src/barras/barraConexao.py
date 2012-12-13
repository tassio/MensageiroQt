# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt, QSize
from PyQt4.QtGui import QLabel, QMenu, QIcon, QWidget, QPainter, QPixmap
from mensageiroCore.servicos.informacao.informacaoMensageiro import Status



class BarraConexao(QLabel):
    def __init__(self, servico, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(30,30))

        self._servico = servico
        self._servico.conectado.connect(self.atualizarConexao)

        self._atualizarToolTip()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            menu = QMenu()
            menu.setWindowOpacity(0.9)
            actions = []
            
            actions.append(menu.addAction(QIcon('images/fundo/on.png'), str(Status(Status.ONLINE)), lambda: self.setStatus(Status.ONLINE)))
            actions.append(menu.addAction(QIcon('images/fundo/ausente.png'), str(Status(Status.AUSENTE)), lambda: self.setStatus(Status.AUSENTE)))
            actions.append(menu.addAction(QIcon('images/fundo/ocupado.png'), str(Status(Status.OCUPADO)), lambda: self.setStatus(Status.OCUPADO)))
            actions.append(menu.addAction(QIcon('images/fundo/off.png'), str(Status(Status.OFFLINE)), lambda: self.setStatus(Status.OFFLINE)))

            for i in actions:
                i.setEnabled(self._servico.estaConectado())
                
            menu.exec_(event.globalPos())

    def setStatus(self, tipo):
        self._servico.setStatus(Status(tipo))
        self._atualizarToolTip()
        self.update()

    def atualizarConexao(self, con):
        self._atualizarToolTip()
        self.update()

    def _atualizarToolTip(self):
        msg = str(self._servico.getStatus()) if self._servico.estaConectado() else str(Status(Status.OFFLINE))
        self.setToolTip('Status: {0}'.format(msg))

    def paintEvent(self, event):
        QWidget.paintEvent(self, event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cor = self._servico.getStatus().corStatus() if self._servico.estaConectado() else Status(Status.OFFLINE).corStatus()
        painter.setOpacity(0.7)
        painter.setBrush(cor)
        painter.drawEllipse(self.rect().adjusted(7,5,-7,-5))
        painter.drawPixmap(self.rect(), QPixmap('images/conexao.png'))
        
        painter.end()

