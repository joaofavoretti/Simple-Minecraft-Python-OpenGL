import glfw
import glm
from OpenGL.GL import *
import numpy as np

class Block:
    def __init__ (self, pos):
        """
            Initialize the block centered at (x, y, z)

            pos(glm.vec3) - Position of the block in the space. Must be integers, otherwise can cause interpolation problems.
        """

        self.size = 1.0
        
        self.verts = self.defineVertices(pos, self.size)

        self.texture = self.defineTexture()
        
        self.colors = self.defineColors()

        self.model = glm.mat4(1.0)

    # TODO: Use a block.obj file to define the vertices
    def defineVertices(self, pos, size):
        """
            Define the vertices of the block

            pos(tuple(float, float, float)) - Position of the block in the world
            size(float) - Size of the block
        """
        return np.array([

            (pos[0] - size/2, pos[1] - size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] - size/2, pos[2] + size/2),
            (pos[0] - size/2, pos[1] + size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] + size/2),

            (pos[0] + size/2, pos[1] - size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] - size/2),

            (pos[0] + size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] - size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] - size/2),
            (pos[0] - size/2, pos[1] + size/2, pos[2] - size/2),

            (pos[0] - size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] - size/2, pos[1] - size/2, pos[2] + size/2),
            (pos[0] - size/2, pos[1] + size/2, pos[2] - size/2),
            (pos[0] - size/2, pos[1] + size/2, pos[2] + size/2),

            (pos[0] - size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] + size/2, pos[1] - size/2, pos[2] - size/2),
            (pos[0] - size/2, pos[1] - size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] - size/2, pos[2] + size/2),

            (pos[0] - size/2, pos[1] + size/2, pos[2] + size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] + size/2),
            (pos[0] - size/2, pos[1] + size/2, pos[2] - size/2),
            (pos[0] + size/2, pos[1] + size/2, pos[2] - size/2)
        ], dtype=np.float32)

    def defineColors(self):
        """
            Define the colors of the 1.0block
        """

        return np.array([(1.0, 0.0, 0.0, 1.0),
                         (0.0, 0.0, 1.0, 1.0),
                         (1.0, 0.6, 0.0, 1.0),
                         (0.0, 1.0, 0.0, 1.0),
                         (1.0, 1.0, 1.0, 1.0),
                         (1.0, 1.0, 0.0, 1.0)])

    def defineTexture(self):
        """
            Define the texture of the block
        """
        return np.array([

            (0.0, 0.0),
            (0.0625, 0.0),
            (0.0, 0.0625),
            (0.0625, 0.0625),

            (0.0, 0.0),
            (1.0, 0.0),
            (0.0, 1.0),
            (1.0, 1.0),

            (0.0, 0.0),
            (1.0, 0.0),
            (0.0, 1.0),
            (1.0, 1.0),

            (0.0, 0.0),
            (1.0, 0.0),
            (0.0, 1.0),
            (1.0, 1.0),

            (0.0, 0.0),
            (1.0, 0.0),
            (0.0, 1.0),
            (1.0, 1.0),

            (0.0, 0.0),
            (1.0, 0.0),
            (0.0, 1.0),
            (1.0, 1.0)
        ], dtype=np.float32)

    def getVertices(self):
        """
            Return the vertices of the block
        """
        
        return self.verts

    def getTexture(self):
        """
            Return the texture of the block
        """
        
        return self.texture

    def drawFace(self, program, face):
        """
            Draw a face of the block

            program(OpenGL.GL.shaders.ShaderProgram) - Shader program
            vert_start_idx(int) - Index of the first vertex of the block. Offset in the vertex array
            face(int) - Face to draw. Index in the vertex array of the cubie
        """
        
        # loc_color = glGetUniformLocation(program, "color")
        
        # # Draw the face of the cubie according the the color
        # colorR, colorG, colorB, colorA = self.colors[face]
        # glUniform4f(loc_color, colorR, colorG, colorB, colorA)

        # Draw the texture of the face
        glBindTexture(GL_TEXTURE_2D, 0)

        glDrawArrays(GL_TRIANGLE_STRIP, face * 4, 4)

        # Draw the black border of the face        
        # border_vertex_idx = np.array([face * 4 + 0, 
        #                               face * 4 + 1,
        #                               face * 4 + 3,
        #                               face * 4 + 2,
        #                               face * 4 + 0])
        
        # glUniform4f(loc_color, 0.0, 0.0, 0.0, 1.0)
        # glDrawElements(GL_LINE_STRIP, len(border_vertex_idx), GL_UNSIGNED_INT, border_vertex_idx)

    def draw(self, program, view, proj):
        
        loc_model = glGetUniformLocation(program, "model")
        model_array = np.array(self.model, dtype=np.float32)
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, model_array)

        loc_view = glGetUniformLocation(program, "view")
        view_array = np.array(view, dtype=np.float32)
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, view_array)

        loc_projection = glGetUniformLocation(program, "projection")
        projection_array = np.array(proj, dtype=np.float32)
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, projection_array)

        for face in range(6):
            self.drawFace(program, face)
            
