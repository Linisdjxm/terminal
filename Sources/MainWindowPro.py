#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   MainWindowPro.py
@Time    :   2024/10/18 16:08:20
@Author  :   WangXi 
@Version :   1.0
@Desc    :   Built in PyQt5
             网络演示系统的地面站终端主界面逻辑控制
             主界面设计文件为 MainWindowPro.ui->Ui_MainWindowPro.py
'''

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtWidgets

from Forms.Ui_MainWindowPro import Ui_MainWindowPro
from Sources.Component.ComTimeFun import ComTimeFun
from Sources.Component.ComChatFun import ComChatFun
from Sources.Component.ComCameraFun import ComCameraFun
from Sources.Component.ComMapPresentationFun import ComMapPresentationFun

class MainWindowPro(QMainWindow,Ui_MainWindowPro):
    def __init__(self, parent=None) -> None:
        super(MainWindowPro,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("网络演示系统：地面站终端")
        self.setWindowState(Qt.WindowState.WindowMaximized)
        
        self.initComponent()

    def initComponent(self):
        self.comTimeFun = ComTimeFun("Time显示功能示例组件",**{'TimeObjLabel':self.TimeObjLabel,'paramTestSize':40})
        
        self.comChatFun = ComChatFun("信令传输功能示例组件",**{ 'qTextbrowser':self.qTextbrowser,
                                                            'sendfileButton':self.sendfileButton,
                                                            'sendButton':self.sendButton,
                                                            'InputtextEdit':self.InputtextEdit,
                                                            'hostlineEdit':self.textEdit,
                                                            'portSendlineEdit':self.portSendlineEdit,
                                                            'portRecvlineEdit':self.portRecvlineEdit,
                                                            'startListenButton':self.startListenButton})
        
        self.comCameraFun = ComCameraFun("Camera组件",**{ 'CameraObjCheckBox':self.CameraOPEN,
                                                            'CameraObjLabel':self.label,
                                                            'CameraObjLabel_2':QtWidgets.QLabel(),
                                                            'CameraObjPushButton':self.pushButton,
                                                            'CameraObjPushButton_2':self.pushButton_2,
                                                            'CameraObjTextEdit':self.textEdit,
                                                            'CameraObjTextEdit_2':self.textEdit_2,
                                                            'CameraObjTextEdit_3':self.textEdit_3,
                                                            'CameraObjTextEdit_4':self.textEdit_4,
                                                            'CameraObjComboBox':self.comboBox,
                                                            'QualityObjComboBox':self.comboBox_2
                                                            })

        self.comMapPresentationFun = ComMapPresentationFun("地图展示功能示例组件",**{'mapShowWebengine':self.mapShowWebengine,
                                                                                    'uavlistCombox':self.uavlistCombox,
                                                                                    'downPushButton':self.downPushButton,
                                                                                    'goaheadPushButton':self.goaheadPushButton,
                                                                                    'gobackPushButton':self.gobackPushButton,
                                                                                    'landPushButton':self.landPushButton,
                                                                                    'leftmovePushButton':self.leftmovePushButton,
                                                                                    'rightmovePushButton':self.rightmovePushButton,
                                                                                    'stopPushButton':self.stopPushButton,
                                                                                    'takeoffPushButton':self.takeoffPushButton,
                                                                                    'upPushButton':self.upPushButton,
                                                                                    'checklogPushButton':self.checklogPushButton,
                                                                                    'cleartrackPushButton':self.cleartrackPushButton,
                                                                                    'returnPushButton':self.returnPushButton,
                                                                                    'getinfoPushButton':self.getInfoPushButton,
                                                                                    'setpointPushButton':self.setpointPushButton,
                                                                                    'devNic':self.comChatFun.devNIC})



    