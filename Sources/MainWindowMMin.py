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

        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter) 
        self.layout.addWidget(self.label)

        #self.serTCP_1 = TCPSerThread_1()
        #self.serTCP_1.hold_request.connect(self.hold_R)
        #self.serTCP_1.start()

        #self.startAudio()

        screen_geometry = QApplication.desktop().screenGeometry()
        width = int(screen_geometry.width() * 0.8)
        height = int(screen_geometry.height() * 0.8)
        self.setFixedSize(width, height)
        #self.pushButton.clicked.connect(self.prev_person)
        #self.pushButton_2.clicked.connect(self.next_person)
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
        #self.comCameraFun = ComCameraFun("Camera组件",**{ 'CameraObjCheckBox':self.CameraOPEN,
        #                                                    'CameraObjLabel':self.label,
        #                                                    'CameraObjLabel_2':QtWidgets.QLabel(),
        #                                                    'CameraObjPushButton':self.pushButton,
        #                                                    'CameraObjPushButton_2':self.pushButton_2,
        #                                                    'CameraObjTextEdit':self.textEdit,
        #                                                    'CameraObjTextEdit_2':self.textEdit_2,
        #                                                    'CameraObjTextEdit_3':self.textEdit_3,
        #                                                    'CameraObjTextEdit_4':self.textEdit_4,
        #                                                    'CameraObjComboBox':self.comboBox,
        #                                                    'QualityObjComboBox':self.comboBox_2
        #                                                    })
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



    