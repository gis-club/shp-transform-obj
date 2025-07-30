import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, Point, LinearRing
import triangle  # 用于三角化
import geopy.distance as geoDistance
import trimesh
import aspose.threed as a3d
from createTriangle import  polygonToTriangleNormal, polygonToTriangleHole
from coordinate  import calculateCoordinate

# 读取shp文件
# read shp file
shapefile_path = r'data\\building.shp'
gdf = gpd.read_file(shapefile_path)

shpCenter = np.array([(gdf.total_bounds[0] + gdf.total_bounds[2]) / 2,(gdf.total_bounds[1] + gdf.total_bounds[3])/2])

buildingHeight = 3

# 存储OBJ文件的内容
obj_content = []

# 生成OBJ文件头部
obj_content.append("# Generated OBJ file\n")

# 用于记录顶点索引的计数器
vertex_counter = 1

for idx, row in gdf.iterrows():
    geom = row.geometry

    if isinstance(geom, Polygon):
        # 孔洞个数
        interiorLength = len(geom.interiors)

        # 孔洞点位数
        interiorCount = 0

        # 三角分割结果
        triangulation = None
        if interiorLength > 0:
            triangulation = polygonToTriangleHole(geom, geom.interiors)
            for interior in geom.interiors:
                if isinstance(interior, LinearRing):
                    interiorCoords = interior.coords[:-1]
                    interiorCount += len(interiorCoords)
        else:
            triangulation = polygonToTriangleNormal(geom)

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

        num_vertices = len(coords) + interiorCount
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
with open('buildings.obj', 'w') as f:
    f.writelines(obj_content)

# 保存txt文件
with open('center.txt', 'w') as f:
    f.writelines(str(shpCenter))

# # 输入的.obj 文件路径
obj_path = 'buildings.obj'
glb_path = 'buildings.glb'
# mesh = trimesh.load(obj_path, None, None, 'mesh')
# mesh.export(glb_path)
scene = a3d.Scene.from_file(obj_path)
scene.save(glb_path)
