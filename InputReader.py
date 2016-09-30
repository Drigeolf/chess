from base_modules import BaseModule
from msgs import ReadInput, QuitGame

class InputReader(BaseModule):
    def __init__(self):
        super(InputReader, self).__init__()
        self.name = "InpReader"
        self.reading = False
        self.reading_for = None
        # Parser related

    def handle_msg(self, msg):
        if msg.mtype == "READING_STATUS":
            if msg.player:
                self.set_status(msg.content, player=msg.player)
            else:
                self.set_status(msg.content)
        else:
            pass

    def set_status(self, status, player=None):
        self.reading = status
        if player:
            self.reading_for = player
        else:
            self.reading_for = None

    def run(self):
        while len(self.msg_q) > 0:
            curr_msg = self.msg_q.pop(0)
            self.handle_msg(curr_msg)
        if self.reading == "MOVE" and self.reading_for:
            inp = raw_input("")
            inp = self.clean_inp(inp)
            print(inp)
            IM = ReadInput(content=inp, player=self.reading_for)
            self.reading = False
            self.send_to_bus(IM)
        elif self.reading == "COMMAND":
            inp = raw_input("")
            inp = self.clean_inp(inp)
            print(inp)
            IM = ReadInput(content=inp)
            self.reading = False
            self.send_to_bus(IM)
        else:
          pass

    def clean_inp(self, inp):
        return inp.strip()
