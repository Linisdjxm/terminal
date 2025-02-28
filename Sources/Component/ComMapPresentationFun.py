#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   ComMapPresentationFun.py
@Time    :   2024/11/15 
@Author  :   CRC1109 
@Version :   1.0
@Desc    :   Built in PyQt5
             
'''

import math
import random
from PyQt5.QtWidgets import QPushButton,QComboBox
from PyQt5.QtCore import Qt,pyqtSlot,QTimer,pyqtRemoveInputHook, pyqtRestoreInputHook
from Sources.Component.ComBaseFun import ComBaseFun
from Sources.Device.DevMapFolium.DevMapFolium import DevMapFolium
from Sources.Device.DevMapHtml.DevMapHtml import DevMapHtml
from Sources.Device.DevVirUAV import DevVirUAV
from Sources.Device.DevNIC import DevNIC

class ComMapPresentationFun(ComBaseFun):
    def __init__(self, name:str, **kwargs):
        super(ComMapPresentationFun,self).__init__(name)
        self.register(**kwargs)
        self.ready()

    def register(self, **kwargs):
        self.uavlistCombox: QComboBox = kwargs.get('uavlistCombox')
        self.downPushButton: QPushButton = kwargs.get('downPushButton')
        self.goaheadPushButton: QPushButton = kwargs.get('goaheadPushButton')
        self.gobackPushButton: QPushButton = kwargs.get('gobackPushButton')
        self.landPushButton: QPushButton = kwargs.get('landPushButton')
        self.leftmovePushButton: QPushButton = kwargs.get('leftmovePushButton')
        self.rightmovePushButton: QPushButton = kwargs.get('rightmovePushButton')
        self.stopPushButton: QPushButton = kwargs.get('stopPushButton')
        self.takeoffPushButton: QPushButton = kwargs.get('takeoffPushButton')
        self.upPushButton: QPushButton = kwargs.get('upPushButton')
        self.checklogPushButton: QPushButton = kwargs.get('checklogPushButton')
        self.cleartrackPushButton: QPushButton = kwargs.get('cleartrackPushButton')
        self.returnPushButton: QPushButton = kwargs.get('returnPushButton')
        self.getinfoPushButton: QPushButton = kwargs.get('getinfoPushButton')
        self.setpointPushButton: QPushButton = kwargs.get('setpointPushButton')

        self.devNic = kwargs.get('devNic')
        self.devMap = DevMapHtml("地图控制设备",**kwargs)
        self.devVirUAV_list: list[DevVirUAV] = [DevVirUAV("无人机1号",**kwargs), DevVirUAV("无人机2号",**kwargs), DevVirUAV("无人机3号",**kwargs)]
        
        
    def ready(self):
        self.uavlistCombox.addItems([devVirUAV.name for devVirUAV in self.devVirUAV_list])
        
        self.downPushButton.clicked.connect(self.on_downPushButton_clicked)
        self.goaheadPushButton.clicked.connect(self.on_goaheadPushButton_clicked)
        self.gobackPushButton.clicked.connect(self.on_gobackPushButton_clicked)
        self.landPushButton.clicked.connect(self.on_landPushButton_clicked)
        self.leftmovePushButton.clicked.connect(self.on_leftmovePushButton_clicked)
        self.rightmovePushButton.clicked.connect(self.on_rightmovePushButton_clicked)
        self.stopPushButton.clicked.connect(self.on_stopPushButton_clicked)
        self.takeoffPushButton.clicked.connect(self.on_takeoffPushButton_clicked)
        self.upPushButton.clicked.connect(self.on_upPushButton_clicked)
        self.checklogPushButton.clicked.connect(self.on_checklogPushButton_clicked)
        self.cleartrackPushButton.clicked.connect(self.on_cleartrackPushButton_clicked)
        self.returnPushButton.clicked.connect(self.on_returnPushButton_clicked)
        self.getinfoPushButton.clicked.connect(self.on_getinfoPushButton_clicked)
        self.setpointPushButton.clicked.connect(self.on_setpointPushButton_clicked)

        self.devMap.ready()

        # 初始化各个点的位置信息
        self.location = [119.670533, 25.943939]
        UAV_POINT_LON_LAT = [self.__get_point_lon_lat(self.location, 100, 0),
                                self.__get_point_lon_lat(self.location, 200, 45),
                                self.__get_point_lon_lat(self.location, 100, 90)]
        print(UAV_POINT_LON_LAT)
        for i,devVirUAV in enumerate(self.devVirUAV_list):
            devVirUAV.ctlSetLocation(UAV_POINT_LON_LAT[i][0], UAV_POINT_LON_LAT[i][1])
        

    @pyqtSlot()
    def on_downPushButton_clicked(self):
        print(self.name+":downPushButton clicked")
        
    @pyqtSlot()
    def on_goaheadPushButton_clicked(self):
        print(self.name+":goaheadPushButton clicked")
        
    @pyqtSlot()
    def on_gobackPushButton_clicked(self):
        print(self.name+":gobackPushButton clicked")
        
    @pyqtSlot()
    def on_landPushButton_clicked(self):
        print(self.name+":landPushButton clicked")
        
    @pyqtSlot()
    def on_leftmovePushButton_clicked(self):
        print(self.name+":leftmovePushButton clicked")
        
    @pyqtSlot()
    def on_rightmovePushButton_clicked(self):
        print(self.name+":rightmovePushButton clicked")
        
    @pyqtSlot()
    def on_stopPushButton_clicked(self):
        print(self.name+":stopPushButton clicked")
        self.refreshPeriodTimer.stop()
        
    @pyqtSlot()
    def on_takeoffPushButton_clicked(self):
        print(self.name+":takeoffPushButton clicked")
        
    @pyqtSlot()
    def on_upPushButton_clicked(self):
        print(self.name+":upPushButton clicked")
        
    @pyqtSlot()
    def on_checklogPushButton_clicked(self):
        print(self.name+":checklogPushButton clicked")
        
    @pyqtSlot()
    def on_cleartrackPushButton_clicked(self):
        print(self.name+":cleartrackPushButton clicked")
        
    @pyqtSlot()
    def on_returnPushButton_clicked(self):
        print(self.name+":returnPushButton clicked")
        
    @pyqtSlot()
    def on_getinfoPushButton_clicked(self):
        print(self.name+":getinfoPushButton clicked")
        
    @pyqtSlot()
    def on_setpointPushButton_clicked(self):
        print(self.name+":setpointPushButton clicked")
        self.refreshPeriodTimer = QTimer(self)
        self.refreshPeriodTimer.timeout.connect(self.__refresh_map)
        self.refreshPeriodTimer.start(100)
    

    def __refresh_map(self):
        self.devMap.ctlRemove()

        self.devMap.ctlAddMark(self.location[0], self.location[1], popup="地面站", icon="GRO")

        for devVirUAV in self.devVirUAV_list:
            self.devMap.ctlAddMark(devVirUAV.lontitude, devVirUAV.latitude, popup=devVirUAV.name, icon="UAV")

        self.devMap.ctlAddLine(self.location[0], self.location[1], 
                               self.devVirUAV_list[0].lontitude, self.devVirUAV_list[0].latitude, 
                               popup="link_1", color="red")
        
        self.devMap.ctlAddLine(self.location[0], self.location[1], 
                               self.devVirUAV_list[2].lontitude, self.devVirUAV_list[2].latitude, 
                               popup="link_2", color="red")
        
        self.devMap.ctlAddLine(self.devVirUAV_list[0].lontitude, self.devVirUAV_list[0].latitude, 
                               self.devVirUAV_list[1].lontitude, self.devVirUAV_list[1].latitude, 
                               popup="link_3", color="red")
        
        self.devMap.ctlAddLine(self.devVirUAV_list[2].lontitude, self.devVirUAV_list[2].latitude, 
                               self.devVirUAV_list[1].lontitude, self.devVirUAV_list[1].latitude, 
                               popup="link_4", color="red")
        
        self.__refresh_uav_location()
        

    def __refresh_uav_location(self):
        for devVirUAV in self.devVirUAV_list:
            random_distance = random.uniform(0, 5)
            random_angle = random.randint(0, 359)
            new_location = self.__get_point_lon_lat([devVirUAV.lontitude, devVirUAV.latitude], random_distance, random_angle)
            devVirUAV.ctlSetLocation(new_location[0], new_location[1])

            self.devNic.writeTimeStamp()
            self.devNic.writeAppend("UAV:{}, new_location:{}".format(devVirUAV.name, new_location), Qt.AlignmentFlag.AlignRight)
    
    def __get_point_lon_lat(self, center_point, distance, bearing):
        # 将距离从米转换为度
        # 注意：这些转换因子是粗略估计，适合小范围内的坐标转换
        lat_change_per_km = 1 / 111.32
        lon_change_per_km_at_lat = 1 / (111.32 * math.cos(math.radians(center_point[1])))

        delta_lat = distance * lat_change_per_km / 1000
        delta_lon = distance * lon_change_per_km_at_lat / 1000

        # 计算新的坐标
        new_lat = center_point[1] + delta_lat * math.sin(math.radians(bearing))
        new_lon = center_point[0] + delta_lon * math.cos(math.radians(bearing))

        return [new_lon, new_lat]