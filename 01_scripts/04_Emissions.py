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

pol = ['PM10', 'PM2.5', 'CO', 'NOx', 'SO2', 'NMVOC']

wrfchemi_path = '../../portugal/WRF/WRF-4.2.1/test/em_real/wrfchemi_00z_d01'

# Loading wrfchemis and original htap emission
wrfchemi = xr.open_dataset(wrfchemi_path)
edgarv5_all = {}
edgarv5 = {}
edgarv5_wrf = {}

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
fig, axes = plt.subplots(3,2, figsize=(16, 8), subplot_kw = {'projection': ccrs.PlateCarree()})

for p, ax in zip(pol, axes.flat):
    edgarv5_wrf[p].plot(ax=ax, cmap='inferno_r', y='lat', x='lon', vmax = 100,
                        cbar_kwargs={'shrink':0.5, 'label': '$mol\;km^{-2}\; hr^{-1}$'})
    ax.set_title("Emissões de "+p+" do EDGARv5")

    ax.set_yticks(np.arange(edgarv5_wrf[p].lat.min().round(1),
                          edgarv5_wrf[p].lat.max().round(1),
                          1),
                   crs=ccrs.PlateCarree())
    ax.set_xticks(np.arange(edgarv5_wrf[p].lon.min().round(1),
                            edgarv5_wrf[p].lon.max().round(1), 2),
                       crs=ccrs.PlateCarree())
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.coastlines('10m')
    ax.add_feature(cfeature.BORDERS)
    ax.coastlines()

plt.savefig("../03_output/fig/analysis/wrfchemis_map.png", bbox_inches="tight", dpi=300)



