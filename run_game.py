from CBoard import CBoard
from MainBus import MainBus
from BoardDisplay import DisplayDriver
from InputParser import InputParser
from InputReader import InputReader
from GameState import GameState
from Referee import CRef
from msgs import DisplayBoard
import sys

MB = MainBus()
CB = CBoard()
BDisp = DisplayDriver()
IParse = InputParser()
Ref = CRef()
Inp = InputReader()
GState = GameState()

MB.connect_module(CB)
MB.connect_module(BDisp)
MB.connect_module(IParse)
MB.connect_module(Ref)
MB.connect_module(Inp)
MB.connect_module(GState)

# Need to figure out a more elegant way of sorting this out
# possibly the "evaluate now" thing that the article mentioned
print("New game starting!")
MB.msg_q.append(DisplayBoard())
while len(MB.msg_q) > 0:
    MB.run()
    CB.run()
    BDisp.run()

while GState.running:
    MB.run()
    Inp.run()
    IParse.run()
    Ref.run()
    CB.run()
    BDisp.run()
    GState.run()

sys.exit()
