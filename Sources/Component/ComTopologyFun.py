from time import sleep
from Sources.Component.ComBaseFun import ComBaseFun
from Sources.Device.DevNIC import DevNIC
from Config.Config import Config
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class SendConnectPackThread(QThread):
    def __init__(self, devNIC, configList):
        super().__init__()
        self.devNIC = devNIC
        self.configList = configList

    def run(self):
        broadcastIP = '255.255.255.255'
        broadcastPort = str(self.configList.getConfigItem("StrSendToPort"))
        print("running!")
        while True:
            self.devNIC.sendData(broadcastIP, broadcastPort, "Topology" + 
                                 self.configList.getConfigItem("DeviceName"))
            sleep(1)

class ReceiveConnectPackThread(QThread):
    def __init__(self, devNIC, configList, detectedIP, IP2Name):
        super().__init__()
        self.devNIC = devNIC
        self.configList = configList
        self.detectedIP = detectedIP
        self.IP2Name = IP2Name

    def run(self):
        HOST = ''
        print("2running!")
        PORT = str(self.configList.getConfigItem("StrReceiveFromPort"))
        self.devNIC.UdpOpenListen()
        while True:
            topoInfo = self.devNIC.recvData()
            if topoInfo and topoInfo[0][:8] == "Topology" and topoInfo[1].toString() not in self.detectedIP:
                self.detectedIP.append(topoInfo[1].toString())
                self.IP2Name.append(topoInfo[0][8:])
                print(topoInfo[1].toString())
            sleep(1)

class ComTopologyFun(ComBaseFun):
    def __init__(self, name: str):
        super(ComTopologyFun, self).__init__(name)
        self.detectedIP = []
        self.IP2Name = []
        self.configList = Config()
        self.devNIC = DevNIC('NIC设备实现')
        self.devNIC.ready()
        self.ready()

    def ready(self):
        self.thread1 = SendConnectPackThread(self.devNIC, self.configList)
        self.thread2 = ReceiveConnectPackThread(self.devNIC, self.configList, self.detectedIP, self.IP2Name)
        self.thread1.start()
        self.thread2.start()



