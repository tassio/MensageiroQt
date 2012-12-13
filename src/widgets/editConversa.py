# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal, Qt, QTimer
from PyQt4.QtGui import QTextEdit, QKeyEvent


class EditEnviar(QTextEdit):
    VAZIO = "0"
    DIGITANDO = "1"
    APAGANDO = "2"
    SITUACOES = ["","digitando","apagando"]
    
    situacaoModificada = pyqtSignal(str)
    textoDigitado = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)

        self._situacao = EditEnviar.VAZIO

    def _modificarSituacao(self, sit):
        if self._situacao != sit:
            self._situacao = sit
            self.situacaoModificada.emit(sit)

    def _analisarSituacao(self):
        if len(self.toPlainText()) == 0:
            self._modificarSituacao(EditEnviar.VAZIO)

    def clear(self):
        self.setText('')
        self._modificarSituacao(EditEnviar.VAZIO)

    def enviarTexto(self):
        texto = self.toPlainText().strip(' ')
        if texto:
            self.textoDigitado.emit(texto)
            self.clear()
        
    def keyPressEvent(self, event):
        key = event.key()
        modifier = event.modifiers()
        numChars = len(self.toPlainText())
        
        if key in [Qt.Key_Return, Qt.Key_Enter]:
            if modifier == Qt.ShiftModifier:
                event = QKeyEvent(event.type(), Qt.Key_Return, Qt.NoModifier, event.text())
            else:
                self.enviarTexto()
                return

        #Atualizando o texto do Edit
        QTextEdit.keyPressEvent(self, event)
        
        if numChars > 0 and len(self.toPlainText()) == 0:
            self._modificarSituacao(EditEnviar.APAGANDO)
            QTimer.singleShot(2000, lambda: self._analisarSituacao())
        elif numChars == 0 and len(self.toPlainText()) > 0:
            self._modificarSituacao(EditEnviar.DIGITANDO)


class EditReceber(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setReadOnly(True)

    def receberTexto(self, nome, texto):
        self.append('<b>{0} diz: </b>{1}'.format(nome, texto))
        
    def renomearUsuario(self, nome, novoNome):
        self.setText(self.toHtml().replace("{0} diz: ".format(nome), "{0} diz: ".format(novoNome)))
        