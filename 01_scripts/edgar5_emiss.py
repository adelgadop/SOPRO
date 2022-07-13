import numpy as np
import xarray as xr
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim, cartopy_ylim, latlon_coords)
import cartopy.crs as ccrs

#CO
wrfchemi_path = '../../portugal/WRF/WRF-4.2.1/test/em_real/wrfchemi_00z_d01'
edgarv5_path ='/scr2/alejandro/WRF/DATA/util/EDGARv5_MOZART/edgar_v5_2015_CO_0.1x0.1.nc' 

# Loading wrfchemis and original htap emission
wrfchemi = xr.open_dataset(wrfchemi_path)
edgarv5  = xr.open_dataset(edgarv5_path)

# Emission names
emiss_names = list(wrfchemi.keys())[3:]
print(emiss_names)

#Reading Edgarv5 - wrfchemi
wrfchemi_co = wrfchemi.E_CO.isel(emissions_zdim_stag=0, Time=0)
wrf_edgar_ds = xr.Dataset({'E_CO': (('y', 'x'), wrfchemi_co.values)},
                         coords = {'lat': (('y', 'x'), wrfchemi.XLAT.values),
                                   'lon': (('y', 'x'), wrfchemi.XLONG.values)})

# Reading Edgarv5
edgar_co = edgarv5.TOTAL.isel(time=8) # September 2015
edgar_co_lon = (edgar_co.
               assign_coords({"lon": (((edgarv5.lon + 180) % 360) - 180)}).
               sortby('lon'))
edgar_co_wrf = edgar_co_lon.sel(lat=slice(wrfchemi.XLAT.values.min(), 
                                        wrfchemi.XLAT.values.max()),
                              lon=slice(wrfchemi.XLONG.values.min(),
                                        wrfchemi.XLONG.values.max()))
edgar_co_wrf = edgar_co_wrf * 3600 * 10**6 * 10**3 / 30

# Make a plot
fig, axes = plt.subplots(2, figsize=(12, 8),subplot_kw = {'projection': ccrs.PlateCarree()})
wrf_edgar_ds.E_CO.plot(ax=axes[0],cmap='inferno_r', y='lat', x='lon', vmax = 100,
                           cbar_kwargs={'shrink':0.5,
                                        'label': '$mol\;km^{-2}\; hr^{-1}$'})
axes[0].set_title("Emissões de CO do wrfchemi_d01")

edgar_co_wrf.plot(ax=axes[1], cmap='inferno_r', y='lat', x='lon', vmax = 100,
                           cbar_kwargs={'shrink':0.5,
                                        'label': '$mol\;km^{-2}\; hr^{-1}$'})
axes[1].set_title("Emissões de CO do EDGARv5")

plt.savefig("../03_output/fig/analysis/wrfchemis_map.png", bbox_inches="tight", dpi=300)
