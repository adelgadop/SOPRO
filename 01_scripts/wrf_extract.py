import wrf
import numpy as np
import pandas as pd
from netCDF4 import Dataset
#import matplotlib.pyplot as plt
#%matplotlib inline
import glob
import pickle as pkl

print("Reading each wrfout...")
month = input('month (e.g., 09): ')
year = input('year: ')
domain = input('domain (d01, d02, d03, d04): ')
wrfout = [Dataset(i) for i in sorted(glob.glob('../../portugal/wrfout/wrfout_'+ domain +'_'+year+'-'+month+'-*'))]

print("Extracting meteorological variables...")
t2 = wrf.getvar(wrfout, 'T2', timeidx=wrf.ALL_TIMES, method='cat')
rh2 = wrf.getvar(wrfout, 'rh2', timeidx=wrf.ALL_TIMES, method='cat')
wind = wrf.getvar(wrfout, 'uvmet10_wspd_wdir', timeidx=wrf.ALL_TIMES, method='cat')
ws = wind.sel(wspd_wdir='wspd')
wd = wind.sel(wspd_wdir='wdir')
psfc = wrf.getvar(wrfout, 'PSFC', timeidx=wrf.ALL_TIMES, method='cat')

#print("Extracting polutants variables...")
o3 = wrf.getvar(wrfout, 'o3', timeidx=wrf.ALL_TIMES, method='cat')
no = wrf.getvar(wrfout, 'no', timeidx=wrf.ALL_TIMES, method='cat')
no2 = wrf.getvar(wrfout, 'no2', timeidx=wrf.ALL_TIMES, method='cat')
co = wrf.getvar(wrfout, 'co', timeidx=wrf.ALL_TIMES, method='cat')
#tol = wrf.getvar(wrfout, 'tol',timeidx=wrf.ALL_TIMES, method='cat')
pm2 = wrf.getvar(wrfout, 'PM2_5_DRY',timeidx=wrf.ALL_TIMES, method='cat')
pm10 = wrf.getvar(wrfout, 'PM10',timeidx=wrf.ALL_TIMES, method='cat')

# Retrieving values from surface
o3_sfc  = o3.isel(bottom_top=0)
co_sfc  = co.isel(bottom_top=0)
no_sfc  = no.isel(bottom_top=0)
no2_sfc = no2.isel(bottom_top=0)
#tol_sfc = tol.isel(bottom_top=0)
pm2_sfc = pm2.isel(bottom_top=0)
pm10_sfc = pm10.isel(bottom_top=0)

print("From ppm to ug/m3...o3, no, no2, tol")
# [ug/m3] = [ppm] * P * M_i / (R * T)
# R = 8.3143 J/K mol
# P in Pa
# T in K
# WRF-Chem gas units in ppmv
R = 8.3144598 # J/K mol
o3_u = o3_sfc * psfc * (16 * 3) / (R * t2)
no_u = no_sfc * psfc * (14 + 16) / (R * t2)
no2_u = no2_sfc * psfc * (14 + 2*16) / (R * t2)
#tol_u = tol_sfc * psfc * 92.14 / (R * t2)

print("Reading file with station location points")
stations = pd.read_csv('./stations.csv')
print(stations)

# Locating stations in west_east (x) and north_south (y) coordinates
stations_xy = wrf.ll_to_xy(wrfout,
                           latitude = stations.lat,
                           longitude= stations.lon)
stations['x'] = stations_xy[0]
stations['y'] = stations_xy[1]

# Filter stations inside WRF domain
filter_dom = (stations.x > 0) & (stations.x < t2.shape[2]) & (stations.y > 0) & \
 (stations.y < t2.shape[1])
port_dom = stations[filter_dom]

# Function to retrieve variables from WRF-Chem
def station_from_wrf(i, to_local=True):
    wrf_est = pd.DataFrame({
    'date': t2.Time.values,
    'tc':  t2.sel(south_north = port_dom.y.values[i],
       west_east= port_dom.x.values[i]).values - 273.15,
    'rh': rh2.sel(south_north=port_dom.y.values[i],
       west_east= port_dom.x.values[i]).values,
    'ws': ws.sel(south_north= port_dom.y.values[i],
       west_east= port_dom.x.values[i]).values,
    'wd': wd.sel(south_north= port_dom.y.values[i],
       west_east= port_dom.x.values[i]).values,
    'o3': o3_u.sel(south_north= port_dom.y.values[i],
       west_east=port_dom.x.values[i]).values,
    'no': no_u.sel(south_north= port_dom.y.values[i],
       west_east=port_dom.x.values[i]).values,
    'no2': no2_u.sel(south_north= port_dom.y.values[i],
       west_east=port_dom.x.values[i]).values,
    'co': co_sfc.sel(south_north= port_dom.y.values[i],
       west_east=port_dom.x.values[i]).values,
    'pm2.5': pm2_sfc.sel(south_north= port_dom.y.values[i],
       west_east=port_dom.x.values[i]).values,
    'pm10': pm10_sfc.sel(south_north= port_dom.y.values[i],
       west_east=port_dom.x.values[i]).values,    
#'tol': tol_u.sel(south_north=cetesb_dom.y.values[i],
    #   west_east=cetesb_dom.x.values[i]).values,
    'code': port_dom.code.values[i]})
    if to_local:
        wrf_est['local_date'] = wrf_est['date'].dt.tz_localize('UTC').dt.tz_convert('Europe/Lisbon')
    return(wrf_est)

print("Extracting data and saving it in a dictionary")
wrf_port = {}

for i in range(0,len(port_dom)):
    wrf_port[port_dom.code.iloc[i]] = station_from_wrf(i)

print('Exporting to pickle ')
pkl.dump(wrf_port, open('../02_data/processed/' + input('scenario: ') + '_' + domain +'_'+year+'_'+month+'.pkl','wb'))

#name = '_FIN_d02.csv' #input('_name.csv: ')
#def cetesb_write_wrf(df):
#    file_name = str(df.code[0]) + name
#    df.to_csv(file_name, index=False)

#for k, v in wrf_cetesb.items():
#    cetesb_write_wrf(v)

print('''
!!!!!!!!!!!!!!!!!
!! Succesfully !!
!!!!!!!!!!!!!!!!!
''')
