import numpy as np

from Material import UniformMatrix4
from Object import BaseObject


class StaticMesh(BaseObject):
    def __init__(self, objName, pos, mesh, material_instance):
        BaseObject.__init__(self, objName, pos, mesh)
        self.matrix_model = None
        self.matrix_mvp = None
        self.set_material_instance(material_instance)

    def set_material_instance(self, material_instance):
        BaseObject.set_material_instance(self, material_instance)
        if material_instance:
            self.matrix_model = UniformMatrix4(material_instance.program, "model")
            self.matrix_mvp = UniformMatrix4(material_instance.program, "mvp")

    def bind(self, vpMatrix):
        self.matrix_model.bind(self.transform.matrix)
        self.matrix_mvp.bind(np.dot(self.transform.matrix, vpMatrix))