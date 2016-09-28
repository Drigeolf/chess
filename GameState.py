from base_modules import BaseModule
from Players import HumanPlayer, AIPlayer
from msgs import ReadingStatus, RenderMenu, InvalidCommand, DisplayBoard, StartGame

class GameState(BaseModule):
    def __init__(self):
        super(GameState, self).__init__()
        self.menu_state = "MAIN_MENU"
        self.name = "GameState"
        self.in_game = False
        self.running = True
        self.paused = False
        self.players = []
        self.menu_dict = {"MAIN MENU": ["NEW GAME","LOAD GAME","SETTINGS","EXIT GAME"],
                          "NEW GAME": ["SINGLEPLAYER", "LOCAL MULTIPLAYER"],
                          "LOAD GAME": ["NOT_IMPLEMENTED"], 
                          "SETTINGS": ["NOT_IMPLEMENTED"], 
                          "EXIT GAME": ["QUIT_GAME"], 
                          "SINGLEPLAYER": ["NOT_IMPLEMENTED"], 
                          "LOCAL MULTIPLAYER": ["NEW_LMULTI"]}

    def handle_msg(self, msg):
        # Handle quitting
        if msg.mtype == "QUIT_GAME":
            print("Quitting game!")
            self.running = False
        # Handle invalid stuff
        elif msg.mtype == "INVALID_COMMAND":
            print("Invalid command, try again.")
            if msg.player:
                msg.player.read_input()
            else:
                self.send_to_bus(ReadingStatus(content="COMMAND"))
        elif msg.mtype == "INVALID_MOVE":
            print("Invalid move, try again.")
            msg.player.read_input()
        # Handle menus
        elif msg.mtype == "GOTO_MENU":
            MM = self.set_menu(msg)
            self.send_to_bus(MM)
        elif msg.mtype == "START_GAME":
            self.players = msg.players
            self.in_game = True
            self.send_now(DisplayBoard())
        elif msg.mtype == "INIT_GAME":
            # Initialize game, we are in menus now
            if self.menu_state != "MAIN MENU":
                self.menu_state = "MAIN MENU"
            self.send_now(RenderMenu(content=self.menu_state, menu_dict=self.menu_dict, prev_menu=self.menu_state))
        else:
            pass

    def set_menu(self, msg):
        # some logic here
        if not msg.content:
            return RenderMenu(content=self.menu_state, menu_dict=self.menu_dict, prev_menu=self.menu_state)

        if self.menu_dict[msg.content] == ["NEW_LMULTI"]:
            import random
            t1 = random.randint(0,100)%2 
            t2 = (t1+1)%2
            Player1 = HumanPlayer(turn=t1)
            Player2 = HumanPlayer(turn=t2)
            return StartGame(players=[Player1, Player2])
        elif self.menu_dict[msg.content] == ["NEW_SINGLE"]:
            import random
            t1 = random.randint(0,100)%2 
            t2 = (t1+1)%2
            Player1 = HumanPlayer(turn=t1)
            Player2 = AIPlayer(turn=t2)
            return StartGame(players=[Player1, Player2])

        if (not self.in_game) or self.paused:
            self.prev_menu = self.menu_state
            self.menu_state = msg.content
        # Now we can handle the rendering
        return RenderMenu(content=self.menu_state, menu_dict=self.menu_dict, prev_menu=self.prev_menu)

    def add_player(self, player):
        self.players.append(add_player)
