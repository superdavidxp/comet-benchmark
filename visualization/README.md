
1. Make vtk file one for each frame.

2. Install VTK wih MPI

```
cmake -DModule_vtkCommonCore:BOOL=ON -DModule_vtkCommonDataModel:BOOL=ON -DModule_vtkIOMPIParallel:BOOL=ON .
```

3. How to write time series

3.1. convert your vtk files to xml paraview files (e.g. VTU or VTM files) : open your vtk files with paraview, and write the new files with File > Save Data. You needd to check the "write all timesteps as file-series".

3.2. create a ParaView Data File (.pvd). In this file we can specify the timestep value for each file. Here is an example:
```
<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">
        <Collection>
            <DataSet timestep="0"         file='file_0.vtu'/>
            <DataSet timestep="0.022608"  file='file_1.vtu'/>
            <DataSet timestep="0.73781"   file='file_2.vtu'/>
        </Collection>
    </VTKFile>
```
3.3. load the .pvd file in paraview. we can now use the Annotate Time filter with the good timestep values.
