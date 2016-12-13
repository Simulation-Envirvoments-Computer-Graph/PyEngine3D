import os
import glob
import configparser
import time
import traceback

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GL.shaders import glDetachShader
from PIL import Image

from Render import *
from Core import logger
from Utilities import Singleton, getClassName
from Render import Shader, Material, Texture
from Object import Triangle, Quad, Mesh, Primitive


# -----------------------#
# CLASS : MetaData
# -----------------------#
class MetaData:
    def __init__(self, filePath):
        if filePath != "" and os.path.exists(filePath):
            self.filePath = filePath
            self.dateTime = os.path.getmtime(filePath)
            self.timeStamp = time.ctime(self.dateTime)
        else:
            self.filePath = ""
            self.dateTime = 0.0
            self.timeStamp = time.ctime(self.dateTime)


# -----------------------#
# CLASS : ResourceLoader
# -----------------------#
class ResourceLoader(object):
    def __init__(self, dirName, fileExt):
        self.resources = {}
        self.metaDatas = {}
        self.dirName = dirName
        self.fileExt = fileExt.lower()

    def initialize(self):
        logger.info("initialize " + getClassName(self))

        # collect shader files
        for dirname, dirnames, filenames in os.walk(self.dirName):
            for filename in filenames:
                if self.fileExt == ".*" or self.fileExt == os.path.splitext(filename)[1].lower():
                    filename = os.path.join(dirname, filename)
                    resource = self.loadResource(filename)
                    if resource:
                        self.registResource(resource, filename)
                    else:
                        logger.error("load %s error" % filename)
            
    def createResource(self):
        """ create resource file and regist."""
        pass
    
    def deleteResource(self, resource):
        """ delete resource file and release."""
        if resource:
            metaData = self.getMetaData(resource)
            self.releaseResource(resource)            
            if metaData:
                filePath = metaData.filePath
                if os.path.exists(filePath):
                    os.remove(filePath)
                    logger.info("Remove %s file" & filePath)
       
    def registResource(self, resource, filePath=""):
        if resource is None or not hasattr(resource, "name"):
            raise AttributeException("resource have to has name.")        
        newMetaData = MetaData(filePath)                
        # check the file is exsits resource or not.
        if resource.name in self.resources:
            oldResource = self.resources[resource.name]
            oldMetaData = self.getMetaData(oldResource)
            if oldMetaData:
                if newMetaData.filePath == oldMetaData.filePath and newMetaData.dateTime == oldMetaData.dateTime:
                    # Same resource
                    return
        # regist new resource
        self.resources[resource.name] = resource
        self.metaDatas[resource] = newMetaData
        
    def releaseResource(self, resource):
        if resource:
            if resource.name in self.resources:
                self.resources.pop(resource.name)
            if resource in self.metaDatas:
                self.metaDatas.pop(resource)

    @staticmethod
    def splitResourceName(filepath):
        resourceName = os.path.splitext(os.path.split(filepath)[1])[0]
        return resourceName.lower()

    def loadResource(self, filePath):
        raise BaseException("You must implement loadResource.")

    def getResource(self, resourceName):
        if resourceName in self.resources:
            return self.resources[resourceName]
        logger.error("Not found %s." % resourceName)
        return None

    def getResourceList(self):
        return list(self.resources.values())

    def getResourceNameList(self):
        return list(self.resources.keys())
    
    def getMetaData(self, resource):
        if resource in self.metaDatas:
            return self.metaDatas[resource]
        logger.error("Not found meta data of %s." % resource.name)
        return None


# ---------------------------#
# CLASS : VertexShaderLoader
# ---------------------------#
class VertexShaderLoader(ResourceLoader, Singleton):
    def __init__(self):
        super(VertexShaderLoader, self).__init__(PathShaders, ".vs")

    def loadResource(self, filePath):
        try:
            f = open(filePath, 'r')
            shaderSource = f.read()
            f.close()
            shaderName = self.splitResourceName(filePath)
            return VertexShader(shaderName, shaderSource)
        except:
            logger.error(traceback.format_exc())

    def close(self):
        for shader in self.resources.values():
            shader.delete()


# ---------------------------#
# CLASS : FragmentShaderLoader
# ---------------------------#
class FragmentShaderLoader(ResourceLoader, Singleton):
    def __init__(self):
        super(FragmentShaderLoader, self).__init__(PathShaders, ".fs")

    def loadResource(self, filePath):
        try:
            f = open(filePath, 'r')
            shaderSource = f.read()
            f.close()
            shaderName = self.splitResourceName(filePath)
            return FragmentShader(shaderName, shaderSource)
        except:
            logger.error(traceback.format_exc())

    def close(self):
        for shader in self.resources.values():
            shader.delete()


# -----------------------#
# CLASS : MaterialLoader
# -----------------------#
class MaterialLoader(ResourceLoader, Singleton):
    def __init__(self):
        super(MaterialLoader, self).__init__(PathMaterials, ".material")

    def loadResource(self, filePath):
        try:
            materialFile = configparser.ConfigParser()
            materialFile.read(filePath)
            vs = VertexShaderLoader.instance().getResource(materialFile.get("VertexShader", "shaderName"))
            fs = FragmentShaderLoader.instance().getResource(materialFile.get("FragmentShader", "shaderName"))
            materialName = self.splitResourceName(filePath)
            return Material(materialName=materialName, vs=vs, fs=fs)
        except:
            logger.error(traceback.format_exc())


# -----------------------#
# CLASS : MeshLoader
# -----------------------#
class MeshLoader(ResourceLoader, Singleton):
    def __init__(self):
        super(MeshLoader, self).__init__(PathMeshes, ".mesh")

    def initialize(self):
        super(MeshLoader, self).initialize()

        # Regist basic meshs
        self.registResource(Triangle())
        self.registResource(Quad())

    def loadResource(self, filePath):
        try:
            # load from mesh
            f = open(filePath, 'r')
            meshData = eval(f.read())
            f.close()
            
            meshName = self.splitResourceName(filePath)
            return Mesh(meshName, meshData)
        except:
            logger.error(traceback.format_exc())
        

# -----------------------#
# CLASS : TextureLoader
# -----------------------#
class TextureLoader(ResourceLoader, Singleton):
    def __init__(self):
        super(TextureLoader, self).__init__(PathTextures, ".*")

    def loadResource(self, filePath):
        try:
            image = Image.open(filePath)
            ix, iy = image.size
            buffer = image.tobytes("raw", "RGBX", 0, -1)
            textureName = self.splitResourceName(filePath)
            return Texture(textureName, buffer, ix, iy)
        except:
            logger.error(traceback.format_exc())

    def getTextureID(self, resourceName):
        return self.resources[resourceName].textureID if resourceName in self.resources else -1


# -----------------------#
# CLASS : ResourceManager
# -----------------------#
class ResourceManager(Singleton):
    def __init__(self):
        self.textureLoader = TextureLoader.instance()
        self.vertexShaderLoader = VertexShaderLoader.instance()
        self.fragmentShaderLoader = FragmentShaderLoader.instance()
        self.materialLoader = MaterialLoader.instance()
        self.meshLoader = MeshLoader.instance()

    def initialize(self):
        self.textureLoader.initialize()
        self.vertexShaderLoader.initialize()
        self.fragmentShaderLoader.initialize()
        self.materialLoader.initialize()
        self.meshLoader.initialize()

    def close(self):
        self.vertexShaderLoader.close()
        self.fragmentShaderLoader.close()

    def getResourceList(self):
        """
        :return [(resource name, resource type)]:
        """
        result = []
        for resName in self.getVertexShaderNameList():
            result.append((resName, getClassName(self.getVertexShader(resName))))
        for resName in self.getFragmentShaderNameList():
            result.append((resName, getClassName(self.getFragmentShader(resName))))
        for resName in self.getMaterialNameList():
            result.append((resName, getClassName(self.getMaterial(resName))))
        for resName in self.getMeshNameList():
            result.append((resName, getClassName(self.getMesh(resName))))
        return result

    def getResourceAttribute(self, resName, resTypeName):
        try:
            resType = eval(resTypeName)
            resource = self.getResource(resName, resType)
            if resource:
                return resource.getAttribute()
            return None
        except:
            logger.error(traceback.format_exc())

    def getResource(self, resName, resType):
        resource = None
        if resType == FragmentShader:
            resource = self.getFragmentShader(resName)
        elif resType == VertexShader:
            resource = self.getVertexShader(resName)
        elif resType == Material:
            resource = self.getMaterial(resName)
        elif resType == Texture:
            resource = self.getTexture(resName)
        elif issubclass(resType, Primitive):
            resource = self.getMesh(resName)
        return resource

    # FUNCTIONS : Shader

    def getVertexShader(self, shaderName):
        return self.vertexShaderLoader.getResource(shaderName)

    def getFragmentShader(self, shaderName):
        return self.fragmentShaderLoader.getResource(shaderName)

    def getVertexShaderNameList(self):
        return self.vertexShaderLoader.getResourceNameList()

    def getFragmentShaderNameList(self):
        return self.fragmentShaderLoader.getResourceNameList()

    # FUNCTIONS : Material

    def getMaterialNameList(self):
        return self.materialLoader.getResourceNameList()

    def getMaterial(self, name):
        return self.materialLoader.getResource(name)

    # FUNCTIONS : Mesh

    def getMeshNameList(self):
        return self.meshLoader.getResourceNameList()

    def getMesh(self, meshName):
        return self.meshLoader.getResource(meshName)

    # FUNCTIONS : Texture

    def getTextureNameList(self):
        return self.textureLoader.getResourceNameList()

    def getTexture(self, textureName):
        return self.textureLoader.getResource(textureName)

    def getTextureID(self, textureName):
        return self.textureLoader.getTextureID(textureName)
