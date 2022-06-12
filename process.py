import bpy
import sys
import os
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
import CFG
import MeshCreator
import imp
imp.reload(CFG)
imp.reload(MeshCreator)
from CFG import *
from MeshCreator import *
from random import random,randint,seed

def process(self):
    vertex_index = {}
    vertices = []
    faces = []
        
    leaf_color = self.leaf_color or [0/255, 102/255, 0/255, 1] 
    trunk_color = self.trunk_color or [51/255, 26/255, 0/255, 1]
    
    pivot = Vector((0,0,0))
    direction = Vector((0,0,1))
    rotation = Vector((0,0,0))
    
    resolution = 8 if "resolution" not in self.vocabulary["F"].args else self.vocabulary["F"].args["resolution"]
    reduction = 0 if "reduction" not in self.vocabulary["F"].args else self.vocabulary["F"].args["reduction"]
    radius_reduction = 1-reduction
    radius = 0.5 if "radius" not in self.vocabulary["F"].args else self.vocabulary["F"].args["radius"]
    last = None
    base = make_circle(radius=radius, subdivisions=resolution)
    add_circle(base,vertices,vertex_index)
    faces += close_circle(base,vertices,vertex_index)
    
    stack = []
    leaves = []
    
    for node in self._state:
        length = 1 if "length" not in node.args else node.args["length"]
        angle = 25 if "angle" not in node.args else node.args["angle"]
        width = 0.5 if "width" not in node.args else node.args["width"]
        height = 0.5 if "height" not in node.args else node.args["height"]
        variation = 0 if "variation" not in node.args else node.args["variation"]
        var_perc = 0.2 if "var_perc" not in node.args else node.args["var_perc"]
        density = 10 if "density" not in node.args else node.args["density"]
        
        if random() < var_perc:
            ang = randint(-variation,variation)
            rotate([direction],(ang,0,0))
            rotation += Vector((ang,0,0))
            ang = randint(-variation,variation)
            rotate([direction],(0,ang,0))
            rotation += Vector((0,ang,0))
            ang = randint(-variation,variation)
            rotate([direction],(0,0,ang))
            rotation += Vector((0,0,ang))
        
        if node == "F":        
            pivot += direction*length
            last = base
            base = make_circle(radius=radius,subdivisions=resolution)
            rotate(base,rotation)
            translate(base, pivot)
            add_circle(base,vertices,vertex_index)
            faces += connect_circles(last,base,vertex_index)
            
            radius *= radius_reduction
            
        elif node == "+":
                
            last = base
            pivot += direction*length
            rotate([direction],(0,angle,0))
            rotation += Vector((0,angle,0))
            pivot += direction*length
            base = make_circle(radius=radius,subdivisions=resolution)
            rotate(base,rotation)
            translate(base,pivot)
            add_circle(base,vertices,vertex_index)
            faces += connect_circles(last,base, vertex_index)
            
            radius *= radius_reduction
        
        elif node == "-":
                
            last = base
            pivot += direction*length
            rotate([direction],(0,-angle,0))
            rotation += Vector((0,-angle,0))
            pivot += direction*length
            base = make_circle(radius=radius,subdivisions=resolution)
            rotate(base,rotation)
            translate(base,pivot)
            add_circle(base,vertices,vertex_index)
            faces += connect_circles(last,base, vertex_index)
            
            radius *= radius_reduction
        
        elif node == "W":
            
            last = base
            pivot += direction*length
            rotate([direction],(angle,0,0))
            rotation += Vector((angle,0,0))
            pivot += direction*length
            base = make_circle(radius=radius,subdivisions=resolution)
            rotate(base,rotation)
            translate(base,pivot)
            add_circle(base,vertices,vertex_index)
            faces += connect_circles(last,base, vertex_index)
            
            radius *= radius_reduction
        
        elif node == "S":
            
            last = base
            pivot += direction*length
            rotate([direction],(-angle,0,0))
            rotation += Vector((-angle,0,0))
            pivot += direction*length
            base = make_circle(radius=radius,subdivisions=resolution)
            rotate(base,rotation)
            translate(base,pivot)
            add_circle(base,vertices,vertex_index)
            faces += connect_circles(last,base, vertex_index)
            
            radius *= radius_reduction
        
        elif node == "R":
            
            last = base
            pivot += direction*length
            rotate([direction],(0,0, angle))
            rotation += Vector((0,0, angle))
            pivot += direction*length
            base = make_circle(radius=radius,subdivisions=resolution)
            rotate(base,rotation)
            translate(base,pivot)
            add_circle(base,vertices,vertex_index)
            faces += connect_circles(last,base, vertex_index)
            
            radius *= radius_reduction
        
        elif node == "L":
            
            last = base
            pivot += direction*length
            rotate([direction],(0,0,-angle))
            rotation += Vector((0,0,-angle))
            pivot += direction*length
            base = make_circle(radius=radius,subdivisions=resolution)
            rotate(base,rotation)
            translate(base,pivot)
            add_circle(base,vertices,vertex_index)
            faces += connect_circles(last,base, vertex_index)
            
            radius *= radius_reduction
            
        elif node == "[":
            stack.append((pivot.copy(), direction.copy(), rotation.copy(),last,base,radius))
        elif node == "]":
            pivot, direction, rotation, last, base, radius = stack.pop()
                
        else:
            pivot += direction*length
            
            if node == "X" or ("leaf" in node.args and node.args["leaf"]):
                res = 8 if "resolution" not in node.args else node.args["resolution"]
                variation = 90 if "variation" not in node.args else node.args["variation"]
                for _ in range(int(density)):
                    leaf = make_leaf(width,height,res)
                    add_circle(leaf, vertices, vertex_index)
                    leaf_faces = close_circle(leaf, vertices, vertex_index, pivot.copy())
                    leaves += [i for i in range(len(faces), len(faces)+len(leaf_faces))]
                    faces += leaf_faces
                    rotate(leaf,(randint(-variation,variation),0,0))
                    rotate(leaf,(0,0,randint(-variation,variation)))
                    rotate(leaf,(0,randint(-variation,variation),0))
                    rotate(leaf,rotation)
                    translate(leaf,pivot)
            
            faces += close_circle(base,vertices, vertex_index, center=pivot.copy())
            pivot -= direction*length
            
            radius *= radius_reduction
        
    tree = create_mesh(vertices,faces)
    trunk_material = make_material(tree, trunk_color)
    leaf_material = make_material(tree, leaf_color)
    tree.active_material = trunk_material
    mat_idx = {mat.name: i for i, mat in enumerate(tree.data.materials)}
    for leaf in leaves:
        tree.data.polygons[leaf].material_index = mat_idx[leaf_material.name]

def main():
    
    grammar = CFG()
    
    grammar.loadCFG("examples/tree 0")
    
    if grammar.seed:
        seed(grammar.seed)
        
    grammar.advance()
    
    process(grammar)


main()
