# shp-transform-obj

| [English](README.md) | [中文](README-zh.md) |

A Python tool for converting Shapefile (.shp) files to 3D OBJ files. This tool can transform geospatial data into 3D models that can be used in 3D modeling software.

## Our Motivation for Creating This Tool

The generated OBJ models are converted to GLB format for loading in Cesium. This tool was developed to bridge the gap between geospatial data and 3D web visualization, enabling seamless integration of building footprints into Cesium-based 3D applications. Therefore, the final exported model coordinate system in this tool is consistent with the Cesium coordinate system. If other coordinate systems are needed, modifications must be made accordingly.

### Background
When working with 3D geospatial visualization projects, we often encountered the challenge of converting 2D building footprint data from Shapefiles into 3D models that could be loaded into Cesium for web-based 3D visualization. Existing tools were either too complex, expensive, or didn't provide the specific functionality needed for this workflow.

### Solution
This tool provides a streamlined solution that:
- Converts Shapefile building footprints directly to 3D OBJ models
- Handles complex polygons with holes automatically
- Performs accurate coordinate transformations from geographic to 3D space
- Generates GLB format output for seamless Cesium integration
- Maintains building height information and geometric accuracy

### Use Case
The primary use case is for urban planning, architectural visualization, and 3D city modeling where building footprint data needs to be converted into 3D models for web-based visualization platforms like Cesium.

## Features

- 🗺️ **Shapefile Support**: Read and process Shapefile format geospatial data
- 🔺 **Triangulation Processing**: Automatically convert polygon faces to triangular meshes
- 🕳️ **Hole Support**: Support complex polygons with holes
- 🏗️ **3D Modeling**: Generate 3D building models with height information
- 📐 **Coordinate Conversion**: Convert geographic coordinates to 3D spatial coordinates
- 🔄 **Rotation Transformation**: Support 2D and 3D coordinate rotation
- 📁 **OBJ Output**: Generate standard OBJ format 3D model files

## Project Structure

```
shp-transform-obj/
├── main.py                    # Main program entry point
├── shp2obj.py                # Core Shapefile to OBJ conversion module
├── coordinate.py              # Geographic coordinate conversion utilities
├── createTriangle.py          # Polygon triangulation algorithms
├── rotation.py                # 2D/3D coordinate rotation transformations
├── LICENSE                    # MIT License file
├── README.md                  # English documentation
├── README-zh.md              # Chinese documentation
├── buildings.obj             # Generated 3D model output
├── buildings.glb             # GLB format 3D model
├── buildings.txt                # Center point coordinates
├── aspose_3d-25.3.0-py3-none-win_amd64.whl  # 3D library wheel file
├── data/                     # Input data directory
│   ├── building.shp          # Shapefile geometry data
│   ├── building.shx          # Shapefile index file
│   ├── building.dbf          # Shapefile attribute data
│   ├── building.prj          # Shapefile projection file
│   ├── building.cpg          # Shapefile code page
│   └── building.qmd          # Shapefile metadata
└── test/                     # Test and example files
    ├── normal-polygon.py     # Regular polygon triangulation test
    └── hole-polygon.py       # Polygon with holes triangulation test
```

## SHP Data Acquisition

We use SHP data downloaded from [https://download.geofabrik.de/](https://download.geofabrik.de/).

## Installation

### System Requirements
- Python 3.10
- Windows/Linux/macOS

### Install Python Packages

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

## Usage

### Basic Usage

1. **Prepare Data**: Place your Shapefile file in the `data/` directory
2. **Modify Configuration**: Modify file paths and parameters in `main.py`
3. **Run Program**: Execute the main program

```bash
python main.py
```

### Configuration Parameters

You can modify the following parameters in `main.py`:

```python
# Input file path
shapefile_path = r'data\\building.shp'

# Building height (meters)
buildingHeight = 3

# Output file name
output_file = 'buildings.obj'
```

### Example Code

```python
from shp2obj import shp2obj

if __name__ == '__main__':
    shapefile_path = r'data\\building.shp'
    obj_path = 'building.obj'
    shp2obj(shapefile_path, obj_path)
```

## Core Modules

### coordinate.py
- **Function**: Geographic coordinate conversion
- **Main Function**: `calculateCoordinate()`
- **Purpose**: Convert geographic coordinates to 3D spatial coordinates

### createTriangle.py
- **Function**: Polygon triangulation
- **Main Functions**: 
  - `polygonToTriangleNormal()`: Process regular polygons
  - `polygonToTriangleHole()`: Process polygons with holes
- **Purpose**: Convert polygon faces to triangular meshes

### rotation.py
- **Function**: Coordinate rotation transformation
- **Main Functions**:
  - `rotate_X()`: Rotate around X-axis
  - `rotate_Y()`: Rotate around Y-axis
  - `rotate_Z()`: Rotate around Z-axis
  - `rotate_2d()`: 2D plane rotation

## Output Format

The generated OBJ file contains:
- **Vertex Data**: 3D coordinate points
- **Face Data**: Triangle face definitions
- **Material Information**: Optional material and texture information

### OBJ File Example

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

## Testing

The project includes test files located in the `test/` directory:

```bash
python test/normal-polygon.py
```

## Important Notes

1. **Coordinate System**: Ensure the input Shapefile uses the correct coordinate system (such as WGS84)
2. **Data Quality**: Input polygons should be valid geometric shapes
3. **Memory Usage**: Large datasets may require significant memory
4. **Output Path**: Ensure you have write permissions for the output directory
5. **buildings.txt**: This file contains the center coordinates used for positioning the 3D model when loading in Cesium

## Frequently Asked Questions

### Q: How to handle large Shapefile files?
A: You can process them in batches or increase memory limits.

### Q: Generated OBJ file cannot be opened in 3D software?
A: Check if the OBJ file format is correct and ensure all faces are triangles.

### Q: Coordinate conversion is inaccurate?
A: Check the coordinate system settings of the input data.

## Contributing

We welcome Issue submissions and Pull Requests to improve this project.

## TODO

We will provide corresponding TypeScript code in the future to facilitate web developers' usage.

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Changelog

### v1.0.0
- Initial version release
- Support basic Shapefile to OBJ conversion
- Support triangulation and coordinate conversion
- Support polygon processing with holes 