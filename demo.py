from Renderer import Renderer

import glm
from Shader import Shader

from lighting import DirectionalLight
from model import Model


def main():
    renderer = Renderer("Skyfall", 1380, 800)
    
    dl = DirectionalLight(glm.vec3(1), glm.vec3(0.5), glm.vec3(0.5))
    dl.setDirection(glm.vec3(0.0, -1.0, -1.0))
    renderer.configure_light_source([dl])

    e_field = Model()
    e_field.instances(1000)
    e_field.load_model('resources/models/sun-dial-arrow-obj/sun-dial-arrow.obj')
    field_shader = Shader('resources/models/sun-dial-arrow-obj/custom_shader/field.sdr','shaders/fShader.sdr')
    e_field.custom_shader(field_shader)
    e_field.scale_n_place(glm.vec3(-800.0, 0.0, -80.0), glm.vec3(1))
    e_field.set_orientation(glm.vec3(1.0,0.0,0.0), -90)
    renderer.add_model(e_field)

    mag_field = Model()
    mag_field.instances(1000)
    mag_field.load_model('resources/models/sun-dial-arrow-obj/sun-dial-arrow.obj')
    field_shader = Shader('resources/models/sun-dial-arrow-obj/custom_shader/field.sdr','shaders/fShader.sdr')
    mag_field.custom_shader(field_shader)
    
    for mesh in mag_field.meshes:
        mag_field.materials[mesh.id].diffuse_color=glm.vec4(0,1,0,1)
    mag_field.scale_n_place(glm.vec3(-800.0, 0.0, -80.0), glm.vec3(1))
    renderer.add_model(mag_field)

    renderer.start()


if __name__ == '__main__':
    main()


