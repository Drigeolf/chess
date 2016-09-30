#!/usr/bin/env python
# -*- coding: utf8 -*-

import numpy as np

from base_modules import BaseModule
from msgs import ReadingStatus, QuitGame, GotoMenu

class DisplayDriver(BaseModule):
    def __init__(self, term=None):
        super(DisplayDriver, self).__init__()
        self.name = "Display"
        self.BD = BoardDisplay(driver=self)
        self.term = term

    def handle_msg(self, msg):
        # Pass moves to board displayer
        if msg.mtype == "PROCESSED_MOVE":
            self.BD.handle_msg(msg)
            msg.player.read_input()
        elif msg.mtype == "RENDER_BOARD":
            self.BD.handle_msg(msg)
            msg.player.read_input()
        elif "RENDER_MENU" in msg.mtype:
            self.menu_display(msg)
            self.send_to_bus(ReadingStatus(content="COMMAND"))
        else:
            pass


    def menu_display(self, msg):
        if self.term:
            self._menu_display_term(msg)
        else:
            self._menu_display_noterm(msg)

    def _menu_display_term(self, msg):
        menu_name = msg.content
        menu_content = msg.menu_dict[menu_name]
        menu_prev = msg.prev_menu
        if menu_content[0] == "NOT_IMPLEMENTED":
            return GotoMenu(content=msg.prev_menu)
        elif menu_content[0] == "QUIT_GAME":
            return QuitGame()
        # We have blessings, let's improve the view
        print(self.term.clear())
        h, w = self.term.height, self.term.width
        print(self.term.move(h/2-(h/4), 0) + "{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print("{0:{fill}{align}{width}}".format(" Welcome to Chessmasher5000 ", fill="#", align="^", width=w) )
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print("")
        # Print menu name here
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print("{0:{fill}{align}{width}}".format(" "+menu_name+" ", fill="#", align="^", width=w) )
        print("{0:{fill}{align}{width}}".format(" Type to navigate menus ", fill="#", align="^", width=w) )
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print("")
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        for elem in menu_content:
            print("{0:{fill}{align}{width}}".format(" "+elem+" ", fill="#", align="^", width=w) )
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print("Please enter a command:")

    def _menu_display_noterm(self, msg):
        menu_name = msg.content
        menu_content = msg.menu_dict[menu_name]
        menu_prev = msg.prev_menu
        if menu_content[0] == "NOT_IMPLEMENTED":
            return GotoMenu(content=msg.prev_menu)
        elif menu_content[0] == "QUIT_GAME":
            return QuitGame()
        print("###################################")
        print("### Welcome to Chessmasher5000 ####")        
        print("###################################")        
        # Print menu name here
        print("# {0}".format(menu_name))
        print("## Type to navigate menus #########")        
        print("###################################")        
        for elem in menu_content:
            print("# {0}".format(elem))
        print("###################################")        
        print("Please enter a command:")

class BoardDisplay(BaseModule):
    def __init__(self, driver=None):
        super(BoardDisplay, self).__init__()
        self.name = "BoardDisplay"
        self.DisplayDriver = driver

        #try:
        self.pieceDict = {
              0: ".", 1: u'\u2659', 2: u'\u2658', 
              3: u'\u2657', 4: u'\u2656', 5: u'\u2655',
              6: u'\u2654', -1: u'\u265F', -2: u'\u265E', 
              -3: u'\u265D', -4: u'\u265C', -5: u'\u265B',
              -6: u'\u265A'}
        #except:
        #    self.pieceDict = {
        #          0: ".", 1: "P", 2: "N", 
        #          3: "B", 4: "R", 5: "Q",
        #          6: "K", -1: "o", -2: "n", 
        #          -3: "b", -4: "r", -5: "q",
        #          -6: "k" }

    def displayMove(self, content):
        if self.DisplayDriver.term:
            self._displayMoveTerm(content)
        else:
            self._displayMoveNoTerm(content)

    def _displayMoveNoTerm(self,content):
        self.board, turn = content

        if not turn:
            print("###################################")        
            print("#####   Whites turn to play   #####")
        else:
            print("###################################")        
            print("#####   Blacks turn to play   #####")
        self._printBoardNoTerm()

    def _displayMoveTerm(self,content):
        self.board, turn = content

        t = self.DisplayDriver.term
        h, w = t.height, t.width
        print(t.clear())
        if not turn:
            print(t.move(h/2-(h/4),0) + "{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
            print("{0:{fill}{align}{width}}".format(" Whites turn to play ", fill="#", align="^", width=w) )
            print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        else:
            print(t.move(h/2-(h/4),0) + "{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
            print("{0:{fill}{align}{width}}".format(" Blacks turn to play ", fill="#", align="^", width=w) )
            print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        self._printBoardTerm()

    def handle_msg(self, msg):
        if msg.mtype == "PROCESSED_MOVE":
            self.displayMove(msg.content)
        elif msg.mtype == "RENDER_BOARD":
            self.displayMove(msg.content)
        else:
            pass

    def trPiece(self, piece):
        """
        Helper function for translating the chess pieces. Meant to be 
        used for function "map" in order to convert from index to piece.

        """
        return self.pieceDict[piece]

    def _printBoardNoTerm(self):
        """
        A way to print the board to the output. For now it only uses
        print but later we should implement stuff to deal with commandlines
        so that this works in bash/zsh etc. 

        Returns:
          Nothing, just prints the board. 
        """
        flatBoard = np.array(map(self.trPiece, self.board.flatten()))
        strBoard = flatBoard.reshape((8,8))
        #print("Current Board State")
        print("###################################")        
        print("   --------------------------")
        print( u" 8 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[7][::-1])) 
        print( u" 7 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[6][::-1])) 
        print( u" 6 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[5][::-1])) 
        print( u" 5 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[4][::-1])) 
        print( u" 4 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[3][::-1])) 
        print( u" 3 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[2][::-1])) 
        print( u" 2 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[1][::-1])) 
        print( u" 1 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[0][::-1])) 
        print("   --------------------------")
        print( "     {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7}  "\
                     .format(*['A','B','C','D','E','F','G','H',]))
        print("###################################")        

    def _printBoardTerm(self):
        """
        A way to print the board to the output. For now it only uses
        print but later we should implement stuff to deal with commandlines
        so that this works in bash/zsh etc. 

        Returns:
          Nothing, just prints the board. 
        """

        t = self.DisplayDriver.term
        h, w = t.height, t.width

        flatBoard = np.array(map(self.trPiece, self.board.flatten()))
        strBoard = flatBoard.reshape((8,8))
        print("")
        print("{0:{align}{width}}".format("   --------------------------", align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 8 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[7][::-1]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 7 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[6][::-1]), align="^", width=w)) 
        print(u'{0:{align}{width}}'.format(u" 6 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[5][::-1]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 5 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[4][::-1]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 4 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[3][::-1]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 3 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[2][::-1]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 2 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[1][::-1]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 1 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[0][::-1]), align="^", width=w))
        print("{0:{align}{width}}".format("   --------------------------", align="^", width=w))
        print("{0:{align}{width}}".format( "     {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7}  "\
                     .format(*['A','B','C','D','E','F','G','H',]), align="^", width=w))
        print("")
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
