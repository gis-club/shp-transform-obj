import geopy.distance as geoDistance
import numpy as np
from rotation import rotate_2d

# 计算坐标
def calculateCoordinate(targeCoordinate, centerCoordinate):
    # 以中心点为坐标原点，进行坐标构建
    lon = targeCoordinate[0] - centerCoordinate[0]
    lat = targeCoordinate[1] - centerCoordinate[1]

    # 判断象限
    quadrantX = True
    quadrantY = True
    if lon < 0 and lat < 0:
        quadrantX = False
        quadrantY = False
    elif lon < 0 and lat > 0:
        quadrantX = False
    elif lon > 0 and lat < 0:
        quadrantY = False

    # 计算距离
    distX = geoDistance.geodesic((targeCoordinate[1], centerCoordinate[0]), (centerCoordinate[1], centerCoordinate[0]), ellipsoid='WGS-84').meters
    distY = geoDistance.geodesic((centerCoordinate[1], targeCoordinate[0]), (centerCoordinate[1], centerCoordinate[0]), ellipsoid='WGS-84').meters

    # X对应Y, Y对应X
    if not bool(quadrantX):
        distY = 0 - distY
    if not bool(quadrantY):
        distX = 0 - distX

    # 逆时针旋转90°
    point = rotate_2d(np.array([distY, -distX]), -90)

    return point