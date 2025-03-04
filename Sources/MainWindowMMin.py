#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   MainWindowPro.py
@Time    :   2025/03
@Author  :   L 
@Version :   1.0
@Desc    :   Built in PyQt5
             网络演示系统的地终端主界面逻辑控制
             主界面设计文件为 MainWindowMMin.ui->Ui_MainWindowMMin.py
'''

from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Forms.Ui_MainWindowMMin import Ui_MainWindowMMin
from Sources.Component.ComTimeFun import ComTimeFun
from Sources.Component.ComChatFun import ComChatFun
from Sources.Component.ComCameraFun import ComCameraFun
from Sources.Component.ComMapPresentationFun import ComMapPresentationFun
from Sources.Component.ComTopologyFun import ComTopologyFun
from Sources.Component.ComFocusFun import ComFocusFun


class MainWindowMMin(QMainWindow,Ui_MainWindowMMin):
    def __init__(self, parent=None) -> None:
        super(MainWindowMMin,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("网络演示系统：终端")
        self.reMap()
        #self.setWindowState(Qt.WindowState.WindowMaximized)
        self.initComponent()
    def reMap(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        screen_geometry = QApplication.desktop().screenGeometry()
        width = int(screen_geometry.width() * 0.8)
        height = int(screen_geometry.height() * 0.8)
        self.label.setGeometry(QtCore.QRect(0, 0, width, height))
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter) 
        self.layout.addWidget(self.label)

        self.setFixedSize(width, height)    
        self.pushButton.setGeometry(QtCore.QRect(10, height // 2, int(width / 9.5), int(height / 8.6)))
        self.pushButton_2.setGeometry(QtCore.QRect(width - int(width / 9.5) - 10, height // 2, int(width / 9.5), int(height / 8.6)))
        
    def initComponent(self):
        self.comTopologyFun = ComTopologyFun("网络结构组件")
        #self.comTimeFun = ComTimeFun("Time显示功能示例组件",**{'TimeObjLabel':self.TimeObjLabel,#'paramTestSize':40})
        #
        #self.comChatFun = ComChatFun("信令传输功能示例组件",**{ 'qTextbrowser':self.qTextbrowser,
        #                                                    'sendfileButton':self.sendfileButton,
        #                                                    'sendButton':self.sendButton,
        #                                                    'InputtextEdit':self.InputtextEdit,
        #                                                    'hostlineEdit':self.textEdit,
        #                                                    'portSendlineEdit':self.portSendlineEdit,
        #                                                    'portRecvlineEdit':self.portRecvlineEdit,
        #                                                    'startListenButton':self.startListenButton})
        #
        self.comFocusFun = ComFocusFun("Focus组件", self.comTopologyFun, **{
                                                            'FocusPrevPushButton':self.pushButton,
                                                            'FocusNextPushButton_2':self.pushButton_2,
                                                            })
        self.comCameraFun = ComCameraFun("Camera组件", self.comTopologyFun, self.comFocusFun, **{
                                                            'CameraObjCheckBox':self.checkBox,
                                                            'CameraObjLabel':self.label,
                                                            'QualityObjComboBox':self.comboBox
                                                            })
#
        #self.comMapPresentationFun = ComMapPresentationFun("地图展示功能示例组件",**{'mapShowWebengine':self.#mapShowWebengine,
        #                                                                            'uavlistCombox':self.#uavlistCombox,
        #                                                                            'downPushButton':self.#downPushButton,
        #                                                                            'goaheadPushButton':self.#goaheadPushButton,
        #                                                                            'gobackPushButton':self.#gobackPushButton,
        #                                                                            'landPushButton':self.#landPushButton,
        #                                                                            'leftmovePushButton':self.#leftmovePushButton,
        #                                                                            'rightmovePushButton':self#.rightmovePushButton,
        #                                                                            'stopPushButton':self.#stopPushButton,
        #                                                                            'takeoffPushButton':self.#takeoffPushButton,
        #                                                                            'upPushButton':self.#upPushButton,
        #                                                                            'checklogPushButton':self.#checklogPushButton,
        #                                                                            'cleartrackPushButton':sel#f.cleartrackPushButton,
        #                                                                            'returnPushButton':self.#returnPushButton,
        #                                                                            'getinfoPushButton':self.#getInfoPushButton,
        #                                                                            'setpointPushButton':self.#setpointPushButton,
        #                                                                            'devNic':self.comChatFun.devNIC})



    