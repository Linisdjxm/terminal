'''
@File    :   DevTime.py
@Time    :   2024/10/27 16:15
@Version :   1.0
@Desc    :   Built in PyQt5
             虚拟Time设备, 功能需要
             - QLabel 虚拟Time呈现形式
'''

from Sources.Device.DevBase import DevBase

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtCore import QDateTime

class DevTime(DevBase):
    def __init__(self, name:str, **kwargs):

        super(DevTime,self).__init__(name)

        self.register(**kwargs)
        self.paramTestSize:int = kwargs.get('paramTestSize')

    def register(self, **kwargs):
        self.TimeObjLabel:QLabel = kwargs.get('TimeObjLabel')

    def ready(self):
        self.Timer = QTimer()
        self.Timer.start(100) 
        self.Timer.timeout.connect(self.updateTime)
        self.paramSize = str(self.paramTestSize) + "px"
        self.TimeObjLabel.setStyleSheet(f"QLabel {{ font-size: {self.paramSize}}}")

    @pyqtSlot()
    def updateTime(self):
        time = QDateTime.currentDateTime()
        timePlay = time.toString('yyyy-MM-dd hh:mm:ss.zzz dddd')
        self.TimeObjLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.TimeObjLabel.setText(timePlay)


    
