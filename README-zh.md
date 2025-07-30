# shp-transform-obj

| [English](README.md) | [中文](README-zh.md) |

一个用于将Shapefile（.shp）文件转换为3D OBJ文件的Python工具。该工具可以将地理空间数据转换为可在3D建模软件中使用的3D模型。

## 我们做这个工具的初衷

生成的OBJ模型会转换为GLB格式，用于在Cesium中加载。这个工具的开发是为了弥合地理空间数据和3D网络可视化之间的差距，实现建筑轮廓与基于Cesium的3D应用程序的无缝集成。因此该工具中最终导出的模型坐标系是跟cesium坐标系一致的，如果是其他坐标系，需要自行修改。

### 背景
在从事3D地理空间可视化项目时，我们经常遇到将Shapefile中的2D建筑轮廓数据转换为可在Cesium中加载的3D模型的挑战。现有工具要么过于复杂、昂贵，要么无法提供此工作流程所需的特定功能。

### 解决方案
这个工具提供了一个简化的解决方案：
- 直接将Shapefile建筑轮廓转换为3D OBJ模型
- 自动处理带孔洞的复杂多边形
- 执行从地理坐标到3D空间的精确坐标转换
- 生成GLB格式输出以无缝集成到Cesium
- 保持建筑高度信息和几何精度

### 使用场景
主要应用场景是城市规划、建筑可视化和3D城市建模，其中建筑轮廓数据需要转换为3D模型以用于基于Web的可视化平台，如Cesium。

## 功能特性

- 🗺️ **Shapefile支持**: 读取并处理Shapefile格式的地理数据
- 🔺 **三角化处理**: 自动将多边形面转换为三角网格
- 🕳️ **孔洞支持**: 支持带孔洞的复杂多边形
- 🏗️ **3D建模**: 生成具有高度信息的3D建筑模型
- 📐 **坐标转换**: 将地理坐标转换为3D空间坐标
- 🔄 **旋转变换**: 支持2D和3D坐标旋转
- 📁 **OBJ输出**: 生成标准的OBJ格式3D模型文件

## 项目结构

```
shp-transform-obj/
├── main.py                    # 主程序入口文件
├── shp2obj.py                # 核心Shapefile转OBJ转换模块
├── coordinate.py              # 地理坐标转换工具
├── createTriangle.py          # 多边形三角化算法
├── rotation.py                # 2D/3D坐标旋转变换
├── LICENSE                    # MIT许可证文件
├── README.md                  # 英文文档
├── README-zh.md              # 中文文档
├── buildings.obj             # 生成的3D模型输出
├── buildings.glb             # GLB格式3D模型
├── buildings.txt                # 中心点坐标
├── aspose_3d-25.3.0-py3-none-win_amd64.whl  # 3D库wheel文件
├── data/                     # 输入数据目录
│   ├── building.shp          # Shapefile几何数据
│   ├── building.shx          # Shapefile索引文件
│   ├── building.dbf          # Shapefile属性数据
│   ├── building.prj          # Shapefile投影文件
│   ├── building.cpg          # Shapefile代码页
│   └── building.qmd          # Shapefile元数据
└── test/                     # 测试和示例文件
    ├── normal-polygon.py     # 普通多边形三角化测试
    └── hole-polygon.py       # 带孔洞多边形三角化测试
```

## 安装依赖

### 系统要求
- Python 3.10
- Windows/Linux/macOS

### 安装Python包

```bash
pip install geopandas
pip install numpy
pip install shapely
pip install triangle
pip install geopy
pip install trimesh
pip install aspose-threed
pip install matplotlib
pip install ./aspose_3d-25.3.0-py3-none-win_amd64.whl
```

## 使用方法

### 基本使用

1. **准备数据**: 将你的Shapefile文件放在`data/`目录下
2. **修改配置**: 在`main.py`中修改文件路径和参数
3. **运行程序**: 执行主程序

```bash
python main.py
```

### 配置参数

在`main.py`中可以修改以下参数：

```python
# 输入文件路径
shapefile_path = r'data\\building.shp'

# 建筑高度（米）
buildingHeight = 3

# 输出文件名
output_file = 'buildings.obj'
```

### 示例代码

```python
from shp2obj import shp2obj

if __name__ == '__main__':
    shapefile_path = r'data\\building.shp'
    obj_path = 'building.obj'
    shp2obj(shapefile_path, obj_path)
```

## 核心模块说明

### coordinate.py
- **功能**: 地理坐标转换
- **主要函数**: `calculateCoordinate()`
- **作用**: 将地理坐标转换为3D空间坐标

### createTriangle.py
- **功能**: 多边形三角化
- **主要函数**: 
  - `polygonToTriangleNormal()`: 处理普通多边形
  - `polygonToTriangleHole()`: 处理带孔洞的多边形
- **作用**: 将多边形面转换为三角网格

### rotation.py
- **功能**: 坐标旋转变换
- **主要函数**:
  - `rotate_X()`: 绕X轴旋转
  - `rotate_Y()`: 绕Y轴旋转
  - `rotate_Z()`: 绕Z轴旋转
  - `rotate_2d()`: 2D平面旋转

## 输出格式

生成的OBJ文件包含：
- **顶点数据**: 3D坐标点
- **面数据**: 三角形面片定义
- **材质信息**: 可选的材质和纹理信息

### OBJ文件示例

```
# Generated OBJ file
v 0.0 0.0 0.0
v 10.0 0.0 0.0
v 10.0 0.0 10.0
v 0.0 0.0 10.0
v 0.0 3.0 0.0
v 10.0 3.0 0.0
v 10.0 3.0 10.0
v 0.0 3.0 10.0
f 1 2 3
f 1 3 4
...
```

## 测试

项目包含测试文件，位于`test/`目录：

```bash
python test/normal-polygon.py
```

## 注意事项

1. **坐标系**: 确保输入的Shapefile使用正确的坐标系（如WGS84）
2. **数据质量**: 输入的多边形应该是有效的几何形状
3. **内存使用**: 大型数据集可能需要较多内存
4. **输出路径**: 确保有写入权限的目录
5. **buildings.txt**: 此文件包含在Cesium中加载时用于定位3D模型的中心坐标

## 常见问题

### Q: 如何处理大型Shapefile文件？
A: 可以分批处理或增加内存限制。

### Q: 生成的OBJ文件无法在3D软件中打开？
A: 检查OBJ文件格式是否正确，确保所有面都是三角形。

### Q: 坐标转换不准确？
A: 检查输入数据的坐标系设置。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的Shapefile到OBJ转换
- 支持三角化和坐标转换
- 支持带孔洞的多边形处理
