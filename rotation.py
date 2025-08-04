"""
Coordinate rotation transformation utilities for 2D and 3D coordinate systems.
This module provides functions for rotating points around different axes in 3D space and 2D plane.
"""

import numpy as np

def rotate_z(x, y, z, gamma):
    """
    Rotate a 3D point around the Z-axis by a specified angle.
    
    This function applies a rotation matrix around the Z-axis:
    | cos(γ)  -sin(γ)  0 |
    | sin(γ)   cos(γ)  0 |
    |   0        0     1 |
    
    Args:
        x (float): X-coordinate of the point
        y (float): Y-coordinate of the point
        z (float): Z-coordinate of the point
        gamma (float): Rotation angle in degrees (positive for counterclockwise)
    
    Returns:
        tuple: Rotated coordinates (x_r, y_r, z_r)
    """
    # Convert degrees to radians
    gamma = gamma * (np.pi / 180)
    
    # Apply Z-axis rotation matrix
    x_r = np.cos(gamma)*x - np.sin(gamma)*y
    y_r = np.sin(gamma)*x + np.cos(gamma)*y
    z_r = z
    
    # Print rotation result for debugging
    print(f"{(x, y, z)} rotate {gamma*(180/np.pi)} degrees around the Z-axis,result {(x_r, y_r, z_r)}")
    return x_r, y_r, z_r

def rotate_y(x, y, z, beta):
    """
    Rotate a 3D point around the Y-axis by a specified angle.
    
    This function applies a rotation matrix around the Y-axis:
    |  cos(β)  0  sin(β) |
    |    0     1    0     |
    | -sin(β)  0  cos(β) |
    
    Args:
        x (float): X-coordinate of the point
        y (float): Y-coordinate of the point
        z (float): Z-coordinate of the point
        beta (float): Rotation angle in degrees (positive for counterclockwise)
    
    Returns:
        tuple: Rotated coordinates (x_r, y_r, z_r)
    """
    # Convert degrees to radians
    beta = beta * (np.pi / 180)
    
    # Apply Y-axis rotation matrix
    x_r = np.cos(beta)*x + np.sin(beta)*z
    y_r = y
    z_r = -np.sin(beta)*x + np.cos(beta)*z
    
    # Print rotation result for debugging
    print(f"{(x, y, z)} rotate {beta*(180/np.pi)} degrees around the Y-axis,result {(x_r, y_r, z_r)}")
    return x_r, y_r, z_r

def rotate_x(x, y, z, alpha):
    """
    Rotate a 3D point around the X-axis by a specified angle.
    
    This function applies a rotation matrix around the X-axis:
    | 1    0        0      |
    | 0  cos(α)  -sin(α)  |
    | 0  sin(α)   cos(α)  |
    
    Args:
        x (float): X-coordinate of the point
        y (float): Y-coordinate of the point
        z (float): Z-coordinate of the point
        alpha (float): Rotation angle in degrees (positive for counterclockwise)
    
    Returns:
        tuple: Rotated coordinates (x_r, y_r, z_r)
    """
    # Convert degrees to radians
    alpha = alpha * (np.pi / 180)
    
    # Apply X-axis rotation matrix
    x_r = x
    y_r = np.cos(alpha)*y - np.sin(alpha)*z
    z_r = np.sin(alpha)*y + np.cos(alpha)*z
    
    # Print rotation result for debugging
    print(f"{(x, y, z)} rotate {alpha*(180/np.pi)} degrees around the X-axis,result {(x_r, y_r, z_r)}")
    return x_r, y_r, z_r

def rotate_2d(point, angle):
    """
    Rotate a 2D point by a specified angle around the origin.
    
    This function applies a 2D rotation matrix:
    | cos(θ)  -sin(θ) |
    | sin(θ)   cos(θ) |
    
    Args:
        point (numpy.ndarray): 2D point coordinates [x, y]
        angle (float): Rotation angle in degrees (positive for counterclockwise)
    
    Returns:
        numpy.ndarray: Rotated 2D point coordinates
    """
    # Convert degrees to radians
    theta = np.radians(angle)
    
    # Calculate trigonometric values
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    
    # Create 2D rotation matrix
    matrix = np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])
    
    # Apply rotation transformation
    result = np.dot(point, matrix)
    return result