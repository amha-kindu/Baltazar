import math
import glm
import glfw

keys = {}

class Camera:
    deltaTime = 1000.0

    def __init__(self, position: glm.vec3, target: glm.vec3):
        
        self.cameraPos = position
        
        self.cameraFront = glm.normalize(target - self.cameraPos)
        
        self.pitch = glm.degrees(math.asin(self.cameraFront.y))
        self.yaw = glm.degrees(math.atan2(self.cameraFront.x, self.cameraFront.z)+math.pi/2)
        
        self.cameraUp = glm.vec3(0.0, 1.0, 0.0)
        self.cameraRight = glm.normalize(glm.cross(self.cameraFront, self.cameraUp))
        self.view = glm.lookAt(self.cameraPos, self.cameraFront + self.cameraPos , self.cameraUp)
        
        self.roll = glm.degrees(math.asin(self.cameraUp.x))
        
    def update(self):
        cameraSpeed =0.006* Camera.deltaTime
        if keys.get(glfw.KEY_W, False):
            self.cameraPos += cameraSpeed * self.cameraFront
        if keys.get(glfw.KEY_S, False):
            self.cameraPos -= cameraSpeed * self.cameraFront
        if keys.get(glfw.KEY_A, False):
            self.cameraPos -= self.cameraRight * cameraSpeed
        if keys.get(glfw.KEY_D, False):
            self.cameraPos += self.cameraRight * cameraSpeed
        if keys.get(glfw.KEY_UP, False):
            self.cameraPos += self.cameraUp * cameraSpeed
        if keys.get(glfw.KEY_DOWN, False):
            self.cameraPos -= self.cameraUp * cameraSpeed
        
        self.view = glm.lookAt(self.cameraPos, self.cameraFront + self.cameraPos, self.cameraUp)