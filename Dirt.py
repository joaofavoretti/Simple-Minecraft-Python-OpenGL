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
            "left": (1, 1),
            "right": (1, 1),
            "front": (1, 2),
            "back": (1, 2),
        }
        
        super().__init__(pos)