import ctypes
import glm
import OpenGL.GL as gl
import numpy as np

import time


class Material(object):
    def __init__(self):
        self.diffuse_map = None
        self.specular_map = None

        self.textures = {}

        self.diffuse_color = None
        self.specular_color = None
        self.ambient_color = None
        self.shininess = 0
        self.opacity = 1.0
        self.IOR = 1.0

    def set_map_textures(self, textures) -> None:
        for texture in textures:
            self.textures[texture.type] = texture

    def set_color(self, ambient: glm.vec4, diffuse: glm.vec4, specular: glm.vec4, shininess: float):
        self.diffuse_color = diffuse
        self.specular_color = specular
        self.ambient_color = ambient
        self.shininess = shininess


class Mesh(object):

    
    def __init__(self, id: int, vertices, indices, attributes=[3,3,2], count=1) -> None:
        self.id = id
        
        self.vertices = np.array(vertices, np.float32)
        self.indices = np.array(indices, np.uint32)

        self.VAO = 0
        self.VBO = 0
        self.EBO = 0
        self.attributes = attributes
        self.count = count

        self.setup_mesh()


    def Draw(self, shader_id: int, mat: Material):
        ##########
        # Colors #
        ##########

        if mat:
            # Ambient
            gl.glUniform4fv(
                gl.glGetUniformLocation(
                    shader_id,
                    "material.ambient",
                ),
                1,
                np.array(mat.ambient_color, np.float32)
            )
            # Diffuse
            gl.glUniform4fv(
                gl.glGetUniformLocation(
                    shader_id,
                    "material.diffuse",
                ),
                1,
                np.array(mat.diffuse_color, np.float32)
            )

            # Specular
            gl.glUniform4fv(
                gl.glGetUniformLocation(
                    shader_id,
                    "material.specular",
                ),
                1,
                np.array(mat.specular_color, np.float32)
            )

            # Shininess
            gl.glUniform1f(
                gl.glGetUniformLocation(
                    shader_id,
                    "material.shininess",
                ),
                mat.shininess
            )
            
            # Shininess
            gl.glUniform1f(
                gl.glGetUniformLocation(
                    shader_id,
                    "material.opacity",
                ),
                mat.opacity
            )
            # IOR
            gl.glUniform1f(
                gl.glGetUniformLocation(
                    shader_id,
                    "material.IOR",
                ),
                mat.IOR
            )

            # Instances
            gl.glUniform1i(
                gl.glGetUniformLocation(
                    shader_id,
                    'count'
                ),
                self.count
            )

            #################
            # Material maps #
            #################
        
            for tex_type, texture in mat.textures.items():
                name = ""
                if tex_type == 'DIFFUSE':
                    name = 'material.diffuse_map'
                elif tex_type == 'SPECULAR':
                    name = 'material.specular_map'
                elif tex_type == 'CUBEMAP':
                    name = 'skybox'
                elif tex_type == 'NORMAL':
                    name = 'material.normal_map'
                elif tex_type == 'DISPLACEMENT':
                    name = 'material.displacement_map'
                
                location = gl.glGetUniformLocation(
                        shader_id,
                        name,
                    )
                texture.bind()
                gl.glUniform1i(
                    location,
                    texture.unit
                )

        gl.glBindVertexArray(self.VAO)

        gl.glDrawElementsInstanced(
            gl.GL_TRIANGLES,
            self.indices.size,
            gl.GL_UNSIGNED_INT,
            None,
            self.count
        )

        for texture in mat.textures.values():
            texture.unbind()

        gl.glBindVertexArray(0)


    
    def setup_mesh(self):
        self.VAO = gl.glGenVertexArrays(1)
        self.VBO = gl.glGenBuffers(1)
        self.EBO = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.VAO)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.VBO)
        start = time.time()
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            self.vertices.size * ctypes.sizeof(ctypes.c_float),
            self.vertices,
            gl.GL_STATIC_DRAW
        )
        end = time.time()
        print("glBufferData Overhead: ", end - start)
    
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            self.indices.size * ctypes.sizeof(ctypes.c_uint),
            self.indices,
            gl.GL_STATIC_DRAW
        )
        offset = self.vertices.size // 4
        # print(offset)

        # Vertex Positions
        gl.glVertexAttribPointer(
            0,
            3,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            0,
            ctypes.c_void_p(0)
        )
        gl.glEnableVertexAttribArray(0)

        

        # Vertex Normals
        gl.glVertexAttribPointer(
            1,
            3,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            0,
            ctypes.c_void_p(offset * ctypes.sizeof(ctypes.c_float))
        )
        gl.glEnableVertexAttribArray(1)

        # Vertex Texture coordinates
        gl.glVertexAttribPointer(
            2,
            3,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            0,
            ctypes.c_void_p(2 * offset * ctypes.sizeof(ctypes.c_float))
        )
        gl.glEnableVertexAttribArray(2)

        # tangent vector
        gl.glVertexAttribPointer(
            3,
            3,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            0,
            ctypes.c_void_p(3 * offset * ctypes.sizeof(ctypes.c_float))
        )
        gl.glEnableVertexAttribArray(3)
        gl.glBindVertexArray(0)





