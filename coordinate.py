"""
Coordinate conversion utilities for transforming geographic coordinates to 3D spatial coordinates.
This module handles the conversion from geographic (lat/lon) coordinates to local 3D coordinates.
"""

import geopy.distance as geoDistance
import numpy as np
from rotation import rotate_2d

def calculateCoordinate(targeCoordinate, centerCoordinate):
    """
    Convert geographic coordinates to local 3D coordinates relative to a center point.
    
    This function performs the following transformations:
    1. Calculates relative position from center point
    2. Determines quadrant for proper sign assignment
    3. Converts geographic distances to meters using geodesic calculations
    4. Applies coordinate system rotation for 3D modeling
    
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
    # This aligns the coordinate system with standard 3D modeling conventions
    point = rotate_2d(np.array([distY, -distX]), -90)

    return point