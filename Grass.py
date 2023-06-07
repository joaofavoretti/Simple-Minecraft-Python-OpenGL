import glfw
import glm
from OpenGL.GL import *
import numpy as np
from Block import Block

class Grass (Block):
    
    def __init__(self, pos, block_index):

        self.texture_indices = {
            'top': (2, 0),
            'bottom': (1, 0),
            'side': (3, 0),
        }
        
        super().__init__(pos, block_index)