import sys
import glm
import assimp_py as assimp
import OpenGL.GL as gl

from Mesh import Material, Mesh
from Texture import Texture



class Model(object):
    def __init__(self) -> None:
        self.count = 1

        self.meshes = []
        self.materials = {}
        self.model_dir = ''
        self.location = glm.vec3(0.0)
        self.scale = glm.vec3(1.0)
        self.axis = glm.vec3(1.0)
        self.angle = 0
        self.shader= None
        self.background = False
    
    def instances(self, count: int):
        self.count = count

    def custom_shader(self, shader):
        self.shader = shader

    def draw(self, shader_id: int):

        if not self.shader is None:
            shader_id = self.shader.program_id
        if self.background:
            gl.glDepthMask(gl.GL_FALSE)
        gl.glUseProgram(shader_id)
        self.update(shader_id)
        for mesh in self.meshes:
            mesh.Draw(shader_id, self.materials[mesh.id])
        gl.glDepthMask(gl.GL_TRUE)

    def scale_n_place(self, loc: glm.vec3, scale=glm.vec3(1.0)):
        self.location = self.location if loc is None else loc
        self.scale = self.scale if scale is None else scale

    def set_orientation(self, axis, angle):
        self.axis = axis
        self.angle = glm.radians(angle)

    def update(self, shader_id: int):
        model_loc = gl.glGetUniformLocation(shader_id, 'model')

        translate = glm.translate(self.location)
        rotate = glm.rotate(translate, self.angle, self.axis)
        model = glm.scale(rotate, self.scale)

        gl.glUniformMatrix4fv(model_loc, 1, gl.GL_FALSE, glm.value_ptr(model))

    
    def load_model(self, model_path: str) -> None:
        index = model_path.rfind("\\")
        index = model_path.rfind("/") if index == -1 else index
        self.model_dir = model_path[:index+1]

        # -- loading the scene
        process_flags = (
            assimp.Process_Triangulate | assimp.Process_CalcTangentSpace
        )
        try:
            scene = assimp.ImportFile(model_path, process_flags)
        except:
            print("Couldn't import file!")
            sys.exit(1)

        self.generate_meshes(scene)
        self.generate_materials(scene)
        print("Number of meshes: ", len(self.meshes))

    
    def generate_meshes(self, scene):
        
        for aiMesh in scene.meshes:
            indices =[]
            for i in aiMesh.indices:
                if len(i)!=3:
                    continue
                indices.append(i)
            
            m = Mesh(aiMesh.material_index, aiMesh.vertices + aiMesh.normals + aiMesh.texcoords[0]+aiMesh.tangents, indices, count=self.count)

            self.meshes.append(m)

    
    def generate_materials(self, scene) -> None:

        for mesh in scene.meshes:
            material = scene.materials[mesh.material_index]
            diffuse_color = material["COLOR_DIFFUSE"]
            ambient_color = material["COLOR_AMBIENT"]
            specular_color = material["COLOR_SPECULAR"]
            shininess = material["SHININESS"]
            opacity = material["OPACITY"]
            IOR = material["REFRACTI"]
            m = Material()

            textures = material["TEXTURES"]
            tex_maps = []
            if textures != {} and assimp.TextureType_DIFFUSE in textures.keys():
                diffuse_color = [0.0, 0.0, 0.0]
                diffuse_map = textures.pop(assimp.TextureType_DIFFUSE)
                last = diffuse_map[0].rfind('\\')
                last = diffuse_map[0].rfind('/') if last == -1 else last
                diffuse_map[0] = diffuse_map[0] if last == -1 else diffuse_map[0][last+1:]
                print(diffuse_map[0])
                t_diffuse = Texture(self.model_dir+"textures/"+diffuse_map[0], "DIFFUSE")
                
                tex_maps.append(t_diffuse)
            
            if textures != {} and assimp.TextureType_SPECULAR in textures.keys():
                specular_color = [0.0, 0.0, 0.0]
                specular_map = textures.pop(assimp.TextureType_SPECULAR)
                last = specular_map[0].rfind('\\')
                last = specular_map[0].rfind('/') if last == -1 else last
                specular_map[0] = specular_map[0] if last == -1 else specular_map[0][last + 1:]
                print(specular_map[0])
                t_specular = Texture(self.model_dir+"textures/"+specular_map[0], "SPECULAR", 1)

                tex_maps.append(t_specular)

            if textures != {} and assimp.TextureType_HEIGHT in textures.keys():
                
                normal_map = textures.pop(assimp.TextureType_HEIGHT)
                last = normal_map[0].rfind('\\')
                last = normal_map[0].rfind('/') if last == -1 else last
                normal_map[0] = normal_map[0] if last == -1 else normal_map[0][last+1:]
                print(normal_map[0])
                t_normal= Texture(self.model_dir+"textures/"+normal_map[0], "NORMAL", 2)
                
                tex_maps.append(t_normal)

            if textures != {} and assimp.TextureType_DISPLACEMENT in textures.keys():
                
                displacement_map = textures.pop(assimp.TextureType_DISPLACEMENT)
                last = displacement_map[0].rfind('\\')
                last = displacement_map[0].rfind('/') if last == -1 else last
                displacement_map[0] = displacement_map[0] if last == -1 else displacement_map[0][last+1:]
                print(displacement_map[0])
                displacement_texture= Texture(self.model_dir+"textures/"+displacement_map[0], "DISPLACEMENT", 3)
                
                tex_maps.append(displacement_texture)

            m.set_color(
                glm.vec4(ambient_color+[opacity]), 
                glm.vec4(diffuse_color+[opacity]), 
                glm.vec4(specular_color+[opacity]), 
                shininess,
            )
            m.IOR = IOR
            m.set_map_textures(tex_maps)
            self.materials[mesh.material_index] = m


