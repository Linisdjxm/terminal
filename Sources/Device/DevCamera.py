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
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal, QSize, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui
import cv2
import numpy as np
import time

from Sources.Device.DevBase import DevBase
from Sources.Device.DevNIC import DevNIC
from Config.Config import Config

class ReceiveThread(QThread):
    def __init__(self, devNIC, parent):
        super().__init__()
        self.devNIC = devNIC
        self.is_running = True
        self.send_flag = False
        self.parent = parent
    def run(self):
        while self.devNIC.hasPendingDatagrams():
            datagram, host=  self.devNIC.recvData()
            # 解码数据，此处需要根据发送端的编码格式进行解码
            # 例如，如果是 JPEG 格式，可以这样解码
            self.nparr = np.frombuffer(datagram, np.uint8)
            self.frame = cv2.imdecode(self.nparr, cv2.IMREAD_COLOR)
            if self.frame is not None:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
                self.parent.CameraObjLabel.setPixmap(QPixmap.fromImage(self.img))
            else:
                print("接收端编码失败")

class CameraThread(QThread):
    frame_ready = pyqtSignal(QPixmap, np.ndarray)  # 新增信号用于传递帧数据

    def __init__(self, cap, quality, devNIC, sendtoIP, sendtoport):
        super().__init__()
        self.cap = cap
        self.quality = quality
        self.devNIC = devNIC
        self.sendtoIP = sendtoIP
        self.sendtoport = sendtoport
        self.is_running = True
        self.send_flag = False

    def run(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # 处理显示帧
            show_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(show_frame.data, show_frame.shape[1], show_frame.shape[0], 
                       QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            
            # 发送信号到主线程更新UI
            #self.frame_ready.emit(pixmap, frame)
            
            # 处理传输逻辑
            if self.is_running:
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
                _, imgencode = cv2.imencode('.jpg', frame, encode_param)
                data = imgencode.tobytes()
                self.devNIC.sendData("NONE", "0", data)

            self.msleep(25)  # 更合适的延迟方式

    def stop(self):
        self.is_running = False
        self.wait()

class DevCamera(DevBase):
    def __init__(self, name:str, topology, focus, **kwargs):
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

        self.devNIC = DevNIC('NIC设备实现',"UDP", type3 = "Video", sendList = focus.devNIC.sendList)
        self.devNIC.ready()
        self.devNIC.video_data_received.connect(self.handle_video_data)        
        self.configList = Config()
        self.camera_thread = None  # 新增线程对象
        self.cap = None
        self.CameraRunning = False
        self.pixmap = None
        self.ScreenShot_pixmap = None
        self.fps = None
        self.sendtoIP = None
        self.sendtoport = self.configList.getConfigItem("VideoSendToPort")
        self.receivefromIP = None
        self.receivefromport = self.configList.getConfigItem("VideoReceiveFromPort")
        self.SendFlag = False
        self.ReceiveFlag = False
        self.nparr = None
        self.frame = None
        self.showframe = None
        self.quality = 90
        self.send_socket = QUdpSocket()
        self.receive_socket = QUdpSocket()
        self.FirstRun = 1

        screen_geometry = QApplication.desktop().screenGeometry()
        self.display_size = QSize(
            int(screen_geometry.width() * 0.8),
            int(screen_geometry.height() * 0.8)
        )


        self.topology = topology
        self.focus = focus
        self.devNIC.UdpOpenListen()
    def register(self, **kwargs):
        self.CameraObjCheckBox:QCheckBox = kwargs.get('CameraObjCheckBox')
        self.CameraObjLabel:QLabel = kwargs.get('CameraObjLabel')
        self.QualityObjComboBox:QComboBox = kwargs.get('QualityObjComboBox')
        self.QualityObjComboBox.addItem("90")
        self.QualityObjComboBox.addItem("60")
        self.QualityObjComboBox.addItem("30")
        

    def ready(self):
        self.CameraObjCheckBox.stateChanged.connect(self.CameraState)
        #self.CameraObjPushButton.clicked.connect(self.ScreenShot)
        if self.CameraObjCheckBox.isChecked():
            self.CameraState(Qt.Checked)
        #self.thread1 = ReceiveThread(self.devNIC, self)
        #self.thread1.start()
        self.QualityObjComboBox.currentIndexChanged.connect(self.on_quality_index_changed)
        self.destroyed.connect(self.release_resources)

    def release_resources(self):
        self.cap.release()

    def on_quality_index_changed(self,index):
        selected_state = self.QualityObjComboBox.itemText(index)
        if selected_state == "90":
            self.quality = 90
        elif selected_state == "60":
            self.quality = 60
        else:
            self.quality = 30
    def handle_video_data(self, data):
        nparr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            scaled_pixmap = QPixmap.fromImage(img).scaled(
            self.CameraObjLabel.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
            )
            self.CameraObjLabel.setPixmap(scaled_pixmap)
            #self.CameraObjLabel.setPixmap(QPixmap.fromImage(img))
    def on_combobox_index_changed(self, index):
        selected_state = self.QualityObjComboBox.itemText(index)
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
                    self.QualityObjComboBox.setCurrentText("全部暂停")
            else:
                print("无有效地址")
                self.QualityObjComboBox.setCurrentText("全部暂停")
        elif selected_state == "接收状态":
            if self.receivefromIP and self.receivefromport:
                if self.CameraRunning == False:
                    self.SendFlag = False
                    self.ReceiveFlag = True
                    print("开始接收...")
                    self.Startreceive()
                else:
                    print("摄像正在工作，请关闭摄像头后再试")
                    self.QualityObjComboBox.setCurrentText("全部暂停")
            else:
                print("无有效地址")
                self.QualityObjComboBox.setCurrentText("全部暂停")
        elif selected_state == "全部暂停":
            self.SendFlag = False
            self.ReceiveFlag = False
            print("暂停所有操作...")
            self.allstop()

    def receive_data(self):
        while self.devNIC.hasPendingDatagrams():
            datagram, host=  self.devNIC.recvData()

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
        #print('IP摄像头是否开启： {}'.format(self.cap.isOpened()))
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


    def show_camera_feed(self, pixmap, frame):
    # 直接使用label当前尺寸进行缩放
        #print(self.CameraObjLabel.size())
        scaled_pixmap = pixmap.scaled(
            self.CameraObjLabel.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.CameraObjLabel.setPixmap(scaled_pixmap)
    def CameraState(self, state):
        if state == Qt.Checked:
            self.init_camera()
            if not self.cap.isOpened():
                print("摄像头打开失败，请检查设备连接或驱动问题")
                return

            # 创建并启动摄像头线程
            self.camera_thread = CameraThread(
                self.cap, self.quality, self.devNIC,
                self.sendtoIP, self.sendtoport
            )
            self.camera_thread.frame_ready.connect(self.show_camera_feed)
            self.camera_thread.send_flag = self.SendFlag
            self.CameraRunning = True
            if self.FirstRun == 1:
                self.FirstRun = 0
                self.init_timer = QTimer()
                self.init_timer.timeout.connect(self._delayed_init)
                self.init_timer.start(100)  # 每100ms检查一次
            else:
                self.camera_thread.start()
        else:
            self.CameraRunning = False
            if self.camera_thread:
                self.camera_thread.stop()
                self.camera_thread = None
            if self.cap:
                self.cap.release()
            print("摄像头已关闭，资源已释放")
    def _delayed_init(self):
        """异步初始化方法"""
        if len(self.topology.detectedIP) > 0:
            # 当检测到IP地址时停止定时器
            self.init_timer.stop()
            # 执行原有初始化操作
            self.camera_thread.start()
    def ScreenShot(self):
        if self.CameraRunning == False and self.ReceiveFlag == False:
            print("无视频源，无法截图")
        else:
            self.ScreenShot_pixmap = self.pixmap
            self.CameraObjLabel_2.setPixmap(self.ScreenShot_pixmap)
