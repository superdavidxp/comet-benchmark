
1. Make vtk file one for each frame.

2. Install VTK wih MPI

```
cmake -DModule_vtkCommonCore:BOOL=ON -DModule_vtkCommonDataModel:BOOL=ON -DModule_vtkIOMPIParallel:BOOL=ON .
```