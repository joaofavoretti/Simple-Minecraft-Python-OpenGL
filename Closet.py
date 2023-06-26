import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Closet (Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (9, 0),
            "bottom": (9, 0),
            "left": (9, 0),
            "right": (9, 0),
            "front": (9, 0),
            "back": (9, 0),
        }
        
        super().__init__(pos)
