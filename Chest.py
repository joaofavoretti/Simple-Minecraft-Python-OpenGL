import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Chest (Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            "top": (7, 0),
            "bottom": (7, 0),
            "left": (7, 1),
            "right": (7, 1),
            "front": (7, 1),
            "back": (7, 1),
        }
        
        super().__init__(pos)
