#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

# Brian Blaylock
# January 30, 2017                                 It's cold outside


"""
This script plots multiplut stations on one plot
"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

## Reset the defaults (see more here: http://matplotlib.org/users/customizing.html)
mpl.rcParams['figure.figsize'] = [15,8]
mpl.rcParams['figure.titlesize'] = 13
mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10
mpl.rcParams['axes.labelsize'] = 10
mpl.rcParams['axes.titlesize'] =12
mpl.rcParams['grid.linewidth'] = .25
mpl.rcParams['figure.subplot.wspace']  = 0.05

mpl.rcParams['legend.fontsize'] = 15
mpl.rcParams['legend.loc'] = 'best'

mpl.rcParams['savefig.bbox'] = 'tight'
#mpl.rcParams['savefig.dpi'] = 1000     # For publication purposes

import numpy as np
from datetime import datetime, timedelta


import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
sys.path.append('/uufs/chpc.utah.edu/sys/pkg/python/2.7.3_rhel6/lib/python2.7/site-packages/')
import pygrib
from BB_basemap.draw_maps import *
from BB_cmap.landuse_colormap import *

import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.


#print "Content-Type: text/html\n"
print "Content-Type: image/png\n"

#print sys.modules.keys()
#print 'matplitlib version', mpl.__version__,'<br><br>'

form = cgi.FieldStorage()	# CGI function takes in web arguments

# The subset indecies for the HRRR domain.
# Oder is xmin, xmax, ymin, ymax
subset = {'Utah':[470,725,391,603],
          'GSL':[630,697,453,511],
          'UtahLake':[611,635,486,505],
          'west':[0,1799,0,950],
          'east':[0,1799,850,1799],
          'CONUS':[0,1799,0,1799],
          'Uintah':[470,725,391,603], #need to fix these indexes. currently is Utah domain
         }

try:
      date = form['date'].value
      DATE = datetime.strptime(date,'%Y-%m-%d') # convert to datetime
      yesterday = date # the string format
except:
      DATE = datetime.now()-timedelta(days=1)
      yesterday = DATE.strftime('%Y-%m-%d')
try:
      hour = form['hour'].value
except:
      hour = '03'

try:
      domain = form['domain'].value
except:
      domain = 'GSL'

#print date, hour


DIR = '/uufs/chpc.utah.edu/common/home/horel-group/archive/%04d%02d%02d/models/' % (DATE.year, DATE.month, DATE.day)

# Open HRRR and get surface temperature
grbs = pygrib.open(DIR+'hrrr/hrrr.t'+hour+'z.wrfsfcf00.grib2')
temp = grbs.select(name="Vegetation Type")[0].values[subset[domain][0]:subset[domain][1],subset[domain][2]:subset[domain][3]]
lat, lon = grbs.select(name="Vegetation Type")[0].latlons()
lat = lat[subset[domain][0]:subset[domain][1],subset[domain][2]:subset[domain][3]]
lon = lon[subset[domain][0]:subset[domain][1],subset[domain][2]:subset[domain][3]]

# Open HRRRx and get surface temperature
grbsX = pygrib.open(DIR+'hrrrX/hrrrX.t'+hour+'z.wrfsfcf00.grib2')
if len(np.unique(grbsX[87].values))==19:
      tempX = grbsX[87].values[subset[domain][0]:subset[domain][1],subset[domain][2]:subset[domain][3]] # new HRRRx
else:
      tempX = grbsX[86].values[subset[domain][0]:subset[domain][1],subset[domain][2]:subset[domain][3]] # old HRRRx

# Note: lat/lon and latX/lonX should be the same
# Note: Don't trim data, it doubles time to plot
if domain == 'GSL':
   m = draw_GSL_map()
elif domain == 'Utah':
    m = draw_Utah_map()
elif domain == 'UtahLake':
    m = draw_UtahLake_map()
elif domain == 'Uintah':
    m = draw_Uintah_map()
elif domain == 'west':
    m = draw_HRRRwest()
    lon, lat = m(lon,lat)
elif domain == 'east':
    m = draw_HRRReast()
    lon, lat = m(lon,lat)
elif domain == 'CONUS':
    m = draw_CONUS_HRRR_map()
    lon, lat = m(lon,lat)

# MODIS Landuse Colormap
cm, labels = LU_MODIS20()

# Draw map and plot temperatures
fig = plt.figure(figsize=[13,5])
# first pannel
ax = fig.add_subplot(131)

m.drawstates()
m.drawcoastlines()
m.drawcountries()
m.pcolormesh(lon, lat, temp, cmap=cm, vmin=1, vmax=len(labels) + 1)
cbar = plt.colorbar(orientation='horizontal', shrink=.99, pad=.03)
cbar.set_ticks(np.arange(0.5, len(labels) + 1))
cbar.ax.set_xticklabels(labels, rotation=90)
cbar.ax.tick_params(labelsize=10)
plt.title('hrrr')

# second pannel
ax = fig.add_subplot(132)

m.drawstates()
m.drawcoastlines()
m.drawcountries()
m.pcolormesh(lon, lat, tempX, cmap=cm, vmin=1, vmax=len(labels) + 1)
cbar = plt.colorbar(orientation='horizontal', shrink=.99, pad=.03)
cbar.set_ticks(np.arange(0.5, len(labels) + 1))
cbar.ax.set_xticklabels(labels, rotation=90)
cbar.ax.tick_params(labelsize=10)
plt.title('hrrrX')

# third pannel
ax = fig.add_subplot(133)

m.drawstates()
m.drawcoastlines()
m.drawcountries()
m.pcolormesh(lon, lat, tempX-temp, cmap='bwr', vmax=5, vmin=-5)
plt.colorbar(orientation='horizontal', shrink=.9, pad=.03, extend='both')
plt.title('hrrrX - hrrr')

plt.suptitle(yesterday+" h"+hour+'z   Vegetation Type')


plt.savefig(sys.stdout)	# Plot standard output.
