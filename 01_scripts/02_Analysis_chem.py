#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 17:03:19 2022

@author: adelgado
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle as pkl
import functions.mod_stats as ms
import glob

#%% Import the observed and modeled data -------------------------------------

month = '09'

# Observations
obs = pd.read_csv('02_data/raw/air_quality/aq_data.csv', sep = ',', decimal='.')
obs['local_date'] = pd.to_datetime(obs['date'], format = '%Y-%m-%d %H:%M').dt.tz_localize('Etc/GMT-1')

obs = obs.melt(id_vars=['local_date', 'code', 'name'], 
               value_vars=['pm10', 'pm2.5', 'no2', 'co', 'o3', 'so2'],
               var_name='pol',
               value_name='Obs')
#%% Simulations using WRF-Chem
# Mechanism = MOZCART
# Model domain = d02
# Horizontal resolution = 9 km
mod = pkl.load(open('02_data/processed/chem_d02_2017_'+month+'.pkl', 'rb'))

stations = pd.read_csv('02_data/raw/air_quality/stations.csv')

station_codes = list(stations.code)

nomes = {}
cidades = {}
for k in station_codes:
    nomes[k] = stations.loc[stations.code == k, 'name'].values[0]
    cidades[k] = stations.loc[stations.code == k, 'city'].values[0]
    mod[k].rename(columns={'pm2':'pm2.5'}, inplace=True)
    
mod_long = pd.DataFrame()

for k in list(stations.code):
    col_index = ['date','tc','rh', 'ws', 'wd','no']
    mod_long = mod_long.append(mod[k], ignore_index=True).drop(columns=col_index)  
    
mod_long = mod_long.melt(id_vars=['local_date', 'code'], 
               value_vars=['pm10', 'pm2.5', 'no2', 'o3', 'co'],
               var_name='pol',
               value_name='Mod')

#%% Merge two type of data

data_2col = mod_long.merge(obs, 
                      on = ['local_date', 'code', 'pol'],
                      how='left')

data_2col['city'] = [cidades[i] for i in data_2col.code]

data = data_2col.melt(id_vars=['local_date', 'code', 'name','city', 'pol'],
                 value_vars=['Obs', 'Mod'],
                 var_name = 'Result',
                 value_name='Conc')

data.set_index('local_date', inplace = True)
data_2col.drop(columns='code', inplace=True)
data_2col.set_index('local_date', inplace = True)

#%% Make Plots: Boxplot
sns.set_style("ticks")
fig, axes = plt.subplots(2,3, figsize = (8,5), sharex=True, gridspec_kw={'wspace':0.5})

labels = {'pm10':'PM$_{10}$', 'pm2.5':'PM$_{2.5}$', 'o3':'O$_3$', 'no2': 'NO$_2$', 'co':'CO'}

for p, ax in zip(labels.keys(), axes.flatten()):
    g = sns.boxplot(data=data.loc[data.pol==p],
                x = 'city',
                y = 'Conc',
                hue = 'Result',
                linewidth=1,
                width=0.5,
               # whis= 5,
                flierprops = dict(marker='+', markerfacecolor = '0.50', markersize = 2),
                ax = ax)
    ax.get_legend().remove()
    ax.set_ylabel("$\mu$g.m$^{-3}$")
    ax.set_title(labels[p], loc='left')
    g.set_xlabel("")
        
    if p == 'co':
        sns.boxplot(data=data.loc[data.pol==p],
                    x = 'city',
                    y = 'Conc',
                    hue = 'Result',
                    linewidth=1,
                    width=0.5,
                   # whis= 5,
                    flierprops = dict(marker='+', markerfacecolor = '0.50', markersize = 2),
                    ax = ax)
        ax.set_ylabel("ppm")
        ax.set_xlabel("Cidade")
        ax.get_legend().remove()
        
    
# add legend
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels[:2], loc='lower right', ncol=1, bbox_to_anchor=(0.85, 0.25))
fig.delaxes(axes[1][2])

# add common ylabel
#fig.text(0.04, 0.5,"Concentração em $\mu$g.m$^{-3}$", va='center', rotation='vertical')
fig.savefig('03_output/fig/analysis/boxplot_pols', bbox_inches = 'tight', facecolor = 'w', dpi = 300)

#%% Time series boxplot

data['day'] = data.index.day

labels = {'pm10':'PM$_{10}$', 'pm2.5':'PM$_{2.5}$', 'o3':'O$_3$', 'no2': 'NO$_2$', 'co':'CO'}
fig, axes = plt.subplots(2,3, figsize = (12,7), sharex=True, gridspec_kw={'wspace':0.25})

for p, ax in zip(labels.keys(), axes.flatten()):
    
   bp1= data.loc[(data.pol == p) & (data.Result == 'Mod'),['day','Conc']].boxplot(by='day', ax = ax, positions= data.day.unique()+0.25, # patch_artist = True,
                                                                                  manage_ticks=True,  widths=0.2, color='g',)

   
   bp2=data.loc[(data.pol == p) & (data.Result == 'Obs'),['day','Conc']].boxplot(by='day', ax = ax, positions= data.day.unique()-0.25, 
                                                                              widths=0.2, color='b', showfliers=True)
   ax.set_xlabel('Dia')
   ax.set_title(labels[p])
   ax.set_ylabel("$\mu$g.m$^{-3}$")
   if p == 'co':
       ax.set_ylabel("ppm")

fig.delaxes(axes[1][2])
fig.suptitle('')

import matplotlib.patches as mpatches

green_patch = mpatches.Patch(color='g', label='WRF-Chem')
blue_patch = mpatches.Patch(color='b', label='Obs')
fig.legend(handles=[green_patch, blue_patch], bbox_to_anchor=(0.85, 0.25),loc='lower right', ncol=1)

#handles, labels = ax.get_legend_handles_labels()

fig.savefig('03_output/fig/analysis/boxplot_day_sep', bbox_inches = 'tight', facecolor = 'w', dpi = 300)

#%% 

#%% FUNCTION ---------------------------------------------------------

def fig_param(dct, p_obs, p_mod, stations, size_fig, ylabel, vmax, step, path):
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
                           figsize = size_fig, gridspec_kw={'hspace':0.3})

    for i, k in enumerate(stations):
        dct[k][['local_date', 
               p_mod]].plot(x='local_date', style = ['g-'], lw = 2.5,
                               alpha = .7, ax = ax[i], legend = False)
        dct[k][['local_date', 
               p_obs]].plot(x='local_date', style = ['k.'], ax = ax[i],
                            legend = False, markersize = 4)
        ax[i].set_yticks(np.arange(0, vmax+1, step))
        
        ax[i].set_title(nomes[k] + " ("+ str(k) +") - " + cidades[k],loc = 'left', fontsize = 8)
        ax[i].set_xlabel('Local date')
        ax[len(stations)-1].legend(['WRF', 'Obs'], ncol = 2, fontsize = 8)

        fig.text(0.04, 0.5, ylabel, 
                 va='center', 
                 rotation='vertical')
        
        # We save the figure
        fig.savefig(path, bbox_inches = 'tight', facecolor = 'w', dpi = 300)


                       
#%% We use the function to print the figure
stations = [1024,3071,3083,3084,3089,3097]
fig_param(dct,'pm10_obs', 'pm10_mod', 
          stations, # code stations with data
          size_fig = (6,8), 
          ylabel = 'PM$_{10}$ [$\mu$g.m$^{-3}$]',
          vmax=50,
          step=10,
          path = '03_output/fig/analysis/pm10_test'+month+'.png')

#%% Prepare data



#%% Relative humidity --------------------------------------------------------

fig_param(dct,'pm2.5', 'pm2', 
          stations, 
          size_fig = (6,8), 
          ylabel = 'PM$_{10}$ [$\mu$g.m$^{-3}$]',
          path = '03_output/fig/analysis/pm2_test'+month+'.png')


#%% Wind speed ---------------------------------------------------------------

fig_param(dct, 'ws_obs', 'ws_mod', 
          stations, 
          size_fig = (6,8), 
          ylabel = 'Wind speed [m s$^{-1}$]',
          path = '03_output/fig/analysis/wind_speed'+month+'.pdf')

# Wind direction ---------------------------------------------------------------

fig_param(dct, 'wd_obs', 'wd_mod', 
          stations, 
          size_fig = (6,8), 
          ylabel = 'Wind direction [degree]',
          path = '03_output/fig/analysis/wind_direction'+month+'.pdf')

# Statistical evaluation -----------------------------------------------------

df = pd.DataFrame()
for k in stations:
    res = ms.met_stats(dct[k], mets = ['tc','rh','ws','wd'])
    res['name'] = k
    df = pd.concat([df, res])

df.dropna(thresh=3,inplace = True)
df.sort_index(inplace = True)

df.round(2).to_csv('03_output/tab/'+month+'_2017_statistics.csv')