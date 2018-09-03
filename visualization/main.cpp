#include "main.h"

int main(int argc, char** argv)
{
    int irank, nrank;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nrank);
    MPI_Comm_rank(MPI_COMM_WORLD, &irank);

    int nx = 64;
    int ny = 32;
    int nz = 16;
    int ix, iy, iz;
    char localname[LEN];

    sprintf(localname, "demo.pvts");

    printf("|    RANK : %d, localname = %s\n", irank, localname);

    // Create a grid
    vtkSmartPointer<vtkStructuredGrid> structuredGrid = vtkSmartPointer<vtkStructuredGrid>::New();

    vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();

    for (iz=0; iz<nz; iz++)
    {
        for (iy=0; iy<ny; iy++)
        {
            for (ix=0; ix<nx; ix++)
            {
                points->InsertNextPoint(ix, iy, iz);
            }
        }
    }

    // Specify the dimensions of the grid
    structuredGrid->SetDimensions(nx,ny,nz);
    structuredGrid->SetPoints(points);

    // Write file
    vtkSmartPointer<vtkXMLPStructuredGridWriter> writer = vtkSmartPointer<vtkXMLPStructuredGridWriter>::New();

    writer->SetFileName(localname);

    writer->SetNumberOfPieces(2);
    writer->SetStartPiece(0);
    writer->SetEndPiece(2-1);

#if VTK_MAJOR_VERSION <= 5
    writer->SetInput(structuredGrid);
#else
    writer->SetInputData(structuredGrid);
#endif

//    writer->Write();
    writer->Update();

    MPI_Barrier(MPI_COMM_WORLD);

    MPI_Finalize();

    return 0;
}