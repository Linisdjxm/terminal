#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   DevLed.py
@Time    :   2024/10/18 19:08:21
@Author  :   CRC1109 
@Version :   1.0
@Desc    :   Built in PyQt5
             虚拟LED设备, 功能需要
             - QLabel 虚拟LED呈现形式
'''

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QColor

from Sources.Device.DevBase import DevBase

class DevLed(DevBase):
    def __init__(self, name:str, **kwargs):
        """Virtual LED device

        Args:
            name (str): the name defined by developer of the Led device
            **kwargs (dict): the Qt Gui Object used, should include
                {
                    'LedObjLabel': QLabel
                }
        """
        super(DevLed,self).__init__(name)

        self.register(**kwargs)

        self.colorClose = Qt.GlobalColor.gray
        self.colorOpen = Qt.GlobalColor.red
        self.colorCurrent = Qt.GlobalColor.gray

        # 频闪模式参数
        self.blinkPeriod = 1500
        self.blinkInterval = 150
        self.blinkNumber = 3
        # 创建闪烁间隔定时器
        self.blinkIntervalTimer = QTimer(self)
        self.blinkIntervalTimer.timeout.connect(self.__toggleBlinking)
        # 创建闪烁周期定时器
        self.blinkPeriodTimer = QTimer(self)
        self.blinkPeriodTimer.timeout.connect(self.__startBlinking)
        # 闪烁过程控制参数
        self.blinkCount = 0
        self.blinking = False
        
    def register(self, **kwargs):
        self.LedObjLabel:QLabel = kwargs.get('LedObjLabel')

    def ready(self):
        self.ctlChangeSize(50)
        self.close()

    def open(self):
        self.blinkPeriodTimer.stop()
        self.blinkIntervalTimer.stop()
        self.blinkCount = 0
        self.blinking = False
        self.ctlChangeColor(self.colorOpen)
    
    def close(self):
        self.blinkPeriodTimer.stop()
        self.blinkIntervalTimer.stop()
        self.blinkCount = 0
        self.blinking = False
        self.ctlChangeColor(self.colorClose)

    def ctlChangeSize(self,size:int):
        self.LedObjLabel.setFixedSize(size,size)
    
    def ctlChangeColor(self,color:Qt.GlobalColor):
        self.colorCurrent = color
        self.LedObjLabel.setStyleSheet(f"QLabel {{ background-color: {QColor(color).name()}; border-radius: 25px;}}")

    def ctlBlinkParam(self,blinkNumber:int):
        self.blinkNumber = blinkNumber
        self.blinkPeriodTimer.start(self.blinkPeriod)

    @pyqtSlot()
    def __toggleBlinking(self):
        if self.colorCurrent == self.colorClose:
            self.ctlChangeColor(self.colorOpen)
        else:
            self.ctlChangeColor(self.colorClose)
        self.blink_count += 1
        if self.blink_count >= self.blinkNumber*2:
            self.blinking = False
            self.blinkIntervalTimer.stop()
            self.blinkPeriodTimer.start(self.blinkPeriod)

    @pyqtSlot()
    def __startBlinking(self):
        if not self.blinking:
            self.blinking = True
            self.blink_count = 0
            self.blinkIntervalTimer.start(150)
