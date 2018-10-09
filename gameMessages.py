import libtcodpy as libtcod

import textwrap

class Message:
    def __init__(self, text, color=libtcod.white):
        self.text   = text
        self.color  = color

class messageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x        = x
        self.width    = width
        self.height   = height

    def addMessage(self, msg):
        # split message if too long
        nuMsgLines = textwrap.wrap(msg.text, self.width)

        for line in nuMsgLines:
            # if buffer = full, rm first line to make room
            if len(self.messages) == self.height:
                del self.messages[0]

            # add new line as Message OBJ, w/ txt and color
            self.messages.append(Message(line, msg.color))
