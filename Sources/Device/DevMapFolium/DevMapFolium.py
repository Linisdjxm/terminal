#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   DevMap.py
@Time    :   2024/11/15
@Author  :   CRC1109 
@Version :   1.0
@Desc    :   Built in PyQt5
             
'''

from Sources.Device.DevBase import DevBase
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QUrl
import os
import folium
from folium import CustomIcon

class DevMapFolium(DevBase):
    def __init__(self, name:str, **kwargs):
        """Map device

        Args:
            name (str): 地图控制设备
        """
        super(DevMapFolium,self).__init__(name)
        self.register(**kwargs)

    def register(self, **kwargs):
        self.mapShowWebengine:QtWebEngineWidgets = kwargs.get('mapShowWebengine')

    def ready(self):
        self.mapHtmlDir = os.getcwd() + "\\Sources\\Device\\DevMapFolium\\"
        self.mapHtmlPath = self.mapHtmlDir + "map.html"
        self.mapHtmlQUrl = QUrl(("file:\\" + self.mapHtmlPath).replace('\\', '/'))

        self.__generateMapHtml()
        self.mapShowWebengine.load(self.mapHtmlQUrl)

    def ctlAddClickLatLng(self):
        """添加在地图上点击鼠标显示经纬度的功能
        """
        self.mapFoliumObj.add_child(folium.LatLngPopup())
        self.ctlReload()

    def ctlAddClickPoint(self):
        """添加在地图上点击鼠标放置点的功能
        """
        self.mapFoliumObj.add_child(folium.ClickForMarker(popup='Waypoint'))
        self.ctlReload()

    def ctlReload(self):
        """重新加载地图
        """
        self.mapFoliumObj.save("save_map.html")
        self.mapShowWebengine.load(QUrl(self.mapHtmlPath))

    def ctlAddMark(self, Lat:float, Lng:float, popup:str="Mark", icon:str="cloud", color:str="blue"):
        """在地图上添加标记点

        Args:
            Lat (float): 经度
            Lng (float): 纬度
            popup (str, optional): 标记的命名. Defaults to "Mark".
            icon (str, optional): 标记的图标. Defaults to "cloud".
            color (str, optional): 标记的颜色. Defaults to "blue".
        """
        folium.Marker(
            location=[Lat, Lng],
            popup=popup,
            icon=folium.Icon(color=color, icon=icon)
            ).add_to(self.mapFoliumObj)
        self.ctlReload()

    def __generateMapHtml(self):
        """地图的html控制文件生成
        """
        self.mapFoliumObj = folium.Map(location=[45.7330, 126.6313],
                 zoom_start=20,
                 control_scale=True,
                 tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                 attr='default')
        
        # 地图上添加标记点
        GRO_POINT_LAT_LON = [45.7330, 126.6317]
        UAV_POINT_LAT_LON = [[45.7334,126.6337],[45.7321,126.6335],[45.7326,126.6359]]

        ground_icon_image = self.mapHtmlDir + "ground.png"

        ground_icon = CustomIcon(
            ground_icon_image,
            icon_size=(100, 100),
            icon_anchor=(50, 50)
        )

        folium.Marker(
            location=GRO_POINT_LAT_LON,
            icon=ground_icon
            ).add_to(self.mapFoliumObj)
    
        
        for uav_point in UAV_POINT_LAT_LON:
            uav_icon_image = self.mapHtmlDir + "uav.png"

            uav_icon = CustomIcon(
                uav_icon_image,
                icon_size=(100, 100),
                icon_anchor=(50, 50)
                )

            folium.Marker(
                location=uav_point,
                icon=uav_icon
                ).add_to(self.mapFoliumObj)

        # 地图上添加标记线
        line_points = [GRO_POINT_LAT_LON, UAV_POINT_LAT_LON[0], UAV_POINT_LAT_LON[2], UAV_POINT_LAT_LON[1], GRO_POINT_LAT_LON]
        folium.PolyLine(
            locations=line_points,
            color='red',
            weight=2.5,
            opacity=1
            ).add_to(self.mapFoliumObj)

        self.mapFoliumObj.save(self.mapHtmlPath)


    