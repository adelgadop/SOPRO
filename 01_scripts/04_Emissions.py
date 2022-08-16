import numpy as np
import xarray as xr
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
#from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim, cartopy_ylim, latlon_coords)
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.patheffects as PathEffects

#%% NOx PM10, PM2.5, CO

pol = {'PM10':200, 'PM2.5':200, 'CO':1000, 'NOx':1000, 'SO2':300, 'NMVOC':1000}
pol_name = {'PM10':'PM$_{10}$', 'PM2.5':'PM$_{2.5}$', 'CO':'CO', 'NOx':'NO$_x$',
            'SO2':'SO$_{2}$', 'NMVOC':'NMVOC'}


#wrfchemi_path = '../../portugal/WRF/WRF-4.2.1/test/em_real/wrfchemi_00z_d01'

# Loading wrfchemis and original htap emission
#wrfchemi = xr.open_dataset(wrfchemi_path)
edgarv5_all = {}
edgarv5 = {}
edgarv5_wrf = {}

for p in pol.keys():
    print(p)
    f = '/Volumes/passport/EDGARv5/edgar_v5_2015_'+p+'_0.1x0.1.nc'
    edgarv5_all[p] = xr.open_dataset(f)
    
    edgarv5[p] = edgarv5_all[p].TOTAL.isel(time=8) # September 2015
    edgar_lon = (edgarv5[p].
                 assign_coords({"lon": (((edgarv5_all[p].lon + 180) % 360) - 180)}).
                 sortby('lon'))
    edgarv5_wrf[p] = edgar_lon.sel(lat=slice( 34.08085,#wrfchemi.XLAT.values.min(), 
                                              46.696537), #wrfchemi.XLAT.values.max()),
                                    lon=slice(-17.50528, #wrfchemi.XLONG.values.min(),
                                              0.50527954)) #wrfchemi.XLONG.values.max()))
    edgarv5_wrf[p] = edgarv5_wrf[p] * 3600 * 10**6 * 10**3 # g km^-2 hr^-1
    
# Make a plot
fig, axes = plt.subplots(3,2, figsize=(10, 9.5), subplot_kw = {'projection': ccrs.PlateCarree()})

for p, ax in zip(pol.keys(), axes.flatten()):
    edgarv5_wrf[p].plot(ax=ax, cmap='inferno_r', y='lat', x='lon', vmax = pol[p],
                        cbar_kwargs={'shrink':0.5, 'label': '$ g\;km^{-2}\; hr^{-1}$', 
                                     'spacing':'proportional'})
    ax.set_title(pol_name[p])

    ax.set_yticks(np.arange(edgarv5_wrf[p].lat.min().round(1), 
                           edgarv5_wrf[p].lat.max().round(1), 2.5),
                  crs=ccrs.PlateCarree())
    ax.set_xticks(np.arange(edgarv5_wrf[p].lon.min().round(1),
                            edgarv5_wrf[p].lon.max().round(1), 3),
                  crs=ccrs.PlateCarree())
    
    ax.set_ylabel('')
    ax.set_xlabel('')
    #ax.coastlines('10m')
    ax.add_feature(cfeature.COASTLINE, color='b', linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, edgecolor ='blue', linestyle='--', alpha=1)
    #gl=ax.gridlines(draw_labels=False, dms=True, x_inline=False, y_inline=False)
    #gl.xlabel_style = {'size':8}
    #gl.ylabel_style = {'size':8}

fig.savefig("03_output/fig/analysis/wrfchemis_map.png", bbox_inches="tight", dpi=300)


#%% Function
def subset_map(edgarv5_wrf, city_coords, city, pol, pol_name, deg, path_name):
    for p in pol.keys():
        ds_pol = edgarv5_wrf[p]

    top = city_coords['lat']+ deg
    bottom = city_coords['lat']- deg
    left = city_coords['lon'] - deg
    right = city_coords['lon'] + deg
    
    mask_lon = (ds_pol.lon >= left) & (ds_pol.lon <= right)
    mask_lat = (ds_pol.lat >= bottom) & (ds_pol.lat <= top)

    ds_sel = ds_pol.where(mask_lon & mask_lat, drop=True)
    
    fig, axes = plt.subplots(len(pol), figsize=(6, 6), subplot_kw = {'projection': ccrs.PlateCarree()})
    plt.subplots_adjust(wspace=0.2, hspace=0.4)
    
    for p, ax in zip(pol.keys(), axes.flatten()):
            levels = list(np.arange(0,pol[p], 100))
            ds_sel.plot(ax = ax, cmap='inferno_r', y='lat', x='lon', vmax = pol[p],
                           cbar_kwargs={'shrink':0.8, 'label': '$ g\;km^{-2}\; hr^{-1}$', 
                                     'spacing':'proportional', 'ticks':levels
                             })
            ax.set_title(pol_name[p])
            ax.set_ylabel('')
            ax.set_xlabel('')
            ax.add_feature(cfeature.COASTLINE, color='b', linewidth=0.5)
            ax.add_feature(cfeature.LAKES, alpha=0.5, color ='b')
            ax.add_feature(cfeature.RIVERS, color='b')
            ax.text(city_coords['lon'], city_coords['lat'], 'o', 
                    color='b', size=8, ha='center', va='center', 
                    transform=ccrs.PlateCarree(),
                    path_effects=[PathEffects.withStroke(linewidth=3, foreground="w", alpha=1)]
                    )
            ax.text(city_coords['lon']-0.35, city_coords['lat']+0.4, city, 
                    color='k', size=12, ha='center', va='center', 
                    transform=ccrs.PlateCarree(),
                    path_effects=[PathEffects.withStroke(linewidth=3, foreground="w", alpha=.5)]
                    )
            ax.set_yticks(np.arange(ds_sel.lat.min().round(1), 
                                   ds_sel.lat.max().round(1), 0.5),
                          crs=ccrs.PlateCarree())
            ax.set_xticks(np.arange(ds_sel.lon.min().round(1),
                                    ds_sel.lon.max().round(1), 0.5),
                          crs=ccrs.PlateCarree())
            
    fig.savefig(path_name+".png", bbox_inches="tight", dpi=300)

#%% Lisboa
pol = {'PM10':1000, 'PM2.5':500}
pol_name = {'PM10':'PM$_{10}$', 'PM2.5':'PM$_{2.5}$'}

path_name = "03_output/fig/analysis/lisboa_map_pm"
subset_map(edgarv5_wrf, 
           {'lon': -9.13, 'lat': 38.716}, 
           'Lisboa', 
           pol, 
           pol_name, 
           1, 
           path_name)

#%% Porto
pol = {'PM10':1000, 'PM2.5':500}
pol_name = {'PM10':'PM$_{10}$', 'PM2.5':'PM$_{2.5}$'}

path_name = "03_output/fig/analysis/porto_map_pm"
subset_map(edgarv5_wrf, 
           {'lon': -8.61, 'lat': 41.15}, 
           'Porto', 
           pol, 
           pol_name, 
           0.5, 
           path_name)






