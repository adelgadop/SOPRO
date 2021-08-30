#!/bin/bash

# First run with one  day of spin up:
STARTYEAR=2017
STARTMONTH=10
STARTDAY=30
STARTHOUR=00
RESTART=.true.
RESTINT=8640

ENDYEAR=2017
ENDMONTH=11
ENDDAY=06
ENDHOUR=00

# Environment:
SOPRO=/scr2/alejandro/WRF/sopro/
WRFDIR=$SOPRO/WRF
CONFIGDIR=$SOPRO/namelists

# Cleaning:
rm $WRFDIR/wrfinput*
rm $WRFDIR/wrfbdy*
rm $WRFDIR/rsl*
rm $WRFDIR/met_em*

# setting namelist.input
echo "setting namelist.input"
cp $CONFIGDIR/namelist.input $WRFDIR/namelist.input

sed -i "s/STARTYEAR/$STARTYEAR/g" $WRFDIR/namelist.input
sed -i "s/STARTMONTH/$STARTMONTH/g" $WRFDIR/namelist.input
sed -i "s/STARTDAY/$STARTDAY/g" $WRFDIR/namelist.input
sed -i "s/STARTHOUR/$STARTHOUR/g" $WRFDIR/namelist.input

sed -i "s/ENDYEAR/$ENDYEAR/g" $WRFDIR/namelist.input
sed -i "s/ENDMONTH/$ENDMONTH/g" $WRFDIR/namelist.input
sed -i "s/ENDDAY/$ENDDAY/g" $WRFDIR/namelist.input
sed -i "s/ENDHOUR/$ENDHOUR/g" $WRFDIR/namelist.input
sed -i "s/RESTART/$RESTART/g" $WRFDIR/namelist.input
sed -i "s/RESTINT/$RESTINT/g" $WRFDIR/namelist.input

# WRF programs
echo "running WRF programs (please wait!!!)"
cd $WRFDIR
ln -sf ../met_em/met_em* .
./real.exe
echo "Done real.exe"

mpirun -np 16 -machinefile host_jano ./wrf.exe

echo "First run with one day of spin-up"

echo "moving wrfout spin up"
mv wrfout_*-$STARTMONTH-$STARTDAY\_* ../spin_up/

echo "moving wrfout to ../wrfout_met/"
mv wrfout_* ../wrfout_met/

echo "Successfully first run"

# Second run with two days of spin up: ----------------------------------------------
echo "starting 2 run"
STARTYEAR=2017
STARTMONTH=11
STARTDAY=05
STARTHOUR=00
RESTART=.true.
RESTINT=7200

ENDYEAR=2017
ENDMONTH=11
ENDDAY=11
ENDHOUR=00

# Cleaning:
rm $WRFDIR/wrfinput*
rm $WRFDIR/wrfbdy*
rm $WRFDIR/rsl*

# setting namelist.input
echo "setting namelist.input"
cp $CONFIGDIR/namelist.input $WRFDIR/namelist.input

sed -i "s/STARTYEAR/$STARTYEAR/g" $WRFDIR/namelist.input
sed -i "s/STARTMONTH/$STARTMONTH/g" $WRFDIR/namelist.input
sed -i "s/STARTDAY/$STARTDAY/g" $WRFDIR/namelist.input
sed -i "s/STARTHOUR/$STARTHOUR/g" $WRFDIR/namelist.input

sed -i "s/ENDYEAR/$ENDYEAR/g" $WRFDIR/namelist.input
sed -i "s/ENDMONTH/$ENDMONTH/g" $WRFDIR/namelist.input
sed -i "s/ENDDAY/$ENDDAY/g" $WRFDIR/namelist.input
sed -i "s/ENDHOUR/$ENDHOUR/g" $WRFDIR/namelist.input
sed -i "s/RESTART/$RESTART/g" $WRFDIR/namelist.input
sed -i "s/RESTINT/$RESTINT/g" $WRFDIR/namelist.input

# WRF programs
echo "running WRF programs (please wait!!!)"
cd $WRFDIR
./real.exe
echo "Done real.exe"

mpirun -np 16 -machinefile host_jano ./wrf.exe
echo "next runs with 1 day of spin-up"

echo "moving wrfout spin up"
mv wrfout_*-11-$STARTDAY\_* ../spin_up/

echo "moving wrfout to ../wrfout_met/"
mv wrfout_* ../wrfout_met/

echo "Successfully 2 run"

# third run with two days of spin up: ----------------------------------------------
echo "starting 3 run"
STARTYEAR=2017
STARTMONTH=11
STARTDAY=10
STARTHOUR=00
RESTART=.true.
RESTINT=7200

ENDYEAR=2017
ENDMONTH=11
ENDDAY=16
ENDHOUR=00

# Cleaning:
rm $WRFDIR/wrfinput*
rm $WRFDIR/wrfbdy*
rm $WRFDIR/rsl*

# setting namelist.input
echo "setting namelist.input"
cp $CONFIGDIR/namelist.input $WRFDIR/namelist.input

sed -i "s/STARTYEAR/$STARTYEAR/g" $WRFDIR/namelist.input
sed -i "s/STARTMONTH/$STARTMONTH/g" $WRFDIR/namelist.input
sed -i "s/STARTDAY/$STARTDAY/g" $WRFDIR/namelist.input
sed -i "s/STARTHOUR/$STARTHOUR/g" $WRFDIR/namelist.input

sed -i "s/ENDYEAR/$ENDYEAR/g" $WRFDIR/namelist.input
sed -i "s/ENDMONTH/$ENDMONTH/g" $WRFDIR/namelist.input
sed -i "s/ENDDAY/$ENDDAY/g" $WRFDIR/namelist.input
sed -i "s/ENDHOUR/$ENDHOUR/g" $WRFDIR/namelist.input
sed -i "s/RESTART/$RESTART/g" $WRFDIR/namelist.input
sed -i "s/RESTINT/$RESTINT/g" $WRFDIR/namelist.input

# WRF programs
echo "running WRF programs (please wait!!!)"
cd $WRFDIR
./real.exe
echo "Done real.exe"

mpirun -np 16 -machinefile host_jano ./wrf.exe

echo "Next runs with 1 day of spin-up"

echo "moving wrfout spin up"
mv wrfout_*-11-$STARTDAY\_* ../spin_up/

echo "moving wrfout to ../wrfout_met/"
mv wrfout_* ../wrfout_met/

echo "Successfully 3 run"

# 4 run with two days of spin up: ----------------------------------------------
echo "starting 4 run"
STARTYEAR=2017
STARTMONTH=11
STARTDAY=15
STARTHOUR=00
RESTART=.true.
RESTINT=7200

ENDYEAR=2017
ENDMONTH=11
ENDDAY=21
ENDHOUR=00

# Cleaning:
rm $WRFDIR/wrfinput*
rm $WRFDIR/wrfbdy*
rm $WRFDIR/rsl*

# setting namelist.input
echo "setting namelist.input"
cp $CONFIGDIR/namelist.input $WRFDIR/namelist.input

sed -i "s/STARTYEAR/$STARTYEAR/g" $WRFDIR/namelist.input
sed -i "s/STARTMONTH/$STARTMONTH/g" $WRFDIR/namelist.input
sed -i "s/STARTDAY/$STARTDAY/g" $WRFDIR/namelist.input
sed -i "s/STARTHOUR/$STARTHOUR/g" $WRFDIR/namelist.input

sed -i "s/ENDYEAR/$ENDYEAR/g" $WRFDIR/namelist.input
sed -i "s/ENDMONTH/$ENDMONTH/g" $WRFDIR/namelist.input
sed -i "s/ENDDAY/$ENDDAY/g" $WRFDIR/namelist.input
sed -i "s/ENDHOUR/$ENDHOUR/g" $WRFDIR/namelist.input
sed -i "s/RESTART/$RESTART/g" $WRFDIR/namelist.input
sed -i "s/RESTINT/$RESTINT/g" $WRFDIR/namelist.input

# WRF programs
echo "running WRF programs (please wait!!!)"
cd $WRFDIR
./real.exe
echo "Done real.exe"

mpirun -np 16 -machinefile host_jano ./wrf.exe
echo "Next runs with 1 day of spin-up"

echo "moving wrfout spin up"
mv wrfout_*-11-$STARTDAY\_* ../spin_up/

echo "moving wrfout to ../wrfout_met/"
mv wrfout_* ../wrfout_met/

echo "Successfully 4 run"

# 5 run with two days of spin up: ----------------------------------------------
echo "starting 5 run"
STARTYEAR=2017
STARTMONTH=11
STARTDAY=20
STARTHOUR=00
RESTART=.true.
RESTINT=7200

ENDYEAR=2017
ENDMONTH=11
ENDDAY=26
ENDHOUR=00

# Cleaning:
rm $WRFDIR/wrfinput*
rm $WRFDIR/wrfbdy*
rm $WRFDIR/rsl*

# setting namelist.input
echo "setting namelist.input"
cp $CONFIGDIR/namelist.input $WRFDIR/namelist.input

sed -i "s/STARTYEAR/$STARTYEAR/g" $WRFDIR/namelist.input
sed -i "s/STARTMONTH/$STARTMONTH/g" $WRFDIR/namelist.input
sed -i "s/STARTDAY/$STARTDAY/g" $WRFDIR/namelist.input
sed -i "s/STARTHOUR/$STARTHOUR/g" $WRFDIR/namelist.input

sed -i "s/ENDYEAR/$ENDYEAR/g" $WRFDIR/namelist.input
sed -i "s/ENDMONTH/$ENDMONTH/g" $WRFDIR/namelist.input
sed -i "s/ENDDAY/$ENDDAY/g" $WRFDIR/namelist.input
sed -i "s/ENDHOUR/$ENDHOUR/g" $WRFDIR/namelist.input
sed -i "s/RESTART/$RESTART/g" $WRFDIR/namelist.input
sed -i "s/RESTINT/$RESTINT/g" $WRFDIR/namelist.input

# WRF programs
echo "running WRF programs (please wait!!!)"
cd $WRFDIR
./real.exe
echo "Done real.exe"

mpirun -np 16 -machinefile host_jano ./wrf.exe
echo "Next runs with 1 day of spin-up" 

echo "moving wrfout spin up"
mv wrfout_*-11-$STARTDAY\_* ../spin_up/

echo "moving wrfout to ../wrfout_met/"
mv wrfout_* ../wrfout_met/

echo "Successfully 5 run"

# 6 run with two days of spin up: ----------------------------------------------
echo "starting 6 run"
STARTYEAR=2017
STARTMONTH=11
STARTDAY=25
STARTHOUR=00
RESTART=.true.
RESTINT=7200

ENDYEAR=2017
ENDMONTH=12
ENDDAY=01
ENDHOUR=00

# Cleaning:
rm $WRFDIR/wrfinput*
rm $WRFDIR/wrfbdy*
rm $WRFDIR/rsl*

# setting namelist.input
echo "setting namelist.input"
cp $CONFIGDIR/namelist.input $WRFDIR/namelist.input

sed -i "s/STARTYEAR/$STARTYEAR/g" $WRFDIR/namelist.input
sed -i "s/STARTMONTH/$STARTMONTH/g" $WRFDIR/namelist.input
sed -i "s/STARTDAY/$STARTDAY/g" $WRFDIR/namelist.input
sed -i "s/STARTHOUR/$STARTHOUR/g" $WRFDIR/namelist.input

sed -i "s/ENDYEAR/$ENDYEAR/g" $WRFDIR/namelist.input
sed -i "s/ENDMONTH/$ENDMONTH/g" $WRFDIR/namelist.input
sed -i "s/ENDDAY/$ENDDAY/g" $WRFDIR/namelist.input
sed -i "s/ENDHOUR/$ENDHOUR/g" $WRFDIR/namelist.input
sed -i "s/RESTART/$RESTART/g" $WRFDIR/namelist.input
sed -i "s/RESTINT/$RESTINT/g" $WRFDIR/namelist.input

# WRF programs
echo "running WRF programs (please wait!!!)"
cd $WRFDIR
./real.exe
echo "Done real.exe"

mpirun -np 16 -machinefile host_jano ./wrf.exe
echo "Next runs with 1 day of spin-up"

echo "moving wrfout spin up"
mv wrfout_*-11-$STARTDAY\_* ../spin_up/

echo "moving wrfout to ../wrfout_met/"
mv wrfout_* ../wrfout_met/

echo "Successfully 6 run"

