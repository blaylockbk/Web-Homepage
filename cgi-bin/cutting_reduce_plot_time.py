# Does cutting really increase the plotting time??

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
## Reset the defaults (see more here: http://matplotlib.org/users/customizing.html)
mpl.rcParams['figure.figsize'] = [10,10]
mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['savefig.dpi'] = 80     # For web purposes


import numpy as np
from datetime import date, datetime, timedelta
import os


import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
sys.path.append('/uufs/chpc.utah.edu/sys/pkg/python/2.7.3_rhel6/lib/python2.7/site-packages/')
import pygrib
from BB_basemap.draw_maps import draw_CONUS_HRRR_map, Basemap, draw_CONUS_cyl_map
from BB_downloads.HRRR_S3 import get_hrrr_variable
from BB_data.grid_manager import pluck_point_new
#from BB_cmap.mycmap import reflect_ncdc
from BB_MesoWest.MesoWest_STNinfo import get_station_info
from BB_wx_calcs.wind import wind_uv_to_spd

DATE = datetime(2017, 1, 1, 9)
model = 'hrrr'
fxx = 0
lat = 40.74
lon = -111.83
barb_thin = 5
bfr = 150 

#m = draw_CONUS_HRRR_map()
m = draw_CONUS_cyl_map()

#============= CUT DATA =======================================================
timer=datetime.now()
plt.figure(1)
m.drawstates()
# Get data
H_u = get_hrrr_variable(DATE, 'UGRD:10 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False)
H_v = get_hrrr_variable(DATE, 'VGRD:10 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=True)

gridlat = H_u['lat']
gridlon = H_u['lon']
cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
# Cut grid
gridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
gridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]


# Cut variables
H_u['value'] = H_u['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
H_v['value'] = H_v['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]

# Add to plot
thin = barb_thin
m.pcolormesh(gridlon, gridlat, H_u['value'], latlon=True)
m.barbs(gridlon[::thin,::thin], gridlat[::thin,::thin], H_u['value'][::thin,::thin], H_v['value'][::thin,::thin],
        zorder=200, length=5,
        barb_increments={'half':2.5, 'full':5,'flag':25},
        latlon=True)
plt.ylabel(r'Barbs: half=2.5, full=5, flag=25 (ms$\mathregular{^{-1}}$)')
print datetime.now()-timer


#============= NO CUT =========================================================
timer = datetime.now()
plt.figure(2)
m.drawstates()
# Get data
H_u = get_hrrr_variable(DATE, 'UGRD:10 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False)
H_v = get_hrrr_variable(DATE, 'VGRD:10 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False)
gridlat = H_u['lat']
gridlon = H_u['lon']
# Cut variables
# Add to plot
thin = barb_thin
m.pcolormesh(gridlon, gridlat, H_u['value'],latlon=True)
m.barbs(gridlon[::thin,::thin], gridlat[::thin,::thin], H_u['value'][::thin,::thin], H_v['value'][::thin,::thin],
        zorder=200, length=5,
        barb_increments={'half':2.5, 'full':5,'flag':25},
        latlon=True)
plt.ylabel(r'Barbs: half=2.5, full=5, flag=25 (ms$\mathregular{^{-1}}$)')


print datetime.now()-timer

plt.show()