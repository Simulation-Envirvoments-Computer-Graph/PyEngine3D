![PyEngine3D](https://github.com/ubuntunux/PyEngine3D/blob/master/PyEngine3D.png)

### What is PyEngine3D
* An open source OpenGL 3D engine written in Python.
* Reference
    - http://learnopengl.com/
    - http://www.opengl-tutorial.org/
    - https://github.com/neutralord/pyopengl-experiments
    - https://github.com/asylum2010/Asylum_Tutorials
* Similar projects
    - http://glumpy.github.io/
    - https://github.com/JoshuaSenouf/GLEngine
    - https://github.com/bartwronski/CSharpRenderer

## Dependency modules
 - python 3
 - numpy 1.11
 - numba 0.35
 - pillow
 - pyqt4
 - pybullet
 - pyopengl
 - pyopengl_accelerate
 - pygame

## TODO
* Job
    - wrong tangent_to_world matrix bug
    - view frustum culling
    - point light culling
* Optimize
    - Only dynamic shadows are updated on every frame, and static shadows are not updated every time.
    - SSR optimize, hierachical z ray marching
* Actors
    - Tree, Foliage actor
    - Landscape
    - Wind
    - River
    - Probe
    - Particles
* Blender3D plugin
    - transfer geometry, animation, scene datas
    - edit animation, scene, sequence, particles in blender
* Debug
    - performance profiler
    - debug info print
    - render target viewer
* Editor
    - Tab based panel
    - Snap to window rect
* Import
    - FBX
    - Blender
    - Compressed Texture (ETC, DDS)
* InGame GUI
    - input / output
    - progress bar
    - button
* Light
    - Dominant Directional Light, Spot, point, area light
    - SkyLight, AmbientLight, Spherical Harmonic Light
* Object
    - Select, Move, Modify
    - Gizmo
    - View Frustum Culling
    - VTF Skinning
* Particle System
    - runtime particles
    - GPU particle
* PostProcess
    - FXAA
    - Screen Space SSS
    - God Ray
    - Glare
    - Depth Of Field
    - Film Grain
    - Color Correction
    - Color Grading
* Rendering
    - Light Probe lod convolution
    - Hierachical-Z depth
    - Animation calculation in gpu
    - Multisample texture - glTexImage2DMultisample
        - sampler2D/texture by sampler2DMS/texelFetch in the fragment shader
    - View Mode
        - Wire, Solid, Lighting, Color
    - Culling
        - view frustum culling
        - occlusion culling
        - distance culling
    - Coarse Shading, Checkboard rendering
    - Paraboloid environment map    
    - Volumtric Fog
    - Fur Rendering
    - Procedural Terrain
* Resource Manager
    - Load / Unload / Reload system
    - Duplicate resource
* Sound
    - Loader
    - Player
