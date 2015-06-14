# Title: Chess Board Class and its methods
# Author: Vedat Sinan Ural, Ali Sinan Saglam
# Contact: vsural@gmail.com, asinansaglam@gmail.com
# Created on Sat Jun 13 23:53:13 2015

import numpy as np
 
 
class CRef:
    """
    A referee class for the chess engine. 
    This class checks the validity of moves and controls the flow of 
    the game. 
    """
    def __init__(self):
        self.test = 0
