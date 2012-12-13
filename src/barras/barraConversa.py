# -*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QLabel, QWidget, QStackedLayout, QVBoxLayout

from widgets.editConversa import EditEnviar, EditReceber
from mensageiroCore.servicos.informacao.informacaoMensageiro import Usuario
from mensageiroCore.servicos.servicoMensageiro import ServicoClienteMensageiro


NOME_DEFAULT = "<SEM NOME>"

class LabelSituacao(QLabel):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)

        self._usuario = usuario

    def setUsuario(self, usuario):
        self._usuario = usuario

    def setSituacao(self, sit):
        self.setText('' if EditEnviar.VAZIO else "{0} está {1}".format(self._usuario.getNome(), EditEnviar.SITUACOES[int(sit)]))


class BarraConversaUsuario(QWidget):
    def __init__(self, servico, usuario, parent=None):
        super().__init__(parent)
        self._configurarGui()
        
        self._numConversasNaoVisualizadas = 0
        self._servico = servico
        self._usuario = None

        self.setUsuario(usuario)

        self._editEnviar.situacaoModificada.connect(self._enviarSituacao)
        self._editEnviar.textoDigitado.connect(self._enviarConversa)

    def _configurarGui(self):
        layout = QVBoxLayout()
        
        self._lblUsuario = QLabel()
        self._editReceber = EditReceber()
        self._lblSituacao = LabelSituacao(None)
        self._editEnviar = EditEnviar()

        layout.addWidget(self._lblUsuario)
        layout.addWidget(self._editReceber)
        layout.addWidget(self._lblSituacao)
        layout.addWidget(self._editEnviar)
        self.setLayout(layout)
        
    def _enviarSituacao(self, sit):
        self._servico.enviarInformacaoConversa(sit)

    def _enviarConversa(self, conv):
        self._servico.enviarConversa(conv)
        self._editReceber.receberTexto(self._servico.getNome(), conv)

    def atualizarSituacao(self, sit):
        self._lblSituacao.setSituacao(sit)

    def setUsuario(self, usuario):
        """Se o usuário for diferente do atual atualiza o nome do usuário nas 
        conversas recebidas anteriormente."""
        if not self._usuario or self._usuario.getNome() != usuario.getNome():
            nomeAntigo = self._usuario and self._usuario.getNome() or NOME_DEFAULT
            self._editReceber.renomearUsuario(nomeAntigo, usuario.getNome())
            
        self._usuario = usuario
        self._servico.setPara(self._usuario.getIP())
        
        self._lblSituacao.setUsuario(usuario)
        self._lblUsuario.setText(str(usuario))

    def getUsuario(self):
        return self._usuario
    
    def setNumConversasNaoVisualizadas(self, num):
        self._numConversasNaoVisualizadas = num

    def getNumConversasNaoVisualizadas(self):
        return self._numConversasNaoVisualizadas
    
    def receberTexto(self, texto):
        self._editReceber.receberTexto(self._usuario.getNome(), texto)


class BarraConversa(QWidget):
    conversasNaoVisualizadas = pyqtSignal(Usuario, int)
    def __init__(self, servico, parent=None):
        super().__init__(parent)
        self._configurarGui()
        
        self._servico = servico
        self._servico.dadosUsuarioAtualizado.connect(self._atualizarUsuario)
        self._servico.conversaRecebida.connect(self._receberConversa)
        self._servico.informacaoTipoValorRecebida.connect(self._receberSituacao)

    def _configurarGui(self):
        self._stackedLayout = QStackedLayout(self)
        self._stackedLayout.setMargin(0)
        self.setLayout(self._stackedLayout)
        
        self._mostrarTelaInicial()
        
    def _setNumConversasNaoVisualizadas(self, barraConversaUsuario, numConversasNaoVisualizadas):
        barraConversaUsuario.setNumConversasNaoVisualizadas(numConversasNaoVisualizadas)
        self.conversasNaoVisualizadas.emit(barraConversaUsuario.getUsuario(), numConversasNaoVisualizadas)

    def _receberConversa(self, de, inf):
        usuario = Usuario(nome=NOME_DEFAULT, ip=de)

        barraConversaUsuario = self._getOrCreateBarraConversaUsuario(usuario)
        barraConversaUsuario.receberTexto(inf)
        
        if self._stackedLayout.currentWidget() != barraConversaUsuario:
            numConversasNaoVisualizadasAtual = barraConversaUsuario.getNumConversasNaoVisualizadas() + 1
            
            self._setNumConversasNaoVisualizadas(barraConversaUsuario, numConversasNaoVisualizadasAtual)
            
    def _receberSituacao(self, de, tipo, valor):
        if tipo == ServicoClienteMensageiro.INFORMACAO:
            usuario = Usuario(nome=NOME_DEFAULT, ip=de)
            self._getOrCreateBarraConversaUsuario(usuario).atualizarSituacao(valor['informacao'])
            
    def _atualizarUsuario(self, usuario):
        self._getOrCreateBarraConversaUsuario(usuario).setUsuario(usuario)
        
    def _mostrarTelaInicial(self):
        lbl = QLabel("<- Selecione o Usuário")
        self._stackedLayout.insertWidget(0, lbl)
        self._stackedLayout.setCurrentIndex(0)

    def _setConversaUsuarioAtual(self, barraConversaUsuario):
        ind = self._indexWidgetConversa(barraConversaUsuario.getUsuario())
        self._stackedLayout.setCurrentIndex(ind)

    def _indexWidgetConversa(self, usuario):
        for i in range(1, self._stackedLayout.count()):
            if self._stackedLayout.widget(i).getUsuario().getIP() == usuario.getIP():
                return i

        return -1
    
    def _getOrCreateBarraConversaUsuario(self, usuario):
        ind = self._indexWidgetConversa(usuario)
        if ind != -1:
            return self._stackedLayout.widget(ind)
        else:
            barraConversaUsuario = BarraConversaUsuario(self._servico, usuario)
            self._stackedLayout.addWidget(barraConversaUsuario)
            return barraConversaUsuario
        
    def setUsuarioAtual(self, usuario):
        """Altera a conversa visível para a conversa do usuário 
           e reinicia a contagem de conversas não visualizadas."""
        barraConversaUsuario = self._getOrCreateBarraConversaUsuario(usuario)
        barraConversaUsuario.setUsuario(usuario)
        self._setNumConversasNaoVisualizadas(barraConversaUsuario, 0)

        self._setConversaUsuarioAtual(barraConversaUsuario)
        

