#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

# Brian Blaylock
# January 1, 2017                                 It's cold outside


"""
This script plots multiplut stations on one plot
"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
#style_path = '/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2/BB_mplstyle/'
#plt.style.use([style_path+'publications.mplstyle',
#               style_path+'width_100.mplstyle',
#               style_path+'dpi_web.mplstyle'])

## Reset the defaults (see more here: http://matplotlib.org/users/customizing.html)
mpl.rcParams['figure.figsize'] = [16,9]
mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['ytick.labelsize'] = 15
mpl.rcParams['axes.labelsize'] = 17
mpl.rcParams['axes.titlesize'] =20
mpl.rcParams['grid.linewidth'] = .25

mpl.rcParams['legend.fontsize'] = 15
mpl.rcParams['legend.loc'] = 'best'

mpl.rcParams['savefig.bbox'] = 'tight'
#mpl.rcParams['savefig.dpi'] = 1000     # For publication purposes

from matplotlib.dates import DateFormatter, HourLocator
from datetime import datetime, timedelta
from collections import OrderedDict

import numpy as np

import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
from BB_MesoWest.MesoWest_climo import get_mesowest_climatology

import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.


#print "Content-Type: text/html\n"
print "Content-Type: image/png\n"

#print 'hi'
#print sys.modules.keys()
#print 'matplitlib version', mpl.__version__,'<br><br>'

form = cgi.escape(cgi.FieldStorage())	# CGI function takes in web arguments


try:
      stn1 = form['stn1'].value
except:
      stn1 = 'UKBKB'

station = stn1


MONTH = np.array([])
AVG_Temp = np.array([])
MAX_Temp = np.array([])
MIN_Temp = np.array([])

months = np.arange(1, 13)
for m in months:
    start = '%02d010000' % (m)
    if m != 12:
        end = '%02d010000' % (m+1)
    else:
        end = '12312359'

    a = get_mesowest_climatology(station, start, end)

    MONTH = np.append(MONTH, m)

    avg_temp = np.nanmean(a['air_temp'])
    AVG_Temp = np.append(AVG_Temp, avg_temp)
    MAX_Temp = np.append(MAX_Temp, np.nanmax(a['air_temp']))
    MIN_Temp = np.append(MIN_Temp, np.nanmin(a['air_temp']))

plt.plot(MONTH, MAX_Temp, label='Max')
plt.plot(MONTH, AVG_Temp, label='Mean')
plt.plot(MONTH, MIN_Temp, label='Min')
plt.title(station
            + "\n"
            + a['DATETIME'][0].strftime('%Y')
            + ' to '
            + a['DATETIME'][-1].strftime('%Y'))
plt.xlabel('Month')
plt.ylabel('Temperature (C)')
plt.legend()
plt.grid()
plt.xlim([1, 12])
plt.xticks(range(1,13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])


plt.savefig(sys.stdout)	# Plot standard output.

