#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

# Brian Blaylock
# April 26, 2017                                # Jazz won game 5 last night!


"""
Plots a sample image of HRRR reflectivity

Trouble writing the downloaded HRRR file to a space from the webbrowser.

Note: Cannot print anything to screen when outputting a .png file
"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
## Reset the defaults (see more here: http://matplotlib.org/users/customizing.html)
mpl.rcParams['figure.figsize'] = [12,8]
mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['savefig.dpi'] = 80     # For publication purposes


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
      date = form['date'].value
      DATE = datetime.strptime(date,'%Y-%m-%d') # convert to datetime
except:
      DATE = datetime.now()-timedelta(days=1)
      yesterday = DATE.strftime('%Y-%m-%d')
try:
      hour = int(form['hour'].value)
except:
      hour = 0
try:
      fxx = int(form['fxx'].value)
except:
      fxx = 0

def reflect_ncdc():
      reflect_ncdc_cdict ={'red':((0.0000, 0.000, 0.000),
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
m = draw_CONUS_HRRR_map(res='l')

# Clean up Date:
DATE = datetime(DATE.year, DATE.month, DATE.day, hour)

if model == 'hrrrAK':
      plt.figure(1)
      plt.title('Alaska Graphs not available')
      plt.savefig(sys.stdout)	# Plot standard output.

else:
      # Get HRRR Data
      if model == 'hrrr':
            VAR = 'REFC:entire atmosphere'
      elif model == 'hrrrX':
            VAR = 'var discipline=0 center=59 local_table=1 parmcat=16 parm=196'
      H = get_hrrr_variable(DATE, VAR, model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False)

      # Mask empty values
      dBZ = np.ma.array(H['value'])
      dBZ[dBZ==-10] = np.ma.masked

      plt.figure(1)
      m.drawstates()
      m.drawcoastlines()
      m.drawcountries()
      plt.title('%s %s F%02d' % (model.upper(), DATE, fxx))
      X, Y = m(H['lon'], H['lat'])
      m.pcolormesh(X, Y, dBZ, cmap=reflect_ncdc(), vmax=80, vmin=0)
      cb = plt.colorbar(orientation='horizontal', shrink=.8, pad=.01)
      cb.set_label(r'Simulated Composite Reflectivity (dBZ)')

      plt.savefig(sys.stdout)	# Plot standard output.
