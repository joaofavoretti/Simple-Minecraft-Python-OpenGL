import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Leaves(Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (5, 0),
            "bottom": (5, 0),
            "left": (5, 0),
            "right": (5, 0),
            "front": (5, 0),
            "back": (5, 0),
        }

        super().__init__(pos)
