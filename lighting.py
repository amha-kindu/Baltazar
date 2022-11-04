import glm
import OpenGL.GL as gl


class LightSource(object):
    def __init__(self, ambient: glm.vec3, diffuse: glm.vec3, specular: glm.vec3) -> None:
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

    def update(self, cam):
        pass

    def lit_scene(self, shader_id: int, camPos: glm.vec3):
        camPosLoc = gl.glGetUniformLocation(shader_id, 'camPos')
        gl.glUniform3fv(camPosLoc, 1, glm.value_ptr(camPos))


class PointLight(LightSource):
    count = 0

    def __init__(self, ambient: glm.vec3, diffuse: glm.vec3, specular: glm.vec3) -> None:
        super().__init__(ambient, diffuse, specular)
        PointLight.count += 1
        self.position = None
        self.constant = 1.0
        self.linear = 0.09
        self.quadratic = 0.032

    def setPosition(self, pos: glm.vec3) -> None:
        self.position = pos

    def update(self, cam):
        # self.setPosition(self.position)
        pass
        

    def setAttenuation(self, constant: float, linear: float, quadratic: float):
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic
        
    def lit_scene(self, shader_id: int, camPos: glm.vec3):
        super().lit_scene(shader_id, camPos)
        var = 'pt_lights['+str(PointLight.count-1)+']'
        
        gl.glUniform1i(
            gl.glGetUniformLocation(shader_id, var+'.lit'), 
            1
        )
        pointlightLoc = gl.glGetUniformLocation(shader_id, var+'.position')
        gl.glUniform3fv(pointlightLoc, 1, glm.value_ptr(self.position))

        pointLightAmbLoc = gl.glGetUniformLocation(shader_id, var+'.ambient')
        gl.glUniform3fv(pointLightAmbLoc, 1, glm.value_ptr(self.ambient))

        pointLightDiffLoc = gl.glGetUniformLocation(shader_id, var+'.diffuse')
        gl.glUniform3fv(pointLightDiffLoc, 1, glm.value_ptr(self.diffuse))

        pointLightSpecLoc = gl.glGetUniformLocation(shader_id, var+'.specular')
        gl.glUniform3fv(pointLightSpecLoc, 1, glm.value_ptr(self.specular))

        constLoc = gl.glGetUniformLocation(shader_id, var+'.constant')
        gl.glUniform1f(constLoc, self.constant)

        linearLoc = gl.glGetUniformLocation(shader_id, var+'.linear')
        gl.glUniform1f(linearLoc, self.linear)

        quadLoc = gl.glGetUniformLocation(shader_id, var+'.quadratic')
        gl.glUniform1f(quadLoc, self.quadratic)


class DirectionalLight(LightSource):
    def __init__(self, ambient: glm.vec3, diffuse: glm.vec3, specular: glm.vec3) -> None:
        super().__init__(ambient, diffuse, specular)
        self.direction = None

    def setDirection(self, dir: glm.vec3) -> None:
        self.direction = dir


    def lit_scene(self, shader_id: int, camPos: glm.vec3):
        super().lit_scene(shader_id, camPos)
        gl.glUniform1i(
            gl.glGetUniformLocation(shader_id, 'dirLight.lit'), 
            1
        )

        dirlightLoc = gl.glGetUniformLocation(shader_id, 'dirLight.direction')
        gl.glUniform3fv(dirlightLoc, 1, glm.value_ptr(self.direction))

        dirlightAmbLoc = gl.glGetUniformLocation(shader_id, 'dirLight.ambient')
        gl.glUniform3fv(dirlightAmbLoc, 1, glm.value_ptr(self.ambient))

        dirlightDiffLoc = gl.glGetUniformLocation(shader_id, 'dirLight.diffuse')
        gl.glUniform3fv(dirlightDiffLoc, 1, glm.value_ptr(self.diffuse))

        dirlightSpecLoc = gl.glGetUniformLocation(shader_id, 'dirLight.specular')
        gl.glUniform3fv(dirlightSpecLoc, 1, glm.value_ptr(self.specular))


class SpotLight(LightSource):
    def __init__(self, ambient: glm.vec3, diffuse: glm.vec3, specular: glm.vec3) -> None:
        super().__init__(ambient, diffuse, specular)
        self.direction = None
        self.cutOff = 30
        self.outerCutOff = 40

        self.position = None
        self.constant = 1.0
        self.linear = 0.09
        self.quadratic = 0.032
    
    def setPosition(self, pos: glm.vec3) -> None:
        self.position = pos

    def setAttenuation(self, constant: float, linear: float, quadratic: float):
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic

    def setDirection(self, dir: glm.vec3) -> None:
        self.direction = dir

    def setUpCutoff(self, inner: float, outer: float) -> None:
        self.cutOff = glm.radians(inner)
        self.outerCutOff = glm.radians(outer)

    def update(self, cam):
        self.setDirection(cam.cameraFront)
        self.setPosition(cam.cameraPos)

    def lit_scene(self, shader_id: int, camPos: glm.vec3):
        super().lit_scene(shader_id, camPos)

        gl.glUniform1i(
            gl.glGetUniformLocation(shader_id, 'sp_light.lit'), 
            1
        )
        spotLightDirLoc = gl.glGetUniformLocation(shader_id, 'sp_light.direction')
        gl.glUniform3fv(spotLightDirLoc, 1, glm.value_ptr(self.direction))

        spotLightPosLoc = gl.glGetUniformLocation(shader_id, 'sp_light.pt.position')
        gl.glUniform3fv(spotLightPosLoc, 1, glm.value_ptr(self.position))

        spotLightAmbLoc = gl.glGetUniformLocation(shader_id, 'sp_light.pt.ambient')
        gl.glUniform3fv(spotLightAmbLoc, 1, glm.value_ptr(self.ambient))

        spotLightDiffLoc = gl.glGetUniformLocation(shader_id, 'sp_light.pt.diffuse')
        gl.glUniform3fv(spotLightDiffLoc, 1, glm.value_ptr(self.diffuse))

        spotLightSpecLoc = gl.glGetUniformLocation(shader_id, 'sp_light.pt.specular')
        gl.glUniform3fv(spotLightSpecLoc, 1, glm.value_ptr(self.specular))

        spotLightConstLoc = gl.glGetUniformLocation(shader_id, 'sp_light.pt.constant')
        gl.glUniform1f(spotLightConstLoc, self.constant)

        spotLightLinearLoc = gl.glGetUniformLocation(shader_id, 'sp_light.pt.linear')
        gl.glUniform1f(spotLightLinearLoc, self.linear)

        spotLightQuadLoc = gl.glGetUniformLocation(shader_id, 'sp_light.pt.quadratic')
        gl.glUniform1f(spotLightQuadLoc, self.quadratic)

        spotLightCutOffLoc = gl.glGetUniformLocation(shader_id, 'sp_light.cutOff')
        gl.glUniform1f(spotLightCutOffLoc, self.cutOff)

        spotLightOuterCutOffLoc = gl.glGetUniformLocation(shader_id, 'sp_light.outerCutOff')
        gl.glUniform1f(spotLightOuterCutOffLoc, self.outerCutOff)






