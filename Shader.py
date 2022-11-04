import sys
from OpenGL import GL as gl
import glm, glfw

from Camera import Camera

wavefront_radius = 0

class Shader:

    def __init__(self, vPath, fPath, gPath=''):
        self.program_id = gl.glCreateProgram()

        vshaderCode = self.loadShaderCode(vPath)
        fshaderCode = self.loadShaderCode(fPath)
        if not gPath == '':
            gshaderCode = self.loadShaderCode(gPath) 

        vShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        if not gPath == '':
            gShader = gl.glCreateShader(gl.GL_GEOMETRY_SHADER)

        gl.glShaderSource(vShader, vshaderCode)
        gl.glShaderSource(fShader, fshaderCode)
        if not gPath == '':
            gl.glShaderSource(gShader, gshaderCode)

        self.compile(vShader)
        self.compile(fShader)
        if not gPath == '':
            self.compile(gShader)

        gl.glAttachShader(self.program_id, vShader)
        gl.glAttachShader(self.program_id, fShader)
        if not gPath == '':
            gl.glAttachShader(self.program_id, gShader)

        gl.glLinkProgram(self.program_id)
        self.link()

        gl.glDeleteShader(vShader)
        gl.glDeleteShader(fShader)
        if not gPath == '': 
            gl.glDeleteShader(gShader)

    def update(self, view, projection):
        gl.glUseProgram(self.program_id)
        viewLocation = gl.glGetUniformLocation(self.program_id, 'view')
        gl.glUniformMatrix4fv(viewLocation, 1, gl.GL_FALSE, glm.value_ptr(view))

        projectionLocation = gl.glGetUniformLocation(self.program_id, 'projection')
        gl.glUniformMatrix4fv(projectionLocation, 1, gl.GL_FALSE, glm.value_ptr(projection))
        time = glfw.get_time()/5
        # time = 1.5*math.cos(time)
        
        gl.glUniform1f(
            gl.glGetUniformLocation(
                self.program_id,
                "time",
            ),
            time
        )
        global wavefront_radius
        wavefront_radius += Camera.deltaTime * 20
        
        gl.glUniform1f(
            gl.glGetUniformLocation(
                self.program_id,
                "wavefront_radius",
            ),
            wavefront_radius
        )

    @staticmethod
    def loadShaderCode(path):
        code = ''
        with open(path, 'r') as file:
            codeLines = file.readlines()
            for codeLine in codeLines:
                code += codeLine
        return code

    @staticmethod
    def compile(shader):
        gl.glCompileShader(shader)
        success = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
        if not success:
            log_message = gl.glGetShaderInfoLog(shader)
            print(log_message)
            sys.exit(1)

    def link(self):
        gl.glLinkProgram(self.program_id)
        success = gl.glGetProgramiv(self.program_id, gl.GL_LINK_STATUS)
        if not success:
            log_message = gl.glGetProgramInfoLog(self.program_id)
            print(log_message)
            sys.exit(1)

    def bind(self):
        gl.glUseProgram(self.program_id)

    def unbind(self):
        gl.glUseProgram(0)