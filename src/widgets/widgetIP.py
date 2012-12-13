# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QLabel, QHBoxLayout


class WidgetIP(QWidget):
    def __init__(self, ip, parent=None):
        super().__init__(parent)
        self._configurarGui()

        self.setIP(ip)

    def _configurarGui(self):
        layout = QHBoxLayout()
        layout.setMargin(0)
        layout.setAlignment(Qt.AlignCenter)
        
        self._lblIP = QLabel()
        layout.addWidget(self._lblIP)
        self.setLayout(layout)
        
    def setIP(self, ip):
        self._ip = ip
        self._lblIP.setText('Para IP: <b>{0}</b>'.format(self._ip))

    def getIP(self):
        return self._ip
        
