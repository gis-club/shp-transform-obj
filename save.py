"""
OBJ file writing utilities for 3D model export.
This module provides functions to write 3D model data to OBJ format files.
"""

def write_obj_normal(filepath, positions, faces, normals):
    """
    Write OBJ file with vertex positions, faces, and vertex normals.
    
    This function generates an OBJ file that includes vertex positions, face definitions,
    and vertex normal vectors for proper lighting and shading.
    
    Args:
        filepath (str): Output file path for the OBJ file
        positions (list): List of vertex positions as [x, y, z] coordinates
        faces (list): List of face definitions with vertex indices
        normals (list): List of vertex normal vectors as [nx, ny, nz]
    
    Returns:
        None: Writes the OBJ file to disk
    """
    # Initialize strings for different OBJ components
    v_line = ''    # Vertex positions
    vn_line = ''   # Vertex normals
    f_line = ''    # Face definitions

    # Write vertex positions
    for p in positions:
        v_line = f'{v_line}\nv {p[0]} {p[1]} {p[2]}'

    # Write vertex normals
    for n in normals:
        vn_line = f'{vn_line}\nvn {n[0]} {n[1]} {n[2]}'

    # Write faces with normal indices
    i = 0
    for f in faces:
        i += 1
        # Format: f vertex_index//normal_index for each vertex
        f_line = f'{f_line}\nf {f[0]}//{i} {f[1]}//{i} {f[2]}//{i}'

    # Combine all components into final OBJ content
    out = f'# Generated OBJ file\n{v_line}\n{vn_line}\n{f_line}'

    # Write to file
    with open(filepath, 'w') as f:
        f.write(out)

def write_obj_default(filepath, positions, faces):
    """
    Write basic OBJ file with vertex positions and faces only.
    
    This function generates a simple OBJ file without normal vectors,
    suitable for basic 3D model representation.
    
    Args:
        filepath (str): Output file path for the OBJ file
        positions (list): List of vertex positions as [x, y, z] coordinates
        faces (list): List of face definitions with vertex indices
    
    Returns:
        None: Writes the OBJ file to disk
    """
    # Initialize OBJ content with header
    obj_content = ["# Generated OBJ file\n"]

    # Add vertex positions
    for point in positions:
        obj_content.append(f"v {point[0]} {point[1]} {point[2]}\n")

    # Add face definitions
    for face in faces:
        obj_content.append(f"f {face[0]} {face[1]} {face[2]}\n")

    # Save the generated OBJ file
    with open(filepath, 'w') as f:
        f.writelines(obj_content)