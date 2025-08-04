"""
OBJ file normal vector calculation and processing utilities.
This module provides functions to read OBJ files, calculate vertex normals, and generate enhanced OBJ files with normal vectors.
"""

import re
import numpy as np
import argparse
from pathlib import Path
from save import write_obj_normal

def operate_obj(filepath=None):
    """
    Main function to process an OBJ file and generate normals.
    
    This function reads an OBJ file, extracts vertex positions and faces,
    calculates normal vectors for each face, and writes an enhanced OBJ file.
    
    Args:
        filepath (str): Path to the input OBJ file
    
    Returns:
        None: Writes enhanced OBJ file to disk
    """
    # Read the OBJ file content
    with open(filepath) as obj:
        r = obj.read()

    # Extract vertex positions and face data
    position_data = get_position(r)
    faces_data = get_faces(r)
    
    # Calculate normal vectors for all faces
    obj_n = obj_normals(position_data, faces_data)
    
    # Get filename without extension for output
    filename = filepath.split('.')[0]

    # Write enhanced OBJ file with normals
    write_obj_normal(filename, position_data, faces_data, obj_n)

def get_position(obj):
    """
    Extract vertex positions from OBJ file content.
    
    This function parses the OBJ file content and extracts all vertex
    position lines (starting with 'v ') into a list of coordinates.
    
    Args:
        obj (str): Raw content of the OBJ file
    
    Returns:
        list: List of vertex positions as [x, y, z] coordinates
    """
    position = list()
    # Regular expression to match vertex lines
    v_re = re.compile('v .*')
    v_lines = v_re.findall(obj)

    # Parse each vertex line
    for line in v_lines:
        elements = line.split()[1:]  # Skip the 'v' prefix
        
        # Convert string coordinates to float
        x = float(elements[0])
        y = float(elements[1])
        z = float(elements[2])
          
        position.append([x, y, z])

    return position

def get_faces(obj):
    """
    Extract face definitions from OBJ file content.
    
    This function parses the OBJ file content and extracts all face
    definition lines (starting with 'f ') into a list.
    
    Args:
        obj (str): Raw content of the OBJ file
    
    Returns:
        list: List of face definition strings
    """
    # Regular expression to match face lines
    f_re = re.compile('f .*')
    f_lines = f_re.findall(obj)

    return f_lines

def obj_normals(position, faces):
    """
    Calculate normal vectors for all faces in the OBJ model.
    
    This function computes normalized normal vectors for each face
    using the cross product of two edge vectors.
    
    Args:
        position (list): List of vertex positions
        faces (list): List of face definitions
    
    Returns:
        list: List of normalized normal vectors for each face
    """
    normals = list()

    # Calculate normal for each face
    for f in faces:
        # Get the three vertices of the face (OBJ indices are 1-based)
        p1 = np.asarray(position[f[0] - 1])
        p2 = np.asarray(position[f[1] - 1])
        p3 = np.asarray(position[f[2] - 1])

        # Calculate and add the normalized normal vector
        normals.append(normalized(p1, p2, p3))

    return normals  

def normalized(p1, p2, p3):
    """
    Calculate normalized normal vector for a triangle face.
    
    This function computes the normal vector of a triangle defined by three points
    using the cross product of two edge vectors, then normalizes the result.
    
    Args:
        p1 (numpy.ndarray): First vertex position
        p2 (numpy.ndarray): Second vertex position
        p3 (numpy.ndarray): Third vertex position
    
    Returns:
        numpy.ndarray: Normalized normal vector with 4 decimal precision
    """
    # Calculate edge vectors
    v1 = p2 - p1
    v2 = p3 - p1
    
    # Calculate normal using cross product
    n = np.cross(v1, v2)

    # Normalize the normal vector
    n_normalized = n / np.linalg.norm(n)
    
    # Round to 4 decimal places for precision
    n_normalized = np.around(n_normalized, decimals=4)

    return n_normalized
