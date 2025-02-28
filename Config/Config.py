# -*- coding: utf-8 -*-
'''
@File    :   DevCamera.py
@Time    :   2025/02
@Author  :   Author
@Version :   1.0
@Desc    :   Built in PyQt5
             配置文件
             
'''
from Config.ConfBase import ConfBase

class Config(ConfBase):
    def __init__(self):
        super(Config, self).__init__()
        self._Config = {
            'DeviceName':"Device 1",
            'StrSendToPort':"50505",
            'StrReceiveFromPort':"50506",
            'VideoSendToPort':"50510",
            'VideoReceiveFromPort':"50511"
        }
    def getConfigItem(self, item:str):
        return self._Config.get(item)
