#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:10:33 2022

@author: adelgado
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pytz
import seaborn as sns
import matplotlib.ticker as plticker

#print(pytz.all_timezones)

air = pd.read_csv('02_data/raw/air_quality/aq_data.csv', sep = ',', decimal='.')
air['date'] = pd.to_datetime(air['date'], format = '%Y-%m-%d %H:%M').dt.tz_localize('Etc/GMT-1')

#%% Figures particulate matter

df_set = air.loc[(air.date >= "2017-09-01") & (air.date <= "2017-09-03"), :]
names = list(air.name.unique())
porto = names[0:2]
lisbon = ['Olivais', 'Laranjeiro']
lisbon2 = names[2:][4:]
pols = list(air.columns[-6:])
ylabel = '$\mu$gm$^{-3}$'
ylabel_co = 'mg.m$^{-3}$'

    
fig, ax = plt.subplots(2, figsize = (6, 5), sharex = True, sharey = True)
for i, n in enumerate(lisbon):
    df_set.loc[df_set.name == n, :].plot(x = 'date', y=['pm10', 'pm2.5'], ax = ax[i], legend = False)
    ax[i].set_title(n, loc = 'left', fontsize = 8)
    ax[-len(lisbon)].legend(['PM$_{10}$', 'PM$_{2.5}$'])
    fig.text(0.07, 0.5, ylabel, va = 'center', rotation='vertical')
fig.savefig('03_output/fig/analysis/obs_pm_lisbon_set.png', bbox_inches='tight', facecolor='w', dpi=300)



#%% Figures
names = list(air.name.unique())
porto = names[0:2]
lisbon = names[2:][:4]
lisbon2 = names[2:][4:]
pols = list(air.columns[-6:])
ylabel = '$\mu$gm$^{-3}$'
ylabel_co = 'mg.m$^{-3}$'

fig, ax = plt.subplots(len(porto), figsize = (12, 6), sharex = True, sharey = True)
for i, n in enumerate(porto):
    air.loc[air.name == n, :].plot(x = 'date', y=['pm10', 'pm2.5'], ax = ax[i], legend = False)
    ax[i].set_title(n, loc = 'left', fontsize = 8)
    
    ax[len(porto)-1].legend(['PM$_{10}$', 'PM$_{2.5}$'])
    fig.text(0.07, 0.5, ylabel, va = 'center', rotation='vertical')

fig.savefig('03_output/fig/analysis/obs_pm_porto.png', bbox_inches='tight', facecolor='w', dpi=300)
    
#%%

fig, ax = plt.subplots(len(lisbon), figsize = (12, 8), sharex = True, sharey = True)
for i, n in enumerate(lisbon):
    air.loc[air.name == n, :].plot(x = 'date', y=['pm10', 'pm2.5'], ax = ax[i], legend = False)
    ax[i].set_title(n, loc = 'left', fontsize = 8)
    ax[-len(lisbon)].legend(['PM$_{10}$', 'PM$_{2.5}$'])
    fig.text(0.07, 0.5, ylabel, va = 'center', rotation='vertical')
fig.savefig('03_output/fig/analysis/obs_pm_lisbon.png', bbox_inches='tight', facecolor='w', dpi=300)

#%%

fig, ax = plt.subplots(len(lisbon2), figsize = (12, 8), sharex = True, sharey = True)
for i, n in enumerate(lisbon2):
    air.loc[air.name == n, :].plot(x = 'date', y=['pm10', 'pm2.5'], ax = ax[i], legend = False)
    ax[i].set_title(n, loc = 'left', fontsize = 8)
    ax[-len(lisbon)].legend(['PM$_{10}$', 'PM$_{2.5}$'])
    fig.text(0.07, 0.5, ylabel, va = 'center', rotation='vertical')
fig.savefig('03_output/fig/analysis/obs_pm_lisbon2.png', bbox_inches='tight', facecolor='w', dpi=300)

fig, ax = plt.subplots(len(porto), figsize = (12, 4), sharex = True, sharey = True)
for i, n in enumerate(porto):
    air.loc[air.name == n, :].plot(x = 'date', y=['no2', 'o3'], ax = ax[i], legend = False)
    ax[i].set_title(n, loc = 'left', fontsize = 8)
    
    ax[len(porto)-1].legend(['NO$_2$', 'O$_3$'])
    fig.text(0.07, 0.5, ylabel, va = 'center', rotation='vertical')

fig.savefig('03_output/fig/analysis/obs_no2_o3_porto.png', bbox_inches='tight', facecolor='w', dpi=300)
    
fig, ax = plt.subplots(len(lisbon), figsize = (12, 8), sharex = True, sharey = True)
for i, n in enumerate(lisbon):
    air.loc[air.name == n, :].plot(x = 'date', y=['no2', 'o3'], ax = ax[i], legend = False)
    ax[i].set_title(n, loc = 'left', fontsize = 8)
    ax[-len(lisbon)].legend(['NO$_2$', 'O$_3$'])
    fig.text(0.07, 0.5, ylabel, va = 'center', rotation='vertical')
fig.savefig('03_output/fig/analysis/obs_no2_o3_lisbon.png', bbox_inches='tight', facecolor='w', dpi=300)

fig, ax = plt.subplots(len(lisbon2), figsize = (12, 8), sharex = True, sharey = True)
for i, n in enumerate(lisbon2):
    air.loc[air.name == n, :].plot(x = 'date', y=['no2', 'o3'], ax = ax[i], legend = False)
    ax[i].set_title(n, loc = 'left', fontsize = 8)
    ax[-len(lisbon)].legend(['NO$_2$', 'O$_3$'])
    fig.text(0.07, 0.5, ylabel, va = 'center', rotation='vertical')
fig.savefig('03_output/fig/analysis/obs_no2_o3_lisbon2.png', bbox_inches='tight', facecolor='w', dpi=300)

fig, ax = plt.subplots(len(porto), figsize = (12, 4), sharex = True, sharey = True)
for i, n in enumerate(porto):
    air.loc[air.name == n, :].plot(x = 'date', y='co', ax = ax[i], legend = False)
    ax[i].set_title(n, loc = 'left', fontsize = 8)
    
    ax[len(porto)-1].legend(['CO'])
    fig.text(0.07, 0.5, ylabel_co, va = 'center', rotation='vertical')

fig.savefig('03_output/fig/analysis/obs_co_porto.png', bbox_inches='tight', facecolor='w', dpi=300)
    
fig, ax = plt.subplots(len(lisbon), figsize = (12, 8), sharex = True, sharey = True)
for i, n in enumerate(lisbon):
    air.loc[air.name == n, :].plot(x = 'date', y='co', ax = ax[i], legend = False)
    ax[i].set_title(n, loc = 'left', fontsize = 8)
    ax[-len(lisbon)].legend(['CO'])
    fig.text(0.07, 0.5, ylabel_co, va = 'center', rotation='vertical')
fig.savefig('03_output/fig/analysis/obs_co_lisbon.png', bbox_inches='tight', facecolor='w', dpi=300)

fig, ax = plt.subplots(len(lisbon2), figsize = (12, 8), sharex = True, sharey = True)
for i, n in enumerate(lisbon2):
    air.loc[air.name == n, :].plot(x = 'date', y='co', ax = ax[i], legend = False)
    ax[i].set_title(n, loc = 'left', fontsize = 8)
    ax[-len(lisbon)].legend(['CO'])
    fig.text(0.07, 0.5, ylabel_co, va = 'center', rotation='vertical')
fig.savefig('03_output/fig/analysis/obs_co_lisbon2.png', bbox_inches='tight', facecolor='w', dpi=300)

#%%



import folium

locations = pd.read_csv('02_data/raw/air_quality/stations.csv', sep=',', decimal = '.')
locations = locations[['lat', 'lon', 'name']]
map = folium.Map(location=[locations.lat.mean(), locations.lon.mean()],
                 zoom_start=14, control_scale=True)

for index, location_info in locations.iterrows():
    folium.Marker([location_info["lat"], location_info["lon"]], popup=location_info["name"]).add_to(map)
    
map.save("03_output/fig/analysis/aq_stations.html")

