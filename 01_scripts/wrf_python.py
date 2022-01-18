from wrf import getvar
from netCDF4 import Dataset
import xarray as xr
import pyproj
import glob
import numpy as np

# Extract the variables of interest at time index 17
print("Reading each wrfout...")
month = input('month (e.g., 09): ')
year = input('year: ')
domain = input('domain (d01, d02, d03, d04): ')
ds = Dataset('../../wrfout_met/wrfout_'+ domain +'_'+year+'-'+month+'-01_00:00:00')
variables = [getvar(ds, var, 17) for var in ('z','T2','rh2', 'uvmet10_wspd_wdir')]

data = xr.merge(variables)

# Define the WRF projection 
wrf_proj = pyproj.Proj(proj= 'lcc', lat_1=ds.TRUELAT1, lat_2=ds.TRUELAT2,
                       lat_0=ds.MOAD_CEN_LAT, lon_0=ds.STAND_LON,
                       a = 6370000, b = 6370000)

# Easting and Northing of the domain center point
wgs_proj = pyproj.Proj(proj='latlong', datum='WGS84')
e, n = pyproj.transform(wgs_proj, wrf_proj, ds.CEN_LON, ds.CEN_LAT)

# Grid parameters
dx, dy = ds.DX, ds.DY
nx, ny = ds.dimensions['west_east'].size, ds.dimensions['south_north'].size

# Lower left corner of the domain
x0 = -(nx-1) / 2. * dx + e
y0 = -(ny-1) / 2. * dy + n

# Get grid values
x, y = np.arange(nx) * dx + x0, np.arange(ny) * dy + y0

# Add in dimension coordinates
eta_attrs = {attr: ds['ZNU'].getncattr(attr) for attr in ds['ZNU'].ncattrs()}
eta_attrs['axis'] = 'Z'
data['bottom_top'] = xr.DataArray(ds['ZNU'][17], dims='bottom_top', attrs=eta_attrs)
data['south_north'] = xr.DataArray(y, dims='south_north', attrs={'axis': 'Y', 'units': 'm'})
data['west_east'] = xr.DataArray(x, dims='west_east', attrs={'axis': 'X', 'units': 'm'})

# Define the grid_mapping
data['LambertConformal'] = xr.DataArray(np.array(0), attrs={
    'grid_mapping_name': 'lambert_conformal_conic',
    'earth_radius': 6370000,
    'standard_parallel': (ds.TRUELAT1, ds.TRUELAT2),
    'longitude_of_central_meridian': ds.STAND_LON,
    'latitude_of_projection_origin': ds.MOAD_CEN_LAT
})
for var in data.data_vars:
    data[var].attrs['grid_mapping'] = 'LambertConformal'
    if 'projection' in data[var].attrs:
        del data[var].attrs['projection']
    if 'coordinates' in data[var].attrs:
        del data[var].attrs['coordinates']
        
# Save result
data.to_netcdf('../02_data/processed/wrfout'+'_'+domain+'_' + year+'-'+month+'_processed.nc')

print("""
SUCCESFULLY
""")
