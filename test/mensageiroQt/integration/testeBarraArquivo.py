#-*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication

from barras.barraArquivo import BarraArquivo
from utilTeste import printt
from mensageiroCore.servicos.informacao.informacaoMensageiro import Usuario


app = QApplication([])


a = BarraArquivo()
a.setUsuario(Usuario("Teste", "qwe", "127.0.0.1"))

a.arquivoCanceladoEnviar.connect(printt("Arquivo Cancelado Enviar:"))
a.arquivoCanceladoReceber.connect(printt("Arquivo Cancelado Receber:"))
a.arquivoEnviado.connect(printt("Arquivo Enviado:"))
a.arquivoRecebido.connect(printt("Arquivo Recebido:"))
a.enviandoArquivo.connect(printt("Enviando Arquivo:"))
a.recebendoArquivo.connect(printt("Recebendo Arquivo:"))

a.show()

app.exec_()