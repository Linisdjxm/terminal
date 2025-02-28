# 1. 控件名称含义
# 2. Dev与Com功能拆分
# 3. Print打印信息，添加打印来源
# 4. 格式化函数注释
# 5. 私有函数与开放函数的封装
# 6. 变量名称选择

# -*- coding: utf-8 -*-
'''
@File    :   DevCamera.py
@Time    :   2024/12
@Author  :   CRC1109 
@Version :   1.0
@Desc    :   Built in PyQt5
             
'''

from PyQt5.QtWidgets import QLabel, QCheckBox, QPushButton, QComboBox, QTextEdit
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
import cv2
import numpy as np
import time

from Sources.Device.DevBase import DevBase

class DevCamera(DevBase):
    def __init__(self, name:str, **kwargs):
        """Virtual Camera device

        Args:
            name (str): the name defined by developer of the Camera device
            **kwargs (dict): the Qt Gui Object used, should include
                {
                    'CameraObjCheckBox': QCheckBox, Fun:CameraCtl
                    'CameraObjLabel': QLabel, Fun:ShowVedio
                    'CameraObjLabel_2': QLabel, Fun:ShowScreenshot
                    'CameraObjPushButton': QPushButton,Fun:Screenshot
                    'CameraObjComboBox': QComboBox,Fun:ChooseReceiveAndSend
                    'CameraObjTextEdit': QTextEdit,Fun:SendToIP
                    'CameraObjTextEdit_2': QTextEdit,Fun:SendToPort
                    'CameraObjTextEdit_3': QTextEdit,Fun:ReceiveFromPort
                    'CameraObjTextEdit_4': QTextEdit,Fun:ReceiveFromIP
                    'QualityObjComboBox':QComboBox,Fun:ChooseTransQuality
                }
        """
        super(DevCamera,self).__init__(name)

        self.register(**kwargs)

        self.cap = None
        self.CameraRunning = False
        self.pixmap = None
        self.ScreenShot_pixmap = None
        self.fps = None
        self.sendtoIP = None
        self.sendtoportort = None
        self.receivefromIP = None
        self.receivefromport = None
        self.SendFlag = False
        self.ReceiveFlag = False
        self.nparr = None
        self.frame = None
        self.showframe = None
        self.quality = 90
        self.send_socket = QUdpSocket()
        self.receive_socket = QUdpSocket()
#本机IP:192.168.31.65
#可使用端口:3000,3001


    def register(self, **kwargs):
        self.CameraObjCheckBox:QCheckBox = kwargs.get('CameraObjCheckBox')
        self.CameraObjLabel:QLabel = kwargs.get('CameraObjLabel')
        self.CameraObjLabel_2:QLabel = kwargs.get('CameraObjLabel_2')
        self.CameraObjPushButton:QPushButton = kwargs.get('CameraObjPushButton')
        self.SendToIP:QTextEdit = kwargs.get('CameraObjTextEdit')
        self.SendToPort:QTextEdit = kwargs.get('CameraObjTextEdit_2')
        self.ReceiveFromIP:QTextEdit = kwargs.get('CameraObjTextEdit_4')
        self.ReceiveFromPort:QTextEdit = kwargs.get('CameraObjTextEdit_3')
        self.CameraObjComboBox:QComboBox = kwargs.get('CameraObjComboBox')
        self.CameraObjComboBox.addItem("全部暂停")
        self.CameraObjComboBox.addItem("传输状态")
        self.CameraObjComboBox.addItem("接收状态")
        self.QualityObjComboBox:QComboBox = kwargs.get('QualityObjComboBox')
        self.QualityObjComboBox.addItem("90")
        self.QualityObjComboBox.addItem("60")
        self.QualityObjComboBox.addItem("30")
        

    def ready(self):
        self.CameraObjCheckBox.stateChanged.connect(self.CameraState)
        self.CameraObjPushButton.clicked.connect(self.ScreenShot)
        self.CameraObjComboBox.currentIndexChanged.connect(self.on_combobox_index_changed)
        self.SendToIP.textChanged.connect(self.on_text_changed)
        self.SendToPort.textChanged.connect(self.on_text_changed_2)
        self.ReceiveFromIP.textChanged.connect(self.on_text_changed_3)
        self.ReceiveFromPort.textChanged.connect(self.on_text_changed_4)
        self.destroyed.connect(self.release_resources)

    def release_resources(self):
        self.cap.release()

    def on_text_changed(self):
        self.sendtoIP = self.SendToIP.toPlainText()

    def on_text_changed_2(self):
        self.sendtoport = self.SendToPort.toPlainText()

    def on_text_changed_3(self):
        self.receivefromIP = self.ReceiveFromIP.toPlainText()

    def on_text_changed_4(self):
        self.receivefromport = self.ReceiveFromPort.toPlainText()
    
    def on_quality_index_changed(self,index):
        selected_state = self.CameraObjComboBox.itemText(index)
        if selected_state == "90":
            self.quality = 90
        elif selected_state == "60":
            self.quality = 60
        else:
            self.quality = 30
    
    def on_combobox_index_changed(self, index):
        selected_state = self.CameraObjComboBox.itemText(index)
        print(f"Selected state: {selected_state}")
        # 这里可以根据不同的状态执行不同的操作
        if selected_state == "传输状态":
            if self.sendtoIP and self.sendtoport:
                if self.CameraRunning == True:
                    self.SendFlag = True
                    self.ReceiveFlag = False
                    print("开始传输...")
                    self.Startsend()
                else:
                    print("摄像头未工作，无传输源")
                    self.CameraObjComboBox.setCurrentText("全部暂停")
            else:
                print("无有效地址")
                self.CameraObjComboBox.setCurrentText("全部暂停")
        elif selected_state == "接收状态":
            if self.receivefromIP and self.receivefromport:
                if self.CameraRunning == False:
                    self.SendFlag = False
                    self.ReceiveFlag = True
                    print("开始接收...")
                    self.Startreceive()
                else:
                    print("摄像正在工作，请关闭摄像头后再试")
                    self.CameraObjComboBox.setCurrentText("全部暂停")
            else:
                print("无有效地址")
                self.CameraObjComboBox.setCurrentText("全部暂停")
        elif selected_state == "全部暂停":
            self.SendFlag = False
            self.ReceiveFlag = False
            print("暂停所有操作...")
            self.allstop()

    def Startreceive(self):
        self.receive_socket.bind(QHostAddress(self.receivefromIP), int(self.receivefromport))
        self.receive_socket.readyRead.connect(self.receive_data)
        """if self.cap is not None:
                if self.ReceiveFlag == True:
                    self.CameraRunning = False
                    self.cap.release()
                    self.CameraObjCheckBox.setChecked(False)
                    print("摄像头已关闭，资源已释放")
        """

    def receive_data(self):
        while self.receive_socket.hasPendingDatagrams():
            datagram, host, port = self.receive_socket.readDatagram(self.receive_socket.pendingDatagramSize())
            # 解码数据，此处需要根据发送端的编码格式进行解码
            # 例如，如果是 JPEG 格式，可以这样解码
            self.nparr = np.frombuffer(datagram, np.uint8)
            self.frame = cv2.imdecode(self.nparr, cv2.IMREAD_COLOR)
            if self.frame is not None:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
                self.CameraObjLabel.setPixmap(QPixmap.fromImage(self.img))
                self.pixmap = QPixmap.fromImage(self.img)
            else:
                print("接收端编码失败")

    def Startsend(self):
        self.send_socket.connectToHost(QHostAddress(self.sendtoIP), int(self.sendtoport))  

      
    def allstop(self):
        if self.send_socket.state() == QUdpSocket.ConnectedState:
            self.send_socket.disconnectFromHost()
        if self.receive_socket.state() == QUdpSocket.BoundState:
            self.receive_socket.close() 

    def init_camera(self):
        # 打开USB摄像头
        self.cap = cv2.VideoCapture(0)

        # 如果有其他摄像头的话（IP摄像头相关代码，这里可以根据实际需求添加更完善的逻辑来切换摄像头类型）
        # camera_url_ip = 'http://admin:admin@192.168.1.101:8081/'
        # 创建一个VideoCapture
        # self.cap = cv2.VideoCapture(camera_url_ip)

        print('IP摄像头是否开启： {}'.format(self.cap.isOpened()))

        # 显示缓存数
        print(self.cap.get(cv2.CAP_PROP_BUFFERSIZE))
        # 设置缓存区的大小
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # 调节摄像头分辨率（这里可以后续添加代码根据需求设置具体分辨率）
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        print('width:', self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        print('height:', self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 设置FPS
        self.fps = 30
        print('FPS值为:', self.cap.set(cv2.CAP_PROP_FPS, self.fps))
        print(self.cap.get(cv2.CAP_PROP_FPS))

    def show_camera_feed(self):
       while self.CameraRunning:
            ret, self.frame = self.cap.read()
            cv2.waitKey(1)
            self.showframe = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.img = QImage(self.showframe.data, self.showframe.shape[1], self.showframe.shape[0], QImage.Format_RGB888)
            #scaled_pixmap = pixmap.scaled(self.CameraObjLabel.size(), Qt.KeepAspectRatio)
            self.CameraObjLabel.setPixmap(QPixmap(self.img))
            #self.CameraObjLabel.setPixmap(QPixmap(self.img).scaled(self.CameraObjLabel.size(), Qt.KeepAspectRatio))
            self.pixmap = QPixmap(self.img)
            if self.SendFlag == True:
                # 编码帧为 JPEG 格式
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
                #ret, self.frame = self.cap.read()
                result, imgencode = cv2.imencode('.jpg', self.frame, encode_param)
                data = np.array(imgencode)
                string_data = data.tobytes()
                # 发送数据
                self.send_socket.writeDatagram(string_data, QHostAddress(self.sendtoIP), int(self.sendtoport))
            time.sleep(0.04)

    def CameraState(self, state):
        if state == Qt.Checked:
            self.init_camera()
            if not self.cap.isOpened():
                print("摄像头打开失败，请检查设备连接或驱动问题")
                return
            self.CameraRunning = True
            self.show_camera_feed()
        else:
            if self.cap is not None:
                self.CameraRunning = False
                if self.SendFlag == True:
                    self.SendFlag = False
                    self.CameraObjComboBox.setCurrentText("全部暂停")
                    print("传输已停止")
                self.cap.release()
                print("摄像头已关闭，资源已释放")

    def ScreenShot(self):
        if self.CameraRunning == False and self.ReceiveFlag == False:
            print("无视频源，无法截图")
        else:
            self.ScreenShot_pixmap = self.pixmap
            self.CameraObjLabel_2.setPixmap(self.ScreenShot_pixmap)
