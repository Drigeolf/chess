from base_modules import BaseModule
from msgs import ReadingStatus, RenderMenu, InvalidCommand

class GameState(BaseModule):
    def __init__(self):
        super(GameState, self).__init__()
        self.menu_state = "MAIN_MENU"
        self.name = "GameState"
        self.in_game = False
        self.running = True
        self.paused = False
        self.players = []
        self.menu_dict = {"MAIN_MENU": ["NEW_GAME","LOAD_GAME","SETTINGS","EXIT_GAME"],
                          "NEW_GAME": ["SINGLE_PLAYER", "LOCAL_MULTI_PLAYER"],
                          "LOAD_GAME": ["NOT_IMPLEMENTED"], 
                          "SETTINGS": ["NOT_IMPLEMENTED"], 
                          "EXIT_GAME": ["QUIT_GAME"], 
                          "SINGLE_PLAYER": ["NOT_IMPLEMENTED"], 
                          "LOCAL_MULTI_PLAYER": ["ACTION_NEW_LMULTI"]}

    def handle_msg(self, msg):
        # Handle quitting
        if msg.mtype == "QUIT_GAME":
            print("Quitting game!")
            self.running = False
        # Handle invalid stuff
        elif msg.mtype == "INVALID_COMMAND":
            print("Invalid command, try again.")
            self.send_to_bus(ReadingStatus(content=True))
        elif msg.mtype == "INVALID_MOVE":
            print("Invalid move, try again.")
            self.send_to_bus(ReadingStatus(content=True))
        # Handle menus
        elif msg.mtype == "GOTO_MENU":
            MM = self.set_menu(msg)
            self.send_to_bus(MM)
        elif msg.mtype == "START_GAME":
            self.in_game = True
        else:
            pass

    def set_menu(self, msg):
        # some logic here
        if not msg.content:
            return RenderMenu(content=self.menu_state, menu_dict=self.menu_dict, prev_menu=self.menu_state)

        if not self.in_game or self.paused:
            self.prev_menu = self.menu_state
            self.menu_state = msg.content
        # Now we can handle the rendering
        if self.menu_state != omenu_st:
            return RenderMenu(content=self.menu_state, menu_dict=self.menu_dict, prev_menu=self.prev_menu)
        else:
            return InvalidCommand()

    def add_player(self, player):
        self.players.append(add_player)
