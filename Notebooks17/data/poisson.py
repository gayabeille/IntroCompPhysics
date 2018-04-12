#!/usr/bin/env python

import numpy as np
from scipy.io import netcdf 


Nx = 80
Ny = 80
Nz = 80
px = 20
py = 20
pz = 10

Vp = np.zeros((Nx,Ny,Nz))
V = np.zeros((Nx,Ny,Nz))
rho = np.zeros((Nx,Ny,Nz))

delta = 1/Nx

tol = 1E-5

c = 0
for k in (Nz//2 - pz,):
    for i in range(Nx//2 - px, Nx//2 + px):
        for j in range(Ny//2 - px, Ny//2 + px):
            rho[i,j,k] = 1.0
            c+=1

for k in (Nz//2 + pz,):
    for i in range(Nx//2 - px, Nx//2 + px):
        for j in range(Ny//2 - px, Ny//2 + px):
            rho[i,j,k] = -1.0
rho /= c

dV = 1.0
t = 0
maxiter = 10000
while (dV > tol) and (t < maxiter):
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            for k in range(1, Nz-1):
                V[i,j,k] = (1.0/6.0)*(Vp[i-1,j,k] + Vp[i+1,j,k] + Vp[i,j+1,k] + Vp[i,j-1,k] +
                                      Vp[i,j,k+1] + Vp[i,j,k-1]) + rho[i,j,k]*delta**2/6
    dV = np.sum(np.abs(V - Vp))
    Vp = V.copy()
    t+=1
    if (t % 5 == 0):
        print('Iteration {0}'.format(t))

fp = netcdf.NetCDFFile('potential.nc','w')
fp.xyz_origin = np.zeros(3)
fp.xyz_step = np.array([1.0, 1.0, 1.0])
fp.grid_size = [Nx, Ny, Nz]

# Define the dimensions and set the units
fp.createDimension('x',Nx)
x = fp.createVariable('x', 'd', ('x',))
#x[:] = np.arange(0, Nx, 1.0)
x[:] = np.linspace(0.0,Nx,Nx,endpoint=False)
x.units = 'm'
fp.createDimension('y',Ny)
y = fp.createVariable('y', 'd', ('y',))
y[:] = np.linspace(0.0,Ny,Ny,endpoint=False)
#y[:] = np.arange(0, Ny, 1.0)
y.units = 'm'
fp.createDimension('z',Nz)
z = fp.createVariable('z', 'd', ('z',))
z[:] = np.linspace(0.0,Nz,Nz,endpoint=False)
#z[:] = np.arange(0, Nz, 1.0)
z.units = 'm'

# Store the data array
data_array       = fp.createVariable('Potential', 'd', ('z','y','x'))
data_array.units = 'V'
data_array[:]    = np.transpose(V[:])

fp.close()
