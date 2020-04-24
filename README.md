# Introduction

This is the v.1 release of the "onelab" python package. It is a proof on concept package for easily interfacing with the [gmsh](http://gmsh.info/) and [onelab](http://onelab.info/) clients using python. 

A more detailed version of the documentation will follow, along with examples of how the api can be used and a set of useful functions to make it easier to manipulate mesh data in Python.

Currently the package contains the APIs as distributed [HERE](https://gitlab.onelab.info/gmsh/gmsh).

# Features 

- Create geometries with Python. 
- Generate meshes with Python.
- Control Gmsh and Onelab with Python.
- Quickly link solvers written in your proramming language of choice.
- Contol files from the Onelab GUI or the command line.

# Getting started with Onelab & Python

If you are not familiar with Onelab or Gmsh, I highly recommend that you familiarise yourself with these software packages before reading on. 

According to the Onelab website - "Onelab is an open-source, lightweight interface to finite element software. It is completely free: the default ONELAB software bundle contains the mesh generator Gmsh, the finite element solver GetDP and the optimization library conveks."

Onelab and Gmsh both support Python, Julia and C++ application programming interfaces. The purpose of this project is to package the respective Python APIs aong with a set of useful fucntions and classes that will make interacting with the software a lot easier. 

Onelab and Gmsh are powerful open source engineering design tools. However, they have a steep learning curve on account of the fact that geometries, solvers and optimisation libraries all require different programming / scripting languages and data formats. 

With this package, users can define their geometry, mesh, solver, post processing view and optimisation functions in Python. They are have the capability to easily hook into solvers created in ther languages such as C, Fortran or Matlab. 

# Examples

### Import packages

    from onelab import gmsh # Import Onelab API
    import meshio # Import mesh conversion library
    import numpy as np # Import Numpy for numerical processing
    from solidspy import solids_GUI # Import solverenter code here

  ### Define Geometry 

    # Initialise geometry call
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.model.add("disc")
    lc = 0.1
    
    # Define points
    gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
    gmsh.model.geo.addPoint(1, 0,  0, lc, 2)
    gmsh.model.geo.addPoint(0, 1, 0, lc, 3)
    
    # Define lines
    gmsh.model.geo.addLine(3, 1, 1)
    gmsh.model.geo.addLine(1, 2, 2)
    gmsh.model.geo.addCircleArc(2, 1, 3)
    
    # Define physical surfaces and groups
    gmsh.model.geo.addCurveLoop([2, 3, 1], 1)
    gmsh.model.geo.addPlaneSurface([1], 1)
    
    gmsh.model.addPhysicalGroup(1, [1], 1)
    gmsh.model.addPhysicalGroup(1, [2], 2)
    gmsh.model.addPhysicalGroup(1, [3], 3)
    gmsh.model.addPhysicalGroup(2, [1], 4)]
    
    # Output .msh file
    gmsh.option.setNumber("Mesh.MshFileVersion", 2)
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)
    gmsh.write("disc.msh")
    gmsh.finalize()
    
    
   ### Convert mesh formats and define solver conditions

    mesh = meshio.read("disc.msh")
    points = mesh.points
    cells = mesh.cells
    point_data = mesh.point_data
    cell_data = mesh.cell_data
    
    # Element data
    eles = cells[1][1]
    els_array = np.zeros([eles.shape[0], 6], dtype=int)
    els_array[:, 0] = range(eles.shape[0])
    els_array[:, 1] = 3
    els_array[:, 3::] = eles
    
    # Nodes
    nodes_array = np.zeros([points.shape[0], 5])
    nodes_array[:, 0] = range(points.shape[0])
    nodes_array[:, 1:3] = points[:, :2]
    
    # Boundaries
    lines = cells[0]
    bounds = cell_data["gmsh:physical"][1]
    nbounds = len(bounds)
    
    # Loads
    id_cargas = [4]
    nloads = len(id_cargas)
    load = -10e8 # N/m
    loads_array = np.zeros((nloads, 3))
    loads_array[:, 0] = id_cargas
    loads_array[:, 1] = 0
    loads_array[:, 2] = load
    
    # Boundary conditions
    d_izq = [cont for cont in range(nbounds) if
    bounds[cont] == 1]
    id_inf = [cont for cont in range(nbounds) if
    bounds[cont] == 2]
    nodes_izq = lines[1][0:9]
    nodes_izq = nodes_izq.flatten()
    nodes_inf = lines[1][10:19]
    nodes_inf = nodes_inf.flatten()
    nodes_array[nodes_izq, 3] = -1
    nodes_array[nodes_inf, 4] = -1
    
    #  Materials
    mater_array = np.array([[70e9, 0.35],
                        [70e9, 0.35]])
    maters = cell_data["gmsh:physical"][1]
    els_array[:, 2]  = [1 for mater in maters if mater == 4]
    
    # Create files
    np.savetxt("eles.txt", els_array, fmt="%d")
    np.savetxt("nodes.txt", nodes_array, fmt=("%d", "%.4f", "%.4f", "%d", "%d"))
    np.savetxt("loads.txt", loads_array, fmt=("%d", "%.6f", "%.6f"))
    np.savetxt("mater.txt", mater_array, fmt="%.6f")

### Call SolidsPy Solver

    """
    Make call to SolidsPy solver library
    Import SolidsPy formtted .txt files generated above
    """
    # Call to solver
    UC = solids_GUI()
    
    node_index = np.arange(0, len(UC), 1).tolist()
    num_nodes = len(UC)

### Convert solution data to .pos data format (Optional)

    # Output .pos files for Onelab
    with open('disc.pos', 'w') as f:
    f.write('$MeshFormat\n')
    f.write('2.2 0 8\n')
    f.write('$EndMeshFormat\n')
    f.write('$NodeData\n')
    f.write('1\n')
    f.write('"Magnitude"\n')
    f.write('1\n')
    f.write('0\n')
    f.write('3\n')
    f.write('0\n')
    f.write('1\n')
    f.write('%f\n' % (int(num_nodes)))
    for x in node_index:
        index = x+1
        # x_value = UC[x][0]
        y_value = UC[x][1]
        # z_value = 0
        f.write("%d %.6f\n" % (index, y_value))
    f.write('$EndNodeData')


