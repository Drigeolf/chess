from base_modules import BaseModule
from msgs import ReadingStatus

class GameState(BaseModule):
    def __init__(self):
        super(GameState, self).__init__()
        self.name = "GameState"
        self.running = True
        self.paused = False

    def handle_msg(self, msg):
        if msg.mtype == "QUIT_GAME":
            print("Quitting game!")
            self.running = False
        elif msg.mtype == "INVALID_COMMAND":
            print("Invalid command, try again.")
            self.send_to_bus(ReadingStatus(content=True))
        elif msg.mtype == "INVALID_MOVE":
            print("Invalid move, try again.")
            self.send_to_bus(ReadingStatus(content=True))
        else:
            pass
