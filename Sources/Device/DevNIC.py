#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   DevNIC.py
@Time    :   2024/12/24 16:19
@Author  :   CRC1109 
@Version :   1.0
@Desc    :   Built in PyQt5
             虚拟NIC设备, 功能需要
             - 实现信令互传
'''

from Sources.Device.DevBase import DevBase
from Config.Config import Config
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QByteArray,Qt,QDateTime
from PyQt5.QtWidgets import QLineEdit,QPushButton,QTextEdit,QTextBrowser
from PyQt5.QtGui import QTextCursor, QTextBlockFormat
from PyQt5.QtNetwork import QUdpSocket, QHostAddress, QAbstractSocket

class DevNIC(DevBase):
    def __init__(self, name: str ,**kwargs):
        super(DevNIC,self).__init__(name)
        self.UdpSocket = QUdpSocket()

    def ready(self):
        self.configList = Config()

        self.portSend = self.configList.getConfigItem("StrSendToPort")
        self.portRecv = self.configList.getConfigItem("StrReceiveFromPort")
        self.UdpSocket.readyRead.connect(self.recvData)

    def UdpOpenListen(self):
        print ("udp try to open port: " + self.portRecv)
        self.UdpSocket.bind(QHostAddress(QHostAddress.SpecialAddress.Any), int(self.portRecv), QAbstractSocket.BindFlag.ShareAddress)

    def UdpCloseListen(self):
        print ("udp try to close port: " + self.portRecv)
        self.UdpSocket.close()

    def sendData(self, ip_address:str, port:str, message:str):
        self.dataGram:QByteArray = message.encode('utf-8')
        if(port != ""):
            self.UdpSocket.writeDatagram(self.dataGram,
                                        QHostAddress(ip_address),
                                        int(port))
        else:  # Unlikely to happen
            print("Please enter the send port number")

    @pyqtSlot()
    def recvData(self):
        while(self.UdpSocket.hasPendingDatagrams()): 
            self.dataGram = QByteArray()
            self.dataGram.resize(self.UdpSocket.pendingDatagramSize())
            [tempbytes, host, _] = self.UdpSocket.readDatagram(self.dataGram.size())
            if(tempbytes!=None):
                return (tempbytes.decode("utf-8"), host)
            else:
                print("Port Not Found")
        