import glfw
import glm
from OpenGL.GL import *
import numpy as np
import threading

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

class Camera:
    def __init__ (self, world):
        
        self.cameraPos = glm.vec3(0.0, 15.0,  0.0)
        self.cameraFront = glm.vec3(0.0, 0.0, -1.0)
        self.cameraUp = glm.vec3(0.0, 1.0,  0.0)

        self.firstMouse = True
        self.yaw = -90.0
        self.pitch = 0.0
        self.lastX = WINDOW_WIDTH / 2.0
        self.lastY = WINDOW_HEIGHT / 2.0
        self.fov = 45.0
        self.farDistance = 600
        
        self.view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)
        self.proj = glm.perspective(glm.radians(self.fov), WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, self.farDistance)

        self.world = world
        self.updatingChunks = False

        self.nearest_chunk_coord = self.getNearestChunkCoord(self.cameraPos)

    def getView(self):
        return self.view

    def getProj(self):
        return self.proj

    def getNearestChunkCoord(self, pos):
        # TODO: Maybe use euclidean distance from the nearest 4 point ??
        return (round(pos.x / 16), round(pos.z / 16))

    def updateView(self):
        self.view = glm.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)

        if (self.getNearestChunkCoord(self.cameraPos) != self.nearest_chunk_coord and not self.updatingChunks):
            self.nearest_chunk_coord = self.getNearestChunkCoord(self.cameraPos)
            #self.world.updateChunks(self.nearest_chunk_coord)
            self.updatingChunks = True
            update_chunks_thread = threading.Thread(target = self.parallelUpdate)
            update_chunks_thread.start()
    
    def parallelUpdate(self):
        print(self.nearest_chunk_coord)
        self.world.updateChunks(self.nearest_chunk_coord)
        self.updatingChunks = False
    
    def updateProj(self):
        self.proj = glm.perspective(glm.radians(self.fov), WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, self.farDistance)

    def moveForward(self, deltaTime):
        # Andar na direcao de cameraFront, mas sem alterar a altura
        self.cameraPos += glm.normalize(glm.vec3(self.cameraFront.x, 0.0, self.cameraFront.z)) * deltaTime * 0.1
        
        # Andar em direcao a camera
        # self.cameraPos += self.cameraFront * deltaTime * 0.1
        self.updateView()

    def moveBackward(self, deltaTime):
        # Andar na direcao oposta a cameraFront, mas sem alterar a altura
        self.cameraPos -= glm.normalize(glm.vec3(self.cameraFront.x, 0.0, self.cameraFront.z)) * deltaTime * 0.1

        # Andar em direcao oposta a camera
        # self.cameraPos -= self.cameraFront * deltaTime * 0.1
        self.updateView()

    def moveLeft(self, deltaTime):
        self.cameraPos -= glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * deltaTime * 0.1
        self.updateView()

    def moveRight(self, deltaTime):
        self.cameraPos += glm.normalize(glm.cross(self.cameraFront, self.cameraUp)) * deltaTime * 0.1
        self.updateView()

    def moveUp(self, deltaTime):
        self.cameraPos += self.cameraUp * deltaTime * 0.1
        self.cameraPos.y = min(40.0, self.cameraPos.y)
        self.updateView()

    def moveDown(self, deltaTime):
        self.cameraPos -= self.cameraUp * deltaTime * 0.1
        self.cameraPos.y = max(1.0, self.cameraPos.y)
        self.updateView()
    
    def increaseFov(self, deltaTime):
        self.fov += deltaTime * 0.1
        self.fov = min(80.0, self.fov)
        self.updateProj()

    def decreaseFov(self, deltaTime):
        self.fov -= deltaTime * 0.1
        self.fov = max(20.0, self.fov)
        self.updateProj()

    def increaseFar(self, deltaTime):
        self.farDistance += deltaTime
        self.updateProj()

    def decreaseFar(self, deltaTime):
        self.farDistance -= deltaTime
        self.updateProj()

    def breakBlock(self):
        print('break block - Yet to be implemented')

    def placeBlock(self):
        print('place block - Yet to be implemented')

    def processMouseMovement(self, xpos, ypos):
        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos

        self.lastX = xpos
        self.lastY = ypos

        sensitivity = 0.1
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.cameraFront = glm.normalize(front)

        self.updateView()

        
