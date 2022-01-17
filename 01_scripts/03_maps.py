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

print(data['d02']['t2'].shape)

# Reading lon and lat
lon = {'d02': np.load(path + 'lon_d02_201709.npy'),
       'd03': np.load(path + 'lon_d03_201709.npy'),
       'd04': np.load(path + 'lon_d04_201709.npy')
       }

lat = {'d02': np.load(path + 'lat_d02_201709.npy'),
       'd03': np.load(path + 'lat_d03_201709.npy'),
       'd04': np.load(path + 'lat_d04_201709.npy')
       }

# Local times as UTC
horas = pd.date_range("2017-09-01 00:00", periods = 225, freq = 'H')

# Make a Dataset for both months
dset = {'d02': xr.Dataset(), 'd03': xr.Dataset(), 'd04': xr.Dataset}

for k in dset.keys():
    dset[k]['t2'] = (('time', 'lat', 'lon'), data[k]['t2'])
    dset[k]['rh2'] = (('time', 'lat', 'lon'), data[k]['rh2'])
    dset[k]['wind'] = (('time', 'lat', 'lon'), data[k]['wind'])
    dset[k].coords['lat'] = (('lat'), lat[k])
    dset[k].coords['lon'] = (('lon'), lon[k])
    dset[k].coords['time'] = horas
    dset[k].attrs['title'] = k
    print(dset[k])

dset['d02']['t2'][0,:,:].plot()


#%%

