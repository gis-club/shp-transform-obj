"""
Test script for polygon with holes triangulation and 3D model generation.
This script demonstrates the complete workflow from Shapefile to 3D OBJ/GLB model for complex polygons with interior holes.
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, LinearRing
import triangle  # For triangulation
import geopy.distance as geoDistance
import trimesh
import aspose.threed as a3d
import matplotlib.pyplot as plt
from createTriangle import  drawDelaunayFromTriangle
from rotation import rotate_2d

# Read Shapefile data
shapefile_path = r'../data/building.shp'
gdf = gpd.read_file(shapefile_path)

# Calculate the center point of the entire Shapefile for coordinate normalization
shpCenter = np.array([(gdf.total_bounds[0] + gdf.total_bounds[2]) / 2,(gdf.total_bounds[1] + gdf.total_bounds[3])/2])

# Set building height for 3D model generation
buildingHeight = 30

# Store OBJ file content as a list of strings
obj_content = []

# Add OBJ file header comment
obj_content.append("# Generated OBJ file\n")

# Vertex counter for tracking vertex indices in OBJ format
vertex_counter = 1

def polygon_to_triangles(polygon, interior):
    """
    Convert a Shapely polygon with holes to triangular mesh using triangle library.
    
    This function performs constrained triangulation for complex polygons with interior holes,
    ensuring the resulting triangles respect both exterior and interior boundaries.
    
    Args:
        polygon (shapely.geometry.Polygon): Input polygon geometry
        interior (list): List of interior LinearRing objects representing holes
    
    Returns:
        dict: Triangulation result containing vertices, triangles, and edges
    """
    # Convert Shapely polygon to triangle library format
    coords = np.array(polygon.exterior.coords[:-1])

    # Define exterior boundary constraints
    edges = []
    index = 0
    for i in range(len(coords) - 1):
        edges.append([i, i + 1])
        index = i + 1
    # Close the exterior boundary
    edges.append([len(coords) - 1, 0])

    # Process interior holes
    interiosEdges = []
    interiorCoords = None
    center = 0

    if isinstance(interior[0], LinearRing):
        # Calculate hole center for triangle library
        center = interior[0].centroid.coords[0]
        interiorCoords = interior[0].coords[:-1]

    index = index + 1
    # Define interior boundary constraints
    for i in range(len(interiorCoords) - 1):
        interiosEdges.append([i + index, i + index + 1])

    # Close the interior boundary
    interiosEdges.append([len(interiorCoords) - 1 + index, index])
    # interiosEdges = np.array(interiosEdges)

    # Convert boundary constraints to numpy array
    # edges = np.array(edges)

    # Define triangulation constraints including both exterior and interior edges
    constraints = {'segments': edges + interiosEdges}
    coords = coords.tolist()
    coords = coords + interiorCoords

    # Perform constrained triangulation with hole specification
    triangulation = triangle.triangulate({'vertices': coords, 'segments': constraints['segments'], 'holes': [center] }, '-pe')
    
    # Extract triangulation results
    triangles = triangulation['triangles']
    vertices = triangulation['vertices']
    edges = triangulation['edges']
    
    # Visualize the triangulation result
    plt.figure(num='triangle库效果')
    drawDelaunayFromTriangle(edges, vertices)
    plt.show()
    
    return triangulation

def calculateCoordinate(targeCoordinate, centerCoordinate):
    """
    Convert geographic coordinates to local 3D coordinates relative to a center point.
    
    This function performs coordinate transformation from geographic (lat/lon) to local coordinates
    suitable for 3D modeling, including quadrant determination and geodesic distance calculations.
    
    Args:
        targeCoordinate (tuple): Target geographic coordinates (longitude, latitude)
        centerCoordinate (tuple): Center reference coordinates (longitude, latitude)
    
    Returns:
        numpy.ndarray: Local 3D coordinates [x, y] in meters
    """
    # Calculate relative position from center point (origin-based coordinate system)
    lon = targeCoordinate[0] - centerCoordinate[0]
    lat = targeCoordinate[1] - centerCoordinate[1]

    # Determine quadrant for proper sign assignment in coordinate system
    quadrantX = True
    quadrantY = True
    if lon < 0 and lat < 0:
        # Southwest quadrant
        quadrantX = False
        quadrantY = False
    elif lon < 0 and lat > 0:
        # Northwest quadrant
        quadrantX = False
    elif lon > 0 and lat < 0:
        # Southeast quadrant
        quadrantY = False

    # Calculate geodesic distances in meters using WGS-84 ellipsoid
    # X distance: latitude difference at center longitude
    distX = geoDistance.geodesic((targeCoordinate[1], centerCoordinate[0]), (centerCoordinate[1], centerCoordinate[0]), ellipsoid='WGS-84').meters
    # Y distance: longitude difference at center latitude
    distY = geoDistance.geodesic((centerCoordinate[1], targeCoordinate[0]), (centerCoordinate[1], centerCoordinate[0]), ellipsoid='WGS-84').meters

    # Apply quadrant-based sign corrections
    # Note: X corresponds to Y, Y corresponds to X due to coordinate system mapping
    if not bool(quadrantX):
        distY = 0 - distY
    if not bool(quadrantY):
        distX = 0 - distX

    # Apply 90-degree counterclockwise rotation for 3D modeling coordinate system
    point = rotate_2d(np.array([distY, -distX]), -90)

    return point

# Process each polygon in the Shapefile
for idx, row in gdf.iterrows():
    geom = row.geometry
    interiors = gdf.interiors
    interior = interiors.values[idx]

    if isinstance(geom, Polygon):
        triangulation = None

        # Only process polygons with holes
        if len(interior) > 0:
            triangulation = polygon_to_triangles(geom, interior)
        else:
            continue
            
        coords = np.array(geom.exterior.coords[:-1])
        
        # Set building height (could be extracted from attribute field)
        # height = row['MEAN']
        height = 0

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

        # Count interior hole vertices
        interiorCount = 0

        # Process interior hole vertices
        if isinstance(interior[0], LinearRing):
            interiorCenter = interior[0].centroid.coords[0]
            interiorCoords = interior[0].coords[:-1]
            interiorCount += len(interiorCoords)
            # Alternative approach for hole vertices (commented out)
            # for coord in interiorCoords:
            #     point = calculateCoordinate(coord, interiorCenter)
            #     obj_content.append(f"v {point[0]} {height} {point[1]}\n")

        # Add top face vertices
        for point in points:
            obj_content.append(f"v {point[0] + center[0]} {height + buildingHeight} {point[1] + center[1]}\n")

        # Calculate vertex count and offset for indexing
        num_vertices = len(coords) + interiorCount
        num_triangles = len(triangulation['triangles'])
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
with open('../buildings.obj', 'w') as f:
    f.writelines(obj_content)

# Save center coordinates to a text file for reference
with open('../center.txt', 'w') as f:
    f.writelines(str(shpCenter))

# Convert OBJ to GLB format for Cesium compatibility
obj_path = '../buildings.obj'
glb_path = '../buildings.glb'
# Alternative conversion using trimesh (commented out)
# mesh = trimesh.load(obj_path, None, None, 'mesh')
# mesh.export(glb_path)
scene = a3d.Scene.from_file(obj_path)
scene.save(glb_path)
