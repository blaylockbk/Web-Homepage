#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

# Brian Blaylock
# June 7, 2017                                # The train broke down today


"""
Plots a sample image of HRRR near the fire.
-Zoom in on Fire area
-Contourfill where winds are higher than 15 mph and 25 mph
-Contour Radar dBZ interval 5

Note: For CGI, cannot print anything to screen when outputting a .png file
"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
## Reset the defaults (see more here: http://matplotlib.org/users/customizing.html)
mpl.rcParams['figure.figsize'] = [12,8]
mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['savefig.dpi'] = 80     # For web purposes


import numpy as np
from datetime import datetime, timedelta
import os
import getpass

import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
sys.path.append('/uufs/chpc.utah.edu/sys/pkg/python/2.7.3_rhel6/lib/python2.7/site-packages/')
import pygrib
from BB_basemap.draw_maps import *
from BB_downloads.HRRR_S3 import *
from BB_data.grid_manager import pluck_point_new

import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.


#print "Content-Type: text/html\n"
print "Content-Type: image/png\n"

#print sys.modules.keys()
#print 'matplitlib version', mpl.__version__,'<br><br>'

form = cgi.FieldStorage()	# CGI function takes in web arguments

try:
    model = form['model'].value
except:
    model = 'hrrr'
try:
    name = form['name'].value
except:
    name = '(no name)'
try:
    date = form['validdate'].value
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
    lat = float(form['lat'].value)
except:
    plt.figure(1)
    plt.title('Something wrong with latitude')
    plt.savefig(sys.stdout)	# Plot standard output.

try:
    lon = float(form['lon'].value)
except:
    plt.figure(1)
    plt.title('Something wrong with longitude')
    plt.savefig(sys.stdout)	# Plot standard output.


def reflect_ncdc():
    reflect_ncdc_cdict = {'red':((0.0000, 0.000, 0.000),
                                 (0.0714, 0.000, 0.000),
                                 (0.1429, 0.000, 0.000),
                                 (0.2143, 0.000, 0.000),
                                 (0.2857, 0.000, 0.000),
                                 (0.3571, 0.000, 0.000),
                                 (0.4286, 1.000, 1.000),
                                 (0.5000, 0.906, 0.906),
                                 (0.5714, 1.000, 1.000),
                                 (0.6429, 1.000, 1.000),
                                 (0.7143, 0.839, 0.839),
                                 (0.7857, 0.753, 0.753),
                                 (0.8571, 1.000, 1.000),
                                 (0.9286, 0.600, 0.600),
                                 (1.000, 0.923, 0.923)),
                          'green':((0.0000, 0.925, 0.925),
                                   (0.0714, 0.627, 0.627),
                                   (0.1429, 0.000, 0.000),
                                   (0.2143, 1.000, 1.000),
                                   (0.2857, 0.784, 0.784),
                                   (0.3571, 0.565, 0.565),
                                   (0.4286, 1.000, 1.000),
                                   (0.5000, 0.753, 0.753),
                                   (0.5714, 0.565, 0.565),
                                   (0.6429, 0.000, 0.000),
                                   (0.7143, 0.000, 0.000),
                                   (0.7857, 0.000, 0.000),
                                   (0.8571, 0.000, 0.000),
                                   (0.9286, 0.333, 0.333),
                                   (1.000, 0.923, 0.923)),
                          'blue':((0.0000, 0.925, 0.925),
                                  (0.0714, 0.965, 0.965),
                                  (0.1429, 0.965, 0.965),
                                  (0.2143, 0.000, 0.000),
                                  (0.2857, 0.000, 0.000),
                                  (0.3571, 0.000, 0.000),
                                  (0.4286, 0.000, 0.000),
                                  (0.5000, 0.000, 0.000),
                                  (0.5714, 0.000, 0.000),
                                  (0.6429, 0.000, 0.000),
                                  (0.7143, 0.000, 0.000),
                                  (0.7857, 0.000, 0.000),
                                  (0.8571, 1.000, 1.000),
                                  (0.9286, 0.788, 0.788),
                                  (1.000, 0.923, 0.923))}
    reflect_ncdc_coltbl = LinearSegmentedColormap('REFLECT_NCDC_COLTBL',reflect_ncdc_cdict)
    return reflect_ncdc_coltbl

# Get Map Object
m = Basemap(resolution='i', projection='cyl',\
            llcrnrlon=lon-.75, llcrnrlat=lat-.75,\
            urcrnrlon=lon+.75, urcrnrlat=lat+.75,)

# Convert Valid Date to Run Date, adjusted by the forecast
DATE = DATE - timedelta(hours=fxx)



# Get HRRR Data
H_ref = get_hrrr_variable(DATE, 'REFC:entire atmosphere', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False)
H_wind = get_hrrr_variable(DATE, 'WIND:10 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=True)
H_u = get_hrrr_variable(DATE, 'UGRD:10 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=True)
H_v = get_hrrr_variable(DATE, 'VGRD:10 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=True)

# Cut data down for faster contouring
cut_v, cut_h = pluck_point_new(lat,
                               lon,
                               H_ref['lat'],
                               H_ref['lon'])
bfr = 35
H_ref['lon'] = H_ref['lon'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
H_ref['lat'] = H_ref['lat'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
H_ref['value'] = H_ref['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
H_wind['value'] = H_wind['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
H_u['value'] = H_u['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
H_v['value'] = H_v['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]

plt.figure(1)
m.arcgisimage(service='World_Shaded_Relief',
              xpixels=500,
              verbose=False)
m.drawstates()

plt.title('%s (%s)\n       Run: %s F%02d\nVaild: %s' % (name, model.upper(), DATE, fxx, DATE+timedelta(hours=fxx)))

# Plot high wind speed shading
plt.contourf(H_ref['lon'], H_ref['lat'], H_wind['value'], levels=[10, 15, 20, 25], colors=('yellow', 'orange', 'red'),
             barb_increments={'half':2.5, 'full':5,'flag':25},
             alpha=.5,
             extend='max')
cb = plt.colorbar(orientation='horizontal', shrink=.5, pad=.01)
cb.set_label(r'10 m Wind Speed (ms$\mathregular{^{-1}}$)')

# Plot reflectivity contours
cREF = plt.contour(H_ref['lon'], H_ref['lat'], H_ref['value'], cmap=reflect_ncdc(), levels=range(10, 80, 10))
plt.clabel(cREF, cREF.levels[::2], fmt='%2.0f', colors='k', fontsize=9)
#plt.pcolormesh(H_ref['lon'], H_ref['lat'], H_ref['value'], cmap=reflect_ncdc(), vmax=80, vmin=0, alpha=.5)
cb2 = plt.colorbar(shrink=.7)
cb2.set_label('Simulated Composite Reflectivity (dBZ)')

# Plot surface wind barbs
thin = 2
plt.barbs(H_ref['lon'][::thin,::thin], H_ref['lat'][::thin,::thin], H_u['value'][::thin,::thin], H_v['value'][::thin,::thin], zorder=200, length=5)

plt.savefig(sys.stdout)	# Plot standard output.
