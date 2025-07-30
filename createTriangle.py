"""
Polygon triangulation algorithms for converting 2D polygons to triangular meshes.
This module provides functions for triangulating both simple polygons and polygons with holes.
"""

import triangle as tr
from shapely.geometry import LinearRing
import matplotlib.pyplot as plt
import numpy as np

def drawDelaunayFromTriangle(edges, vertices):
    """
    Visualize the triangulation result using matplotlib.
    
    Args:
        edges (numpy.ndarray): Array of edge indices defining triangle boundaries
        vertices (numpy.ndarray): Array of vertex coordinates
    
    Returns:
        None: Displays the triangulation plot
    """
    # Draw each edge of the triangulation
    for eachEdge in edges:
        # Convert edge indices to coordinate points
        edgePoint = changeIndexToCoordinate(list(eachEdge), vertices)
        plt.plot(edgePoint[:, 0], edgePoint[:, 1], color='black', linewidth=1)  # Draw each edge of the triangulation

    plt.gca().set_aspect(1)

def changeIndexToCoordinate(pointList, vertices):
    """
    Convert vertex indices to coordinate points.
    
    Args:
        pointList (list or int): Vertex indices (single index or list of indices)
        vertices (numpy.ndarray): Array of all vertex coordinates
    
    Returns:
        numpy.ndarray: Coordinate points corresponding to the input indices
    """
    # Create empty array for converted coordinates
    coordinate = np.empty(shape=(len(pointList), 2))

    # Handle list of indices
    if type(pointList) is list:
        # Convert each index to its corresponding coordinate
        for index, each in enumerate(pointList):
            coordinate[index, :] = vertices[each]  # Convert array format to list format
        return coordinate

    # Handle single index
    else:
        coordinate[0, :] = vertices[pointList]
        return coordinate

def polygonToTriangleNormal(polygon):
    """
    Triangulate a simple polygon without holes using the triangle library.
    
    This function converts a Shapely polygon to a triangular mesh by:
    1. Extracting exterior coordinates
    2. Defining boundary constraints
    3. Performing constrained triangulation
    4. Visualizing the result
    
    Args:
        polygon (shapely.geometry.Polygon): Input polygon geometry
    
    Returns:
        dict: Triangulation result containing vertices, triangles, and edges
    """
    # Convert Shapely polygon to triangle library format
    coords = np.array(polygon.exterior.coords[:-1])

    # Define boundary constraints for triangulation
    edges = []
    for i in range(len(coords) - 1):
        edges.append([i, i + 1])
    # Close the boundary
    edges.append([len(coords) - 1, 0])

    # Convert boundary constraints to numpy array
    edges = np.array(edges)

    # Define triangulation constraints
    constraints = {'segments': edges}

    # Perform constrained triangulation with edge preservation
    triangulation = tr.triangulate({'vertices': coords, 'segments': constraints['segments']}, '-pe')

    # Extract triangulation results
    triangles = triangulation['triangles']
    vertices = triangulation['vertices']
    edges = triangulation['edges']
    
    # Visualize the triangulation result
    plt.figure(num='triangle库效果')
    drawDelaunayFromTriangle(edges, vertices)
    # plt.show()

    return triangulation

def polygonToTriangleHole(polygon, interiors):
    """
    Triangulate a polygon with holes using the triangle library.
    
    This function handles complex polygons with interior holes by:
    1. Processing exterior boundary
    2. Processing interior hole boundaries
    3. Defining constraints for both exterior and interior edges
    4. Performing constrained triangulation with hole specification
    
    Args:
        polygon (shapely.geometry.Polygon): Input polygon geometry
        interiors (list): List of interior LinearRing objects representing holes
    
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
    centerList = []

    coords = coords.tolist()

    for interior in interiors:
        if isinstance(interior, LinearRing):
            # Calculate hole center for triangle library
            center = interior.centroid.coords[0]
            centerList.append(center)
            interiorCoords = interior.coords[:-1]

        index = index + 1
        # Define interior boundary constraints
        for i in range(len(interiorCoords) - 1):
            interiosEdges.append([i + index, i + index + 1])

        # Close the interior boundary
        interiosEdges.append([len(interiorCoords) - 1 + index, index])
        coords = coords + interiorCoords
        index += len(interiorCoords) - 1

    # Define triangulation constraints including both exterior and interior edges
    constraints = {'segments': edges + interiosEdges}

    # Perform constrained triangulation with hole specification
    triangulation = tr.triangulate({'vertices': coords, 'segments': constraints['segments'], 'holes': centerList }, '-pe')
    
    # Extract triangulation results
    triangles = triangulation['triangles']
    vertices = triangulation['vertices']
    edges = triangulation['edges']
    
    # Visualize the triangulation result
    plt.figure(num='triangle库效果')
    drawDelaunayFromTriangle(edges, vertices)
    # plt.show()
    
    return triangulation

# Example usage and testing code (commented out)
# # Regular square
# if __name__ == '__main__':
#     polygon2 = [[0, 0], [10, 0], [10, 10], [0, 10]]
#     segments2 = [[0, 1], [1, 2], [2, 3], [3, 0]]
#     t2 = tr.triangulate({'vertices': polygon2, 'segments': segments2}, 'peq30a0.5')
#     triangles2 = t2['triangles']
#     vertices2 = t2['vertices']
#     edges2 = t2['edges']
#     plt.figure(num='triangle库效果2')
#     drawDelaunayFromTriangle(edges2, vertices2)
#     plt.show()
#
# # Square with single hole
# if __name__ == '__main__':
#     polygon = [[0, 0], [10, 0], [10, 10], [0, 10], [4, 4], [6, 4], [6, 6], [4, 6]]      # Square
#     segments = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4]]
#     holes = [[5, 5]]
#     t = tr.triangulate({'vertices': polygon, 'segments': segments}, 'peq30a0.5')
#     triangles = t['triangles']
#     vertices = t['vertices']
#     edges = t['edges']
#     plt.figure(num='triangle库效果')
#     drawDelaunayFromTriangle(edges, vertices)
#     plt.show()

# # Square with multiple holes
# if __name__ == '__main__':
#     polygon = [[0, 0], [10, 0], [10, 10], [0, 10], (1, 1), (3, 1), (3, 3), (1, 3), (4, 4), (6, 4), (6, 6), (4, 6)]      # Square
#     segments = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4],[8,9], [9,10], [10,11],[11,8]]
#     holes = [(2, 2), (5,5)]
#     t = tr.triangulate({'vertices': polygon, 'segments': segments, 'holes': holes}, 'peq30a0.5')
#     triangles = t['triangles']
#     vertices = t['vertices']
#     edges = t['edges']
#     plt.figure(num='triangle库效果')
#     drawDelaunayFromTriangle(edges, vertices)
#     plt.show()

