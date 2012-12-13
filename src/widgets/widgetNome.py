# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal, Qt
from PyQt4.QtGui import QLabel, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton


class LabelDrop(QLabel):
    doubleClicked = pyqtSignal()
    textoModificado = pyqtSignal(str)
    def __init__(self, texto='', parent=None):
        super().__init__(texto, parent)

        self.setText(texto)
        self.setAcceptDrops(True)
        
    def setText(self, text):
        super().setText("<b>" + text + "</b>")
        
    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        text = event.mimeData().text()
        self.setText(text)
        self.textoModificado.emit(text)


class EditLabel(QWidget):
    textoModificado = pyqtSignal(str)
    visivelModificado = pyqtSignal()
    def __init__(self, texto, parent=None):
        super().__init__(parent)
        self._configurarGui(texto)

        self._edit.returnPressed.connect(self.mudarVisivel)
        self._label.doubleClicked.connect(self.mudarVisivel)
        self._label.textoModificado.connect(self.setTexto)

    def _configurarGui(self, texto):
        layout = QVBoxLayout()
        layout.setMargin(0)
    
        self._label = LabelDrop(texto)
        self._edit = QLineEdit(texto)
        self._edit.setVisible(False)

        layout.addWidget(self._label)
        layout.addWidget(self._edit)
        self.setLayout(layout)

    def setTexto(self, texto):
        self._label.setText(texto)
        self._edit.setText(texto)
        self.textoModificado.emit(texto)

    def getTexto(self):
        return self.edit.text()

    def mudarVisivel(self):
        self._label.setVisible(not self._label.isVisible())
        self._edit.setVisible(not self._edit.isVisible())

        if self._edit.text() != self._label.text():
            self.setTexto(self._edit.text())
            
        self.visivelModificado.emit()


class WidgetNome(QWidget):
    nomeModificado = pyqtSignal(str)
    def __init__(self, texto='', parent=None):
        super().__init__(parent)
        self._configurarGui(texto)

        self._lblNome.visivelModificado.connect(self._mostrarModificarGravar)
        self._lblNome.textoModificado.connect(lambda nome: self.nomeModificado.emit(nome))
        self._btnGravar.clicked.connect(self._lblNome.mudarVisivel)

    def _configurarGui(self, texto):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        layout.setMargin(0)
        
        self._spacer = QSpacerItem(0,0,QSizePolicy.Expanding,QSizePolicy.Maximum)
        self._layoutSpacer = QHBoxLayout()
        self._layoutSpacer.addItem(self._spacer)
        
        lbl = QLabel('Nome: ', self)
        self._lblNome = EditLabel(texto)
        self._btnGravar = QPushButton('Modificar')

        layout.addWidget(lbl)
        layout.addWidget(self._lblNome)
        layout.addLayout(self._layoutSpacer)
        layout.addWidget(self._btnGravar)
        self.setLayout(layout)

    def _mostrarModificarGravar(self):
        if self._lblNome.isVisible():
            self._btnGravar.setText('Modificar')
            self._layoutSpacer.addItem(self._spacer)            
        else:
            self._btnGravar.setText('Gravar')
            self._layoutSpacer.removeItem(self._spacer)

    def getNome(self):
        return self._lblNome.getTexto()

    def setNome(self, nome):
        self._lblNome.setTexto(str(nome))

