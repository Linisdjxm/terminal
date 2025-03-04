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
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QByteArray, Qt, QDateTime, QThread, QObject, QMutexLocker, QMutex, QTimer
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTextEdit, QTextBrowser
from PyQt5.QtGui import QTextCursor, QTextBlockFormat
from PyQt5.QtNetwork import QUdpSocket, QHostAddress, QAbstractSocket, QTcpServer, QTcpSocket

class DevNIC(DevBase):
    sendTcpData = pyqtSignal(str, str, bool, bool)
    #connectToTcpHost = pyqtSignal(str)
    video_data_received = pyqtSignal(bytes)  # 在DevNIC类中新增信号

    def __init__(self, name: str, type: str, type2 = 1, type3 = "Topo", sendList = None):
        super(DevNIC, self).__init__(name)
        self.configList = Config()
        self.type1 = type
        self.response = 0
        self.type2 = type2
        self.type3 = type3
        self.sendList = sendList # TCP NIC
        if type == "UDP":
            self.UdpSocket = QUdpSocket()
        else:
            self.sendList = []
            self.tcp_lock = QMutex()
            self._init_tcp_server()

        # 连接信号到槽函数
        self.sendTcpData.connect(self._send_tcp_data)
        #self.connectToTcpHost.connect(self._connect_to_tcp_host)

    def ready(self):
        type3 = self.type3
        if type3 == "Topo":
            self.portSend = self.configList.getConfigItem("StrSendToPort")
            self.portRecv = self.configList.getConfigItem("StrReceiveFromPort")
        elif type3 == "Video":
            self.portSend = self.configList.getConfigItem("VideoSendToPort")
            self.portRecv = self.configList.getConfigItem("VideoReceiveFromPort")
        else:
            pass
        self.UdpSocket.readyRead.connect(self.recvData)

    def _init_tcp_server(self):
        # 初始化TCP服务器
        if self.type2 == 1:
            self.TCPSendPort = int(self.configList.getConfigItem("TCPStrSendToPort"))
            self.TCPReceivePort = int(self.configList.getConfigItem("TCPStrReceiveFromPort"))
        else:
            self.TCPSendPort = int(self.configList.getConfigItem("TCPStrSendToPort2"))
            self.TCPReceivePort = int(self.configList.getConfigItem("TCPStrReceiveFromPort2"))
        self.tcp_server = QTcpServer()
        self.tcp_server.newConnection.connect(self._handle_tcp_connection)
        self.tcp_server.listen(QHostAddress.Any, self.TCPReceivePort)

    @pyqtSlot(str, str, bool, bool)
    def _send_tcp_data(self, ip, data, flag, flag2):
        configList2 = Config()
        tcp_cli_sock = QTcpSocket()
        while not tcp_cli_sock.waitForConnected(1000):
            if not tcp_cli_sock.connectToHost(ip, self.TCPSendPort):
                continue
        if flag2:
            tcp_cli_sock.write(data.encode())
        elif flag:
            print("Hello to " + str(ip))
            tcp_cli_sock.write(b"HELLO")
        else:
            print("Bye to " + str(ip))
            tcp_cli_sock.write(b"BYE")
        if not tcp_cli_sock.waitForBytesWritten(1000):
            print("TCP Timeout!")
        tcp_cli_sock.disconnectFromHost()

    '''@pyqtSlot(str)
    def _connect_to_tcp_host(self, ip):
        configList2 = Config()
        tcp_cli_sock = QTcpSocket()
        while not tcp_cli_sock.waitForConnected(1000):
            if not tcp_cli_sock.connectToHost(ip, int(configList2.getConfigItem("TCPStrSendToPort"))):
                continue
    '''
    class TCPWorker(QThread):
        """TCP连接处理线程"""
        finished = pyqtSignal()
        def __init__(self, socket, addr, parent=None):
            super().__init__(parent)
            self.socket = socket
            self.addr = addr
            self.parent = parent
            self.socket.readyRead.connect(self.handle_read)
        
        def run(self):
            self.exec_()  # Start the event loop
        
        def handle_read(self):
            if self.socket.bytesAvailable() > 0:
                data = self.socket.readAll()
            cache = str(data.data(), encoding='utf-8').strip()
            print(cache)
            if cache == "HELLO":
                with QMutexLocker(self.parent.tcp_lock):
                    if self.addr[0] not in self.parent.sendList:
                        print(f"{self.addr[0]} welcomes me!")
                        self.parent.sendList.append(self.addr[0])
            elif cache == "BYE":
                with QMutexLocker(self.parent.tcp_lock):
                    if self.addr[0] in self.parent.sendList:
                        print(f"Okay, {self.addr[0]} close the connection.")
                        self.parent.sendList.remove(self.addr[0])            
            elif cache == "Check Lifecycle":
                self.parent.response = 1
            else:
                print("Unknown Data")
                pass
            print("Video sending list length: " + str(len(self.parent.sendList)))
            self.socket.disconnectFromHost()
            self.finished.emit()
            self.quit()  # Ensure the thread exits after handling the read

    def _handle_tcp_connection(self):
        tcp_cli_sock = self.tcp_server.nextPendingConnection()
        thread = QThread()
        addr = (tcp_cli_sock.peerAddress().toString(),
                tcp_cli_sock.peerPort())
        tcp_cli_sock.setParent(None)  # 解除父对象关联

        worker = self.TCPWorker(tcp_cli_sock, addr, self)
        worker.moveToThread(thread)
        worker.finished.connect(worker.deleteLater)
        worker.finished.connect(thread.quit)
        worker.finished.connect(thread.wait)
        thread.started.connect(worker.run)
        thread.start()

    def tcp_send(self, ip, data='', flag=True, flag2=False):
        """发送TCP消息的接口方法"""
        self.sendTcpData.emit(ip, data, flag, flag2)

    # =============== UDP 部分 ===============

    def UdpOpenListen(self):
        print ("udp try to open port: " + self.portRecv)
        self.UdpSocket.bind(QHostAddress(QHostAddress.SpecialAddress.Any), int(self.portRecv), QAbstractSocket.BindFlag.ShareAddress)

    def UdpCloseListen(self):
        print ("udp try to close port: " + self.portRecv)
        self.UdpSocket.close()

    def sendData(self, ip_address:str, port:str, message): #ipaddress:str    
        print(self.type3)        
        if self.type3 == "Topo":
            self.dataGram = QByteArray(message.encode('utf-8'))
        elif self.type3 == "Video":  # 处理 bytes 类型
            self.dataGram = QByteArray(message)  # 假设 message 是 QByteArray 或兼容类型
        else:
            print("Error")
            pass
    # 或者直接使用：
        if port == "0":
            port = self.portSend
        if(ip_address != "NONE"):
            self.UdpSocket.writeDatagram(self.dataGram,
                                        QHostAddress(ip_address),
                                        int(port))
        else:
            for item in self.sendList:
                print("Sending Video/Audio MSG to " + item + ":" + str(port))
                self.UdpSocket.writeDatagram(self.dataGram,
                                        QHostAddress(item),
                                        int(port))
    @pyqtSlot()
    def recvData(self):
        while self.UdpSocket.hasPendingDatagrams():
            datagram = QByteArray()
            datagram.resize(self.UdpSocket.pendingDatagramSize())
            [recvbytes, host, _] = self.UdpSocket.readDatagram(datagram.size())
            print("Received " + self.type3)
            if self.type3 == "Topo":
               # print(recvbytes.decode("utf-8"))
                return (recvbytes.decode("utf-8"),host)
            elif self.type3 == "Video":
                self.video_data_received.emit(bytes(recvbytes))  # 发射原始字节数据
    '''@pyqtSlot()
    def recvData(self):
        while(self.UdpSocket.hasPendingDatagrams()): 
            self.dataGram = QByteArray()
            self.dataGram.resize(self.UdpSocket.pendingDatagramSize())
            [tempbytes, host, _] = self.UdpSocket.readDatagram(self.dataGram.size())
            if self.type3 == "Topo":
                print("Received Topo MSG")
                return (tempbytes.decode("utf-8"), host)
            else:
                print("Received Other MSG")
                return (tempbytes, host)'''
    def hasPendingDatagrams(self):
        return self.UdpSocket.hasPendingDatagrams()