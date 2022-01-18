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
from matplotlib import ticker
import matplotlib as mpl
import pickle as pkl
import xarray as xr
import h5py
from netCDF4 import Dataset
import glob
# import wrf
import pytz
#from mpl_toolkits.basemap import Basemap
import cartopy
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
            't2'  : d02.get('t2')[:,:,:],
            'rh2' : d02.get('rh2')[::,:,:],
            'ws': d02.get('ws')[:,:,:],
            'wd': d02.get('ws')[:,:,:]
            },
        "d03" : {
            't2'  : d03.get('t2')[:,:,:],
            'rh2' : d03.get('rh2')[:,:,:],
            'ws': d03.get('ws')[:,:,:],
            'wd': d03.get('ws')[:,:,:]
            },
        "d04" : {
            't2'  : d04.get('t2')[:,:,:],
            'rh2' : d04.get('rh2')[:,:,:],
            'ws': d04.get('ws')[:,:,:],
            'wd': d04.get('ws')[:,:,:]
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
horas = pd.date_range("2017-09-01 00:00", periods = 24, freq = 'H')

# Make a Dataset for both months
dset = {'d02': xr.Dataset(), 'd03': xr.Dataset(), 'd04': xr.Dataset()}

#%%


for k in dset.keys():
    dset[k]['t2']  = (('time', 'lat', 'lon'), data[k]['t2'])
    dset[k]['rh2'] = (('time', 'lat', 'lon'), data[k]['rh2'])
    dset[k]['ws']  = (('time', 'lat', 'lon'), data[k]['ws'])
    dset[k]['wd']  = (('time', 'lat', 'lon'), data[k]['wd'])
    dset[k].coords['lat'] = (('lat'), lat[k])
    dset[k].coords['lon'] = (('lon'), lon[k])
    dset[k].coords['time'] = horas
    dset[k].attrs['title'] = k
    print(dset[k])

dset['d02']['t2'][0,:,:].plot()


#%% Temperature

extension = {'d02': [-15, -4, 33.0, 45.0],
             'd03': [-10, -7, 40.5, 42.5],
             'd04': [-10, -8, 37.9, 39.3]
    }

for k in dset.keys():
    
    air = dset[k].t2.isel(time= [6, 12, 18, 23]) - 273.15
    # This is the map projection we want to plot *onto*
    map_proj = ccrs.LambertConformal(central_longitude=-8.78, central_latitude=39.99)

    p = air.plot(
        transform=ccrs.PlateCarree(),  # the data's projection
        col="time",
        col_wrap=2,  # multiplot settings
        aspect= 1.25,  # for a sensible figsize
        subplot_kws={"projection": map_proj},
        cbar_kwargs={"label": "Temperature at 2 m (ºC)"}
        )  # the plot's projection


    # We have to set the map's options on all axes
    for ax in p.axes.flat:
        ax.add_feature(cartopy.feature.BORDERS)
        ax.coastlines()
        ax.set_extent(extension[k])
        #gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, x_inline=False, 
        #                  y_inline=False, linewidth=0.33, color='k',alpha=0.5)
        #gl.right_labels = gl.top_labels = False
        #gl.ylocator = ticker.FixedLocator([36, 38, 40, 42, 44])
        #gl.xlocator = ticker.FixedLocator([-12, -10, -8, -6])
    
    plt.savefig("03_output/fig/analysis/map_temp_"+k+".pdf", bbox_inches='tight', facecolor='w')
    
    
#%% Relative humidity

extension = {'d02': [-15, -4, 33.0, 45.0],
             'd03': [-10, -7, 40.5, 42.5],
             'd04': [-10, -8, 37.9, 39.3]
    }

for k in dset.keys():
    
    air = dset[k].rh2.isel(time= [6, 12, 18, 23])
    # This is the map projection we want to plot *onto*
    map_proj = ccrs.LambertConformal(central_longitude=-8.78, central_latitude=39.99)

    p = air.plot(
        transform=ccrs.PlateCarree(),  # the data's projection
        col="time",
        col_wrap=2,  # multiplot settings
        aspect= 1.25,  # for a sensible figsize
        subplot_kws={"projection": map_proj},
        cbar_kwargs={"label": "Relative humidity at 2 m (%)"}
        )  # the plot's projection


    # We have to set the map's options on all axes
    for ax in p.axes.flat:
        ax.add_feature(cartopy.feature.BORDERS)
        ax.coastlines()
        ax.set_extent(extension[k])
        #gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, x_inline=False, 
        #                  y_inline=False, linewidth=0.33, color='k',alpha=0.5)
        #gl.right_labels = gl.top_labels = False
        #gl.ylocator = ticker.FixedLocator([36, 38, 40, 42, 44])
        #gl.xlocator = ticker.FixedLocator([-12, -10, -8, -6])
    
    plt.savefig("03_output/fig/analysis/map_rh2_"+k+".pdf", bbox_inches='tight', facecolor='w')

#%% Wind speed

extension = {'d02': [-15, -4, 33.0, 45.0],
             'd03': [-10, -7, 40.5, 42.5],
             'd04': [-10, -8, 37.9, 39.3]
    }

for k in dset.keys():
    
    air = dset[k].ws.isel(time= [6, 12, 18, 23])
    # This is the map projection we want to plot *onto*
    map_proj = ccrs.LambertConformal(central_longitude=-8.78, central_latitude=39.99)

    p = air.plot(
        transform=ccrs.PlateCarree(),  # the data's projection
        col="time",
        col_wrap=2,  # multiplot settings
        aspect= 1.25,  # for a sensible figsize
        subplot_kws={"projection": map_proj},
        cbar_kwargs={"label": "Wind speed at 10 m (m/s)"}
        )  # the plot's projection


    # We have to set the map's options on all axes
    for ax in p.axes.flat:
        ax.add_feature(cartopy.feature.BORDERS)
        ax.coastlines()
        ax.set_extent(extension[k])
        #gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, x_inline=False, 
        #                  y_inline=False, linewidth=0.33, color='k',alpha=0.5)
        #gl.right_labels = gl.top_labels = False
        #gl.ylocator = ticker.FixedLocator([36, 38, 40, 42, 44])
        #gl.xlocator = ticker.FixedLocator([-12, -10, -8, -6])
    
    plt.savefig("03_output/fig/analysis/map_ws_"+k+".pdf", bbox_inches='tight', facecolor='w')






