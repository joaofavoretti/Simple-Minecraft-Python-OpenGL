import glfw
import glm
from OpenGL.GL import *
import numpy as np
from PIL import Image

import Block
import Camera

VERTEX_SHADER_FNAME = './shaders/vertex.glsl'
FRAGMENT_SHADER_FNAME = './shaders/fragment.glsl'

TEXTURE_FILE = './assets/texture_atlas.png'

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def applyShaders(vert_code, frag_code):
    """
        Execute the correct pipeline to apply the shaders to the program

        vert_code(str) - Vertex shader code
        frag_code(str) - Fragment shader code
    """

    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex, vert_code)
    glShaderSource(fragment, frag_code)

    glCompileShader(vertex)
    glCompileShader(fragment)

    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    glLinkProgram(program)
    glUseProgram(program)

    return program

def createWindow(vert_code, frag_code):
    """
        Execute the correct pipeline to create the window and apply the shaders

        vert_code(str) - Vertex shader code
        frag_code(str) - Fragment shader code
    """

    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Cubo", None, None)
    glfw.make_context_current(window)

    program = applyShaders(vert_code, frag_code)

    return window, program

def sendVerticesAndTexture(program, vertices, texture):
    """
        Send the vertices to the GPU

        program(OpenGL.GL.shaders.ShaderProgram) - Shader program
        vertices(numpy.ndarray) - Vertices to be sent to the GPU
        texture(numpy.ndarray) - Texture to be sent to the GPU
    """

    # TODO: Testar usar o comando glGenBuffers 2 vezes (Para separar essa funcao em duas)

    buffer = glGenBuffers(2)
    
    # Vertices
    glBindBuffer(GL_ARRAY_BUFFER, buffer[0])
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)

    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)

    glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

    # Texture
    glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
    glBufferData(GL_ARRAY_BUFFER, texture.nbytes, texture, GL_STATIC_DRAW)

    loc = glGetAttribLocation(program, "texture")
    glEnableVertexAttribArray(loc)

    stride = texture.strides[0]
    offset = ctypes.c_void_p(0)

    glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)


def keyHandler(window, key, scancode, action, mods):
    """
        Handle the key events

        window(glfw._GLFWwindow) - Window
        key(int) - Key code
        scancode(int) - Scancode
        action(int) - Action code
        mods(int) - Modifiers
    """

    global c

    # If not key hold, return
    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    if key == glfw.KEY_W:
        c.moveForward(1.0)
    elif key == glfw.KEY_S:
        c.moveBackward(1.0)
    elif key == glfw.KEY_A:
        c.moveLeft(1.0)
    elif key == glfw.KEY_D:
        c.moveRight(1.0)

def mouseHandler(window, xpos, ypos):
    """
        Handle the mouse events

        window(glfw._GLFWwindow) - Window
        xpos(float) - X position
        ypos(float) - Y position
    """

    global c

    c.processMouseMovement(xpos, ypos)

def loadTexture(texture_file):
    """
        Load the texture file

        texture_file(str) - Texture file path
    """

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, 0)

    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)	
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)	
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Load image
    image = Image.open(texture_file)
    img_data = image.tobytes("raw", "RGB", 0, -1)

    # Generate texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

def main():
    global c

    vertex_code = open(VERTEX_SHADER_FNAME, 'r').read()
    fragment_code = open(FRAGMENT_SHADER_FNAME, 'r').read()

    window, program = createWindow(vertex_code, fragment_code)
    glfw.set_key_callback(window, keyHandler)
    glfw.set_cursor_pos_callback(window, mouseHandler)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    glEnable(GL_TEXTURE_2D)
    loadTexture(TEXTURE_FILE)

    glfw.show_window(window)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.678, 0.847, 0.901, 1.0)

    # TODO: Add a way to keep information about the vertex indices for each Block
    b = Block.Block((0.0, 0.0, 0.0))
    c = Camera.Camera()

    vertices = b.getVertices()
    texture = b.getTexture()
    print(texture)
    sendVerticesAndTexture(program, vertices, texture)
    
    # TODO: todo
    # texture = b.getTexture()
    # sendTexture(program, texture)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        b.draw(program, c.getView(), c.getProj())

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
