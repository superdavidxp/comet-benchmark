import numpy as np

nx = 64
ny = 32
nz = 16

tstep = 10

array = np.zeros(nx*ny*nz*tstep, dtype=np.float32)

value_init = np.float32(1500.0)

for it in range(tstep):

    for iz in range(nz):

        value = np.float32(value_init + iz * 100.0 + it * 10.0)

        print('iz = {}, value = {}'.format(iz, value))

        for iy in range(ny):
            for ix in range(nx):

                idx = iz * ny * nx + iy * nx + ix

                # print('iz = {}, iy = {}, ix = {}, value = {}'.format(iz, iy, ix, value))

                array[idx] = value

fid = open('demo3d.raw', 'wb')
array.tofile(fid)
fid.close()
