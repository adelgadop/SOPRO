#!/bin/bash

# Environment:
SOPRO=/scr2/alejandro/WRF/sopro/
WPSDIR=$SOPRO/WPS

# Cleaning:
rm $WPSDIR/GRIBFILE.*
# rm $WPSDIR/met_em.*
rm $WPSDIR/FILE:*
rm $WPSDIR/ungrib.log
rm $WPSDIR/metgrid.log
echo "cleaning old files"

# WPS programs
cd $WPSDIR
./geogrid.exe
./link_grib.csh /scr2/alejandro/WRF/DATA/LBC/NCEP_GDAS/gdas1.fnl0p25.201801* 
./ungrib.exe
echo 'ungrib done'
./metgrid.exe
echo 'metgrid done'
mv met_em* ../met_em/
echo 'met_em in met_em/ folder'
