# README for VTK Volume Rendering Script

## Overview
This script performs volume rendering on a 3D scalar dataset (Pressure values from a Hurricane Simulation). It utilizes VTK's ray-casting technique with color and opacity transfer functions. It also supports Phong shading for advanced lighting effects.

## Requirements
- Python 3
- VTK library (install using `pip install vtk`)
- Dataset file: `Isabel_3D.vtk`

## How to Run the Script
1. Ensure you have the required dependencies installed.
2. Run the script using:
   ```bash
   python Q2.py [use_phong]
   ```
   - Replace `[use_phong]` with `true` to enable Phong shading or `false` to disable it.
   - Example:
     ```bash
     python Q2.py true
     ```

## Expected Output
- A 1000x1000 interactive render window displaying the volume-rendered hurricane dataset.
- If Phong shading is enabled, the rendering will have enhanced lighting effects.
- The volume will be outlined with a bounding box.

## Notes
- The script automatically maps colors and opacity based on given data values.
- The background is set to black for better contrast.
- Close the render window to exit the script.