import wrf
import numpy as np
import pandas as pd
from netCDF4 import Dataset
#import matplotlib.pyplot as plt
#%matplotlib inline
import h5py
import glob
import pickle as pkl

print("Reading each wrfout...")
month = input('month (e.g., 09): ')
year = input('year: ')
domain = input('domain (d01, d02, d03, d04): ')
wrfout = [Dataset(i) for i in sorted(glob.glob('../../wrfout_met/wrfout_'+ domain +'_'+year+'-'+month+'-01*'))]

print("Extracting meteorological variables...")
t2 = wrf.getvar(wrfout, 'T2', timeidx=wrf.ALL_TIMES, method='cat')
rh2 = wrf.getvar(wrfout, 'rh2', timeidx=wrf.ALL_TIMES, method='cat')
wind = wrf.getvar(wrfout, 'uvmet10_wspd_wdir', timeidx=wrf.ALL_TIMES, method='cat')
ws = wind.sel(wspd_wdir='wspd')
wd = wind.sel(wspd_wdir='wdir')
psfc = wrf.getvar(wrfout, 'PSFC', timeidx=wrf.ALL_TIMES, method='cat')

lon = t2.XLONG[0,:].values
lat = t2.XLAT[:,0].values

# print("Extracting polutants variables...")
# o3 = wrf.getvar(wrfout, 'o3', timeidx=wrf.ALL_TIMES, method='cat')

# Retrieving values from surface
# o3_sfc  = o3.isel(bottom_top=0)

# print("From ppm to ug/m3...o3, no, no2, tol")
# [ug/m3] = [ppm] * P * M_i / (R * T)
# R = 8.3143 J/K mol
# P in Pa
# T in K
# WRF-Chem gas units in ppmv
# R = 8.3144598 # J/K mol
# o3_u = o3_sfc * psfc * (16 * 3) / (R * t2)

hf = h5py.File('../02_data/processed/'+'map'+domain+'_'+str(year)+str(month)+'.h5','w')
hf.create_dataset('t2', data = t2, compression = 'gzip', compression_opts=9)
hf.create_dataset('rh2', data = rh2, compression = 'gzip', compression_opts=9)
hf.create_dataset('wind', data = wind, compression = 'gzip', compression_opts=9)
hf.create_dataset('psfc', data = psfc, compression = 'gzip', compression_opts=9)
hf.create_dataset('lon', data = lon, compression = 'gzip', compression_opts=9)
hf.create_dataset('lat', data = lat, compression = 'gzip', compression_opts=9)
#hf.create_dataset('o3_u', data = o3_u, compression = 'gzip', compression_opts=9)
hf.close()

print('''
!!!!!!!!!!!!!!!!!
!! Succesfully !!
!!!!!!!!!!!!!!!!!
''')
