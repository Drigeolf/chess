import numpy as np

from base_modules import BaseModule
from msgs import ReadingStatus, QuitGame

class DisplayDriver(BaseModule):
    def __init__(self):
        super(DisplayDriver, self).__init__()
        self.name = "Display"
        self.BD = BoardDisplay(driver=self)

    def handle_msg(self, msg):
        # Pass moves to board displayer
        if msg.mtype == "PROCESSED_MOVE":
            DM = self.BD.handle_msg(msg)
            self.send_to_bus(DM)
        elif msg.mtype == "RENDER_BOARD":
            DM = self.BD.handle_msg(msg)
        elif "RENDER_MENU" in msg.mtype:
            DM = self.menu_display(msg)
            self.send_to_bus(DM)
        else:
            pass

    def menu_display(self, msg):
        # We deal with menu displaying here
        if msg.mtype == "RENDER_MENU":
            if msg.content == "MAIN_MENU":
                print("###################################")        
                print("### Welcome to Chessmasher5000 ####")        
                print("###################################")        
                print("## Main Menu ######################")        
                print("## Type to navigate menus #########")        
                print("###################################")        
                print("# New Game ########################")        
                print("# Load Game #######################")        
                print("# Settings ########################")        
                print("# Exit Game #######################")        
                print("###################################")        
            elif msg.content == "NEW_GAME":
                print("###################################")        
                print("### Welcome to Chessmasher5000 ####")        
                print("###################################")        
                print("## New Game #######################")        
                print("## Type to navigate menus #########")        
                print("###################################")        
                print("# Singleplayer ####################")        
                print("# Local Multiplayer ###############")        
                print("###################################")        
            elif msg.content == "LOAD_GAME":
                print("###################################")        
                print("### Welcome to Chessmasher5000 ####")        
                print("###################################")        
                print("## Load Game ######################")        
                print("## Type to navigate menus #########")        
                print("###################################")        
                print("# NOT IMPLEMENTED YET #############")        
                print("###################################")        
                return QuitGame()
            elif msg.content == "NEW_GAME_SINGLE":
                print("###################################")        
                print("### Welcome to Chessmasher5000 ####")        
                print("###################################")        
                print("## Singleplayer Game ##############")        
                print("## Type to navigate menus #########")        
                print("###################################")        
                print("# NOT IMPLEMENTED YET #############")        
                print("###################################")        
                return QuitGame()
            elif msg.content == "SETTINGS_MENU":
                print("###################################")        
                print("### Welcome to Chessmasher5000 ####")        
                print("###################################")        
                print("## Settings #######################")        
                print("## Type to navigate menus #########")        
                print("###################################")        
                print("# NOT IMPLEMENTED YET #############")        
                print("###################################")        
                return QuitGame()
            else:
                print("Msg type not understood, quitting")
                return QuitGame()

class BoardDisplay(BaseModule):
    def __init__(self, driver=None):
        super(BoardDisplay, self).__init__()
        self.name = "BoardDisplay"
        self.DisplayDriver = driver

        self.pieceDict = {
              0: ".", 1: "P", 2: "N", 
              3: "B", 4: "R", 5: "Q",
              6: "K", -1: "o", -2: "n", 
              -3: "b", -4: "r", -5: "q",
              -6: "k" }

    def displayMove(self, content, change_read=True):
        self.board, turn = content
        if change_read:
            DM = ReadingStatus(content=True)
        else:
            DM = None

        if not turn:
            print("###################################")        
            print("#####   Whites turn to play   #####")
        else:
            print("###################################")        
            print("#####   Blacks turn to play   #####")
        self.printBoard()
        return DM

    def handle_msg(self, msg):
        if msg.mtype == "PROCESSED_MOVE":
            DM = self.displayMove(msg.content)
            return DM
        elif msg.mtype == "RENDER_BOARD":
            DM = self.displayMove(msg.content, change_read=False)
            return DM
        else:
            pass

    def trPiece(self, piece):
        """
        Helper function for translating the chess pieces. Meant to be 
        used for function "map" in order to convert from index to piece.

        """
        return self.pieceDict[piece]

    def printBoard(self):
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
        print( " 8 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[7][::-1])) 
        print( " 7 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[6][::-1])) 
        print( " 6 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[5][::-1])) 
        print( " 5 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[4][::-1])) 
        print( " 4 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[3][::-1])) 
        print( " 3 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[2][::-1])) 
        print( " 2 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[1][::-1])) 
        print( " 1 | {7}  {6}  {5}  {4}  {3}  {2}  {1}  {0} |".format(*strBoard[0][::-1])) 
        print("   --------------------------")
        print( "     {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7}  "\
                     .format(*['A','B','C','D','E','F','G','H',]))
        print("###################################")        