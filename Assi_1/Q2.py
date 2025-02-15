import vtk
import argparse

def load_volume_data(filename):
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader

def create_color_transfer_function():
    ctf = vtk.vtkColorTransferFunction()
    ctf.AddRGBPoint(-4931.54, 0, 1, 1)
    ctf.AddRGBPoint(-2508.95, 0, 0, 1)
    ctf.AddRGBPoint(-1873.9, 0, 0, 0.5)
    ctf.AddRGBPoint(-1027.16, 1, 0, 0)
    ctf.AddRGBPoint(-298.031, 1, 0.4, 0)
    ctf.AddRGBPoint(2594.97, 1, 1, 0)
    return ctf

def create_opacity_transfer_function():
    otf = vtk.vtkPiecewiseFunction()
    otf.AddPoint(-4931.54, 1.0)
    otf.AddPoint(101.815, 0.002)
    otf.AddPoint(2594.97, 0.0)
    return otf

def main(filename, use_phong):
    reader = load_volume_data(filename)
    
    volume_mapper = vtk.vtkSmartVolumeMapper()
    volume_mapper.SetInputConnection(reader.GetOutputPort())
    
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(create_color_transfer_function())
    volume_property.SetScalarOpacity(create_opacity_transfer_function())
    
    if use_phong:
        volume_property.SetShade(True)
        volume_property.SetAmbient(0.5)
        volume_property.SetDiffuse(0.5)
        volume_property.SetSpecular(0.5)
    
    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)
    
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)
    render_window.AddRenderer(renderer)
    
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    
    renderer.AddVolume(volume)
    renderer.AddActor(outline_actor)
    renderer.SetBackground(0, 0, 0)
    
    render_window.Render()
    interactor.Start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_phong", action='store_true', help="Enable Phong shading")
    args = parser.parse_args()
    main("./Isabel_3D.vti", args.use_phong)