#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

# Brian Blaylock
# June 8, 2017     # I accidentally made beef jerky in the crock pot last night


"""
Plots a sample image of HRRR near the fire.

Note: For CGI, cannot print anything to screen when outputting a .png file
"""

import numpy as np
from datetime import datetime, timedelta
import h5py

firsttimer = datetime.now()


import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
## Reset the defaults (see more here: http://matplotlib.org/users/customizing.html)
mpl.rcParams['figure.figsize'] = [12, 10]
mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['savefig.dpi'] = 100     # For web
mpl.rcParams['figure.titleweight'] = 'bold'
mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['axes.titlesize'] = 12
mpl.rcParams['figure.subplot.hspace'] = 0.01

# Colorbar
pad = 0.01
shrink = 0.7
# Map Resolution, 'l' - low, 'i' - intermediate, 'h' - high
map_res = 'l'


import sys, os
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
sys.path.append('/uufs/chpc.utah.edu/sys/pkg/python/2.7.3_rhel6/lib/python2.7/site-packages/')
from BB_basemap.draw_maps import draw_CONUS_HRRR_map, Basemap, draw_ALASKA_cyl_map
from BB_downloads.HRRR_S3 import get_hrrr_variable
from BB_MesoWest.MesoWest_STNinfo import get_station_info
from BB_wx_calcs.wind import wind_uv_to_spd
from BB_wx_calcs.humidity import Tempdwpt_to_RH
from BB_data.grid_manager import pluck_point_new

import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.


#print "Content-Type: text/html\n"
print "Content-Type: image/png\n"

#print sys.modules.keys()
#print 'matplitlib version', mpl.__version__,'<br><br>'


# === Load Form Input =========================================================
form = cgi.FieldStorage()	# CGI function takes in web arguments

try:
    model = form['model'].value
except:
    model = 'hrrr'

try:
    date = form['valid'].value
    DATE = datetime.strptime(date,'%Y-%m-%d_%H%M') # convert to datetime
except:
    plt.figure(1)
    plt.title('Something wrong with date')
    plt.savefig(sys.stdout)	# Plot standard output.

try:
    fxx = int(form['fxx'].value)
except:
    fxx = 0

try:
    dsize = form['dsize'].value
except:
    plt.figure(1)
    plt.title('Something wrong with the domain size\noptions: small, medium, large, xlarge, xxlarge, xxxlarge, conus')
    plt.savefig(sys.stdout)	# Plot standard output.