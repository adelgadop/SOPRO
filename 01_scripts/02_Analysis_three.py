#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 11:32:53 2021

@author: adelgado
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import functions.mod_stats as ms
import glob

#%% Import the observed and modeled data -------------------------------------

month = '09'

# Observations
obs = pkl.load(open('02_data/processed/met.pkl', 'rb'))
for k in obs.keys():
    obs[k].reset_index(inplace = True)
    obs[k]['local_date'] = obs[k]['date'].dt.tz_convert('Europe/Lisbon')

# Simulations using WRF
mod_d02 = pkl.load(open('02_data/processed/erai_d02_2017_'+month+'.pkl', 'rb'))
mod_d03 = pkl.load(open('02_data/processed/erai_d03_2017_'+month+'.pkl', 'rb'))
erai = {**mod_d02, **mod_d03}

mod_d02 = pkl.load(open('02_data/processed/curr_d02_2017_'+month+'.pkl', 'rb'))
mod_d03 = pkl.load(open('02_data/processed/curr_d03_2017_'+month+'.pkl', 'rb'))
mod = {**mod_d02, **mod_d03}

stations = list(pd.read_csv('01_scripts/stations.csv').code)

#%% Merge three type of data
dct = {}
for k in stations:
    dct[k] = erai[k].merge(mod[k], 
                         on = 'local_date', 
                         how = 'left', 
                         suffixes = ('_erai', 
                                     '_mod')).merge(obs[k],
                                                    on = 'local_date',
                                                    how = 'left').drop(['date_erai',
                                                                        'date_mod',
                                                                        'code_erai',
                                                                        'code_mod'],
                                                                        axis = 1) 

    
    # Only in case if you forgot to eliminate two first days of wrfout_ files              
    dct[k] = dct[k].iloc[48:,:] # spin-up of two days


#%% Temperature (tc) ---------------------------------------------------------

def fig_param(dct, p_obs, p_mod1, p_mod2, stations, size_fig, ylabel, path):
    """
    
    
    Parameter
    ---------
    dct: Dictionary
        Stations name with pandas DataFrame
    
    p_obs:
        
    p_mod:
        
    stations:
    """
    fig, ax = plt.subplots(len(stations), sharex = True, sharey = True,
                           figsize = size_fig, gridspec_kw={'hspace':0.35})

    for i, k in enumerate(stations):
        
        # NCEP GDAS
        dct[k][['local_date', p_mod1]].plot(x='local_date', 
                                            style = ['g-'], 
                                            lw = 2.5,
                                            alpha = .7, 
                                            ax = ax[i], 
                                            legend = False)
                            
        # ERA Interim
        dct[k][['local_date', p_mod2]].plot(x='local_date', 
                                            style = ['b-'], 
                                            lw = 2.5,
                                            alpha = .7, 
                                            ax = ax[i], 
                                            legend = False)
        
        dct[k][['local_date', 
               p_obs]].plot(x='local_date', style = ['k.'], ax = ax[i],
                               legend = False, markersize = 4)
                               
        ax[i].set_title(k, loc = 'left', fontsize = 8)
        ax[i].set_xlabel('Local date')
        ax[len(stations)-1].legend(['WRF (NCEP 0.25x0.75)', 'WRF (ERAI 0.75x0.75)', 'Obs'], ncol = 3, fontsize = 6)

        fig.text(0.03, 0.5, ylabel, 
                 va='center', 
                 rotation='vertical')
        
        # We save the figure
        fig.savefig(path, bbox_inches = 'tight', facecolor = 'w')

                       
# We use the function to print the figure
fig_param(dct,'tc', 'tc_mod', 'tc_erai',
          stations, 
          size_fig = (5,10), 
          ylabel = '2-m temperature [ºC]',
          path = '03_output/fig/analysis/temp'+month+'.pdf')

#%% Relative humidity --------------------------------------------------------

fig_param(dct,'rh', 'rh_mod', 'rh_erai',
          stations, 
          size_fig = (5,10), 
          ylabel = 'Relative humidity [%]',
          path = '03_output/fig/analysis/rel_hum'+month+'.pdf')


# Wind speed ---------------------------------------------------------------

fig_param(dct, 'ws', 'ws_mod', 'ws_erai',
          stations, 
          size_fig = (5,10), 
          ylabel = 'Wind speed [m s$^{-1}$]',
          path = '03_output/fig/analysis/wind_speed'+month+'.pdf')

# Wind direction ---------------------------------------------------------------

fig_param(dct, 'wd', 'wd_mod', 'wd_erai', 
          stations, 
          size_fig = (5,10), 
          ylabel = 'Wind direction [degree]',
          path = '03_output/fig/analysis/wind_direction'+month+'.pdf')

#%% Statistical evaluation -----------------------------------------------------
month = '09'

# Observations
obs = pkl.load(open('02_data/processed/met.pkl', 'rb'))
for k in obs.keys():
    obs[k].reset_index(inplace = True)
    obs[k]['local_date'] = obs[k]['date'].dt.tz_convert('Europe/Lisbon')

# Simulations using WRF from ERA Interim as IC/BC
mod_d02 = pkl.load(open('02_data/processed/erai_d02_2017_'+month+'.pkl', 'rb'))
mod_d03 = pkl.load(open('02_data/processed/erai_d03_2017_'+month+'.pkl', 'rb'))
mod = {**mod_d02, **mod_d03}

stations = list(pd.read_csv('01_scripts/stations.csv').code)

# Merge two type of data
dct = {}
for k in stations:
    dct[k] = mod[k].merge(obs[k], 
                         on = 'local_date', 
                         how = 'left', 
                         suffixes = ('_mod', '_obs')).drop(['date_mod', 
                                                            'date_obs'],
                                                            axis = 1)
    
    # Only in case if you forgot to eliminate two first days of wrfout_ files              
    dct[k] = dct[k].iloc[48:,:] # spin-up of two days
    
    
df = pd.DataFrame()
for k in stations:
    res = ms.met_stats(dct[k], mets = ['tc','rh','ws','wd'])
    res['name'] = k
    df = pd.concat([df, res])

df.dropna(thresh=3,inplace = True)
df.sort_index(inplace = True)

df.round(2).to_csv('03_output/tab/'+month+'_2017_statistics.csv')