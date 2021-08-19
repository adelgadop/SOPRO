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

#%% Import the observed and modeled data -------------------------------------

# Observations
obs = pkl.load(open('02_data/processed/met.pkl', 'rb'))
for k in obs.keys():
    obs[k].reset_index(inplace = True)
    obs[k]['local_date'] = obs[k]['date'].dt.tz_convert('Europe/Lisbon')


# Simulations using WRF
mod_d02 = pkl.load(open('02_data/processed/curr_d02_2017_09.pkl', 'rb'))
mod_d03 = pkl.load(open('02_data/processed/curr_d03_2017_09.pkl', 'rb'))
mod = {**mod_d02, **mod_d03}

stations = list(pd.read_csv('01_scripts/stations.csv').code)

# Merge two type of data
df = {}
for k in stations:
    df[k] = mod[k].merge(obs[k], 
                         on = 'local_date', 
                         how = 'left', 
                         suffixes = ('_mod', '_obs')).drop(['date_mod', 
                                                            'date_obs'],
                                                            axis = 1)
    df[k] = df[k].iloc[48:,:] # spin-up of two days


#%% Temperature (tc) ---------------------------------------------------------

def fig_param(p_obs, p_mod, stations, size_fig, ylabel, path):
    """
    Parameter
    ---------
    p_obs:
        
    p_mod:
        
    stations:
    """
    fig, ax = plt.subplots(len(stations), sharex = True, sharey = True,
                           figsize = size_fig, gridspec_kw={'hspace':0.3})

    for i, k in enumerate(stations):
        df[k][['local_date', 
               p_mod]].plot(x='local_date', style = ['g-'], lw = 4,
                               alpha = .7, ax = ax[i], legend = False)
        df[k][['local_date', 
               p_obs]].plot(x='local_date', style = ['k.'], ax = ax[i],
                               legend = False)
                               
        ax[i].set_title(k, loc = 'left', fontsize = 8)
        ax[i].set_xlabel('Local date')
        ax[len(stations)-1].legend(['WRF', 'Obs'], ncol = 2, fontsize = 8)

        fig.text(0.04, 0.5, ylabel, 
                 va='center', 
                 rotation='vertical')
        
        # We save the figure
        fig.savefig(path, bbox_inches = 'tight', facecolor = 'w')

                       
# We use the function to print the figure
fig_param('tc_obs', 'tc_mod', 
          stations, 
          size_fig = (6,8), 
          ylabel = '2-m temperature [ºC]',
          path = '03_output/fig/analysis/temp.pdf')

#%% Relative humidity --------------------------------------------------------
# obs = relh
# mod = rh

fig_param('relh', 'rh', 
          stations, 
          size_fig = (6,8), 
          ylabel = 'Relative humidity [%]',
          path = '03_output/fig/analysis/rel_hum.pdf')


#%% Wind speed ---------------------------------------------------------------

fig_param('ws_obs', 'ws_mod', 
          stations, 
          size_fig = (6,8), 
          ylabel = 'Wind speed [m s$^{-1}$]',
          path = '03_output/fig/analysis/wind_speed.pdf')

#%% Wind direction ---------------------------------------------------------------

fig_param('wd_obs', 'wd_mod', 
          stations, 
          size_fig = (6,8), 
          ylabel = 'Wind direction [degree]',
          path = '03_output/fig/analysis/wind_direction.pdf')
                                                            
                                    