#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   DevVirUAV.py
@Time    :   2024/10/18 19:08:21
@Author  :   CRC1109 
@Version :   1.0
@Desc    :   Built in PyQt5
             虚拟VirUAV设备, 功能需要
             - QLabel 虚拟VirUAV呈现形式
'''

from Sources.Device.DevBase import DevBase

class DevVirUAV(DevBase):
    def __init__(self, name:str, **kwargs):
        """Virtual UAV device

        Args:
            name (str): the name defined by developer of the VirUAV device
            **kwargs (dict): the Qt Gui Object used, should include
                {
                    'VirUAVObjLabel': QLabel
                }
        """
        super(DevVirUAV,self).__init__(name)
        self.register(**kwargs)

        
    def register(self, **kwargs):
        pass

    def ready(self):
        pass

    def ctlSetLocation(self,lon:float, lat:float, alt:float=None):
        self.lontitude = lon
        self.latitude = lat
        self.altitude = alt

