import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Dirt (Block):
    
    def __init__(self, pos):

        self.texture_indices = {
            'top': (1, 0),
            'bottom': (1, 0),
            'side': (1, 0),
        }
        
        super().__init__(pos)