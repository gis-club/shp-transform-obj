"""
Core module for converting Shapefile (.shp) files to 3D OBJ format.
This module handles the main conversion process from geospatial data to 3D models.
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, LinearRing
import aspose.threed as a3d
from createTriangle import  polygonToTriangleNormal, polygonToTriangleHole
from coordinate  import calculateCoordinate

def shp2obj(shp_path, obj_path, field=None, buildingHeight=3):
    """
    Convert Shapefile to OBJ format with 3D building models.
    
    Args:
        shp_path (str): Path to the input Shapefile
        obj_path (str): Path for the output OBJ file
        field (str, optional): Field name containing building height data
        buildingHeight (float): Default building height in meters (default: 3)
    
    Returns:
        None: Saves OBJ file and generates GLB format for Cesium
    """
    # Read Shapefile using GeoPandas
    gdf = gpd.read_file(shp_path)

    # Calculate the center point of the entire Shapefile for coordinate normalization
    shpCenter = np.array([(gdf.total_bounds[0] + gdf.total_bounds[2]) / 2,(gdf.total_bounds[1] + gdf.total_bounds[3])/2])

    # Store OBJ file content as a list of strings
    obj_content = []

    # Add OBJ file header comment
    obj_content.append("# Generated OBJ file\n")

    # Vertex counter for tracking vertex indices in OBJ format
    vertex_counter = 1

    # Process each polygon in the Shapefile
    for idx, row in gdf.iterrows():
        geom = row.geometry

        if isinstance(geom, Polygon):
            # Count the number of holes (interiors) in the polygon
            interiorLength = len(geom.interiors)

            # Count total interior vertices
            interiorCount = 0

            # Perform triangulation based on polygon complexity
            triangulation = None
            if interiorLength > 0:
                # Handle polygons with holes using specialized triangulation
                triangulation = polygonToTriangleHole(geom, geom.interiors)
                for interior in geom.interiors:
                    if isinstance(interior, LinearRing):
                        interiorCoords = interior.coords[:-1]
                        interiorCount += len(interiorCoords)
            else:
                # Handle simple polygons without holes
                triangulation = polygonToTriangleNormal(geom)

            # Get exterior coordinates of the polygon
            coords = np.array(geom.exterior.coords[:-1])

            # Get building height from field or use default
            height = row[field] if field else buildingHeight

            # Calculate the centroid of the current polygon
            geoCenter = np.array(geom.centroid.coords[0])

            # Store processed points
            points = []

            # Calculate coordinate offset relative to Shapefile center
            center = calculateCoordinate(geoCenter, shpCenter)

            # Add bottom face vertices
            for coord in triangulation['vertices']:
                point = calculateCoordinate(coord, geoCenter)
                points.append(point)
                obj_content.append(f"v {point[0] + center[0]} {height} {point[1] + center[1]}\n")

            # Add top face vertices
            for point in points:
                obj_content.append(f"v {point[0] + center[0]} {height + buildingHeight} {point[1] + center[1]}\n")

            # Calculate vertex count and offset for indexing
            num_vertices = len(coords) + interiorCount
            offset = num_vertices

            # Add bottom face triangles
            for triangle_indices in triangulation['triangles']:
                obj_content.append("f " + " ".join([str(i + vertex_counter) for i in triangle_indices]) + "\n")

            # Add top face triangles
            for triangle_indices in triangulation['triangles']:
                obj_content.append("f " + " ".join([str(i + vertex_counter + offset) for i in triangle_indices]) + "\n")

            # Add side face triangles to create 3D building walls
            for triangle_indices in triangulation['triangles']:
                base_triangle = [vertex_counter + i for i in triangle_indices]
                top_triangle = [vertex_counter + i + offset for i in triangle_indices]
                # Create side faces by connecting bottom and top vertices
                obj_content.append(f"f {base_triangle[0]} {base_triangle[1]} {top_triangle[1]}\n")
                obj_content.append(f"f {base_triangle[0]} {top_triangle[1]} {top_triangle[0]}\n")
                obj_content.append(f"f {base_triangle[1]} {base_triangle[2]} {top_triangle[2]}\n")
                obj_content.append(f"f {base_triangle[1]} {top_triangle[2]} {top_triangle[1]}\n")
                obj_content.append(f"f {base_triangle[2]} {base_triangle[0]} {top_triangle[0]}\n")
                obj_content.append(f"f {base_triangle[2]} {top_triangle[0]} {top_triangle[2]}\n")

            # Update vertex counter for next polygon
            vertex_counter += num_vertices * 2

    # Save the generated OBJ file
    with open(obj_path, 'w') as f:
        f.writelines(obj_content)

    # Save center coordinates to a text file for reference
    with open(obj_path.replace('.obj', '.txt'), 'w') as f:
        f.writelines(str(shpCenter))

    # Convert OBJ to GLB format for Cesium compatibility
    glb_path = obj_path.replace('.obj', '.glb')
    scene = a3d.Scene.from_file(obj_path)
    scene.save(glb_path)