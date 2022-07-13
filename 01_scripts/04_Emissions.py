#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 15:03:48 2022

@author: adelgado
"""

# Import necessary libraries
import pandas as pd
import os, fnmatch
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from mpl_toolkits.axes_grid1 import AxesGrid
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature


#%% Import processed data

path = '/Volumes/passport/USP/SOPRO/wrfchemi_00z_d01'

emi = xr.open_dataset(path)
emi.E_CO[3].plot()