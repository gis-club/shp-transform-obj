import triangle as tr
from shapely.geometry import LinearRing
import matplotlib.pyplot as plt
import numpy as np

# 绘制三角化之后的图像
# 入参:edges:所有的边索引结构；vertices:所有的顶点坐标
# 返回:画出图像
def drawDelaunayFromTriangle(edges, vertices):
    # 获取每一个边，并对每一个边进行绘制
    for eachEdge in edges:
        # 将每一个边都转换为坐标的形式
        edgePoint = changeIndexToCoordinate(list(eachEdge), vertices)
        plt.plot(edgePoint[:, 0], edgePoint[:, 1], color='black', linewidth=1)  # 绘制三角剖分的每一条边

    plt.gca().set_aspect(1)

# 将点序列转换为坐标的形式
# 入参:pointList:点坐标索引，可以输入单独索引或是列表形式；vertices:要转换的索引所在的所有点的坐标列表；
# 返回:coordinate:输入点索引的坐标形式；例如:[0.1, 0.1]或[[0.1, 0.1], [0.1, 0.1]]；
def changeIndexToCoordinate(pointList, vertices):
    # 创建一个放置转换后坐标的空列表
    coordinate = np.empty(shape=(len(pointList), 2))

    # 判断输入的序列如果是列表则要进行循环
    if type(pointList) is list:

        # 循环输入索引中的每一个索引数字
        for index, each in enumerate(pointList):
            coordinate[index, :] = vertices[each]  # 因为所有的顶点坐标都是数组的形式，这里将其转换为列表的形式
        return coordinate

    # 如果不是列表则直接转换就可以了
    else:
        coordinate[0, :] = vertices[pointList]
        return coordinate

# 常规shp面转三角网
# 入参: 矢量面
def polygonToTriangleNormal(polygon):
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
    triangulation = tr.triangulate({'vertices': coords, 'segments': constraints['segments']}, '-pe')

    triangles = triangulation['triangles']
    vertices = triangulation['vertices']
    edges = triangulation['edges']
    plt.figure(num='triangle库效果')
    drawDelaunayFromTriangle(edges, vertices)
    # plt.show()

    return triangulation

# 带孔洞shp面转三角网
# 入参: polygon:矢量面; interior: 孔洞
def polygonToTriangleHole(polygon, interiors):
    # 将Shapely的多边形转换为triangle库能处理的格式
    coords = np.array(polygon.exterior.coords[:-1])

    # 定义三角化的边界约束
    edges = []
    index = 0
    for i in range(len(coords) - 1):
        edges.append([i, i + 1])
        index = i + 1
    # 闭合边界
    edges.append([len(coords) - 1, 0])

    interiosEdges = []
    interiorCoords = None
    centerList = []

    coords = coords.tolist()

    for interior in interiors:
        if isinstance(interior, LinearRing):
            center = interior.centroid.coords[0]
            centerList.append(center)
            interiorCoords = interior.coords[:-1]


        index = index + 1
        for i in range(len(interiorCoords) - 1):
            interiosEdges.append([i + index, i + index + 1])

        interiosEdges.append([len(interiorCoords) - 1 + index, index])
        coords = coords + interiorCoords
        index += len(interiorCoords) - 1

    # 定义三角化的边界约束
    constraints = {'segments': edges + interiosEdges}

    # 三角化
    triangulation = tr.triangulate({'vertices': coords, 'segments': constraints['segments'], 'holes': centerList }, '-pe')
    triangles = triangulation['triangles']
    vertices = triangulation['vertices']
    edges = triangulation['edges']
    plt.figure(num='triangle库效果')
    drawDelaunayFromTriangle(edges, vertices)
    # plt.show()
    return triangulation

# # 普通正方形
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
# # 带洞的正方形(单个孔洞)
# if __name__ == '__main__':
#     polygon = [[0, 0], [10, 0], [10, 10], [0, 10], [4, 4], [6, 4], [6, 6], [4, 6]]      # 正方形
#     segments = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4]]
#     holes = [[5, 5]]
#     t = tr.triangulate({'vertices': polygon, 'segments': segments}, 'peq30a0.5')
#     triangles = t['triangles']
#     vertices = t['vertices']
#     edges = t['edges']
#     plt.figure(num='triangle库效果')
#     drawDelaunayFromTriangle(edges, vertices)
#     plt.show()

# # 带洞的正方形(多个孔洞)
# if __name__ == '__main__':
#     polygon = [[0, 0], [10, 0], [10, 10], [0, 10], (1, 1), (3, 1), (3, 3), (1, 3), (4, 4), (6, 4), (6, 6), (4, 6)]      # 正方形
#     segments = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4],[8,9], [9,10], [10,11],[11,8]]
#     holes = [(2, 2), (5,5)]
#     t = tr.triangulate({'vertices': polygon, 'segments': segments, 'holes': holes}, 'peq30a0.5')
#     triangles = t['triangles']
#     vertices = t['vertices']
#     edges = t['edges']
#     plt.figure(num='triangle库效果')
#     drawDelaunayFromTriangle(edges, vertices)
#     plt.show()

