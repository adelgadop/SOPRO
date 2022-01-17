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

#%%
data = {
        "d02" : {
            't2'  : d02.get('t2'),
            'rh2' : d02.get('rh2'),
            'wind': d02.get('wind')
            },
        "d03" : {
            't2'  : d03.get('t2'),
            'rh2' : d03.get('rh2'),
            'wind': d03.get('wind')
            },
        "d04" : {
            't2'  : d04.get('t2'),
            'rh2' : d04.get('rh2'),
            'wind': d04.get('wind')
            }
        }

for f in [d02, d03, d04]:
    f.close()
    
print(data['d02']['t2'].shape)