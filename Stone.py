import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Stone (Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (4, 0),
            "bottom": (4, 0),
            "left": (4, 0),
            "right": (4, 0),
            "front": (4, 0),
            "back": (4, 0),
        }
        
        super().__init__(pos)
