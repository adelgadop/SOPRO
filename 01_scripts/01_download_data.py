#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 15:06:28 2021

@author: adelgado
"""

import download_iem as iem
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import pickle as pkl

#%%  Download the data
iem.main(yi= 2017, mi=8, di= 30, yf = 2018, mf=1, df=2)

# This move to raw folder in Mac Os and Linux
!mv LP*.txt ../02_data/raw/

#%% 

files = [file for file in sorted(glob.glob('../02_data/raw/*.txt'))]

#%% Processing the data
met = {}
stations = ['LPAR', 'LPCS', 'LPOV', 'LPPR', 'LPPT', 'LPST']
stat_df = pd.DataFrame(index = stations)

dates = pd.date_range(start = '2017-08-30 00:00', end = '2018-01-01 23:00',
                      freq = 'H', tz = 'UTC')
dates_df = pd.DataFrame({'date': dates})

for f,n in zip(files, stations):
     met[n] = pd.read_csv(f, comment='#', na_values = 'M')
     
     # format the time 
     met[n]['date'] = pd.to_datetime(met[n]['valid'],
                                            format = '%Y-%m-%d  %H:%M').dt.tz_localize('UTC')
     
     # We complete lon and lat by station
     stat_df.loc[n,'lon'] = met[n].lon.unique()
     stat_df.loc[n,'lat'] = met[n].lat.unique()
     
     # We complete dates
     met[n] = dates_df.merge(met[n], on = 'date', how = 'left')
     
     # We get another variables
     met[n]['tc'] = (met[n]['tmpf'] -32)*5/9
     met[n]['ws'] = met[n]['sknt']*0.514444
     met[n]['wd'] = met[n]['drct']
     met[n].set_index('date', inplace = True)
     
     met[n].drop(['valid', 'station','lon', 'lat',
                  'tmpf', 'dwpf', 'drct', 'sknt', 'alti', 'p01i', 'mslp',
                  'vsby','gust', 'skyc1', 'skyc2',
                   'skyc3', 'skyc4', 'skyl1', 'skyl2', 'skyl3', 
                   'skyl4', 'wxcodes', 'ice_accretion_1hr', 'ice_accretion_3hr', 
                   'ice_accretion_6hr', 'peak_wind_gust', 'peak_wind_drct', 
                   'peak_wind_time', 'feel', 'metar'], axis = 1, 
                  inplace = True)
     
# Export data as pickle     
with open('../02_data/processed/met.pkl', 'wb') as handle:
    pkl.dump(met, handle, protocol=pkl.HIGHEST_PROTOCOL)
    
# Export stations as csv
stat_df.to_csv('stations.csv')
    
#%% Figures --------------------------------------------------------------------

labels = ['%', 'ºC', 'm s$^{-1}$', 'degree']

fig1, ax = plt.subplots(6, figsize = (10,14),sharex = True, 
                       gridspec_kw={'hspace': 0.25})
for i, n in enumerate(stations):
    #for p in ['']
    met[n].plot(y = 'tc', style = 'k.',
                alpha = .4,
                ylabel = 'ºC',
                ax = ax[i], 
                legend = False)
    ax[i].set_title(n, loc = 'left')

fig1.savefig('../03_output/fig/analysis/t2_all.pdf', bbox_inches = 'tight', 
             facecolor = 'w')

for i, n in enumerate(stations):
    
    fig2, ax = plt.subplots(figsize = (10,8))
    axes = met[n].plot(subplots = True, layout = (2,2), sharex = True, 
                title = n, legend = False, ax = ax)
    
    for axs, l in zip(axes.flat, labels):
        axs.set_ylabel(l)
        
    fig2.legend(['Relative \n humidity', '2 m Temp.', 'Wind \nspeed', 'Wind \ndirection'], 
                bbox_to_anchor = (1.05, 0.6))
    fig2.savefig('../03_output/fig/analysis/'+ n +'.pdf', bbox_inches = 'tight', 
                 facecolor = 'w')


