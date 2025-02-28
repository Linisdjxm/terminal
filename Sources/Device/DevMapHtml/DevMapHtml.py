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

class DevMapHtml(DevBase):
    def __init__(self, name:str, **kwargs):
        """Map device

        Args:
            name (str): 地图控制设备
        """
        super(DevMapHtml,self).__init__(name)
        self.register(**kwargs)

    def register(self, **kwargs):
        self.mapShowWebengine:QtWebEngineWidgets = kwargs.get('mapShowWebengine')

    def ready(self):
        self.mapHtmlDir = os.getcwd() + "\\Sources\\Device\\DevMapHtml\\baiduMap\\"
        self.mapHtmlPath = self.mapHtmlDir + "map.html"
        self.mapHtmlQUrl = QUrl(("file:\\" + self.mapHtmlPath).replace('\\', '/'))

        self.loc_init = [119.670533, 25.943939]

        self.mapShowWebengine.page().load(self.mapHtmlQUrl)

    def ctlReload(self):
        """重新加载地图
        """
        pass

    def ctlAddMark(self, Lng:float, Lat:float, popup:str="UAV", icon:str="UAV"):
        """在地图上添加标记点

        Args:
            Lng (float): 经度
            Lat (float): 纬度
            popup (str, optional): 标记的命名. Defaults to "Mark".
            icon (str, optional): 标记的图标. Defaults to "cloud".
        """

        js_command = f"add_point('{popup}','{icon}.png','{str(Lng)}','{str(Lat)}')"
        self.mapShowWebengine.page().runJavaScript(js_command)

    def ctlAddLine(self, Lng1:float, Lat1:float, Lng2:float, Lat2:float, popup:str="Line", color:str="red"):
        """在地图上添加线

        Args:
            Lng1 (float): 起点经度
            Lat1 (float): 起点纬度
            Lng2 (float): 终点经度
            Lat2 (float): 终点纬度
            popup (str, optional): 线的命名. Defaults to "Line".
            color (str, optional): 线的颜色. Defaults to "red".
        """

        js_command = f"add_line('{popup}','{str(Lng1)}','{str(Lat1)}','{str(Lng2)}','{str(Lat2)}','{color}')"
        self.mapShowWebengine.page().runJavaScript(js_command)

    def ctlRemove(self, popup:str="all"):
        """在地图上移除标记点或线

        Args:
            popup (str): 要移除的对象

        """

        if popup == "all":
            js_command = "remove_all()"
        elif popup == "redline":
            js_command = "remove_lineRed()"
        elif js_command == "blackline":
            js_command = "remove_lineBlack()"
        elif js_command == "vector":
            js_command = "remove_vector()"
        elif js_command == "point":
            js_command = "remove_point()"
        else:
            print(self.name + " ctlRemove error with " + popup)
            pass

        self.mapShowWebengine.page().runJavaScript(js_command)
