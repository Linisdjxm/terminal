# -*- coding: utf-8 -*-
'''
@File    :   ComFocusFun.py
@Time    :   2025/03
@Author  :   L 
@Version :   1.0
@Desc    :   Built in PyQt5
             
'''
from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
#from PyQt5.QtNetwork import QTcpServer, QHostAddress

from Sources.Component.ComBaseFun import ComBaseFun
from Sources.Device.DevNIC import DevNIC
from Config.Config import Config

class ComFocusFun(ComBaseFun):
    def __init__(self, name:str, topology, **kwargs):

        super(ComFocusFun,self).__init__(name)
        self.register(**kwargs)
        self.focuson = 0
        self.topology = topology
        self.devNIC = DevNIC('NIC设备实现',"TCP")
        self.init_timer = QTimer()
        self.init_timer.timeout.connect(self._delayed_init)
        self.init_timer.start(100)  # 每100ms检查一次
        #self.ready()

    def _delayed_init(self):
        """异步初始化方法"""
        if len(self.topology.detectedIP) > 0:
            # 当检测到IP地址时停止定时器
            self.init_timer.stop()
            # 执行原有初始化操作
            self.ready()

    def register(self, **kwargs):
        #self.CameraObjPushButton_2:QPushButton = kwargs.get('CameraObjPushButton_2')
        self.FocusPrevPushButton:QPushButton = kwargs.get('FocusPrevPushButton')
        self.FocusNextPushButton_2:QPushButton = kwargs.get('FocusNextPushButton_2')
        #print("step1")
    def ready(self):
        #self.CameraObjPushButton_2.clicked.connect(self.SaveScreenShot)
        self.FocusPrevPushButton.clicked.connect(self.PrevItem)
        self.FocusNextPushButton_2.clicked.connect(self.NextItem)
        self.devNIC.tcp_send(self.topology.detectedIP[self.focuson])
    @pyqtSlot()
    def PrevItem(self):
        print(self.topology.detectedIP[0])
        self.devNIC.tcp_send(self.topology.detectedIP[self.focuson],flag=False)
        self.focuson -= 1
        if self.focuson < 0:
            print("Go to the end")
            self.focuson = len(self.topology.detectedIP) - 1
        self.devNIC.tcp_send(self.topology.detectedIP[self.focuson])
    @pyqtSlot()
    def NextItem(self):
        print(self.topology.detectedIP[0])
        self.devNIC.tcp_send(self.topology.detectedIP[self.focuson],flag=False)
        self.focuson += 1
        if self.focuson >= len(self.topology.detectedIP):
            self.focuson = 0
            print("Go to the beginning")
        self.devNIC.tcp_send(self.topology.detectedIP[self.focuson])
