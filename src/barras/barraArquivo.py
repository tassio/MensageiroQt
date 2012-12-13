# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSignal, Qt, QFileInfo
from PyQt4.QtGui import QMenu, QDesktopServices, QFileDialog, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from networkService.servicos.servicoArquivoFuncao import ServicoArquivoEnviar, ServicoArquivoReceber
from widgets.widgetArquivo import WidgetArquivo


class AbstractBarraArquivo(object):
    enviandoArquivo = pyqtSignal(str)
    recebendoArquivo = pyqtSignal(str)
    arquivoCanceladoReceber = pyqtSignal(str)
    arquivoCanceladoEnviar = pyqtSignal(str)
    arquivoRecebido = pyqtSignal(str)
    arquivoEnviado = pyqtSignal(str)
    def __init__(self, usuario=None):
        self._usuario = usuario
        
    def setUsuario(self, usuario):
        self._usuario = usuario
        
    def getUsuario(self):
        return self._usuario


class BarraArquivo(AbstractBarraArquivo, WidgetArquivo):
    enviandoArquivo = pyqtSignal(str)
    recebendoArquivo = pyqtSignal(str)
    arquivoCanceladoReceber = pyqtSignal(str)
    arquivoCanceladoEnviar = pyqtSignal(str)
    arquivoRecebido = pyqtSignal(str)
    arquivoEnviado = pyqtSignal(str)
    def __init__(self, usuario=None, servicoArquivoEnviar=None, servicoArquivoReceber=None, parent=None):
        AbstractBarraArquivo.__init__(self, usuario)
        WidgetArquivo.__init__(self, parent)
        self.setAcceptDrops(True)

        self._servicoEnviar = servicoArquivoEnviar or ServicoArquivoEnviar(40000,40001)
        self._servicoReceber = servicoArquivoReceber or ServicoArquivoReceber(40001,40000)

        self._servicoReceber.pedidoReceberArquivo.connect(self._recebendoArquivo)
        self._servicoEnviar.pedidoReceberAceito.connect(self._enviandoArquivo)
        self._servicoReceber.porcentagem.connect(self._alterarPorcentagem)
        self._servicoEnviar.porcentagem.connect(self._alterarPorcentagem)
        self._servicoReceber.cancelado.connect(self._estadoCanceladoReceber)
        self._servicoEnviar.cancelado.connect(self._estadoCanceladoEnviar)
        self._servicoReceber.finalizado.connect(self._estadoFinalizadoReceber)
        self._servicoEnviar.finalizado.connect(self._estadoFinalizadoEnviar)

        self._btnEnviar.clicked.connect(self._selecionarArquivoEnviar)
        self._btnEnviar.setEnabled(self._usuario != None)
        self._btnReceber.clicked.connect(self._selecionarArquivoReceber)
        self._btnCancelar.clicked.connect(self.cancelar)

    def nomeArquivoReceber(self):
        return self._servicoReceber.getNomeArquivo()
    
    def nomeArquivoEnviar(self):
        return self._servicoEnviar.getNomeArquivo()

    def _estadoCanceladoReceber(self):
        self.arquivoCanceladoReceber.emit(self.nomeArquivoReceber())
        self._estadoCancelado()
        
    def _estadoCanceladoEnviar(self):
        self.arquivoCanceladoEnviar.emit(self.nomeArquivoEnviar())
        self._estadoCancelado()
        
    def _estadoFinalizadoReceber(self):
        self.arquivoRecebido.emit(self.nomeArquivoReceber())
        self._estadoFinalizado()
    
    def _estadoFinalizadoEnviar(self):
        self.arquivoEnviado.emit(self.nomeArquivoEnviar())
        self._estadoFinalizado()

    def _recebendoArquivo(self, de, nomeArquivo):
        self.setTexto("Receber -> {0} de {1}".format(nomeArquivo, de))
        self._btnEnviar.setEnabled(False)
        self._btnReceber.setEnabled(True)
        self._btnCancelar.setVisible(True)
        
    def _enviandoArquivo(self):
        self.setTexto('Enviando ' + self.nomeArquivoEnviar())
        self.enviandoArquivo.emit(self.nomeArquivoEnviar())
        
    def _alterarPorcentagem(self, valor):
        self.setInformacao('Porcentagem: {0}%'.format(valor))
        self.setPorcentagem(valor)

    def mousePressEvent(self, event):
        if (event.button() == Qt.RightButton):
            menu = QMenu()
            cancelar = menu.addAction('Cancelar', self.cancelar)
            cancelar.setEnabled(self.trabalhando())
            menu.exec_(event.globalPos())

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            if not self.trabalhando():
                event.acceptProposedAction()

    def dropEvent(self, event):
        path = event.mimeData().urls()[0].toString()
        if QFileInfo(path).isFile():
            self.enviarArquivo(path)
            event.acceptProposedAction()

    def trabalhando(self):
        return self._servicoEnviar.estaEnviandoArquivo() or self._servicoReceber.estaRecebendoArquivo()

    def setUsuario(self, usuario):
        super().setUsuario(usuario)
        self._estadoInicial()
            
    def cancelar(self):
        if self._servicoEnviar.estaEnviandoArquivo():
            self._servicoEnviar.cancelar()
        elif self._servicoReceber.estaRecebendoArquivo():
            self._servicoReceber.cancelar()

        self._estadoInicial()

    def _selecionarArquivoEnviar(self):
        path = QFileDialog.getOpenFileName(None, 'Enviar...', QDesktopServices.displayName(QDesktopServices.DesktopLocation))
        if path:
            self.enviarArquivo(path)

    def enviarArquivo(self, path):
        self._servicoEnviar.enviarArquivo(path.replace('file:///',''), self._usuario.getIP())
        self.setTexto('Enviar ' + self.nomeArquivoEnviar())
        
    def _selecionarArquivoReceber(self):
        path = QFileDialog.getSaveFileName(None, 'Salvar...', QDesktopServices.displayName(QDesktopServices.DesktopLocation))
        if path:
            self.receberArquivo(path)

    def receberArquivo(self, path):
        self._servicoReceber.aceitarArquivo(path)
        self._btnReceber.setEnabled(False)
        self.recebendoArquivo.emit(self.nomeArquivoReceber())
        
        
class BarraMultiploArquivo(AbstractBarraArquivo, QWidget):
    def __init__(self, usuario=None, servicoArquivoEnviar=None, servicoArquivoReceber=None, parent=None):
        AbstractBarraArquivo.__init__(self, usuario)
        QWidget.__init__(self, parent)
        
        self._servicoArquivoEnviar = servicoArquivoEnviar or ServicoArquivoEnviar(40000,40001)
        self._servicoArquivoReceber = servicoArquivoReceber or ServicoArquivoReceber(40001,40000)
        
        self._barras = []
        
        self._configurarGui()
        
    def _configurarGui(self):
        self._layout = QVBoxLayout(self)
        
        buttonAdd = QPushButton('+')
        buttonAdd.clicked.connect(self._addBarra)
        
        self._layoutBarras = QVBoxLayout()
        
        self._layout.addLayout(self._layoutBarras)
        self._layout.addWidget(buttonAdd)

        self._addBarra()
        
    def setUsuario(self, usuario):
        super().setUsuario(usuario)
        for barra in self._barras:
            barra.setUsuario(usuario)
            
    def _removerBarra(self, barra, widget):
        self._barras.remove(barra)
        widget.close()
        self._layoutBarras.update()
        
        
    def _addBarra(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        barra = BarraArquivo(usuario=self.getUsuario(), servicoArquivoEnviar=self._servicoArquivoEnviar, servicoArquivoReceber=self._servicoArquivoReceber, parent=self)
        
        button = QPushButton('X')
        button.clicked.connect(lambda: self._removerBarra(barra, widget))
        
        layout.addWidget(barra)
        layout.addWidget(button)
        
        self._barras.append(barra)
        self._layoutBarras.addWidget(widget)
        


