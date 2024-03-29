import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Grass (Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (2, 0),
            "bottom": (1, 0),
            "left": (3, 0),
            "right": (3, 0),
            "front": (3, 0),
            "back": (3, 0),
        }

        super().__init__(pos)
