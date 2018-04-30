import numpy as np

from Common import logger
from App.CoreManager import CoreManager
from Object import StaticActor
from Utilities import *


# ------------------------------ #
# CLASS : Camera
# ------------------------------ #
class Camera(StaticActor):
    def __init__(self, name, scene_manager, **object_data):
        StaticActor.__init__(self, name, **object_data)

        self.scene_manager = scene_manager
        self.postprocess = self.scene_manager.renderer.postprocess

        self.transform.setPos([0.0, 1.0, 0.0])

        self.meter_per_unit = object_data.get('meter_per_unit', 1.0)
        self.aspect = object_data.get('aspect', 0.0)
        self.fov = object_data.get('fov', 0.0)
        self.near = object_data.get('near', 0.0)
        self.far = object_data.get('far', 0.0)
        self.move_speed = object_data.get('move_speed', 0.0)
        self.pan_speed = object_data.get('pan_speed', 0.0)
        self.rotation_speed = object_data.get('rotation_speed', 0.0)

        self.left_diagonal = Float3()
        self.right_diagonal = Float3()
        self.top_diagonal = Float3()
        self.bottom_diagonal = Float3()

        self.projection = Matrix4()
        self.projection_offset = Float2()

        self.view = Matrix4()
        self.view_origin = Matrix4()
        self.view_projection = Matrix4()
        self.view_origin_projection = Matrix4()

        self.prev_view = Matrix4()
        self.prev_view_origin = Matrix4()
        self.prev_view_projection = Matrix4()
        self.prev_view_origin_projection = Matrix4()

    def initialize(self):
        config = CoreManager.instance().projectManager.config
        # get properties
        self.fov = config.Camera.fov
        self.near = config.Camera.near
        self.far = config.Camera.far
        self.move_speed = config.Camera.move_speed
        self.pan_speed = config.Camera.pan_speed
        self.rotation_speed = config.Camera.rotation_speed

    def get_save_data(self):
        save_data = StaticActor.get_save_data(self)
        save_data['meter_per_unit'] = 1.0
        save_data['aspect'] = 0.0
        save_data['fov'] = 0.0
        save_data['near'] = 0.0
        save_data['far'] = 0.0
        save_data['move_speed'] = 0.0
        save_data['pan_speed'] = 0.0
        save_data['rotation_speed'] = 0.0
        return save_data

    def write_to_config(self, config):
        config.setValue("Camera", "meter_per_unit", self.meter_per_unit)
        config.setValue("Camera", "aspect", self.aspect)
        config.setValue("Camera", "fov", self.fov)
        config.setValue("Camera", "near", self.near)
        config.setValue("Camera", "far", self.far)
        config.setValue("Camera", "move_speed", self.move_speed)
        config.setValue("Camera", "pan_speed", self.pan_speed)
        config.setValue("Camera", "rotation_speed", self.rotation_speed)

    def getAttribute(self):
        StaticActor.getAttribute(self)
        self.attributes.setAttribute('fov', self.fov)
        self.attributes.setAttribute('near', self.near)
        self.attributes.setAttribute('far', self.far)
        self.attributes.setAttribute('move_speed', self.move_speed)
        self.attributes.setAttribute('pan_speed', self.pan_speed)
        self.attributes.setAttribute('rotation_speed', self.rotation_speed)
        return self.attributes

    def setAttribute(self, attributeName, attributeValue, attribute_index):
        StaticActor.setAttribute(self, attributeName, attributeValue, attribute_index)
        if hasattr(self, attributeName):
            setattr(self, attributeName, attributeValue)
            # update viewport
            self.scene_manager.renderer.resizeScene()

    def update_projection(self, fov=0.0, aspect=0.0, force_update=False):
        need_to_update = False
        if 0.0 < fov and fov != self.fov:
            self.fov = fov
            need_to_update = True

        if 0.0 < aspect and aspect != self.aspect:
            self.aspect = aspect
            need_to_update = True

        if force_update or need_to_update:
            self.projection[...] = perspective(self.fov, self.aspect, self.near, self.far)

    def update(self, force_update=False):
        updated = self.transform.updateTransform(update_view_transform=True, force_update=force_update)

        if updated or force_update:
            self.top_diagonal[...] = normalize(-self.transform.front + self.transform.up / self.projection[1][1])
            self.bottom_diagonal[...] = normalize(-self.transform.front - self.transform.up / self.projection[1][1])
            self.left_diagonal[...] = normalize(-self.transform.front - self.transform.left / self.projection[0][0])
            self.right_diagonal[...] = normalize(-self.transform.front + self.transform.left / self.projection[0][0])

            self.prev_view = self.transform.prev_inverse_matrix
            self.prev_view_origin[...] = self.view_origin

            self.view = self.transform.inverse_matrix
            self.view_origin[...] = self.view
            self.view_origin[3, 0:3] = [0.0, 0.0, 0.0]

        self.prev_view_projection[...] = self.view_projection
        self.prev_view_origin_projection[...] = self.view_origin_projection

        # Update projection jitter.
        # This part is very important because the w value of the projection matrix 3rd row is ​​-1.0.
        self.projection[2][0] = -self.postprocess.jitter[0]
        self.projection[2][1] = -self.postprocess.jitter[1]

        self.view_projection[...] = np.dot(self.view, self.projection)
        self.view_origin_projection[...] = np.dot(self.view_origin, self.projection)
