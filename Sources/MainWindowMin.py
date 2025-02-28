#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   MainWindowMin.py
@Time    :   2024/10/18 16:08:30
@Author  :   WangXi 
@Version :   1.0
@Desc    :   Built in PyQt5
             网络演示系统的移动终端主界面逻辑控制
             主界面设计文件为 MainWindowMin.ui->Ui_MainWindowMin.py
'''

from PyQt5.QtWidgets import QMainWindow

from Forms.Ui_MainWindowMin import Ui_MainWindowMin
from Sources.Component.ComLedFun import ComLedFun
from Sources.Component.ComTimeFun import ComTimeFun

class MainWindowMin(QMainWindow,Ui_MainWindowMin):
    def __init__(self, parent=None) -> None:
        super(MainWindowMin,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("网络演示系统：移动终端")

        self.initComponent()

    def initComponent(self):
        self.comLedFun = ComLedFun("LED控制功能示例组件",**{ 'LedConfirmPushButton':self.LedConfirmPushButtonMin,
                                                            'LedOptionsComboBox':self.LedOptionsComboBoxMin,
                                                            'LedObjLabel':self.LedObjLabelMin})
        self.comLedFun.devLed.ctlChangeSize(100)

        self.comTimeFun =ComTimeFun("Time显示功能示例组件",**{'TimeObjLabel':self.TimeObjLabelMin})

        
        