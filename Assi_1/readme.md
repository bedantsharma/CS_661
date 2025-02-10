# README: 3D Isocontour Extraction

## Overview
This script extracts a 3D isocontour from a given VTK Image Data (`.vti`) file and saves the output as a VTK PolyData (`.vtp`) file. The output can be visualized using ParaView.

## Requirements
- Python 3.x
- VTK library

## Installation
Ensure VTK is installed before running the script. You can install it via:
```sh
pip install vtk
```

## Usage
To run the script, use the following command:
```sh
python script.py <input.vti> <output.vtp> <isovalue>
```
where:
- `<input.vti>` is the path to the input VTK image data file.
- `<output.vtp>` is the path to save the extracted isocontour as a VTK PolyData file.
- `<isovalue>` is the scalar value for which the isocontour is extracted.

## Example
```sh
python script.py Isabel_3D.vti output.vtp 1000
```

## Output
- The script generates a `.vtp` file containing the extracted isocontour.
- You can visualize the output in **ParaView** by opening the `.vtp` file.

## Notes
- The script processes the 3D volume slice-by-slice to extract the isocontour.
- Make sure the input `.vti` file contains valid scalar values in the specified range.

## Troubleshooting
- If the output does not appear as expected, verify that the isovalue is within the data range (-1438, 630).
- Ensure VTK is correctly installed and accessible from Python.
