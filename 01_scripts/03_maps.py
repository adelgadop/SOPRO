#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 10:13:30 2022

@author: adelgado
"""

# Import necessary libraries
import pandas as pd
import os, fnmatch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
import pickle as pkl
import xarray as xr
import h5py
from netCDF4 import Dataset
import glob
# import wrf
import pytz
#from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from mpl_toolkits.axes_grid1 import AxesGrid
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

#%% MDA8 diferences for September and October --------------------------------
path = '../data/wrfout/'
wrfout = [Dataset(i) for i in sorted(glob.glob(path+'wrfout_d02*'))]

t2 = wrf.getvar(wrfout, 'T2', timeidx=wrf.ALL_TIMES, method='cat')
rh2 = wrf.getvar(wrfout, 'rh2', timeidx=wrf.ALL_TIMES, method='cat')
wind = wrf.getvar(wrfout, 'uvmet10_wspd_wdir', timeidx=wrf.ALL_TIMES, method='cat')
ws = wind.sel(wspd_wdir='wspd')
wd = wind.sel(wspd_wdir='wdir')
psfc = wrf.getvar(wrfout, 'PSFC', timeidx=wrf.ALL_TIMES, method='cat')

o3 = wrf.getvar(wrfout, 'o3', timeidx=wrf.ALL_TIMES, method='cat')
o3_sfc  = o3.isel(bottom_top=0)
R = 8.3144598 # J/K mol
o3_u = o3_sfc * psfc * (16 * 3) / (R * t2)
o3_u[0,:,:].plot()

lon = t2.XLONG[0,:].values
lat = t2.XLAT[:,0].values
print(lon, lat)

#%% Import processed data

path = '02_data/processed/'
d02 = h5py.File(path + 'mapd02_201709.h5', 'r')
d03 = h5py.File(path + 'mapd03_201709.h5', 'r')
d04 = h5py.File(path + 'mapd04_201709.h5', 'r')

data = {
        "d02" : {
            't2'  : d02.get('t2')[3:,:,:],
            'rh2' : d02.get('rh2')[3:,:,:],
            'wind': d02.get('wind')[3:,:,:],
            'lon' : d02.get('lon')
            },
        "d03" : {
            't2'  : d03.get('t2')[3:,:,:],
            'rh2' : d03.get('rh2')[3:,:,:],
            'wind': d03.get('wind')[3:,:,:]
            },
        "d04" : {
            't2'  : d04.get('t2')[3:,:,:],
            'rh2' : d04.get('rh2')[3:,:,:],
            'wind': d04.get('wind')[3:,:,:]
            }
        }

for f in [d02, d03, d04]:
    f.close()
    
#%%

print(data['d02']['t2'].shape)