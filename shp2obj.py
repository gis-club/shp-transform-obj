"""
Core module for converting Shapefile (.shp) files to 3D OBJ format.
This module handles the main conversion process from geospatial data to 3D models.
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, LinearRing
import aspose.threed as a3d
from createTriangle import  polygon_to_triangle_normal, polygon_to_triangle_hole
from coordinate  import calculate_coordinate
from normal import obj_normals
from save import  write_obj_default, write_obj_normal

def shp2obj(shp_path, obj_path, field=None, building_height=3, is_normal=False):
    """
    Convert Shapefile to OBJ format with 3D building models.
    
    Args:
        shp_path (str): Path to the input Shapefile
        obj_path (str): Path for the output OBJ file
        field (str, optional): Field name containing building height data
        building_height (float): Default building height in meters (default: 3)
        is_normal (bool): Whether to generate normal vectors for enhanced lighting (default: False)
    
    Returns:
        None: Saves OBJ file and generates GLB format for Cesium
    """
    # Read Shapefile using GeoPandas
    gdf = gpd.read_file(shp_path)

    # Calculate the center point of the entire Shapefile for coordinate normalization
    shp_center = np.array([(gdf.total_bounds[0] + gdf.total_bounds[2]) / 2,(gdf.total_bounds[1] + gdf.total_bounds[3])/2])

    # Vertex counter for tracking vertex indices in OBJ format
    vertex_counter = 1

    # Store all vertex positions for the entire model
    positions = []

    # Store all face definitions for the entire model
    faces = []

    # Process each polygon in the Shapefile
    for idx, row in gdf.iterrows():
        geom = row.geometry

        if isinstance(geom, Polygon):
            # Count total interior vertices
            interior_vertices = 0

            # Perform triangulation based on polygon complexity
            triangulation = None
            if len(geom.interiors) > 0:
                # Handle polygons with holes using specialized triangulation
                triangulation = polygon_to_triangle_hole(geom, geom.interiors)
                for interior in geom.interiors:
                    if isinstance(interior, LinearRing):
                        interior_vertices += len(interior.coords[:-1])
            else:
                # Handle simple polygons without holes
                triangulation = polygon_to_triangle_normal(geom)

            # Get exterior coordinates of the polygon
            coord_list = np.array(geom.exterior.coords[:-1])

            # Get building height from field or use default
            height = row[field] if field else 0

            # Calculate the centroid of the current polygon
            geo_center = np.array(geom.centroid.coords[0])

            # Store processed points
            points = []

            # Calculate coordinate offset relative to Shapefile center
            center = calculate_coordinate(geo_center, shp_center)

            # Add bottom face vertices
            for coord in triangulation['vertices']:
                point = calculate_coordinate(coord, geo_center)
                points.append(point)
                # Store vertex position in global positions list
                positions.append([point[0] + center[0], height, point[1] + center[1]])

            # Add top face vertices
            for point in points:
                # Store top vertex position with building height offset
                positions.append([point[0] + center[0], height + building_height, point[1] + center[1]])

            # Calculate vertex count and offset for indexing
            num_vertices = len(coord_list) + interior_vertices
            offset = num_vertices

            # Add bottom face triangles
            for triangle_indices in triangulation['triangles']:
                # Store bottom face triangle with adjusted vertex indices
                faces.append([i + vertex_counter for i in triangle_indices])

            # Add top face triangles
            for triangle_indices in triangulation['triangles']:
                # Store top face triangle with offset vertex indices
                faces.append([i + vertex_counter + offset for i in triangle_indices])

            # Add side face triangles to create 3D building walls
            for triangle_indices in triangulation['triangles']:
                base_triangle = [vertex_counter + i for i in triangle_indices]
                top_triangle = [vertex_counter + i + offset for i in triangle_indices]
                
                # Create side faces by connecting bottom and top vertices
                # Each edge of the triangle creates two triangular side faces
                faces.append([base_triangle[0], base_triangle[1], top_triangle[1]])
                faces.append([base_triangle[0], top_triangle[1], top_triangle[0]])
                faces.append([base_triangle[1], base_triangle[2], top_triangle[2]])
                faces.append([base_triangle[1], top_triangle[2], top_triangle[1]])
                faces.append([base_triangle[2], base_triangle[0], top_triangle[0]])
                faces.append([base_triangle[2], top_triangle[0], top_triangle[2]])

            # Update vertex counter for next polygon
            vertex_counter += num_vertices * 2

    # Choose output format based on normal vector requirement
    if bool(is_normal):
        # Calculate normal vectors for enhanced lighting and shading
        normal = obj_normals(positions, faces)

        # Save the generated OBJ file with normal vectors
        write_obj_normal(obj_path, positions, faces, normal)
    else:
        # Save the basic OBJ file without normal vectors
        write_obj_default(obj_path, positions, faces)

    # Save center coordinates to a text file for reference
    with open(obj_path.replace('.obj', '.txt'), 'w') as f:
        f.writelines(str(shp_center))

    # Convert OBJ to GLB format for Cesium compatibility
    glb_path = obj_path.replace('.obj', '.glb')
    scene = a3d.Scene.from_file(obj_path)
    scene.save(glb_path)