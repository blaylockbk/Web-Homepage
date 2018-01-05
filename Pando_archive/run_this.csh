#!/bin/csh
#
#--------------------------------------------------------------------------------------
# Run the Python Script for plotting HRRR point forecasts
# CRON job on Meso4, every hour
#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------
# Updates:
#	bkb: 04/25/2017  First set into operations
#	
#--------------------------------------------------------------------------------------

limit coredumpsize 0

cd /uufs/chpc.utah.edu/common/home/u0553130/public_html/Brian_Blaylock/Pando_archive/

module load python/2.7.3
python daily_usage.py
exit
