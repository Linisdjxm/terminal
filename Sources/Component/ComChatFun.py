'''
@File    :   ComChatFun.py
@Time    :   2024/12/11 21:05
@Version :   1.0
@Desc    :   Built in PyQt5
             信令传输功能示例组件, 功能需要
             - 实现信息文件互传
'''

from PyQt5.QtCore import Qt, pyqtSlot, QByteArray
from PyQt5.QtWidgets import QPushButton,QTextEdit,QLineEdit
from Sources.Component.ComBaseFun import ComBaseFun
from Sources.Device.DevNIC import DevNIC
import code

class ComChatFun(ComBaseFun):
    def __init__(self, name:str, **kwargs):
        super(ComChatFun,self).__init__(name)

        self.register(**kwargs)
        self.ready()
    
    def register(self, **kwargs):
        self.devNIC = DevNIC('NIC设备实现',**{'qTextbrowser':kwargs.get('qTextbrowser'),
                                             'portSendlineEdit':kwargs.get('portSendlineEdit'),
                                             'portRecvlineEdit':kwargs.get('portRecvlineEdit')})
        self.sendfileButton:QPushButton = kwargs.get('sendfileButton')
        self.sendButton:QPushButton = kwargs.get('sendButton')
        self.InputtextEdit:QTextEdit = kwargs.get('InputtextEdit')
        self.hostlineEdit:QLineEdit = kwargs.get('hostlineEdit')
        self.startListenButton:QPushButton = kwargs.get('startListenButton')

    def ready(self):
        self.startListenButton.clicked.connect(self.on_startListenButton_clicked)
        self.sendfileButton.clicked.connect(self.on_sendfileButton_clicked)
        self.sendButton.clicked.connect(self.on_sendButton_clicked)

        self.devNIC.ready()
        self.devNIC.UdpOpenListen()
    
    @pyqtSlot()
    def on_startListenButton_clicked(self):
        if(self.devNIC.portRecvlineEdit.text()==""):
            self.devNIC.writeAppend("Please enter the receive port number",Qt.AlignmentFlag.AlignCenter)
            return
        self.devNIC.UdpCloseListen()
        self.devNIC.portRecv = self.devNIC.portRecvlineEdit.text()
        self.devNIC.portSend = self.devNIC.portSendlineEdit.text()
        self.devNIC.UdpOpenListen()

    @pyqtSlot()
    def on_sendfileButton_clicked(self):
        return
    
    @pyqtSlot()
    def on_sendButton_clicked(self):
        sendmessage:str = self.InputtextEdit.toPlainText()        
        self.devNIC.sendData(self.hostlineEdit.toPlainText(),self.devNIC.portSendlineEdit.text(),sendmessage)
        self.devNIC.writeTimeStamp()
        self.devNIC.writeAppend(sendmessage, Qt.AlignmentFlag.AlignRight)
        self.InputtextEdit.clear()
