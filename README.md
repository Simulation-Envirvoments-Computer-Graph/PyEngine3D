### What is GuineaPig
* Opensource Opengl 3D engine was written in python.
* Wiki : https://github.com/ubuntunux/GuineaPig/wiki/main
* Reference
    - http://learnopengl.com/
    - http://www.opengl-tutorial.org/
    - https://github.com/neutralord/pyopengl-experiments
    - https://github.com/asylum2010/Asylum_Tutorials
* Check similar project
    - http://glumpy.github.io/
    - https://github.com/JoshuaSenouf/GLEngine
    - https://github.com/bartwronski/CSharpRenderer

## Dependency modules
 - python 3.5.1
 - Anaconda3-2.4.1 ( https://www.continuum.io/downloads )
 - accelerate 2.0 ( anaconda accelerate library )
 - numpy 1.10.4
 - numba 0.23.1
 - pillow 3.1.1
 - pyqt4
 - kivy 1.9.1
 - pyopengl 3.1
 - pyopengl_accelerate 3.1
 - libpng 1.6.17
 - pygame 1.9.2

## Features
* Project System
    - Load/Save project
    - Resource tree
* Shader
    - Material Template
    - Material Instance
    - Shader Parser
        - #include
        - insert macro
    - TODO : Precompiled shader load / save
* Actor System
    - StaticMesh
    - TODO : SkeletalMesh
    - TODO : Tree, Foliage
    - TODO : Landscape
    - Camera
    - Light
    - TODO : SkyBox
    - TODO : Wind
* Object
    - TODO : Multiple Geometry Mesh
    - TODO : instancing
    - TODO : skinning
* Texture Object
    - TODO : MipMap Filter
    - TODO : Multisample texture - glTexImage2DMultisample
        - sampler2D/texture by sampler2DMS/texelFetch in the fragment shader
    - TODO : Wrap, Mirror, Clamp mode
    - TODO : sRGB, NormalMap, Linear Color type
    - TODO : source file path and data
* Render Target Manager
    - 2D
    - TODO : 3D, Cube, Array
* Rendering
    - TODO : OpenGL Context
    - View Mode
        - Wire, Solid, Lighting, Color
    - TODO : Culling
        - view frustum culling 
        - occlusion culling
        - distance culling
    - RenderBuffer object
    - Texture2D attach to framebuffer    
    - TODO : Multi render target
    - TODO : Copy Texture Interface
    - TODO : RenderTargets Resize when change resolution
    - Forward Renderer
    - TODO : Deferred Renderer
    - TODO : LightPrepass Renderer
    - TODO : PBR
    - TODO : Shadow
    - TODO : Fog
    - TODO : Volumtric Scattering
    - TODO : Atmospheric Scattering
* Transparent Rendering
    - TODO : blend mode
        - Additive, Multiply, Blending
* Particle System
    - TODO
* PostProcess
    - TODO : PostProcess Chain
    - TODO : SSAA, TAA, MSAA, SMAA
    - TODO : Motion Blur
    - TODO : HDR Tonemapping
    - TODO : SSAO, Temporal SSAO
    - TODO : Screen Space Reflection
    - TODO : Screen Space SSS
    - TODO : God Ray
    - TODO : Glare
    - TODO : Depth Of Field
    - TODO : Film Grain
    - TODO : Color Correction
    - TODO : Color Grading
    - TODO : Vignetting
* Font
    - TODO : Console input/output
    - TODO : Shader based rendering
* InGame GUI
    - TODO : input / output
    - TODO : progress bar
    - TODO : button
* Scene Manager
    - Object managing
    - Scene Save/Load
* Resource Manager
    - Create/Remove/Regist/Release resources
    - TODO : resource reload system
* Import/Export
    - OBJ
    - TODO : FBX
    - TODO : Blender
    - TODO : Collada
    - Textures
* GUI Edit Tool
    - QT backend
    - Kivy backend
* Debug
    - performance profiler
    - debug info print
    - TODO : render target viewer
