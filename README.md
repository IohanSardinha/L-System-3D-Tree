# L-System 3D trees
## Lab5 - A3MD @ UPC
## By: Iohan Sardinha
![examples/examples.png](examples/examples.png)

## How to run:
Open blender in the same folder as the scripts
**It's very important that it's opened in the same folder in order for the CFG and MeshCreator scripts to be imported properly!**
```bash 
$ cd location/of/scripts
$ blender
```

Open [process.py](process.py) in blender
![instructions1](examples/instructions1.png)
Change the name of the tree file in the main function to a text file with the Tree CFG format that is described bellow
```python
build_tree(your_file_path)
```

### Tree CFG format:

### Building a grammar directly

### Notes on how it works
The scripts are divided into two APIs
#### CFG
Has all the classes and methods to create and process CFGs
##### Node class
Tokens in the vocabulary of the grammar
```python
F = Node("F",{length:2})
```

##### Rule class
Rules for words
```python
#F 0.6 -> FF
#F 0.4 -> F
r1 = Rule(F,[FF],[F],0.6)
```
**Methods**
- **next()**: computes the token after a processing step, depending on the probability

##### CFG class

**Methods**
The main grammar class, that stores the rules and process the tokens
```python
grammar = CFG(start=[X], vocabulary=[X,F,LB,RB,P,M])
grammar.addRule(grammar.readRule("F:=FF"))
grammar.addRule(grammar.readRule("X:=[+X]-X"))
grammar.advance(5)
print(grammar.state())
```
- **addRule(rule)**:
- **translate(word)**:
- **advance(n=None)**:
- **state()**:
- **readRule(line)**:
- **loadRules(fileName)**:
- **loadCFG(fileName)**:

#### MeshCreator
Has the functions to create the tree mesh and object
- **make_circle(radius=1, center=Vector((0,0,0)), subdivisions=30)**: Returns the vertices of a circle in projected in XY, with given radius and "subdivision" faces
- **make_leaf(dx=1,dy=1, subdivisions=10)**: Returns the vertices of a leaf with "dx" width, "dy" height and "subdivisions" faces
- **add_circle(c,v,vi)**: Adds the `c` list of local vertices to the `v` list of global vertices of a mesh and the `vi` dict with the vertex id to index relation
- **connect_circles(c1,c2,vi)**: Returns the faces that connect the circles `c1` and `c2` creating a cylinder. Needs `vi` the dict with the vertex id to index relation
- **close_circle(c, v, vi, center=None, offset=Vector((0,0,0)))**: Returns the faces that close the circle `c` with in the center. `Offset` is the offset from the `center` of the circle where the central vertex will be. Needs `v` the global vertices list of the mesh and `vi` the dict with the vertex id to index relation
- **rotate(p, r)**: Rotates the the `p` vertices `r` degrees, where r is a touple of X,Y,Z angles in this order 
- **translate(p, t)**: Translates the `p` vertices in `t` where `t`= (X,Y,Z)
- **make_material(mesh, color)**: Creates and adds to `mesh` a material with `color` color
- **create_mesh(vertices,faces)**: Creates a mesh given it's vertices and faces