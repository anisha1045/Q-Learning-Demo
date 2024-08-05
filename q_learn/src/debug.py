import sub

class Obj:
    def __init__(self):
        self.pos = (0, 0)
        self.subo = sub.Color_Detect_Sub(self)
    # calls the sub_object's get_pos function
    def get_pos(self):
        self.subo.get_pos()
    # called by the sub_object to send the message
    def set_pos(self, pos):
        print("SET POS", pos)
        self.pos = pos
        return pos

obj = Obj()
print("WE FOT THE POS: ", obj.pos)