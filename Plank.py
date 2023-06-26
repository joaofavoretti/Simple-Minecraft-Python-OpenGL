import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Plank (Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (6, 1),
            "bottom": (6, 1),
            "left": (6, 1),
            "right": (6, 1),
            "front": (6, 1),
            "back": (6, 1),
        }
        
        super().__init__(pos)
