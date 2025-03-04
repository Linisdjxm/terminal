# -*- coding: utf-8 -*-
'''
@File    :   DevCamera.py
@Time    :   2024/12
@Author  :   CRC1109 
@Version :   1.0
@Desc    :   Built in PyQt5
             
'''
from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot
#from PyQt5.QtNetwork import QTcpServer, QHostAddress

from Sources.Component.ComBaseFun import ComBaseFun
from Sources.Device.DevCamera import DevCamera

class ComCameraFun(ComBaseFun):
    def __init__(self, name:str, topology, focus, **kwargs):
        """Camera control function demo component

        Args:
            name (str): the name defined by developer of the Camera Demo function
            **kwargs (dict): the Qt Gui Object used, should include
                {
                    'CameraObjCheckBox': QCheckBox, Fun:CameraCtl
                    'CameraObjLabel': QLabel, Fun:ShowVedio
                    'CameraObjPushButton': QPushButton,Fun:Screenshot
                    'CameraObjPushButton_2': QPushButton,Fun:SaveScreenshot
                    'QualityObjComboBox': QComboBox,Fun:
                }
        """
        super(ComCameraFun,self).__init__(name)

        self.register(topology, focus, **kwargs)
        self.ready()

        #self.server = QTcpServer(self)
        #if not self.server.listen(QHostAddress.LocalHost, 6666):
           # self.browser.append(self.server.errorString())

    def register(self, topology, focus, **kwargs):
        #self.CameraObjPushButton_2:QPushButton = kwargs.get('CameraObjPushButton_2')
        self.devCamera = DevCamera('Camera设备', topology, focus, **{'CameraObjCheckBox':kwargs.get('CameraObjCheckBox'),
                                                 'CameraObjLabel':kwargs.get('CameraObjLabel'),
                                                 'QualityObjComboBox':kwargs.get('QualityObjComboBox')
                                                 })
        
    def ready(self):
        #self.CameraObjPushButton_2.clicked.connect(self.SaveScreenShot)
        self.devCamera.ready()

    @pyqtSlot()
    def SaveScreenShot(self):
        if self.devCamera.ScreenShot_pixmap == None:
            print("暂无截图可供保存")
        else:
            file_path, _ = QFileDialog.getSaveFileName(self.devCamera.CameraObjLabel_2, "选择图像保存路径", "",
                                                   "Images (*.png *.jpg *.bmp);;All Files (*)")
            if file_path:
                image = self.devCamera.ScreenShot_pixmap.toImage()
                if image.save(file_path):
                    print(f"图像已成功保存至 {file_path}")
                else:
                    print(f"保存图像失败，请检查文件路径和权限等问题")