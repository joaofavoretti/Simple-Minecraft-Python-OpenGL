import glfw
import glm
from OpenGL.GL import *
import numpy as np
from PIL import Image

from Block import Block
from Dirt import Dirt
from Grass import Grass
from Camera import Camera
from Chunk import Chunk
from World import World

VERTEX_SHADER_FNAME = './shaders/vertex.glsl'
FRAGMENT_SHADER_FNAME = './shaders/fragment.glsl'

TEXTURE_FILE = './assets/texture_atlas.png'

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

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
    print("LINKOU")
    glUseProgram(program)
    print("USOU")

    return program

def createWindow(vert_code, frag_code):
    """
        Execute the correct pipeline to create the window and apply the shaders

        vert_code(str) - Vertex shader code
        frag_code(str) - Fragment shader code
    """

    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Cubo", glfw.get_primary_monitor(), None)
    glfw.make_context_current(window)

    program = applyShaders(vert_code, frag_code)

    return window, program

def keyHandler(window, key, scancode, action, mods):
    """
        Handle the key events

        window(glfw._GLFWwindow) - Window
        key(int) - Key code
        scancode(int) - Scancode
        action(int) - Action code
        mods(int) - Modifiers
    """

    global camera

    # If not key hold, return
    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    if key == glfw.KEY_W:
        camera.moveForward(1.0)
    elif key == glfw.KEY_S:
        camera.moveBackward(1.0)
    elif key == glfw.KEY_A:
        camera.moveLeft(1.0)
    elif key == glfw.KEY_D:
        camera.moveRight(1.0)
    elif key == glfw.KEY_SPACE:
        camera.moveUp(1.0)
    elif key == glfw.KEY_Z:
        camera.moveDown(1.0)

def mouseHandler(window, xpos, ypos):
    """
        Handle the mouse events

        window(glfw._GLFWwindow) - Window
        xpos(float) - X position
        ypos(float) - Y position
    """

    global camera

    camera.processMouseMovement(xpos, ypos)

def mouseButtonHandler(window, button, action, mods):
    """
        Handle the mouse button events

        window(glfw._GLFWwindow) - Window
        button(int) - Button code
        action(int) - Action code
        mods(int) - Modifiers
    """

    global camera

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        camera.breakBlock()
    elif button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        camera.placeBlock()

def loadTexture(texture_file):
    """
        Load the texture file. Texture is 16x16. Pixelation is intentional

        texture_file(str) - Texture file path
    """
    glEnable(GL_TEXTURE_2D)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, 0)

    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)	
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)	
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    # Load image
    image = Image.open(texture_file)
    img_data = image.tobytes("raw", "RGB", 0, -1)

    # Generate texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

def main():
    global camera

    # Setup boring code
    vertex_code = open(VERTEX_SHADER_FNAME, 'r').read()
    fragment_code = open(FRAGMENT_SHADER_FNAME, 'r').read()

    window, program = createWindow(vertex_code, fragment_code)
    glfw.set_key_callback(window, keyHandler)
    glfw.set_cursor_pos_callback(window, mouseHandler)
    glfw.set_mouse_button_callback(window, mouseButtonHandler)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    loadTexture(TEXTURE_FILE)
    
    loc_light_dir = glGetUniformLocation(program, "lightDir")
    glUniform3f(loc_light_dir, 1.0, 1.0, 1.0)
    
    loc_ka = glGetUniformLocation(program, "ka")
    glUniform1f(loc_ka, 0.7)


    loc_kd = glGetUniformLocation(program, "kd")
    glUniform1f(loc_kd, 0.3)
    
    loc_ks = glGetUniformLocation(program, "ks")
    glUniform1f(loc_ks, 0.2)
    
    loc_ns = glGetUniformLocation(program, "ns")
    glUniform1f(loc_ns, 3.0)

    glfw.show_window(window)

    #glEnable(GL_CULL_FACE)
    #glCullFace(GL_BACK)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glClearColor(0.678, 0.847, 0.901, 1.0)

    # Now that the magic starts

    world = World(program, window)

    camera = Camera(world)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        world.vertices_semaphore.acquire()
        loc_viewPos = glGetUniformLocation(program, "viewPos")
        glUniform3f(loc_viewPos, camera.cameraPos[0], camera.cameraPos[1], camera.cameraPos[2])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        world.draw(program, camera)
        glfw.swap_buffers(window)
        world.vertices_semaphore.release()

    glfw.terminate()


if __name__ == "__main__":
    main()
