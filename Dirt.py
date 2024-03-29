import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Dirt (Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (1, 0),
            "bottom": (1, 0),
            "left": (1, 0),
            "right": (1, 0),
            "front": (1, 0),
            "back": (1, 0),
        }
        
        super().__init__(pos)
