#-*- coding: utf-8 -*-
#import sys
#sys.path.append(r"/media/376E9CF27352AA77/Users/Tassio/Downloads/base mensageiro/src")

from PyQt4.QtGui import QWidget, QApplication, QHBoxLayout

from mensageiroCore.servicos.servicoMensageiro import ServicoServidorMensageiro
from barras.barraLista import BarraLista


class ServidorMensageiro(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._servico = ServicoServidorMensageiro()
        
        self._configurarGui()

    def _configurarGui(self):
        layout = QHBoxLayout(self)
        layout.setMargin(0)

        self._lista = BarraLista(self._servico)
        layout.addWidget(self._lista)
        
        self.setLayout(layout)
                

if __name__ == '__main__':
    app = QApplication([])
    serv = ServidorMensageiro()
    serv.show()
    app.exec_()
        
