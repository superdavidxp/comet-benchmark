cmake_minimum_required(VERSION 3.2)
project(pvtk)

set(CMAKE_CXX_STANDARD 14)

find_package(MPI REQUIRED)

find_package(VTK 8.0 REQUIRED NO_MODULE)
if (VTK_FOUND)
    message("")
    message("|    VTK_FOUND")
    message("|    VTK_INCLUDE_DIRS = " ${VTK_INCLUDE_DIRS})
    message("|    VTK_LIBRARIES = " ${VTK_LIBRARIES})
endif(VTK_FOUND)

include(${VTK_USE_FILE})
include_directories(${MPI_INCLUDE_PATH} ${VTK_INCLUDE_DIRS})
link_directories(${MPI_LIBRARY} ${VTK_LIBRARIES})

add_executable(pvtk main.cpp main.h)
target_link_libraries(pvtk ${MPI_LIBRARIES} ${VTK_LIBRARIES})
