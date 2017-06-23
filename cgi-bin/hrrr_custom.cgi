#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

# Brian Blaylock
# June 8, 2017     # I accidentally made beef jerky in the crock pot last night


"""
Plots a sample image of HRRR near the fire.

Note: For CGI, cannot print anything to screen when outputting a .png file
"""

import matplotlib as mpl
mpl.use('Agg')
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
from BB_basemap.draw_maps import *
###from BB_downloads.HRRR_S3 import * ### import S3 or oper version, depending on date
from BB_data.grid_manager import pluck_point_new
#from BB_cmap.mycmap import reflect_ncdc
from BB_MesoWest.MesoWest_STNinfo import get_station_info
from BB_wx_calcs.wind import wind_uv_to_spd

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
    location = form['location'].value
except:
    plt.figure(1)
    plt.title('Something wrong with Location\nUse a valid MesoWest Station ID\nor iput a lat/lon (ex: 40.5,-111.5')
    plt.savefig(sys.stdout)	# Plot standard output.

try:
    plotcode = (form['plotcode'].value).split(',')
except:
    plt.figure(1)
    plt.title('Something wrong with the plotting codes')
    plt.savefig(sys.stdout)	# Plot standard output.

try:
    dsize = form['dsize'].value
except:
    plt.figure(1)
    plt.title('Something wrong with the domain size')
    plt.savefig(sys.stdout)	# Plot standard output.

try:
    background = form['background'].value
except:
    plt.figure(1)
    plt.title('Something wrong with the background')
    plt.savefig(sys.stdout)	# Plot standard output.

# configure the latitude/longitude based on the location requested
try:
    if ',' in location:
        # User put inputted a lat/lon point request
        lat, lon = location.split(',')
        lat = float(lat)
        lon = float(lon)
    else:
        # User requested a MesoWest station
        stninfo = get_station_info([location])
        lat = stninfo['LAT']
        lon = stninfo['LON']
except:
    plt.figure(1)
    plt.title('Something wrong with Location\nUse a valid MesoWest Station ID\nor iput a lat/lon (ex: 40.5,-111.5')
    plt.savefig(sys.stdout)	# Plot standard output.


def LU_MODIS21():
    C = np.array([[0, .4, 0],           # 1 Evergreen Needleleaf Forest
                  [0, .4, .2],          # ! 2 Evergreen Broadleaf Forest
                  [.2, .8, .2],         # 3 Deciduous Needleleaf Forest
                  [.2, .8, .4],         # 4 Deciduous Broadleaf Forest
                  [.2, .6, .2],         # 5 Mixed Forests
                  [.3, .7, 0],          # 6 Closed Shrublands
                  [.82, .41, .12],      # 7 Open Shurblands
                  [.74, .71, .41],      # 8 Woody Savannas
                  [1, .84, .0],         # 9 Savannas
                  [0, 1, 0],            # 10 Grasslands
                  [0, 1, 1],            # ! 11 Permanant Wetlands
                  [1, 1, 0],            # 12 Croplands
                  [1, 0, 0],            # 13 Urban and Built-up
                  [.7, .9, .3],         # ! 14 Cropland/Natual Vegation Mosaic
                  [1, 1, 1],            # ! 15 Snow and Ice
                  [.914, .914, .7],     # 16 Barren or Sparsely Vegetated
                  [.5, .7, 1],          # 17 Water (like oceans)
                  [.86, .08, .23],      # 18 Wooded Tundra
                  [.97, .5, .31],       # ! 19 Mixed Tundra
                  [.91, .59, .48],      # ! 20 Barren Tundra
                  [0, 0, .88]           # ! 21 Lake
                 ])

    cm = ListedColormap(C)

    labels = ['Evergreen Needleleaf Forest',
              'Evergreen Broadleaf Forest',
              'Deciduous Needleleaf Forest',
              'Deciduous Broadleaf Forest',
              'Mixed Forests',
              'Closed Shrublands',
              'Open Shrublands',
              'Woody Savannas',
              'Savannas',
              'Grasslands',
              'Permanent Wetlands',
              'Croplands',
              'Urban and Built-Up',
              'Cropland/Natural Vegetation Mosaic',
              'Snow and Ice',
              'Barren or Sparsely Vegetated',
              'Water',
              'Wooded Tundra',
              'Mixed Tundra',
              'Barren Tundra',
              'Lake']

    return cm, labels

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

# configure some setting based on the requested domain size
if dsize == 'small':
    plus_minus_latlon = .27
    barb_thin = 1
    cut = 15
elif dsize == 'medium':
    plus_minus_latlon = .75
    barb_thin = 2
    cut = 35
elif dsize == 'large':
    plus_minus_latlon = 2.5
    barb_thin = 6
    cut = 110
elif dsize == 'xlarge':
    plus_minus_latlon = 5
    barb_thin = 12
    cut = 210
elif dsize == 'xxlarge':   # If domain runs into HRRR boundary, then it'll fail
    plus_minus_latlon = 10
    barb_thin = 20
    cut = 430
elif dsize == 'xxxlarge':
    plus_minus_latlon = 20
    barb_thin = 20
    cut = 700


# Create Map Object for the domain
m = Basemap(resolution='i', projection='cyl',\
            llcrnrlon=lon-plus_minus_latlon, llcrnrlat=lat-plus_minus_latlon,\
            urcrnrlon=lon+plus_minus_latlon, urcrnrlat=lat+plus_minus_latlon,)

# Convert Valid Date to Run Date, adjusted by the forecast
DATE = DATE - timedelta(hours=fxx)

# If run DATE is today's date, then need to grab HRRR from NOMADS instead of Pando
today = datetime.now()
if DATE >= datetime(today.year, today.month, today.day):
    from BB_downloads.HRRR_oper import *
else:
    from BB_downloads.HRRR_S3 import *

got_latlon = False
bfr = cut

# Start the map image
plt.figure(1)
if background == 'arcgis':
    m.arcgisimage(service='World_Shaded_Relief', xpixels=700, verbose=False)
elif background == 'arcgisSat':
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=700, verbose=False)
elif background == 'terrain':
    # Get data
    H_ter = get_hrrr_variable(DATE, 'HGT:surface', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)
    if got_latlon is False:
        gridlat = H_ter['lat']
        gridlon = H_ter['lon']
        cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
        # Cut grid
        gridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        gridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        got_latlon = True
    H_land = get_hrrr_variable(DATE, 'LAND:surface', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)        

    # Cut variables
    H_ter['value'] = H_ter['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
    H_land['value'] = H_land['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]

    # Plot the terrain
    plt.contourf(gridlon, gridlat, H_ter['value'],
                 levels=range(0, 4000, 200),
                 cmap='Greys_r',
                 zorder=2)
    # Plot Water area
    plt.contour(gridlon, gridlat, H_land['value'],
                levels=[0, 1],
                colors='b',
                zorder=10)

elif background == 'landuse':
    # Get data
    H_LU = get_hrrr_variable(DATE, 'VGTYP:surface', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)
    if got_latlon is False:
        gridlat = H_LU['lat']
        gridlon = H_LU['lon']
        cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
        # Cut grid
        gridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        gridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        got_latlon = True

    # Cut variables
    H_LU['value'] = H_LU['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]

    # Plot the terrain
    cm, labels = LU_MODIS21()
    plt.pcolormesh(gridlon, gridlat, H_LU['value'],
                   cmap=cm, vmin=1, vmax=len(labels) + 1)

m.drawstates()
m.drawcountries()
plt.scatter(lon, lat, marker='+', c='r', s=100, zorder=1000)
plt.title('Center:%s Model:%s\n       Run: %s F%02d\nVaild: %s' % (location, model.upper(), DATE, fxx, DATE+timedelta(hours=fxx)))



if 'Barbs10mWind' in plotcode:
    # Get data
    H_u = get_hrrr_variable(DATE, 'UGRD:10 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)

    if got_latlon is False:
        gridlat = H_u['lat']
        gridlon = H_u['lon']
        cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
        # Cut grid
        gridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        gridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        got_latlon = True
    H_v = get_hrrr_variable(DATE, 'VGRD:10 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)

    # Cut variables
    H_u['value'] = H_u['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
    H_v['value'] = H_v['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]

    # Add to plot
    thin = barb_thin
    plt.barbs(gridlon[::thin,::thin], gridlat[::thin,::thin], H_u['value'][::thin,::thin], H_v['value'][::thin,::thin], zorder=200, length=5,barb_increments={'half':2.5, 'full':5,'flag':25})
    plt.ylabel(r'Barbs: half=2.5, full=5, flag=25 (ms$\mathregular{^{-1}}$)')

if ('Barbs80mWind' in plotcode) or ('Shade80mWind' in plotcode):
    # Get data
    H_u80 = get_hrrr_variable(DATE, 'UGRD:80 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)

    if got_latlon is False:
        gridlat = H_u80['lat']
        gridlon = H_u80['lon']
        cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
        # Cut grid
        gridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        gridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        got_latlon = True
    H_v80 = get_hrrr_variable(DATE, 'VGRD:80 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)

    # Cut variables
    H_u80['value'] = H_u80['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
    H_v80['value'] = H_v80['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]

    # Add Barbs to plot
    if 'Barbs80mWind' in plotcode:
        thin = barb_thin
        plt.barbs(gridlon[::thin, ::thin], gridlat[::thin, ::thin], H_u80['value'][::thin, ::thin], H_v80['value'][::thin, ::thin], zorder=200, length=6, color='darkred', barb_increments={'half':2.5, 'full':5,'flag':25})
        plt.ylabel(r'Barbs: half=2.5, full=5, flag=25 (ms$\mathregular{^{-1}}$)')
    if 'Shade80mWind' in plotcode:
        # Add to plot
        plt.contourf(gridlon, gridlat, wind_uv_to_spd(H_u80['value'], H_v80['value']),
                     levels=[10, 15, 20, 25],
                     colors=('yellow', 'orange', 'red'),
                     alpha=.5,
                     extend='max',
                     zorder=10)
        cb = plt.colorbar(orientation='horizontal', shrink=.5, pad=.01)
        cb.set_label(r'80 m Wind Speed (ms$\mathregular{^{-1}}$)')

if 'Shade10mWind' in plotcode:
    H_wind = get_hrrr_variable(DATE, 'WIND:10 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)
    if got_latlon is False:
        gridlat = H_wind['lat']
        gridlon = H_wind['lon']
        cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
        # Cut grid
        gridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        gridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        got_latlon = True

    # Cut variables
    H_wind['value'] = H_wind['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]

    # Add to plot
    plt.contourf(gridlon, gridlat, H_wind['value'],
                 levels=[10, 15, 20, 25],
                 colors=('yellow', 'orange', 'red'),
                 alpha=.4,
                 extend='max',
                 zorder=10)
    cb = plt.colorbar(orientation='horizontal', shrink=.5, pad=.01)
    cb.set_label(r'10 m Wind Speed (ms$\mathregular{^{-1}}$)')



if 'HatchSfcGust' in plotcode:
    H_gust = get_hrrr_variable(DATE, 'GUST:surface', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)
    if got_latlon is False:
        gridlat = H_gust['lat']
        gridlon = H_gust['lon']
        cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
        # Cut grid
        gridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        gridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        got_latlon = True

    # Cut variables
    H_gust['value'] = H_gust['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]

    # Add to plot
    plt.contourf(gridlon, gridlat, H_gust['value'],
                 levels=[0, 10, 15, 20, 25],
                 hatches=[None, '.', '\\\\', '*'],
                 colors='none',
                 extend='max',
                 zorder=10)
    cb = plt.colorbar(orientation='horizontal', shrink=.5, pad=.01)
    cb.set_label(r'Surface Wind Gust (ms$\mathregular{^{-1}}$)')
    plt.contour(gridlon, gridlat, H_gust['value'],
                levels=[10, 15, 20, 25],
                colors='k',
                zorder=10)

if 'FilldBZ' in plotcode or 'ContdBZ' in plotcode:
    # Get Data
    H_ref = get_hrrr_variable(DATE, 'REFC:entire atmosphere', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)
    if got_latlon is False:
        gridlat = H_ref['lat']
        gridlon = H_ref['lon']
        cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
        # Cut grid
        gridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        gridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        got_latlon = True

    # Cut variables
    H_ref['value'] = H_ref['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
    H_ref['value'] = np.ma.array(H_ref['value'])
    H_ref['value'][H_ref['value']==-10] = np.ma.masked
    
    # Add Contour to plot
    if 'ContdBZ' in plotcode:
        cREF = plt.contour(gridlon, gridlat, H_ref['value'], cmap=reflect_ncdc(), levels=range(10, 80, 10))
        plt.clabel(cREF, cREF.levels[::2], fmt='%2.0f', colors='k', fontsize=9)
        cb2 = plt.colorbar(orientation='horizontal', shrink=.5, pad=.01)
        cb2.set_label('Simulated Composite Reflectivity (dBZ)')

    # Add fill to plot
    if 'FilldBZ' in plotcode:
        plt.pcolormesh(gridlon, gridlat, H_ref['value'], cmap=reflect_ncdc(), vmax=80, vmin=0, alpha=.5)
        cb2 = plt.colorbar(orientation='horizontal', shrink=.5, pad=.01)
        cb2.set_label('Simulated Composite Reflectivity (dBZ)')

if 'Fill2mTemp' in plotcode or 'ContFreeze' in plotcode:
    # Get Data
    H_temp = get_hrrr_variable(DATE, 'TMP:2 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)
    if got_latlon is False:
        gridlat = H_temp['lat']
        gridlon = H_temp['lon']
        cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
        # Cut grid
        gridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        gridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        got_latlon = True

    # Cut variables
    H_temp['value'] = H_temp['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
    H_temp['value'] = H_temp['value'] - 273.15 # convert from Kelvin to Celsius

    # Add fill to plot
    if 'Fill2mTemp' in plotcode:
        plt.pcolormesh(gridlon, gridlat, H_temp['value'], cmap="Spectral_r", vmin=np.min(H_temp['value']), vmax=np.max(H_temp['value']), alpha=.3, zorder=1)
        cbT = plt.colorbar(orientation='horizontal', shrink=.5, pad=.01)
        cbT.set_label('2m Temperature (C)')
    # Add freezing contour to plot
    if 'ContFreeze' in plotcode:
        plt.contour(gridlon, gridlat, H_temp['value'], colors='b', levels=[0])

if 'Fill2mRH' in plotcode:
    # Get Data
    try:
        H_RH = get_hrrr_variable(DATE, 'RH:2 m', model=model, fxx=fxx, outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/', verbose=False, value_only=got_latlon)
        if got_latlon is False:
            gridlat = H_RH['lat']
            gridlon = H_RH['lon']
            cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
            # Cut grid
            gridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            gridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            got_latlon = True

        # Cut variables
        H_RH['value'] = H_RH['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        H_RH['value'] = H_RH['value']

        # Add fill to plot
        plt.pcolormesh(gridlon, gridlat, H_RH['value'], cmap="BrBG", vmin=np.min(H_RH['value']), vmax=np.max(H_RH['value']), alpha=.3, zorder=1)
        cbT = plt.colorbar(orientation='horizontal', shrink=.5, pad=.01)
        cbT.set_label('2m Relative Humidity (%)')

    except:
        print "!! Some errors getting the RH value."
        print "!! If you requested an old date, from HRRR version 1, there isn't a RH variable,"
        print "!! and this code doesn't get the dwpt and convert it to RH yet."

if 'ContTerrain' in plotcode:
    pass


plt.savefig(sys.stdout)	# Plot standard output.
