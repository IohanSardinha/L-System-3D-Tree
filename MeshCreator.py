import bpy
from mathutils import Vector, Euler
from math import sin, cos,radians

def add_circle(c,v,vi):
    i = len(v)
    for j,ci in enumerate(c):
        vi[ci[:]] = j+i
    v += c
    
def connect_circles(c1,c2,vi):
    faces = []
    for i in range(len(c1)):
        faces.append([
                    vi[c1[i][:]],
                    vi[c1[(i+1)%len(c1)][:]],
                    vi[c2[i][:]]
                    ])
        faces.append([
                    vi[c1[(i+1)%len(c1)][:]],
                    vi[c2[(i+1)%len(c1)][:]],
                    vi[c2[i][:]]
                    ])
    return faces
    
def close_circle(c, v, vi, center=None, offset=Vector((0,0,0))):
    if center == None:
        center = Vector((0,0,0))
        for ci in c:
            center += ci
        center /= len(c)
        center += offset

    if not center[:] in vi:
        vi[center[:]] = len(v)
        v.append(center)
        
    faces = []
    for i in range(len(c)):
        faces.append([
            vi[c[(i+1)%len(c)][:]],
            vi[center[:]],
            vi[c[i][:]]
        ])
    return faces

def make_circle(radius=1, center=Vector((0,0,0)), subdivisions=30):
    vertices = []
    
    for angle in range(0,360,int(360/subdivisions)):
        v = center+Vector((radius*sin(radians(angle)),radius*cos(radians(angle)),0))
        vertices.append(v)
        
    return vertices

def rotate(p, r):
    for pi in p:
        pi.rotate(Euler((radians(r[0]),0,0),'XYZ'))
        pi.rotate(Euler((0,radians(r[1]),0),'XYZ'))
        pi.rotate(Euler((0,0,radians(r[2])),'XYZ'))
    
def translate(p, t):
    for pi in p:
        pi += Vector(t)

def create_mesh(vertices,faces):
    name="Tree"
    me = bpy.data.meshes.new(name+"Mesh")
    ob = bpy.data.objects.new(name, me)
    ob.location = bpy.context.scene.cursor.location
    bpy.context.scene.collection.objects.link(ob)
    me.from_pydata(vertices, [], faces)
    me.update()
    return ob

def make_leaf(dx=1,dy=1, subdivisions=10):
    vertices = []

    a = dx*1
    b = dy*5/2
    for w in range(0,360,int(360/subdivisions)):
        z = radians(w)
        x=a*(1-sin(z))*cos(z)
        y=(b*(sin(z)-1))+b*2
        z=sin(x/3)+0.03*y**2-0.6*y
        vertices.append(Vector((z,x,y)))
    
    return vertices

def make_material(mesh, color):
    mat = bpy.data.materials.new(name=str(color))
    mesh.data.materials.append(mat)
    mat.diffuse_color = color
    return mat
