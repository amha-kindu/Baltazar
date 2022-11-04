from OpenGL import GL as gl
from PIL import Image as im
import numpy as np


class Texture:
    textureUnits = [
        gl.GL_TEXTURE0, gl.GL_TEXTURE1, gl.GL_TEXTURE2, gl.GL_TEXTURE3, gl.GL_TEXTURE4, gl.GL_TEXTURE5, gl.GL_TEXTURE6, gl.GL_TEXTURE7, gl.GL_TEXTURE8, gl.GL_TEXTURE9, gl.GL_TEXTURE10
    ]

    def __init__(self, filePath: str, tex_type: str, unit = 0, target = gl.GL_TEXTURE_2D):

        tex = im.open(filePath).transpose(im.FLIP_TOP_BOTTOM)
        texelArray = np.array(tex)
        self.width = tex.width
        self.height = tex.height
        tex.close()
        self.unit = unit

        self.tex_id = gl.glGenTextures(1)
        print(self.tex_id, self.textureUnits[self.unit])
        self.type = tex_type

        gl.glActiveTexture(self.textureUnits[self.unit])
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex_id)
        self.configure()
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,                   # texture target
            0,                                  # mipmap level( if we were setting each mipmaps manually)
            gl.GL_RGB,                          # format to store the texture
            self.width,                         #
            self.height,                        #
            0,                                  # legacy parameter(always zero)
            gl.GL_RGB,                          # format of the source image
            gl.GL_UNSIGNED_BYTE,                # data type of the source image
            texelArray                          # image data
        )
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def getUnit(self):
        return self.textureUnits[self.unit]

    def bind(self):
        gl.glActiveTexture(self.textureUnits[self.unit])
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.tex_id)

    def unbind(self):
        gl.glActiveTexture(self.textureUnits[0])
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def configure(self):
        # Setting the texture wrapping mode
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D,           # Texture target
            gl.GL_TEXTURE_WRAP_S,       # Specifying for which axis we want this wrapping, S
            gl.GL_REPEAT       # Texture wrapping mode
        )
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D,           # Texture target
            gl.GL_TEXTURE_WRAP_T,       # Specifying for which axis we want this wrapping, T
            gl.GL_REPEAT       # Texture wrapping mode
        )

        # Setting the texture  mode
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D,               # Texture target
            gl.GL_TEXTURE_MIN_FILTER,       # For minifying operations
            gl.GL_LINEAR_MIPMAP_LINEAR      # Texture filtering mode
        )
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D,               # Texture target
            gl.GL_TEXTURE_MAG_FILTER,       # For magnifying operations
            gl.GL_LINEAR                    # Texture filtering mode
        )


        
class CubeMap(Texture):
    def __init__(self, tblrfb, unit = 0):
        self.type = "CUBEMAP"
        self.unit = unit
        self.tex_id = gl.glGenTextures(1)
        gl.glActiveTexture(Texture.textureUnits[unit])
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.tex_id)
        i = 0
        for face in tblrfb:
            if face == '':
                continue
            tex = im.open(face)
            texelArray = np.array(tex)
            width = tex.width
            height = tex.height
            tex.close()

            gl.glTexImage2D(
                gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X+i,  # texture target
                0,                                  # mipmap level( if we were setting each mipmaps manually)
                gl.GL_RGB,                          # format to store the texture
                width,                              #
                height,                             #
                0,                                  # legacy parameter(always zero)
                gl.GL_RGB,                          # format of the source image
                gl.GL_UNSIGNED_BYTE,                # data type of the source image
                texelArray                          # image data
            )
            i+=1
            
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)
        
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, 0)

    def bind(self):
        gl.glActiveTexture(Texture.textureUnits[self.unit])
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.tex_id)

    def unbind(self):
        gl.glActiveTexture(Texture.textureUnits[self.unit])
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, 0)




