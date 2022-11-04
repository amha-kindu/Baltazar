from Shader import Shader
from lighting import LightSource
from model import Model
import glm


class Scene(object):
    
    def __init__(self, shader: Shader, eye) -> None:
        self.eye = eye

        self.lights = []
        self.models = []
        self.shader = shader
        self.projection = None

    def add_light_source(self, ls: LightSource) -> None:
        self.lights.append(ls)

    def add_models(self, model: Model) -> None:
        self.models.insert(0, model)

    def render(self):
        self.shader.bind()
        self.eye.update()
        for ls in self.lights:
            ls.update(self.eye)
            ls.lit_scene(self.shader.program_id, self.eye.cameraPos)

        for model in self.models:
            if not model.shader is None:
                view = self.eye.view
                if model.background:
                    view = glm.mat4(glm.mat3(view))
                model.shader.update(view, self.projection)
                for ls in self.lights:
                    ls.update(self.eye)
                    ls.lit_scene(model.shader.program_id, self.eye.cameraPos)
            else:
                self.shader.update(self.eye.view, self.projection)

            # if model.pov:
            #     new_pos = (self.eye.cameraPos+glm.vec3(0.0, -10.0, -10*model.scale.x))
            #     model.scale_n_place(new_pos, scale=model.scale)
            #     model.set_orientation(self.eye.cameraRight, self.eye.pitch)

            model.draw(self.shader.program_id)


