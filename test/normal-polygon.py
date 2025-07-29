import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, Point
import triangle  # 用于三角化
import geopy.distance as geoDistance
import trimesh
import aspose.threed as a3d
import matplotlib.pyplot as plt
from createTriangle import  drawDelaunayFromTriangle
from rotation import rotate_2d

# 读取shp文件
shapefile_path = r'../data/building.shp'
gdf = gpd.read_file(shapefile_path)

shpCenter = np.array([(gdf.total_bounds[0] + gdf.total_bounds[2]) / 2,(gdf.total_bounds[1] + gdf.total_bounds[3])/2])

buildingHeight = 30

# 存储OBJ文件的内容
obj_content = []

# 生成OBJ文件头部
obj_content.append("# Generated OBJ file\n")

# 用于记录顶点索引的计数器
vertex_counter = 1

# 构建三角网
def polygon_to_triangles(polygon):
    # 将Shapely的多边形转换为triangle库能处理的格式
    coords = np.array(polygon.exterior.coords[:-1])

    # 定义三角化的边界约束
    edges = []
    for i in range(len(coords) - 1):
        edges.append([i, i + 1])
    # 闭合边界
    edges.append([len(coords) - 1, 0])

    # 将边界约束转化为 numpy 数组
    edges = np.array(edges)

    # 定义三角化的边界约束
    constraints = {'segments': edges}

    # 三角化
    triangulation = triangle.triangulate({'vertices': coords, 'segments': constraints['segments']}, '-pe')

    triangles = triangulation['triangles']
    vertices = triangulation['vertices']
    edges = triangulation['edges']
    plt.figure(num='triangle库效果')
    drawDelaunayFromTriangle(edges, vertices)
    # plt.show()

    return triangulation

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

for idx, row in gdf.iterrows():
    geom = row.geometry
    if isinstance(geom, Polygon):
        triangulation = polygon_to_triangles(geom)
        coords = np.array(geom.exterior.coords[:-1])
        # height = row['MEAN']
        height = 0

        # 获取面的中心
        geoCenter = np.array(geom.centroid.coords[0])

        # 点集合
        points = []

        # 计算模型中心点与shp中心点的距离
        center = calculateCoordinate(geoCenter, shpCenter)

        # 添加底面顶点
        for coord in triangulation['vertices']:

            point = calculateCoordinate(coord, geoCenter)
            points.append(point)
            obj_content.append(f"v {point[0] + center[0]} {height} {point[1] + center[1]}\n")

        # 添加顶部顶点
        for point in points:
            obj_content.append(f"v {point[0] + center[0]} {height + buildingHeight} {point[1] + center[1]}\n")

        num_vertices = len(coords)
        num_triangles = len(triangulation['triangles'])
        offset = num_vertices

        # 添加底面三角形
        for triangle_indices in triangulation['triangles']:
            obj_content.append("f " + " ".join([str(i + vertex_counter) for i in triangle_indices]) + "\n")

        # 添加顶部三角形
        for triangle_indices in triangulation['triangles']:
            obj_content.append("f " + " ".join([str(i + vertex_counter + offset) for i in triangle_indices]) + "\n")

        # 添加侧面三角形
        for triangle_indices in triangulation['triangles']:
            base_triangle = [vertex_counter + i for i in triangle_indices]
            top_triangle = [vertex_counter + i + offset for i in triangle_indices]
            obj_content.append(f"f {base_triangle[0]} {base_triangle[1]} {top_triangle[1]}\n")
            obj_content.append(f"f {base_triangle[0]} {top_triangle[1]} {top_triangle[0]}\n")
            obj_content.append(f"f {base_triangle[1]} {base_triangle[2]} {top_triangle[2]}\n")
            obj_content.append(f"f {base_triangle[1]} {top_triangle[2]} {top_triangle[1]}\n")
            obj_content.append(f"f {base_triangle[2]} {base_triangle[0]} {top_triangle[0]}\n")
            obj_content.append(f"f {base_triangle[2]} {top_triangle[0]} {top_triangle[2]}\n")

        vertex_counter += num_vertices * 2

# 保存OBJ文件
with open('../buildings.obj', 'w') as f:
    f.writelines(obj_content)

# 保存txt文件
with open('../center.txt', 'w') as f:
    f.writelines(str(shpCenter))

# # 输入的.obj 文件路径
obj_path = '../buildings.obj'
glb_path = '../buildings.glb'
# mesh = trimesh.load(obj_path, None, None, 'mesh')
# mesh.export(glb_path)
scene = a3d.Scene.from_file(obj_path)
scene.save(glb_path)
