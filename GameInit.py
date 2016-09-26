from CBoard import CBoard
from MainBus import MainBus
from BoardDisplay import DisplayDriver
from InputParser import InputParser
from InputReader import InputReader
from GameState import GameState
from Referee import CRef
from msgs import DisplayBoard

class GameInit(object):
    def __init__(self):
        self.MB = MainBus()
        self.CB = CBoard()
        self.BDisp = DisplayDriver()
        self.IParse = InputParser()
        self.Ref = CRef()
        self.Inp = InputReader()
        self.GState = GameState()

    def run(self):
        self.MB.connect_module(self.CB)
        self.MB.connect_module(self.BDisp)
        self.MB.connect_module(self.IParse)
        self.MB.connect_module(self.Ref)
        self.MB.connect_module(self.Inp)
        self.MB.connect_module(self.GState)

        # Need to figure out a more elegant way of sorting this out
        # possibly the "evaluate now" thing that the article mentioned
        print("New game starting!")
        self.MB.msg_q.append(DisplayBoard())
        while len(self.MB.msg_q) > 0:
            self.MB.run()
            self.CB.run()
            self.BDisp.run()
        
        while self.GState.running:
            self.MB.run()
            self.Inp.run()
            self.IParse.run()
            self.Ref.run()
            self.CB.run()
            self.BDisp.run()
            self.GState.run()
