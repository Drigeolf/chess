from CBoard import CBoard
from MainBus import MainBus
from BoardDisplay import DisplayDriver
from MoveParser import MoveParser
from InputReader import InputReader
from Referee import CRef
from base_modules import BaseMsg

MB = MainBus()
CB = CBoard()
BDisp = DisplayDriver()
MParse = MoveParser()
Ref = CRef()
Inp = InputReader()

MB.connect_module(CB)
MB.connect_module(BDisp)
MB.connect_module(MParse)
MB.connect_module(Ref)
MB.connect_module(Inp)

# Need to figure out a more elegant way of sorting this out
# possibly the "evaluate now" thing that the article mentioned
print("New game starting!")
MB.msg_q.append(BaseMsg(mtype="DISPLAY_BOARD"))
while len(MB.msg_q) > 0:
    MB.run()
    CB.run()
    BDisp.run()

while Ref.running:
    MB.run()
    Inp.run()
    MParse.run()
    Ref.run()
    CB.run()
    BDisp.run()
