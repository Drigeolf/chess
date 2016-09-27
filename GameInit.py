from CBoard import CBoard
from MainBus import MainBus
from DisplayDriver import DisplayDriver
from InputParser import InputParser
from InputReader import InputReader
from GameState import GameState
from Referee import CRef
from msgs import DisplayBoard, StartGame

class GameInit(object):
    def __init__(self):
        self.MB = MainBus()
        self.GState = GameState()
        self.DDisp = DisplayDriver()
        self.IParse = InputParser()
        self.Inp = InputReader()
        self.MB.connect_module(self.GState)
        self.MB.connect_module(self.IParse)
        self.MB.connect_module(self.DDisp)
        self.MB.connect_module(self.Inp)
        # This will be used as a point to load default
        # options in the future. 

    def init_new_game(self):
        self.CB = CBoard()
        self.Ref = CRef()

        self.MB.connect_module(self.CB)
        self.MB.connect_module(self.Ref)

        # Need to figure out a more elegant way of sorting this out
        # possibly the "evaluate now" thing that the article mentioned
        print("New game starting!")
        self.MB.msg_q.append(DisplayBoard())
        while len(self.MB.msg_q) > 0:
            self.MB.run()
            self.CB.run()
            self.DDisp.run()

        self.MB.msg_q.append(StartGame())

    def run_local_multi(self):
        self.init_new_game()
        while self.GState.running:
            self.MB.run()
            self.Inp.run()
            self.IParse.run()
            self.Ref.run()
            self.CB.run()
            self.DDisp.run()
            self.GState.run()

    def run(self):
        # We should be in the main menu now
        # instead for now we have a new game start
        self.run_local_multi()
