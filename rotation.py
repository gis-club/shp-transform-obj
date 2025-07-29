import numpy as np

# 1、绕Z轴旋转gamma角
def rotate_Z(x, y, z,  gamma):
    gamma = gamma * (np.pi / 180)
    x_r = np.cos(gamma)*x - np.sin(gamma)*y
    y_r = np.sin(gamma)*x + np.cos(gamma)*y
    z_r = z
    print(f"{(x, y, z)} rotate {gamma*(180/np.pi)} degrees around the Z-axis,result {(x_r, y_r, z_r)}")
    return x_r, y_r, z_r

# 2、绕Y轴旋转beta角
def rotate_Y(x, y, z, beta):
    beta = beta * (np.pi / 180)
    x_r = np.cos(beta)*x + np.sin(beta)*z
    y_r = y
    z_r = -np.sin(beta)*x + np.cos(beta)*z
    print(f"{(x, y, z)} rotate {beta*(180/np.pi)} degrees around the Y-axis,result {(x_r, y_r, z_r)}")
    return x_r, y_r, z_r

# 3、绕X轴旋转alpha角
def rotate_X(x, y, z, alpha):
    alpha = alpha * (np.pi / 180)
    x_r = x
    y_r = np.cos(alpha)*y - np.sin(alpha)*z
    z_r = np.sin(alpha)*y + np.cos(alpha)*z
    print(f"{(x, y, z)} rotate {alpha*(180/np.pi)} degrees around the X-axis,result {(x_r, y_r, z_r)}")
    return x_r, y_r, z_r

def rotate_2d(point, angle):
    theta = np.radians(angle)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    matrix = np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])
    rotat_point = np.dot(point, matrix)
    return rotat_point