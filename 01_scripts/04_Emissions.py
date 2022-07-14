import numpy as np
import xarray as xr
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
#from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim, cartopy_ylim, latlon_coords)
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

# NOx PM10, PM2.5, CO

pol = ['NOx', 'PM10', 'PM2.5', 'CO', 'NMVOC']

wrfchemi_path = '../../portugal/WRF/WRF-4.2.1/test/em_real/wrfchemi_00z_d01'

edgarv5_path = []
for p in pol:
    edgarv5_path.append('/scr2/alejandro/WRF/DATA/util/EDGARv5_MOZART/edgar_v5_2015_'+p+'_0.1x0.1.nc')

#%%
# Loading wrfchemis and original htap emission
wrfchemi = xr.open_dataset(wrfchemi_path)
edgarv5_all = xr.Dataset()
edgarv5 = xr.Dataset()
edgarv5_wrf = xr.Dataset()

for p in pol:
    f = '/scr2/alejandro/WRF/DATA/util/EDGARv5_MOZART/edgar_v5_2015_'+p+'_0.1x0.1.nc'
    edgarv5_all[p] = xr.open_dataset(f)
    edgarv5[p] = edgarv5_all[p].TOTAL.isel(time=8) # September 2015
    edgar_lon = (edgarv5[p].
                 assign_coords({"lon": (((edgarv5_all[p].lon + 180) % 360) - 180)}).
                 sortby('lon'))
    edgarv5_wrf[p] = edgarv5[p].sel(lat=slice(wrfchemi.XLAT.values.min(), 
                                              wrfchemi.XLAT.values.max()),
                                    lon=slice(wrfchemi.XLONG.values.min(),
                                              wrfchemi.XLONG.values.max()))
    edgarv5_wrf[p] = edgarv5_wrf[p] * 3600 * 10**6 * 10**3 / 30
    
    
# Make a plot




