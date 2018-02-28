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
mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['savefig.dpi'] = 100     # For web
mpl.rcParams['figure.titleweight'] = 'bold'
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['axes.titlesize'] = 12
mpl.rcParams['figure.subplot.hspace'] = 0.01

# Colorbar
pad = 0.01
shrink = 0.7
# Map Resolution, 'l' - low, 'i' - intermediate, 'h' - high
map_res = 'l'


import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')
sys.path.append('/uufs/chpc.utah.edu/sys/pkg/python/2.7.3_rhel6/lib/python2.7/site-packages/')
from BB_basemap.draw_maps import draw_CONUS_HRRR_map, Basemap
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
    date = form['valid'].value
    DATE = datetime.strptime(date,'%Y-%m-%d_%H%M') # convert to datetime
except:
    plt.figure(1)
    plt.title('Something wrong with date')
    plt.savefig(sys.stdout)	# Plot standard output.

try:
    dsize = form['dsize'].value
except:
    plt.figure(1)
    plt.title('Something wrong with the domain size\noptions: small, medium, large, xlarge, xxlarge, xxxlarge, conus')
    plt.savefig(sys.stdout)	# Plot standard output.

if dsize != 'conus':
    try:
        location = form['location'].value
    except:
        plt.figure(1)
        plt.title('Something wrong with Location\nUse a valid MesoWest Station ID\nor input a lat/lon (ex: 40.5,-111.5)')
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

try:
    plotcode = (form['plotcode'].value).split(',')
except:
    plotcode = ['none', 'here']


# === Some housekeeping variables =============================================
# Valid DATE doesn't need to be adjusted becuase only f00 are availabe for hrrrX
fxx = 0

# Preload the latitude and longitude grid
latlonpath = '/uufs/chpc.utah.edu/common/home/horel-group7/Pando/hrrr/HRRR_latlon.h5'
latlonh5 = h5py.File(latlonpath, 'r')
gridlat = latlonh5['latitude'][:]
gridlon = latlonh5['longitude'][:]


# === Create map of the domain ================================================

if dsize == 'conus':
    mpl.rcParams['figure.figsize'] = [15, 3.6]
    mpl.rcParams['figure.subplot.wspace'] = 0.01
    barb_thin = 70
    alpha = 1
    #m = draw_CONUS_HRRR_map(res=map_res)
    m = np.load('HRRR_CONUS_map_object_'+map_res+'.npy').item()
    m.drawcountries(zorder=500)
    m.drawstates(zorder=500)
    m.drawcoastlines(zorder=500)
    m.fillcontinents(color='tan',lake_color='lightblue', zorder=0)
    m.drawmapboundary(fill_color='lightblue')
else:
    mpl.rcParams['figure.figsize'] = [15, 6]
    mpl.rcParams['figure.subplot.wspace'] = 0.05
    # configure some setting based on the requested domain size
    if dsize == 'small':
        plus_minus_latlon = .27      # +/- latlon box around center point
        barb_thin = 1               # Thin out excessive wind barbs
        bfr = 15                     # trim domain buffer
        alpha = .75                  # Alpha (pcolormesh transparency)
    elif dsize == 'medium':
        plus_minus_latlon = .75
        barb_thin = 2
        bfr = 35
        alpha = .75
    elif dsize == 'large':
        plus_minus_latlon = 2.5
        barb_thin = 6
        bfr = 110
        alpha = .75
    elif dsize == 'xlarge':
        plus_minus_latlon = 5
        barb_thin = 12
        bfr = 210
        alpha = .75
    elif dsize == 'xxlarge':   # If domain runs into HRRR boundary, then it'll fail
        plus_minus_latlon = 10
        barb_thin = 25
        bfr = 430
        alpha = .75
    elif dsize == 'xxxlarge':
        plus_minus_latlon = 15
        barb_thin = 35
        bfr = 700
        alpha = .75
    m = Basemap(resolution=map_res, projection='cyl',\
                area_thresh=3000,\
                llcrnrlon=lon-plus_minus_latlon, llcrnrlat=lat-plus_minus_latlon,\
                urcrnrlon=lon+plus_minus_latlon, urcrnrlat=lat+plus_minus_latlon,)
    m.drawstates(zorder=500)
    m.drawcountries(zorder=500)
    m.drawcoastlines(zorder=500)
    #if dsize == 'small' or dsize == 'medium':
    #    m.drawcounties()


# === Add a Background image ==================================================
# Start the map image
fig, (ax1, ax2, ax3) = plt.subplots(1,3)

plt.sca(ax1)
plt.title('HRRR')
m.drawstates(zorder=500)
m.drawcountries(zorder=500)
m.drawcoastlines(zorder=500)

plt.sca(ax2)
plt.title('HRRRx')
m.drawstates(zorder=500)
m.drawcountries(zorder=500)
m.drawcoastlines(zorder=500)

plt.sca(ax3)
plt.title('HRRRx - HRRR')
m.drawstates(zorder=500)
m.drawcountries(zorder=500)
m.drawcoastlines(zorder=500)

if dsize != 'conus':
    plt.sca(ax1)
    m.scatter(lon, lat, marker='+', c='tomato', s=100, zorder=1000, latlon=True)
    plt.sca(ax2)
    m.scatter(lon, lat, marker='+', c='tomato', s=100, zorder=1000, latlon=True)
    plt.sca(ax3)
    m.scatter(lon, lat, marker='+', c='tomato', s=100, zorder=1000, latlon=True)
    plt.suptitle('Center: %s\n%s' % (location, 'Run: %s F%02d' % (DATE.strftime('%Y-%m-%d %H:%M UTC'), fxx)), fontweight='bold')
else:
    plt.suptitle('%s' % ('Run: %s F%02d' % (DATE.strftime('%Y-%m-%d %H:%M UTC'), fxx)), fontweight='bold')
# =============================================================================

if 'LandUse' in plotcode:
    # Get data
    from BB_cmap.landuse_colormap import LU_MODIS21
    VGTYP = 'VGTYP:surface'
    xVGTYP = 'var discipline=2 center=59 local_table=1 parmcat=0 parm=198'
    H_LU = get_hrrr_variable(DATE, VGTYP,
                             model='hrrr', fxx=fxx,
                             outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                             verbose=False,
                             value_only=True)
    xH_LU = get_hrrr_variable(DATE, xVGTYP,
                              model='hrrrX', fxx=fxx,
                              outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                              verbose=False,
                              value_only=True)

    # Plot the terrain
    cm, labels = LU_MODIS21()
    
    plt.sca(ax1)
    m.pcolormesh(gridlon, gridlat, H_LU['value'],
                 cmap=cm, vmin=1, vmax=len(labels) + 1,
                 zorder=1,
                 latlon=True)
    plt.sca(ax2)
    m.pcolormesh(gridlon, gridlat, xH_LU['value'],
                 cmap=cm, vmin=1, vmax=len(labels) + 1,
                 zorder=1,
                 latlon=True)
    plt.sca(ax3)
    m.pcolormesh(gridlon, gridlat, xH_LU['value']-H_LU['value'],
                 cmap='bwr',
                 zorder=1,
                 latlon=True)
if 'TerrainWater' in plotcode:
    # Get data
    from BB_cmap.terrain_colormap import terrain_cmap_256
    H_ter = get_hrrr_variable(DATE, 'HGT:surface',
                              model='hrrr', fxx=fxx,
                              outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                              verbose=False, value_only=True)
    H_land = get_hrrr_variable(DATE, 'LAND:surface',
                               model='hrrr', fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)        
    xH_ter = get_hrrr_variable(DATE, 'HGT:surface',
                               model='hrrrX', fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    xH_land = get_hrrr_variable(DATE, 'LAND:surface',
                                model='hrrrX', fxx=fxx,
                                outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                                verbose=False, value_only=True)        

    # Make water a low value 
    H_ter['value'][H_land['value']==0]=-99
    xH_ter['value'][xH_land['value']==0]=-99

    plt.sca(ax1)
    m.pcolormesh(gridlon, gridlat, H_ter['value'], cmap=terrain_cmap_256(), latlon=True)
    cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink, ticks=[0, 1000, 2000, 3000, 4000])
    cb.set_label(r'Terrain Height (m)')
    plt.sca(ax2)
    m.pcolormesh(gridlon, gridlat, xH_ter['value'], cmap=terrain_cmap_256(), latlon=True)
    cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink, ticks=[0, 1000, 2000, 3000, 4000])
    cb.set_label(r'Terrain Height (m)')
    plt.sca(ax3)
    m.pcolormesh(gridlon, gridlat, xH_ter['value']-H_ter['value'], cmap='bwr', vmax=50, vmin=-50, latlon=True)
    cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
    cb.set_label(r'$\Delta$ Terrain Height (m)')


if '10mWind_Fill' in plotcode or '10mWind_Shade' in plotcode or '10mWind_Barb' in plotcode or '10mWind_Quiver' in plotcode:
    # Get data
    H_u = get_hrrr_variable(DATE, 'UGRD:10 m',
                            model='hrrr', fxx=fxx,
                            outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                            verbose=False, value_only=True)
    H_v = get_hrrr_variable(DATE, 'VGRD:10 m',
                            model='hrrr', fxx=fxx,
                            outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                            verbose=False, value_only=True)
    spd = wind_uv_to_spd(H_u['value'], H_v['value'])
    
    xH_u = get_hrrr_variable(DATE, 'UGRD:10 m',
                             model='hrrrX', fxx=fxx,
                             outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                             verbose=False, value_only=True)
    xH_v = get_hrrr_variable(DATE, 'VGRD:10 m',
                             model='hrrrX', fxx=fxx,
                             outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                             verbose=False, value_only=True)
    xspd = wind_uv_to_spd(xH_u['value'], xH_v['value'])
    
    vmax = np.max(spd)
    vmin = 0

    if '10mWind_Fill' in plotcode:
        plt.sca(ax1)
        m.pcolormesh(gridlon, gridlat, spd,
                     latlon=True,
                     cmap='magma_r',
                     vmax=vmax, vmin=vmin,
                     alpha=alpha)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'10 m Wind Speed (m s$\mathregular{^{-1}}$)')
        plt.sca(ax2)
        m.pcolormesh(gridlon, gridlat, xspd,
                     latlon=True,
                     cmap='magma_r',
                     vmax=vmax, vmin=vmin,
                     alpha=alpha)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'10 m Wind Speed (m s$\mathregular{^{-1}}$)')
        plt.sca(ax3)
        m.pcolormesh(gridlon, gridlat, xspd - spd,
                     latlon=True,
                     cmap='bwr',
                     vmax=10, vmin=-10,
                     alpha=alpha)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'$\Delta$ 10 m Wind Speed (m s$\mathregular{^{-1}}$)')

    if '10mWind_Shade' in plotcode:
        plt.sca(ax1)
        m.contourf(gridlon, gridlat, spd,
                    levels=[10, 15, 20, 25],
                    colors=('yellow', 'orange', 'red'),
                    alpha=alpha,
                    extend='max',
                    zorder=1,
                    latlon=True)
        cb = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cb.set_label(r'10 m Wind Speed (ms$\mathregular{^{-1}}$)')
        plt.sca(ax2)
        m.contourf(gridlon, gridlat, xspd,
                    levels=[10, 15, 20, 25],
                    colors=('yellow', 'orange', 'red'),
                    alpha=alpha,
                    extend='max',
                    zorder=1,
                    latlon=True)
        cb = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cb.set_label(r'10 m Wind Speed (ms$\mathregular{^{-1}}$)')
    
    if '10mWind_Barb' in plotcode or '10mWind_Quiver' in plotcode:
        # For small domain plots, trimming the edges significantly reduces barb plotting time
        if barb_thin < 20:
            cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
            Cgridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            Cgridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            H_u['value'] = H_u['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            H_v['value'] = H_v['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            xH_u['value'] = xH_u['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            xH_v['value'] = xH_v['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        else:
            Cgridlat = gridlat
            Cgridlon = gridlon

        thin = barb_thin
        # Add to plot
        if '10mWind_Barb' in plotcode:
            plt.sca(ax1)
            m.barbs(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                    H_u['value'][::thin,::thin], H_v['value'][::thin,::thin],
                    zorder=200, length=4.5,
                    barb_increments={'half':2.5, 'full':5,'flag':25},
                    latlon=True)
            plt.sca(ax2)
            m.barbs(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                    xH_u['value'][::thin,::thin], xH_v['value'][::thin,::thin],
                    zorder=200, length=4.5,
                    barb_increments={'half':2.5, 'full':5,'flag':25},
                    latlon=True)
        if '10mWind_Quiver' in plotcode:
            plt.sca(ax1)
            Q = m.quiver(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                         H_u['value'][::thin,::thin], H_v['value'][::thin,::thin],
                         zorder=350,
                         latlon=True)
            qk = plt.quiverkey(Q, .92, 0.07, 10, r'10 m s$^{-1}$',
                            labelpos='S',
                            coordinates='axes',
                            color='darkgreen')
            qk.text.set_backgroundcolor('w')
            plt.sca(ax2)
            Q = m.quiver(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                         xH_u['value'][::thin,::thin], xH_v['value'][::thin,::thin],
                         zorder=350,
                         latlon=True)
            qk = plt.quiverkey(Q, .92, 0.07, 10, r'10 m s$^{-1}$',
                            labelpos='S',
                            coordinates='axes',
                            color='darkgreen')
            qk.text.set_backgroundcolor('w')

if '80mWind_Fill' in plotcode or '80mWind_Shade' in plotcode or '80mWind_Barb' in plotcode or '80mWind_Quiver' in plotcode:
        # Get data
    H_u = get_hrrr_variable(DATE, 'UGRD:80 m',
                            model='hrrr', fxx=fxx,
                            outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                            verbose=False, value_only=True)
    H_v = get_hrrr_variable(DATE, 'VGRD:80 m',
                            model='hrrr', fxx=fxx,
                            outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                            verbose=False, value_only=True)
    spd = wind_uv_to_spd(H_u['value'], H_v['value'])
    xH_u = get_hrrr_variable(DATE, 'UGRD:80 m',
                            model='hrrrX', fxx=fxx,
                            outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                            verbose=False, value_only=True)
    xH_v = get_hrrr_variable(DATE, 'VGRD:80 m',
                            model='hrrrX', fxx=fxx,
                            outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                            verbose=False, value_only=True)
    xspd = wind_uv_to_spd(xH_u['value'], xH_v['value'])

    vmax=np.max(spd)
    vmin=0
    
    if '80mWind_Fill' in plotcode:
        plt.sca(ax1)
        m.pcolormesh(gridlon, gridlat, spd,
                     latlon=True,
                     cmap='magma_r',
                     vmax=vmax, vmin=vmin,
                     alpha=alpha)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'10 m Wind Speed (m s$\mathregular{^{-1}}$)')
        plt.sca(ax2)
        m.pcolormesh(gridlon, gridlat, xspd,
                     latlon=True,
                     cmap='magma_r',
                     vmax=vmax, vmin=vmin,
                     alpha=alpha)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'10 m Wind Speed (m s$\mathregular{^{-1}}$)')
        plt.sca(ax3)
        m.pcolormesh(gridlon, gridlat, xspd-spd,
                     latlon=True,
                     cmap='bwr',
                     vmax=10, vmin=-10,
                     alpha=alpha)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'10 m Wind Speed (m s$\mathregular{^{-1}}$)')

    if '80mWind_Shade' in plotcode:
        plt.sca(ax1)
        m.contourf(gridlon, gridlat, spd,
                    levels=[10, 15, 20, 25],
                    colors=('yellow', 'orange', 'red'),
                    alpha=alpha,
                    extend='max',
                    zorder=10,
                    latlon=True)
        cb = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cb.set_label(r'10 m Wind Speed (ms$\mathregular{^{-1}}$)')
        plt.sca(ax2)
        m.contourf(gridlon, gridlat, xspd,
                    levels=[10, 15, 20, 25],
                    colors=('yellow', 'orange', 'red'),
                    alpha=alpha,
                    extend='max',
                    zorder=10,
                    latlon=True)
        cb = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cb.set_label(r'10 m Wind Speed (ms$\mathregular{^{-1}}$)')
    
    if '80mWind_Barb' in plotcode or '80mWind_Quiver' in plotcode:
        # For small domain plots, trimming the edges significantly reduces barb plotting time
        if barb_thin < 20:
            cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
            Cgridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            Cgridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            H_u['value'] = H_u['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            H_v['value'] = H_v['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            xH_u['value'] = xH_u['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            xH_v['value'] = xH_v['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        else:
            Cgridlat = gridlat
            Cgridlon = gridlon

        # Add to plot
        thin = barb_thin
        if '80mWind_Barb' in plotcode:
            plt.sca(ax1)
            m.barbs(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                    H_u['value'][::thin,::thin], H_v['value'][::thin,::thin],
                    zorder=200, length=4.5, color='darkred',
                    barb_increments={'half':2.5, 'full':5,'flag':25},
                    latlon=True)
            
            plt.sca(ax2)
            m.barbs(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                    xH_u['value'][::thin,::thin], xH_v['value'][::thin,::thin],
                    zorder=200, length=4.5, color='darkred',
                    barb_increments={'half':2.5, 'full':5,'flag':25},
                    latlon=True)

        if '80mWind_Quiver' in plotcode:
            plt.sca(ax1)
            Q = m.quiver(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                         H_u['value'][::thin,::thin], H_v['value'][::thin,::thin],
                         zorder=350,
                         color='darkred',
                         latlon=True)
            qk = plt.quiverkey(Q, .92, 0.07, 10, r'10 m s$^{-1}$',
                            labelpos='S',
                            coordinates='axes',
                            color='darkgreen')
            qk.text.set_backgroundcolor('w')
            
            plt.sca(ax2)
            Q = m.quiver(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                         xH_u['value'][::thin,::thin], xH_v['value'][::thin,::thin],
                         zorder=350,
                         color='darkred',
                         latlon=True)
            qk = plt.quiverkey(Q, .92, 0.07, 10, r'10 m s$^{-1}$',
                            labelpos='S',
                            coordinates='axes',
                            color='darkgreen')
            qk.text.set_backgroundcolor('w')


if 'Gust_Hatch' in plotcode:
    H_gust = get_hrrr_variable(DATE, 'GUST:surface',
                               model='hrrr', fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    xH_gust = get_hrrr_variable(DATE, 'GUST:surface',
                               model='hrrrX', fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)

    # Add to plot
    plt.sca(ax1)
    m.contourf(gridlon, gridlat, H_gust['value'],
               levels=[0, 10, 15, 20, 25],
               hatches=[None, '.', '\\\\', '*'],
               colors='none',
               extend='max',
               zorder=10,
               latlon=True)
    cb = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cb.set_label(r'Surface Wind Gust (ms$\mathregular{^{-1}}$)')
    
    m.contour(gridlon, gridlat, H_gust['value'],
                levels=[10, 15, 20, 25],
                colors='k',
                zorder=10,
                latlon=True)
    
    plt.sca(ax2)
    m.contourf(gridlon, gridlat, xH_gust['value'],
               levels=[0, 10, 15, 20, 25],
               hatches=[None, '.', '\\\\', '*'],
               colors='none',
               extend='max',
               zorder=10,
               latlon=True)
    cb = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cb.set_label(r'Surface Wind Gust (ms$\mathregular{^{-1}}$)')
    
    m.contour(gridlon, gridlat, xH_gust['value'],
                levels=[10, 15, 20, 25],
                colors='k',
                zorder=10,
                latlon=True)
    
    plt.sca(ax3)
    m.pcolormesh(gridlon, gridlat, xH_gust['value']-H_gust['value'],
                     latlon=True,
                     cmap='bwr',
                     vmax=10, vmin=-10,
                     alpha=alpha)
    cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
    cb.set_label(r'$\Delta$ Surface Wind Gust (ms$\mathregular{^{-1}}$)')


if 'dBZ_Fill' in plotcode or 'dBZ_Contour' in plotcode:
    from BB_cmap.reflectivity_colormap import reflect_ncdc
    # Get Data
    REFC = 'REFC:entire'
    xREFC = 'var discipline=0 center=59 local_table=1 parmcat=16 parm=196'
    H_ref = get_hrrr_variable(DATE, REFC,
                              model='hrrr', fxx=fxx,
                              outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                              verbose=False, value_only=True)
    xH_ref = get_hrrr_variable(DATE, xREFC,
                              model='hrrrX', fxx=fxx,
                              outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                              verbose=False, value_only=True)

    # Mask values
    dBZ = H_ref['value']
    dBZ = np.ma.array(dBZ)
    dBZ[dBZ == -10] = np.ma.masked
    xdBZ = xH_ref['value']
    xdBZ = np.ma.array(xdBZ)
    xdBZ[xdBZ == -10] = np.ma.masked
    
    # Add Contour to plot
    if 'dBZ_Contour' in plotcode:
        plt.sca(ax1)
        cREF = m.contour(gridlon, gridlat, dBZ,
                         cmap=reflect_ncdc(),
                         levels=range(10, 80, 10),
                         latlon=True,
                         zorder=50)
        plt.clabel(cREF, cREF.levels[::2], fmt='%2.0f', colors='k', fontsize=9)
        plt.sca(ax2)
        cREF = m.contour(gridlon, gridlat, xdBZ,
                         cmap=reflect_ncdc(),
                         levels=range(10, 80, 10),
                         latlon=True,
                         zorder=50)
        plt.clabel(cREF, cREF.levels[::2], fmt='%2.0f', colors='k', fontsize=9)
        #cb2 = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        #cb2.set_label('Simulated Composite Reflectivity (dBZ)')

    # Add fill to plot
    if 'dBZ_Fill' in plotcode:
        plt.sca(ax1)
        m.pcolormesh(gridlon, gridlat, dBZ,
                     cmap=reflect_ncdc(),
                     vmax=80, vmin=0,
                     alpha=alpha,
                     latlon=True)
        cb2 = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cb2.set_label('Simulated Composite Reflectivity (dBZ)')
        plt.sca(ax2)
        m.pcolormesh(gridlon, gridlat, xdBZ,
                     cmap=reflect_ncdc(),
                     vmax=80, vmin=0,
                     alpha=alpha,
                     latlon=True)
        cb2 = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cb2.set_label('Simulated Composite Reflectivity (dBZ)')
        plt.sca(ax3)
        m.pcolormesh(gridlon, gridlat, xdBZ-dBZ,
                     cmap='bwr',
                     vmax=30, vmin=-30,
                     alpha=alpha,
                     latlon=True)
        cb2 = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cb2.set_label('$\Delta$ Simulated Composite Reflectivity (dBZ)')


if '2mTemp_Fill' in plotcode or '2mTemp_Freeze' in plotcode:
    # Get Data
    H_temp = get_hrrr_variable(DATE, 'TMP:2 m',
                               model='hrrr', fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    xH_temp = get_hrrr_variable(DATE, 'TMP:2 m',
                               model='hrrrX', fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    
    TMP = H_temp['value']-273.15
    xTMP = xH_temp['value']-273.15

    vmax = np.max(TMP)
    vmin = np.min(TMP)

    # Add fill to plot
    if '2mTemp_Fill' in plotcode:
        plt.sca(ax1)
        m.pcolormesh(gridlon, gridlat, TMP,
                       cmap="Spectral_r",
                       alpha=alpha,
                       vmax=vmax, vmin=vmin,
                       zorder=3, latlon=True)
        cbT = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cbT.set_label('2 m Temperature (C)')
        plt.sca(ax2)
        m.pcolormesh(gridlon, gridlat, xTMP,
                       cmap="Spectral_r",
                       alpha=alpha,
                       vmax=vmax, vmin=vmin,
                       zorder=3, latlon=True)
        cbT = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cbT.set_label('2 m Temperature (C)')
        plt.sca(ax3)
        m.pcolormesh(gridlon, gridlat, xTMP-TMP,
                       cmap="bwr",
                       alpha=alpha,
                       vmax=8, vmin=-8,
                       zorder=3, latlon=True)
        cbT = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cbT.set_label('2 m Temperature (C)')
    # Add freezing contour to plot
    if '2mTemp_Freeze' in plotcode:
        plt.sca(ax1)
        m.contour(gridlon, gridlat, TMP,
                  colors='b',
                  levels=[0],
                  zorder=400,
                  latlon=True)
        plt.sca(ax2)
        m.contour(gridlon, gridlat, xTMP,
                  colors='darkgreen',
                  levels=[0],
                  zorder=400,
                  latlon=True)
        plt.sca(ax3)
        m.contour(gridlon, gridlat, TMP,
                  colors='b',
                  levels=[0],
                  zorder=400,
                  latlon=True)
        m.contour(gridlon, gridlat, xTMP,
                  colors='darkgreen',
                  levels=[0],
                  zorder=400,
                  latlon=True)


if '2mRH_Fill' in plotcode:
    # Get Data
    try:
        H_RH = get_hrrr_variable(DATE, 'RH:2 m',
                                 model='hrrr', fxx=fxx,
                                 outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                                 verbose=False, value_only=True)
        xH_RH = get_hrrr_variable(DATE, 'RH:2 m',
                                 model='hrrrX', fxx=fxx,
                                 outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                                 verbose=False, value_only=True)

        # Add fill to plot
        plt.sca(ax1)
        m.pcolormesh(gridlon, gridlat, H_RH['value'], cmap="BrBG",
                     vmin=0, vmax=100,
                     zorder=3,
                     latlon=True)
        cbT = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cbT.set_label('2 m Relative Humidity (%)')
        plt.sca(ax2)
        m.pcolormesh(gridlon, gridlat, xH_RH['value'], cmap="BrBG",
                     vmin=0, vmax=100,
                     zorder=3,
                     latlon=True)
        cbT = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cbT.set_label('2 m Relative Humidity (%)')
        plt.sca(ax3)
        m.pcolormesh(gridlon, gridlat, xH_RH['value']-H_RH['value'], cmap="bwr",
                     vmin=20, vmax=-20,
                     zorder=3,
                     latlon=True)
        cbT = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cbT.set_label(r'$\Delta$ 2 m Relative Humidity (%)')

    except:
        print "!! Some errors getting the RH value."
        print "!! If you requested an old date, from HRRR version 1, there isn't a RH variable,"
        print "!! and this code doesn't get the dwpt and convert it to RH yet."


if 'MSLP_Contour' in plotcode or 'MSLP_Fill' in plotcode:
    MSLP = 'MSLMA:mean sea level'
    xMSLP = 'var discipline=0 center=59 local_table=1 parmcat=3 parm=198:mean sea level'
    H = get_hrrr_variable(DATE, MSLP,
                          model='hrrr', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    xH = get_hrrr_variable(DATE, xMSLP,
                          model='hrrrX', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)

    vmax = np.max(H['value'])/100.
    vmin = np.min(xH['value'])/100.

    if 'MSLP_Contour' in plotcode:
        plt.sca(ax1)
        CS = m.contour(gridlon, gridlat, H['value']/100., 
                       latlon=True,
                       levels=range(952, 1200, 4),
                       colors='k',
                       zorder=400)
        CS.clabel(inline=1, fmt='%2.f',
                  zorder=400)
        plt.sca(ax2)
        CS = m.contour(gridlon, gridlat, xH['value']/100., 
                       latlon=True,
                       levels=range(952, 1200, 4),
                       colors='k',
                       zorder=400)
        CS.clabel(inline=1, fmt='%2.f',
                  zorder=400)

    if 'MSLP_Fill' in plotcode:
        plt.sca(ax1)
        m.pcolormesh(gridlon, gridlat, H['value']/100., 
                     latlon=True, cmap='viridis',
                     vmax=vmax, vmin=vmin)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label('Mean Sea Level Pressure (hPa)')
        
        plt.sca(ax2)
        m.pcolormesh(gridlon, gridlat, xH['value']/100., 
                     latlon=True, cmap='viridis',
                     vmax=vmax, vmin=vmin)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label('Mean Sea Level Pressure (hPa)')
        
        plt.sca(ax3)
        m.pcolormesh(gridlon, gridlat, xH['value']/100.-H['value']/100., 
                     latlon=True, cmap='bwr',
                     vmax=5, vmin=-5)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'$\Delta$ Mean Sea Level Pressure (hPa)')


if '2mPOT_Fill' in plotcode:
    # Get Data
    H_temp = get_hrrr_variable(DATE, 'POT:2 m',
                               model='hrrr', fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    xH_temp = get_hrrr_variable(DATE, 'POT:2 m',
                               model='hrrrX', fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    
    TMP = H_temp['value']-273.15
    xTMP = xH_temp['value']-273.15

    vmax = np.max(TMP)
    vmin = np.min(TMP)

    plt.sca(ax1)
    m.pcolormesh(gridlon, gridlat, TMP,
                    cmap="Oranges",
                    alpha=alpha,
                    vmax=vmax, vmin=vmin,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label('2 m Potential Temperature (C)')
    plt.sca(ax2)
    m.pcolormesh(gridlon, gridlat, xTMP,
                    cmap="Oranges",
                    alpha=alpha,
                    vmax=vmax, vmin=vmin,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label('2 m Potential Temperature (C)')
    plt.sca(ax3)
    m.pcolormesh(gridlon, gridlat, xTMP-TMP,
                    cmap="bwr",
                    alpha=alpha,
                    vmax=8, vmin=-8,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'$\Delta$ 2 m Potential Temperature (C)')

if 'SkinTemp_Fill' in plotcode:
    # Get Data
    H_temp = get_hrrr_variable(DATE, 'TMP:surface',
                               model='hrrr', fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    xH_temp = get_hrrr_variable(DATE, 'TMP:surface',
                               model='hrrrX', fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    
    TMP = H_temp['value']-273.15
    xTMP = xH_temp['value']-273.15

    vmax = np.max(TMP)
    vmin = np.min(TMP)

    plt.sca(ax1)
    m.pcolormesh(gridlon, gridlat, TMP,
                    cmap="Spectral_r",
                    alpha=alpha,
                    vmax=vmax, vmin=vmin,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label('Skin Temperature (C)')
    plt.sca(ax2)
    m.pcolormesh(gridlon, gridlat, xTMP,
                    cmap="Spectral_r",
                    alpha=alpha,
                    vmax=vmax, vmin=vmin,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label('Skin Temperature (C)')
    plt.sca(ax3)
    m.pcolormesh(gridlon, gridlat, xTMP-TMP,
                    cmap="bwr",
                    alpha=alpha,
                    vmax=8, vmin=-8,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'$\Delta$ Skin Temperature (C)')


if 'SnowCover_Fill' in plotcode:
    # Get Data
    H = get_hrrr_variable(DATE, 'SNOWC',
                          model='hrrr', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    xH = get_hrrr_variable(DATE, 'SNOWC',
                          model='hrrrX', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)

    plt.sca(ax1)
    m.pcolormesh(gridlon, gridlat, H['value'],
                    cmap="Blues",
                    alpha=alpha,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label('Snow Cover (%)')
    plt.sca(ax2)
    m.pcolormesh(gridlon, gridlat, xH['value'],
                    cmap="Blues",
                    alpha=alpha,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label('Snow Cover (%)')
    plt.sca(ax3)
    m.pcolormesh(gridlon, gridlat, xH['value']-H['value'],
                    cmap="bwr",
                    alpha=alpha,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'$\Delta$ Snow Cover (%)')

if 'CAPE_Fill' in plotcode:
    # Get Data
    H = get_hrrr_variable(DATE, 'CAPE:surface',
                          model='hrrr', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    xH = get_hrrr_variable(DATE, 'CAPE:surface',
                          model='hrrrX', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)

    vmax = np.max(H['value'])
    vmin = np.min(H['value'])

    plt.sca(ax1)
    m.pcolormesh(gridlon, gridlat, H['value'],
                    cmap="Oranges",
                    alpha=alpha,
                    vmax=vmax, vmin=vmin,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'Surface CAPE (J kg$\mathregular{^{-1}}$)')

    plt.sca(ax2)
    m.pcolormesh(gridlon, gridlat, xH['value'],
                    cmap="Oranges",
                    alpha=alpha,
                    vmax=vmax, vmin=vmin,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'Surface CAPE (J kg$\mathregular{^{-1}}$)')

    plt.sca(ax3)
    m.pcolormesh(gridlon, gridlat, xH['value']-H['value'],
                    cmap="bwr",
                    alpha=alpha,
                    vmax=300, vmin=-300,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'$\Delta$ Surface CAPE (J kg$\mathregular{^{-1}}$)')

if 'CIN_Fill' in plotcode:
    # Get Data
    H = get_hrrr_variable(DATE, 'CIN:surface',
                          model='hrrr', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    xH = get_hrrr_variable(DATE, 'CIN:surface',
                          model='hrrrX', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)

    vmax = np.max(H['value'])
    vmin = np.min(H['value'])

    plt.sca(ax1)
    m.pcolormesh(gridlon, gridlat, H['value'],
                    cmap="BuPu_r",
                    alpha=alpha,
                    vmax=vmax, vmin=vmin,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'Surface CIN (J kg$\mathregular{^{-1}}$)')

    plt.sca(ax2)
    m.pcolormesh(gridlon, gridlat, xH['value'],
                    cmap="BuPu_r",
                    alpha=alpha,
                    vmax=vmax, vmin=vmin,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'Surface CIN (J kg$\mathregular{^{-1}}$)')

    plt.sca(ax3)
    m.pcolormesh(gridlon, gridlat, xH['value']-H['value'],
                    cmap="bwr",
                    alpha=alpha,
                    vmax=300, vmin=-300,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'$\Delta$ Surface CIN (J kg$\mathregular{^{-1}}$)')

if 'RedFlag_Fill' in plotcode:
    # generalized criteria for red flag warning
    # Winds (gusts) greater than 6.7 m/s and RH < 25%
    rf_RH = 25
    rf_WIND = 6.7

    # Get Data
    H_gust = get_hrrr_variable(DATE, 'GUST:surface',
                          model='hrrr', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    H_rh = get_hrrr_variable(DATE, 'RH:2 m',
                          model='hrrr', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    xH_gust = get_hrrr_variable(DATE, 'GUST:surface',
                          model='hrrrX', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    xH_rh = get_hrrr_variable(DATE, 'RH:2 m',
                          model='hrrrX', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    
    RedFlag = np.logical_and(H_gust['value'] >rf_WIND, H_rh['value'] < rf_RH)
    xRedFlag = np.logical_and(xH_gust['value'] >rf_WIND, xH_rh['value'] < rf_RH)

    plt.sca(ax1)
    m.pcolormesh(gridlon, gridlat, RedFlag,
                cmap="YlOrRd",
                alpha=alpha,
                zorder=4, latlon=True)        
    plt.xlabel(r'Red Flag Criteria: Winds > 6.7 m s$\mathregular{^{-1}}$ and RH < 25%')
    
    plt.sca(ax2)
    m.pcolormesh(gridlon, gridlat, xRedFlag,
                cmap="YlOrRd",
                alpha=alpha,
                zorder=4, latlon=True)        
    plt.xlabel(r'Red Flag Criteria: Winds > 6.7 m s$\mathregular{^{-1}}$ and RH < 25%')
    
    plt.sca(ax3)
    m.pcolormesh(gridlon, gridlat, xRedFlag-RedFlag,
                cmap="bwr",
                vmax=1, vmin=-1,
                alpha=alpha,
                zorder=4, latlon=True)        
    plt.xlabel(r'$\Delta$ Red Flag Criteria')

# =============================================================================
# Hack! Plot an extra HRRR variable not listed on the webpage hrrr_custom.html
# This extra argument will let you attempt to plot a different variable for
# a quicklook.
try:
    # Must be a variable from a line in the .idx file
    hrrrVAR = form['extraVAR'].value
    
    extraHRRR = get_hrrr_variable(DATE, hrrrVAR,
                          model='hrrr', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    xextraHRRR = get_hrrr_variable(DATE, hrrrVAR,
                          model='hrrrX', fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    
    vmax = np.max(extraHRRR['value'])
    vmin = np.min(extraHRRR['value'])
    
    plt.sca(ax1)
    m.pcolormesh(gridlon, gridlat, extraHRRR['value'],
                    cmap='viridis',
                    alpha=alpha,
                    vmax=vmax, vmin=vmin,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(hrrrVAR+' (units)')

    plt.sca(ax2)
    m.pcolormesh(gridlon, gridlat, xextraHRRR['value'],
                    cmap='viridis',
                    alpha=alpha,
                    vmax=vmax, vmin=vmin,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(hrrrVAR+' (units)')
    
    plt.sca(ax3)
    m.pcolormesh(gridlon, gridlat, xextraHRRR['value']-extraHRRR['value'],
                    cmap='bwr',
                    alpha=alpha,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(hrrrVAR+' (units)')
except:
    pass
# =============================================================================

plt.savefig(sys.stdout)	# Plot standard output.
