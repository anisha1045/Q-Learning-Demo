import sub

class Obj:
    def __init__(self):
        self.pos = (0, 0)
        self.subo = sub.Color_Detect_Sub()
    # calls the sub_object's get_pos function
    def get_pos(self):
        self.subo.get_pos(self)
    # called by the sub_object to send the message
    def set_pos(self, pos):
        self.pos = pos
        return pos

obj = Obj
subo.get_pos(self)