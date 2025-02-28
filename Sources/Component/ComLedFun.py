#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   ComLedFun.py
@Time    :   2024/10/18 17:46:34
@Author  :   CRC1109 
@Version :   1.0
@Desc    :   Built in PyQt5
             LED控制功能示例组件, 功能需要
             - QPushButton 确认键
             - QComboBox LED模式切换选择
             - QLabel 虚拟LED设备(->DevLed)
'''

from PyQt5.QtWidgets import QPushButton,QComboBox
from PyQt5.QtCore import Qt,pyqtSlot

from Sources.Component.ComBaseFun import ComBaseFun
from Sources.Device.DevLed import DevLed

class ComLedFun(ComBaseFun):
    def __init__(self, name:str, **kwargs):
        """LED control function demo component

        Args:
            name (str): the name defined by developer of the Led Demo function
            **kwargs (dict): the Qt Gui Object used, should include
                {
                    'LedConfirmPushButton': QPushButton,
                    'LedOptionsComboBox': QComboBox,
                    'LedObjLabel': QLabel
                }
        """
        super(ComLedFun,self).__init__(name)
        
        self.LEDMODE = {
            '打开指示灯' : 0,
            '关闭指示灯' : 1,
            '指示灯频闪' : 2,
            '指示灯快闪一次' : 3,
            '指示灯快闪两次' : 4,
            '指示灯快闪三次' : 5,
        }

        self.register(**kwargs)
        self.ready()

    def register(self, **kwargs):
        self.ledConfirmPushButton:QPushButton = kwargs.get('LedConfirmPushButton')
        self.ledOptionsComboBox:QComboBox = kwargs.get('LedOptionsComboBox')
        self.devLed = DevLed('LED控制功能示例组件-LED设备',**{'LedObjLabel':kwargs.get('LedObjLabel')})
        
    def ready(self):
        self.ledConfirmPushButton.clicked.connect(self.on_ledConfirmPushButton_clicked)
        self.ledOptionsComboBox.addItems(list(self.LEDMODE.keys()))
        self.devLed.ready()

    @pyqtSlot()
    def on_ledConfirmPushButton_clicked(self):
        if self.ledOptionsComboBox.currentText() == '打开指示灯':
            self.devLed.open()
        elif self.ledOptionsComboBox.currentText() == '关闭指示灯':
            self.devLed.close()
        elif self.ledOptionsComboBox.currentText() == '指示灯频闪':
            self.devLed.blinkPeriod = 0
            self.devLed.blinkInterval = 150
            self.devLed.ctlBlinkParam(1)
        elif self.ledOptionsComboBox.currentText() == '指示灯快闪一次':
            self.devLed.blinkPeriod = 1500
            self.devLed.blinkInterval = 150
            self.devLed.ctlBlinkParam(1)
        elif self.ledOptionsComboBox.currentText() == '指示灯快闪两次':
            self.devLed.blinkPeriod = 1500
            self.devLed.blinkInterval = 150
            self.devLed.ctlBlinkParam(2)
        elif self.ledOptionsComboBox.currentText() == '指示灯快闪三次':
            self.devLed.blinkPeriod = 1500
            self.devLed.blinkInterval = 150
            self.devLed.ctlBlinkParam(3)
        else:
            pass

        


        


