from paraview.simple import * 
sphere = Sphere()
rep = Show()
Render()
ColorBy(rep, ("POINTS", "vtkProcessId"))
rep.RescaleTransferFunctionToDataRange(True) 
Render()
WriteImage("parasphere.png")
