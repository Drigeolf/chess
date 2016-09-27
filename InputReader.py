from base_modules import BaseModule
from msgs import ReadInput

class InputReader(BaseModule):
    def __init__(self):
        super(InputReader, self).__init__()
        self.name = "InpReader"
        self.reading = True
        # Parser related

    def handle_msg(self, msg):
        if msg.mtype == "READING_STATUS":
            self.set_status(msg.content)
        else:
            pass

    def set_status(self, status):
        self.reading = status

    def run(self):
        while len(self.msg_q) > 0:
            curr_msg = self.msg_q.pop(0)
            self.handle_msg(curr_msg)
        if self.reading:
          inp = raw_input("Plase enter a move: \n")
          IM = ReadInput(content=inp)
          self.reading = False
          self.send_to_bus(IM)
