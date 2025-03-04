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
import builtins

class Config(ConfBase):
    def __init__(self):
        super(Config, self).__init__()
        if builtins._DEBUG == 0:
            self._Config = {
            'DeviceName':"Device 1",
            'StrSendToPort':"50505",
            'StrReceiveFromPort':"50506",
            'VideoSendToPort':"50510",
            'VideoReceiveFromPort':"50511",
            'TCPStrSendToPort':"50508",
            'TCPStrReceiveFromPort':"50509",
            'TCPStrSendToPort2':"50512",
            'TCPStrReceiveFromPort2':"50513",
            'OpenCamera':"1"
            }
        else:  
            self._Config = {
            'DeviceName':"Device 2",
            'StrSendToPort':"50506",
            'StrReceiveFromPort':"50505",
            'VideoSendToPort':"50511",
            'VideoReceiveFromPort':"50510",
            'TCPStrSendToPort':"50509",
            'TCPStrReceiveFromPort':"50508",
            'TCPStrSendToPort2':"50513",
            'TCPStrReceiveFromPort2':"50512",
            'OpenCamera':"0"
            }
    def getConfigItem(self, item:str):
        return self._Config.get(item)
