#-*- coding: utf-8 -*-
from PyQt4.QtGui import QImage, QGraphicsView, QGraphicsTextItem, QColor, QFont, QPalette, QFrame, QWidget, QPainter, QHBoxLayout
from PyQt4.QtCore import QRectF, pyqtSignal, Qt

from widgets.itens import ItemMovel
from widgets.lista import ListaScene
from mensageiroCore.servicos.informacao.informacaoMensageiro import Usuario
from util.resourceUtil import ResourceUtil


class ItemUsuario(ItemMovel):
    def __init__(self, usuario, rect=QRectF(0, 0, 100, 50), parent=None):
        super().__init__(False, True, rect, parent)

        self._numConversasNaoVisualizadas = 0
        self.selected = False
        self._textItem = QGraphicsTextItem(self)
        self._textItem.setFont(self.fontUser())
        self._textItem.setPos(0, 10)
        self.setaImg = ResourceUtil.getImage('images/right.png').scaled(80, 40, aspectRatioMode=Qt.KeepAspectRatio)
        self.topoImg = ResourceUtil.getImage('images/fundo/topo.png')
        self.background = ResourceUtil.getImage('images/postit3.png')

        self.setUsuario(usuario)

    def setUsuario(self, usuario):
        self._usuario = usuario
        self.atualizaTexto()

    def getUsuario(self):
        return self._usuario

    def setNumConversasNaoVisualizadas(self, num):
        self._numConversasNaoVisualizadas = num
        self.atualizaTexto()

    def atualizaTexto(self):
        texto = "<center>{0} - {1}".format(self._usuario.getNome(), self._usuario.getIP())
        if self._numConversasNaoVisualizadas > 0:
            texto += " <b>({0})</b>".format(self._numConversasNaoVisualizadas)
        texto += "</center>"

        self._textItem.setHtml(texto)

    def setRect(self, rect):
        super().setRect(rect)
        self._textItem.setTextWidth(rect.size().width() - self.setaImg.rect().width())

    def paint(self, painter, widget, option):
        painter.setPen(Qt.NoPen)

        if self.selected:
            rect = self.boundingRect()
            rectImg = self.setaImg.rect()
            painter.drawImage(rectImg.adjusted(rect.width() - rectImg.width(), 0, rect.width() - rectImg.width(), 0), self.setaImg)

        painter.drawImage(self.boundingRect(), self.background)

        """if self.isUnderMouse():
            painter.drawImage(self.boundingRect().adjusted(0,10,0,0), self.topoImg)

        painter.save()
        painter.setPen(Qt.NoPen)
        st = Status.getInstance(self.getUsuario().getStatus())
        if st == Status.ONLINE:
            painter.setBrush(QColor(0,255,0,50))
        elif st == Status.OCUPADO:
            painter.setBrush(QColor(255,0,0,50))
        elif st == Status.AUSENTE:
            painter.setBrush(QColor(240, 226, 31, 50))

        painter.drawRoundedRect(self.getRect(), 7, 5)
        painter.restore()"""

        super().paint(painter, widget, option)

    def fontUser(self):
        font = QFont("LoveYaLikeASister")
        font.setBold(True)
        return font


class BarraLista(QGraphicsView):
    usuarioSelecionado = pyqtSignal(Usuario)

    def __init__(self, servico, parent=None):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.viewport().setAutoFillBackground(False)
        self.setFrameShape(QFrame.NoFrame)

        self.setMinimumWidth(150)

        self._scene = ListaScene(self)
        self.setScene(self._scene)

        self._servico = servico

        self._servico.dadosUsuarioAtualizado.connect(self._atualizarDadosUsuario)
        self._scene.doubleClickItem.connect(self._emitirUsuarioSelecionado)

    def _emitirUsuarioSelecionado(self, item):
        self.usuarioSelecionado.emit(item.getUsuario())

        for i in range(self._scene.quantItens()):
            sceneItem = self._scene.getItem(i)
            sceneItem.selected = (sceneItem == item)

    def _atualizarDadosUsuario(self, usuario):
        us = self.getItemUsuario(usuario)
        if not us:
            self.addUsuario(usuario)
        else:
            us.setUsuario(usuario)

    def addUsuario(self, usuario):
        item = ItemUsuario(usuario)

        self.sceneRectChanged.connect(item.resize)
        item.resize(self.sceneRect())

        self._scene.addItem(item)

    def atualizarNumConversasNaoVisualizadas(self, usuario, num):
        self.getItemUsuario(usuario).setNumConversasNaoVisualizadas(num)

    def getItemUsuario(self, usuario):
        for i in range(self._scene.quantItens()):
            if self._scene.getItem(i).getUsuario().getIP() == usuario.getIP():
                return self._scene.getItem(i)

        return None

    def resizeEvent(self, resize):
        size = resize.size()
        self._scene.setSceneRect(0, 0, size.width(), size.height())

    def __getattr__(self, attr):
        return self._scene.__getattribute__(attr)


class NoteLista(QWidget):
    def __init__(self, servico, parent=None):
        super(NoteLista, self).__init__(parent)
        self.barraLista = BarraLista(servico)
        #self.background = ResourceUtil.getImage("images/postit.svg")
        self.configureGui()

    def configureGui(self):
        layout = QHBoxLayout()
        layout.addWidget(self.barraLista)
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        #painter.drawImage(self.rect(), self.background)
