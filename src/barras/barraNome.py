#-*- coding: utf-8 -*-

from widgets.widgetNome import WidgetNome


class BarraNome(WidgetNome):
    def __init__(self, servico, parent=None):
        super().__init__(servico.getNome(), parent)

        self._servico = servico

        self.nomeModificado.connect(self._modificarNome)

    def _modificarNome(self, nome):
        self._servico.setNome(nome)
