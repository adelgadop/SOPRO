#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 09:13:50 2022

@author: adelgado
"""

# imports 
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from mpl_toolkits.axes_grid1 import make_axes_locatable
from wrf import (getvar, interplevel, to_np, latlon_coords)
import glob

#%% read the file

ncfile = Dataset(sorted(glob.glob('../wrfout_met/wrfout_d02_2017-09-01*')))
# select your timestep (index) and pressure level




#%% xxx

p_level = 500
# get the variables
p = getvar(ncfile, "pressure", timeidx=i)
ua = getvar(ncfile, "ua", units="kt", timeidx=i)
va = getvar(ncfile, "va", units="kt", timeidx=i)
# interpolate ua and va to pressure level
u_500 = interplevel(ua, p, p_level)
v_500 = interplevel(va, p, p_level)
# specify your map boundaries
lat_min = 34
lat_max = 45
lon_min = -13
lon_max = -5
# get the lat, lon grid
lats, lons = latlon_coords(u_500)
# specify your colormap and projection
cmap = plt.get_cmap('Reds')
crs = ccrs.PlateCarree()
# plot
fig = plt.figure(figsize=(10,6))    
ax = fig.add_subplot(111, facecolor='None', projection=crs)
ax.coastlines(resolution='10m', alpha=0.5)
plot_uv500 = ax.pcolormesh(lons, lats, np.sqrt(u_500**2+v_500**2), cmap=cmap)
cbar = fig.colorbar(plot_uv500)
cbar.ax.set_ylabel('Wind speed (kts)')
# some fancy schmancy grid lines
gl = ax.gridlines(crs=crs, draw_labels=True, alpha=0.5)
gl.top_labels = None
gl.right_labels = None
xgrid = np.arange(lon_min-10, lon_max+10, 5.)
ygrid = np.arange(lat_min-10, lat_max+10, 5.)
gl.xlocator = mticker.FixedLocator(xgrid.tolist())
gl.ylocator = mticker.FixedLocator(ygrid.tolist())
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}
# set other plot parameters
plt.xlim((lon_min,lon_max))
plt.ylim((lat_min, lat_max))
plt.title('Wind Speed 500mb')
plt.show()