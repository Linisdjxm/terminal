'''
@File    :   ComTimeFun.py
@Time    :   2024/10/27 17:09
@Version :   1.0
@Desc    :   Built in PyQt5
             Time控制功能示例组件, 功能需要
             - QLabel 虚拟Time呈现形式
'''

from PyQt5.QtCore import Qt

from Sources.Component.ComBaseFun import ComBaseFun
from Sources.Device.DevTime import DevTime

class ComTimeFun(ComBaseFun):
    def __init__(self, name:str, **kwargs):
        super(ComTimeFun,self).__init__(name)

        self.register(**kwargs)
        self.ready()

    def register(self, **kwargs):
        self.devtime = DevTime('Time显示功能示例组件-Time设备', **kwargs)

    def ready(self):
        self.devtime.ready()