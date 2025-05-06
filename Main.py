#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   Main.py
@Time    :   2024/10/18 16:07:38
@Author  :   WangXi 
@Version :   1.0
@Desc    :   Built in PyQt5
             网络演示系统程序总入口，通过注释或改写可控制启动界面
             - MainWindowPro() 地面站终端界面
             - MainWindowMin() 移动终端界面
'''

import sys
from PyQt5.QtWidgets import QApplication

from Sources.MainWindowPro import MainWindowPro
from Sources.MainWindowMin import MainWindowMin
from Sources.MainWindowMMin import MainWindowMMin

import builtins
builtins._DEBUG = 0

if __name__ == "__main__":
    # 获取当前时间
    
    app = QApplication(sys.argv)
    MainWindowMMin1 = MainWindowMMin()
    
    # 设置CSS样式
    styleFile = 'Forms/qss/Ubuntu.qss'
    with open(styleFile, 'r') as f:
        qssStyle = f.read()
    MainWindowMMin1.setStyleSheet(qssStyle)
 
    MainWindowMMin1.show()
  
    #mainWindowMin = MainWindowMin()
    #mainWindowMin.show()

    sys.exit(app.exec_())
    