#Anaconda/envs/pyqtenv python
# -*- coding: utf-8 -*-
'''
@File    :   ConfBase.py
@Time    :   2025/02
@Author  :   Author 
@Version :   1.0
@Desc    :   Built in PyQt5
'''

from PyQt5.QtCore import QObject

class ConfBase(QObject):
    def __init__(self):
        super(ConfBase,self).__init__()

    def register(self):
        raise NotImplementedError("Subclasses should implement this!")
    
    def ready(self):
        raise NotImplementedError("Subclasses should implement this!")

    def open(self):
        raise NotImplementedError("Subclasses should implement this!")

    def close(self):
        raise NotImplementedError("Subclasses should implement this!")

    def read(self):
        raise NotImplementedError("Subclasses should implement this!")

    def write(self):
        raise NotImplementedError("Subclasses should implement this!")
    
    def ctl(self):
        raise NotImplementedError("Subclasses should implement this!")

