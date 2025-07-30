"""
Main entry point for the Shapefile to OBJ converter tool.
This script demonstrates how to use the shp2obj module to convert Shapefile data to 3D OBJ format.
"""

from shp2obj import shp2obj

if __name__ == '__main__':
    # Input Shapefile path - contains building footprint data
    shapefile_path = r'data\\building.shp'
    
    # Output OBJ file path - the generated 3D model file
    obj_path = 'building.obj'
    
    # Convert Shapefile to OBJ format
    shp2obj(shapefile_path, obj_path)