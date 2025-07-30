# shp-transform-obj

| [English](README.md) | [中文](README-zh.md) |

A Python tool for converting Shapefile (.shp) files to 3D OBJ files. This tool can transform geospatial data into 3D models that can be used in 3D modeling software.

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
├── main.py              # Main program file
├── coordinate.py        # Coordinate conversion module
├── createTriangle.py    # Triangulation processing module
├── rotation.py          # Rotation transformation module
├── test/               # Test files directory
│   └── normal-polygon.py
├── data/               # Data files directory
│   └── building.shp    # Example Shapefile file
└── README.md           # Project documentation
```

## Installation

### System Requirements
- Python 3.7+
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
import geopandas as gpd
from main import process_shapefile

# Read Shapefile
gdf = gpd.read_file('data/building.shp')

# Process and generate OBJ file
process_shapefile(gdf, building_height=3, output_file='buildings.obj')
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

## Frequently Asked Questions

### Q: How to handle large Shapefile files?
A: You can process them in batches or increase memory limits.

### Q: Generated OBJ file cannot be opened in 3D software?
A: Check if the OBJ file format is correct and ensure all faces are triangles.

### Q: Coordinate conversion is inaccurate?
A: Check the coordinate system settings of the input data.

## Contributing

We welcome Issue submissions and Pull Requests to improve this project.

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Changelog

### v1.0.0
- Initial version release
- Support basic Shapefile to OBJ conversion
- Support triangulation and coordinate conversion
- Support polygon processing with holes 