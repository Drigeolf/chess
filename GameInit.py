from CBoard import CBoard
from MainBus import MainBus
from DisplayDriver import DisplayDriver
from InputParser import InputParser
from InputReader import InputReader
from GameState import GameState
from Referee import CRef
from msgs import InitGame

class GameInit(object):
    def __init__(self):
        self.MB = MainBus()
        self.GState = GameState()
        self.DDisp = DisplayDriver()
        self.IParse = InputParser()
        self.Inp = InputReader()
        self.CB = CBoard()
        self.Ref = CRef()
        self.MB.connect_module(self.GState)
        self.MB.connect_module(self.IParse)
        self.MB.connect_module(self.DDisp)
        self.MB.connect_module(self.Inp)
        self.MB.connect_module(self.CB)
        self.MB.connect_module(self.Ref)

    def run(self):
        # Temporarily just start a game
        self.MB.msg_q.append(InitGame())
        #self.init_new_game()
        while self.GState.running:
            self.MB.run()
            self.Inp.run()
            self.IParse.run()
            self.Ref.run()
            self.CB.run()
            self.DDisp.run()
            self.GState.run()
