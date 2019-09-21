# -*- coding: utf-8 -*-
'''
---------
 main.py
---------
'''
import sys
from Controller import *

if __name__ == '__main__':
    controller = Controller(sys.argv)
    controller.process()
