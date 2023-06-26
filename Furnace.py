import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Furnace (Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (8, 1),
            "bottom": (8, 0),
            "left": (8, 0),
            "right": (8, 0),
            "front": (8, 0),
            "back": (8, 0),
        }
        
        super().__init__(pos)
