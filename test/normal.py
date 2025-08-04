"""
Test module for OBJ file normal vector calculation and processing.
This module provides enhanced functions to read OBJ files, calculate vertex normals, 
and generate OBJ files with proper normal vectors for 3D rendering.

Reference: https://github.com/mariliafernandez/generate-obj-normals
"""

import re
import numpy as np
import argparse
from pathlib import Path

def calculate_normals(filepath):
    """
    Main function to calculate and add normal vectors to an OBJ file.
    
    This function reads an existing OBJ file, calculates normal vectors for each face,
    and outputs an enhanced OBJ file with vertex normals for better 3D rendering.
    
    Args:
        filepath (str): Path to the input OBJ file
    
    Returns:
        None: Writes enhanced OBJ file with '_out' suffix
    """
    # Read the OBJ file content
    with open(filepath) as obj:
        r = obj.read()

    # Parse vertex positions and face data
    position_data = read_position(r)
    faces_data = read_faces(r)
    
    # Calculate normal vectors for all faces
    obj_n = obj_normals(position_data, faces_data)
    
    # Get filename without extension for output
    filename = filepath.split('.')[0]

    # Write enhanced OBJ file with normals
    write_obj(filename, position_data, faces_data, obj_n)

def read_position(r):
    """
    Extract vertex positions from OBJ file content.
    
    This function parses the raw OBJ file content and extracts all vertex
    position lines (starting with 'v ') into a structured list.
    
    Args:
        r (str): Raw content of the OBJ file
    
    Returns:
        list: List of vertex positions as [x, y, z] coordinates
    """
    position = list()
    # Regular expression to match vertex position lines
    v_re = re.compile('v .*')
    v_lines = v_re.findall(r)

    # Parse each vertex line
    for line in v_lines:
        elements = line.split()[1:]  # Skip the 'v' prefix
        
        # Convert string coordinates to float values
        x = float(elements[0])
        y = float(elements[1])
        z = float(elements[2])
          
        position.append([x, y, z])

    return position

def read_faces(r):
    """
    Extract and parse face definitions from OBJ file content.
    
    This function parses the OBJ file content and extracts face definitions,
    converting 1-based OBJ indices to 0-based Python indices.
    
    Args:
        r (str): Raw content of the OBJ file
    
    Returns:
        list: List of face definitions with 0-based vertex indices
    """
    faces = list()
    # Regular expression to match face definition lines
    f_re = re.compile('f .*')
    f_lines = f_re.findall(r)

    # Parse each face line
    for line in f_lines:
        elements = line.split()[1:]  # Skip the 'f' prefix
        
        # Convert 1-based OBJ indices to 0-based Python indices
        v1 = int(elements[0]) - 1
        v2 = int(elements[1]) - 1
        v3 = int(elements[2]) - 1
        
        faces.append([v1, v2, v3])
    
    return faces

def obj_normals(position, faces):
    """
    Calculate normal vectors for all faces in the OBJ model.
    
    This function computes normalized normal vectors for each triangular face
    using the cross product of two edge vectors.
    
    Args:
        position (list): List of vertex positions
        faces (list): List of face definitions with vertex indices
    
    Returns:
        list: List of normalized normal vectors for each face
    """
    normals = list()

    # Calculate normal for each face
    for f in faces:
        # Get the three vertices of the face (using 0-based indices)
        p1 = np.asarray(position[f[0]]) 
        p2 = np.asarray(position[f[1]]) 
        p3 = np.asarray(position[f[2]]) 

        # Calculate and add the normalized normal vector
        normals.append(normal(p1, p2, p3))

    return normals  

def normal(p1, p2, p3):
    """
    Calculate normalized normal vector for a triangular face.
    
    This function computes the normal vector of a triangle defined by three points
    using the cross product of two edge vectors, then normalizes the result.
    
    Args:
        p1 (numpy.ndarray): First vertex position
        p2 (numpy.ndarray): Second vertex position  
        p3 (numpy.ndarray): Third vertex position
    
    Returns:
        numpy.ndarray: Normalized normal vector with 4 decimal precision
    """
    # Calculate edge vectors from first vertex
    v1 = p2 - p1
    v2 = p3 - p1

    # Calculate normal using cross product
    n = np.cross(v1, v2)

    # Normalize the normal vector
    n_normalized = n / np.linalg.norm(n)

    # Round to 4 decimal places for precision
    n_normalized = np.around(n_normalized, decimals=4)
    
    return n_normalized

def write_obj(filename, positions, faces, normals):
    """
    Write an enhanced OBJ file with vertex positions, faces, and normals.
    
    This function generates an OBJ file that includes vertex positions, face definitions,
    and vertex normal vectors in the standard OBJ format.
    
    Args:
        filename (str): Base filename for the output file
        positions (list): List of vertex positions
        faces (list): List of face definitions
        normals (list): List of normal vectors
    
    Returns:
        None: Writes the enhanced OBJ file to disk
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
        # Format: f vertex_index//normal_index (convert back to 1-based)
        f_line = f'{f_line}\nf {f[0]+1}//{i} {f[1]+1}//{i} {f[2]+1}//{i}'
    
    # Combine all components into final OBJ content
    out = f'# {filename}_out.obj\n{v_line}\n{vn_line}\n{f_line}'
    
    # Write to file with '_out' suffix
    with open(f'{filename}_out.obj', 'w') as f:
        f.write(out)

if __name__ == '__main__':
    # Test the normal calculation with a sample OBJ file
    path = '..\\building.obj'
    calculate_normals(path)