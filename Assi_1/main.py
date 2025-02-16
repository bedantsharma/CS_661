import vtk
import sys


class three_d_filter():
    def interpolate(self,p1, v1, p2, v2, isovalue):
        """ Linear interpolation between two points """
        if v2 - v1 == 0:
            return p1  # Avoid division by zero
        t = (isovalue - v1) / (v2 - v1)
        return p1 + t * (p2 - p1)

    def extract_isocontour_3d(self,input_filename, output_filename, isovalue):
        # Read VTK Image Data
        reader = vtk.vtkXMLImageDataReader()
        reader.SetFileName(input_filename)
        reader.Update()
        image_data = reader.GetOutput()

        dims = image_data.GetDimensions()
        spacing = image_data.GetSpacing()
        origin = image_data.GetOrigin()
        extent = image_data.GetExtent()  # Get valid Z range
        
        points = vtk.vtkPoints()
        lines = vtk.vtkCellArray()

        for k in range(extent[4], extent[5]+1):  # Loop over Z slices
            for i in range(dims[0] - 1):
                for j in range(dims[1] - 1):

                    if i + 1 >= dims[0] or j + 1 >= dims[1]:
                        continue  # Avoid out-of-bounds access
                    
                    # Get scalar values for the 4 corners of the cell
                    v00 = image_data.GetScalarComponentAsDouble(i, j, k, 0)
                    v10 = image_data.GetScalarComponentAsDouble(i+1, j, k, 0)
                    v01 = image_data.GetScalarComponentAsDouble(i, j+1, k, 0)
                    v11 = image_data.GetScalarComponentAsDouble(i+1, j+1, k, 0)
                    
                    # Get the coordinates of the cell corners
                    x0, y0, z0 = origin[0] + i * spacing[0], origin[1] + j * spacing[1], origin[2] + k * spacing[2]
                    x1, y1 = origin[0] + (i+1) * spacing[0], origin[1] + (j+1) * spacing[1]

                    edges = []

                    if (v00 < isovalue and v10 >= isovalue) or (v00 >= isovalue and v10 < isovalue):
                        edges.append([self.interpolate(x0, v00, x1, v10, isovalue), y0, z0])
                    if (v10 < isovalue and v11 >= isovalue) or (v10 >= isovalue and v11 < isovalue):
                        edges.append([x1, self.interpolate(y0, v10, y1, v11, isovalue), z0])
                    if (v01 < isovalue and v11 >= isovalue) or (v01 >= isovalue and v11 < isovalue):
                        edges.append([self.interpolate(x0, v01, x1, v11, isovalue), y1, z0])
                    if (v00 < isovalue and v01 >= isovalue) or (v00 >= isovalue and v01 < isovalue):
                        edges.append([x0, self.interpolate(y0, v00, y1, v01, isovalue), z0])

                    if len(edges) == 2:
                        p1_id = points.InsertNextPoint(edges[0][0], edges[0][1], edges[0][2])
                        p2_id = points.InsertNextPoint(edges[1][0], edges[1][1], edges[1][2])
                        line = vtk.vtkLine()
                        line.GetPointIds().SetId(0, p1_id)
                        line.GetPointIds().SetId(1, p2_id)
                        lines.InsertNextCell(line)

        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(points)
        poly_data.SetLines(lines)

        writer = vtk.vtkXMLPolyDataWriter()
        writer.SetFileName(output_filename)
        writer.SetInputData(poly_data)
        writer.Write()

        print(f"3D Isocontour extracted and saved to {output_filename}")
        
        
# class two_d_filter():
#     def interpolate(self,p1, v1, p2, v2, isovalue):
#         """ Linear interpolation between two points """
#         if v2 - v1 == 0:
#             return p1  # Avoid division by zero
#         t = (isovalue - v1) / (v2 - v1)
#         return p1 + t * (p2 - p1)

#     def extract_isocontour(self,input_filename, output_filename, isovalue):
#         # Read VTK Image Data
#         reader = vtk.vtkXMLImageDataReader()
#         reader.SetFileName(input_filename)
#         reader.Update()
#         image_data = reader.GetOutput()
        
#         dims = image_data.GetDimensions()
#         spacing = image_data.GetSpacing()
#         origin = image_data.GetOrigin()
        
#         points = vtk.vtkPoints()
#         lines = vtk.vtkCellArray()
        
#         for i in range(dims[0] - 1):
#             for j in range(dims[1] - 1):
                
#                 if i + 1 >= dims[0] or j + 1 >= dims[1]:
#                     continue  # Avoid out-of-bounds access
                
#                 z_index = 25  # Adjust if needed
#                 v00 = image_data.GetScalarComponentAsDouble(i, j, z_index, 0)
#                 v10 = image_data.GetScalarComponentAsDouble(i+1, j, z_index, 0)
#                 v01 = image_data.GetScalarComponentAsDouble(i, j+1, z_index, 0)
#                 v11 = image_data.GetScalarComponentAsDouble(i+1, j+1, z_index, 0)
                
#                 # Get the coordinates of the cell corners
#                 x0, y0 = origin[0] + i * spacing[0], origin[1] + j * spacing[1]
#                 x1, y1 = origin[0] + (i+1) * spacing[0], origin[1] + (j+1) * spacing[1]
                
#                 edges = []
                
#                 if (v00 < isovalue and v10 >= isovalue) or (v00 >= isovalue and v10 < isovalue):
#                     edges.append([self.interpolate(x0, v00, x1, v10, isovalue), y0])
#                 if (v10 < isovalue and v11 >= isovalue) or (v10 >= isovalue and v11 < isovalue):
#                     edges.append([x1, self.interpolate(y0, v10, y1, v11, isovalue)])
#                 if (v01 < isovalue and v11 >= isovalue) or (v01 >= isovalue and v11 < isovalue):
#                     edges.append([self.interpolate(x0, v01, x1, v11, isovalue), y1])
#                 if (v00 < isovalue and v01 >= isovalue) or (v00 >= isovalue and v01 < isovalue):
#                     edges.append([x0, self.interpolate(y0, v00, y1, v01, isovalue)])
                
#                 if len(edges) == 2:
#                     p1_id = points.InsertNextPoint(edges[0][0], edges[0][1], 0.0)
#                     p2_id = points.InsertNextPoint(edges[1][0], edges[1][1], 0.0)
#                     line = vtk.vtkLine()
#                     line.GetPointIds().SetId(0, p1_id)
#                     line.GetPointIds().SetId(1, p2_id)
#                     lines.InsertNextCell(line)
        
#         poly_data = vtk.vtkPolyData()
#         poly_data.SetPoints(points)
#         poly_data.SetLines(lines)
        
#         writer = vtk.vtkXMLPolyDataWriter()
#         writer.SetFileName(output_filename)
#         writer.SetInputData(poly_data)
#         writer.Write()
        
#         print(f"Isocontour extracted and saved to {output_filename}")



def extract_isocontour_with_vtk(input_filename, output_filename, isovalue):
    # Read VTK Image Data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(input_filename)
    reader.Update()
    
    # Apply VTK's contour filter (Not allowed for the assignment!)
    
    # Write output VTK PolyData (*.vtp)
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_filename)
    contour_filter = three_d_filter()
    writer.SetInputConnection(contour_filter.extract_isocontour_3d(input_filename,output_filename,isovalue))
    writer.Write()
    
    print(f"Isocontour extracted and saved to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input.vti> <output.vtp> <isovalue>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    isovalue = float(sys.argv[3])
    
    extract_isocontour_with_vtk(input_filename, output_filename, isovalue)
