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
obs.drop(['so2'], axis=1, inplace=True)

#%% Simulations using WRF-Chem
# Mechanism = MOZCART

mod1 = pkl.load(open('02_data/processed/res02_chem_d02_2017_'+month+'.pkl', 'rb'))    # 3 km WRF-Chem v3.9.1 emission serial false
mod2 = pkl.load(open('02_data/processed/res03_chem_d02_2017_'+month+'.pkl', 'rb'))    # 3 km WRF-Chem v3.9.1 emission serial true
mod3 = pkl.load(open('02_data/processed/lisboa_amanan_d02_2017_'+month+'.pkl', 'rb')) # 5 km WRF-Chem v4.2.1 emission serial false


stations = pd.read_csv('02_data/raw/air_quality/stations.csv')
codes = list(mod3.keys())
stations = stations.loc[stations.code.isin(codes),:]

mod1_df = pd.DataFrame()
mod2_df = pd.DataFrame()
mod3_df = pd.DataFrame()

for c in codes:
    print(c)
    mod1_df = pd.concat([mod1_df, mod1[c]], axis=0)
    mod2_df = pd.concat([mod2_df, mod2[c]], axis=0)
    mod3_df = pd.concat([mod3_df, mod3[c]], axis=0)
    
mod1_df.drop(['tc', 'rh', 'ws', 'wd', 'no'], axis=1, inplace=True)
mod2_df.drop(['tc', 'rh', 'ws', 'wd', 'no'], axis=1, inplace=True)
mod3_df.drop(['tc', 'rh', 'ws', 'wd', 'no'], axis=1, inplace=True)

all_df1 = mod1_df.merge(obs, how='left', on=['local_date', 'code'], suffixes=['_mod', '_obs'])
all_df2 = mod2_df.merge(obs, how='left', on=['local_date', 'code'], suffixes=['_mod', '_obs'])
all_df3 = mod3_df.merge(obs, how='left', on=['local_date', 'code'], suffixes=['_mod', '_obs'])

#%% Make Plots
def plots_by_station(nombre, all_df1, all_df2, all_df3):
    fig, ax = plt.subplots(3,2, figsize=[12,8], sharex=True, gridspec_kw={'hspace':0.1})
    name=nombre
    plt.suptitle("Estação "+name + " vs Simulações \n (EDGARv5 2015 + MEGAN3 + CAM-Chem chemical IC/BC + queimadas do FINN)")

    # PM10
    all_df1.loc[all_df1.name == name, :].plot(x='local_date', y=['pm10_obs'], style='-ok', lw=1, ax=ax[0,0])
    all_df1.loc[all_df1.name == name, :].plot(x='local_date', y=['pm10_mod'], style='-g',  lw=3, alpha=.7, ax=ax[0,0])
    all_df2.loc[all_df2.name == name, :].plot(x='local_date', y=['pm10_mod'], style='-b',  lw=3, alpha=.7, ax=ax[0,0])
    all_df3.loc[all_df3.name == name, :].plot(x='local_date', y=['pm10_mod'], style='-m',  lw=3, alpha=.7, ax=ax[0,0])
    ax[0,0].legend(['Observações', 
                    '3 km (WRF-Chem v3.9.1)', 
                    '3 km (WRF-Chem v3.9.1) \n emissiões interpoladas (mensal)', 
                    '5 km (WRF-Chem v4.2.1)'], fontsize=14, bbox_to_anchor=(2.2, -0.25))
    ax[0,0].set_ylim([0, 50])
    ax[0,0].set_ylabel('PM$_{10}$ ($\mu$g.m$^{-3}$)')

    # PM2,5
    all_df1.loc[all_df1.name == name, :].plot(x='local_date', y=['pm2.5_obs'], style='-ok', lw=1, ax=ax[0,1])
    all_df1.loc[all_df1.name == name, :].plot(x='local_date', y=['pm2.5_mod'], style='-g', lw=3, alpha=.7, ax=ax[0,1])
    all_df2.loc[all_df2.name == name, :].plot(x='local_date', y=['pm2.5_mod'], style='-b', lw=3, alpha=.7, ax=ax[0,1])
    all_df3.loc[all_df3.name == name, :].plot(x='local_date', y=['pm2.5_mod'], style='-m', lw=3, alpha=.7, ax=ax[0,1])
    ax[0,1].get_legend().remove()
    ax[0,1].set_ylim([0, 30])
    ax[0,1].set_ylabel('PM$_{2.5}$ ($\mu$g.m$^{-3}$)')

    # CO
    all_df1.loc[all_df1.name == name, :].plot(x='local_date', y=['co_obs'], style='-ok', lw=1, ax=ax[1,0])
    all_df1.loc[all_df1.name == name, :].plot(x='local_date', y=['co_mod'], style=['-g'], lw=3, alpha=.7, ax=ax[1,0])
    all_df2.loc[all_df2.name == name, :].plot(x='local_date', y=['co_mod'], style=['-b'], lw=3, alpha=.7, ax=ax[1,0])
    all_df3.loc[all_df3.name == name, :].plot(x='local_date', y=['co_mod'], style=['-m'], lw=3, alpha=.7, ax=ax[1,0])
    ax[1,0].get_legend().remove()
    ax[1,0].set_ylim([0, 0.8])
    ax[1,0].set_ylabel('CO (ppm)')

    # O3
    all_df1.loc[all_df1.name == name, :].plot(x='local_date', y=['o3_obs'], style='-ok', lw=1, ax=ax[2,1])
    all_df1.loc[all_df1.name == name, :].plot(x='local_date', y=['o3_mod'], style='-g', lw=3, alpha=.7, ax=ax[2,1])
    all_df2.loc[all_df2.name == name, :].plot(x='local_date', y=['o3_mod'], style='-b', lw=3, alpha=.7, ax=ax[2,1])
    all_df3.loc[all_df3.name == name, :].plot(x='local_date', y=['o3_mod'], style='-m', lw=3, alpha=.7, ax=ax[2,1])
    ax[2,1].get_legend().remove()
    ax[2,1].set_ylabel('O$_3$ ($\mu$g.m$^{-3}$)')
    ax[2,1].set_xlabel('Tempo local')

    # NO2
    all_df1.loc[all_df1.name == name, :].plot(x='local_date', y=['no2_obs'], style='-ok', lw=1, ax=ax[2,0])
    all_df1.loc[all_df1.name == name, :].plot(x='local_date', y=['no2_mod'], style='-g', lw=3, alpha=.7, ax=ax[2,0])
    all_df2.loc[all_df2.name == name, :].plot(x='local_date', y=['no2_mod'], style='-b', lw=3, alpha=.7, ax=ax[2,0])
    all_df3.loc[all_df3.name == name, :].plot(x='local_date', y=['no2_mod'], style='-m', lw=3, alpha=.7, ax=ax[2,0])
    ax[2,0].get_legend().remove()
    ax[2,0].set_ylabel('NO$_2$ ($\mu$g.m$^{-3}$)')
    ax[2,0].set_xlabel('Tempo local')
    
    fig.delaxes(ax[1,1])
    fig.subplots_adjust(top=0.92)

    fig.savefig('03_output/fig/final/'+name+'.png', bbox_inches = 'tight', facecolor = 'w', dpi = 300)

for n in stations.name:
    plots_by_station(n, all_df1, all_df2, all_df3)

#%% 
# =============================================================================
# Statistical analysis: O3 as 1 hr and PM2.5 as 24 h, according to Emery (2017)
# =============================================================================

stats = {}
sta_df = pd.DataFrame()


for n in all_df1.name.unique():
    stats[n] = ms.aq_stats(all_df1.loc[all_df1.name.isin([n]),:],polls=['o3'])
     
    stats[n].loc[:, 'name'] = (n)
    df = stats[n]
    sta_df = pd.concat([sta_df,df]).round(2).drop(['MAGE','RMSE','IOA'], axis=1)
    sta_df.dropna(inplace=True)
    


    
    







