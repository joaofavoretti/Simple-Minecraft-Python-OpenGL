import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Wood (Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (6, 0),
            "bottom": (6, 0),
            "left": (6, 0),
            "right": (6, 0),
            "front": (6, 0),
            "back": (6, 0),
        }
        
        super().__init__(pos)
