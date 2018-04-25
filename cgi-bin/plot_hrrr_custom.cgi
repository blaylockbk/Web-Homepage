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
            location = location.upper()
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

try:
    background = form['background'].value
except:
    plt.figure(1)
    plt.title('Something wrong with the background, options: arcgis, arcgisRoad, arcgisSat, terrain, landuse, none')
    plt.savefig(sys.stdout)	# Plot standard output.


# === Some housekeeping variables =============================================
VALIDDATE = DATE
# Convert Valid Date to Run Date, adjusted by the forecast
DATE = DATE - timedelta(hours=fxx)

# Preload the latitude and longitude grid
latlonpath = '/uufs/chpc.utah.edu/common/home/horel-group7/Pando/hrrr/HRRR_latlon.h5'
latlonh5 = h5py.File(latlonpath, 'r')

if model == 'hrrr' or model == 'hrrrX':
    gridlat = latlonh5['latitude'][:]
    gridlon = latlonh5['longitude'][:]
elif model == 'hrrrak':
    AK = get_hrrr_variable(datetime(2018, 2, 24, 15), 'TMP:2 m', fxx=0, model='hrrrak', verbose=False)
    gridlat = AK['lat']
    gridlon = AK['lon']

# === Create map of the domain ================================================
if dsize == 'conus' and model != 'hrrrak':
    barb_thin = 70
    alpha = 1
    t1= datetime.now()
    #m = draw_CONUS_HRRR_map(res=map_res)
    m = np.load('HRRR_CONUS_map_object_'+map_res+'.npy').item()
    m.drawcountries(zorder=500)
    m.drawstates(zorder=500)
    m.drawcoastlines(zorder=500)
    m.fillcontinents(color='tan',lake_color='lightblue', zorder=0)
    m.drawmapboundary(fill_color='lightblue')
    t2 = datetime.now()
elif dsize == 'conus' and model == 'hrrrak':
    barb_thin = 75
    alpha = 1
    m = draw_ALASKA_cyl_map(res=map_res)
    m.drawcountries(zorder=500)
    m.drawstates(zorder=500)
    m.drawcoastlines(zorder=500)
    m.fillcontinents(color='tan',lake_color='lightblue', zorder=0)
    m.drawmapboundary(fill_color='lightblue')
else:
    # configure some setting based on the requested domain size
    if dsize == 'small':
        plus_minus_latlon = .27      # +/- latlon box around center point
        barb_thin = 1               # Thin out excessive wind barbs
        arcgis_res = 1000            # ArcGIS image resolution
        bfr = 15                     # trim domain buffer
        alpha = .75                  # Alpha (pcolormesh transparency)
    elif dsize == 'medium':
        plus_minus_latlon = .75
        barb_thin = 2
        arcgis_res = 2500
        bfr = 35
        alpha = .75
    elif dsize == 'large':
        plus_minus_latlon = 2.5
        barb_thin = 6
        arcgis_res = 800
        bfr = 110
        alpha = .75
    elif dsize == 'xlarge':
        plus_minus_latlon = 5
        barb_thin = 12
        arcgis_res = 700
        bfr = 210
        alpha = .75
    elif dsize == 'xxlarge':   # If domain runs into HRRR boundary, then it'll fail
        plus_minus_latlon = 10
        barb_thin = 25
        arcgis_res = 700
        bfr = 430
        alpha = .75
    elif dsize == 'xxxlarge':
        plus_minus_latlon = 15
        barb_thin = 35
        arcgis_res = 1000
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
plt.figure(1)
if background == 'arcgis' and dsize != 'conus':
    m.arcgisimage(service='World_Shaded_Relief', xpixels=arcgis_res, verbose=False)
elif background == 'arcgisSat' and dsize != 'conus':
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=arcgis_res, verbose=False)
elif background == 'arcgisRoad' and dsize != 'conus':
    m.arcgisimage(service='NatGeo_World_Map', xpixels=arcgis_res, verbose=False)
elif background == 'terrain':
    # Get data
    H_ter = get_hrrr_variable(DATE, 'HGT:surface',
                              model=model, fxx=fxx,
                              outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                              verbose=False, value_only=True)
    H_land = get_hrrr_variable(DATE, 'LAND:surface',
                               model=model, fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)        

    # Plot the terrain
    m.contourf(gridlon, gridlat, H_ter['value'],
               levels=range(0, 4000, 200),
               cmap='Greys_r',
               zorder=1,
               latlon=True)
    # Plot Water area
    m.contour(gridlon, gridlat, H_land['value'],
              levels=[0, 1],
              colors='b',
              zorder=1,
              latlon=True)
elif background == 'landuse':
    # Get data
    from BB_cmap.landuse_colormap import LU_MODIS21
    if model=='hrrr':
        VGTYP = 'VGTYP:surface'
    else:
        VGTYP = 'var discipline=2 center=59 local_table=1 parmcat=0 parm=198'
    H_LU = get_hrrr_variable(DATE, VGTYP,
                             model=model, fxx=fxx,
                             outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                             verbose=False,
                             value_only=True)

    # Plot the terrain
    cm, labels = LU_MODIS21()
    m.pcolormesh(gridlon, gridlat, H_LU['value'],
                 cmap=cm, vmin=1, vmax=len(labels) + 1,
                 zorder=1,
                 latlon=True)

# === Figure Title ============================================================
if dsize != 'conus':
    m.scatter(lon, lat, marker='+', c='r', s=100, zorder=1000, latlon=True)
    plt.title('Center: %s\n%s' % (location, model.upper()), fontweight='bold')
else:
    plt.title('%s' % (model.upper()), fontweight='bold')
plt.title('Run: %s F%02d' % (DATE.strftime('%Y-%m-%d %H:%M UTC'), fxx), loc='left')
plt.title('Valid: %s' % (DATE+timedelta(hours=fxx)).strftime('%Y-%m-%d %H:%M UTC') , loc='right')
# =============================================================================


if '10mWind_Fill' in plotcode or '10mWind_Shade' in plotcode or '10mWind_Barb' in plotcode or '10mWind_Quiver' in plotcode or '10mWind_p95_fill' in plotcode:
    # Get data
    #H_u = get_hrrr_variable(DATE, 'UGRD:10 m',
    #                        model=model, fxx=fxx,
    #                        outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
    #                        verbose=False, value_only=True)
    #H_v = get_hrrr_variable(DATE, 'VGRD:10 m',
    #                        model=model, fxx=fxx,
    #                        outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
    #                        verbose=False, value_only=True)
    #spd = wind_uv_to_spd(H_u['value'], H_v['value'])
    H_UV = get_hrrr_variable(DATE, 'UVGRD:10 m',
                             model=model, fxx=fxx,
                             outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                             verbose=False, value_only=True)
    
    if '10mWind_Fill' in plotcode:
        m.pcolormesh(gridlon, gridlat, H_UV['SPEED'],
                     latlon=True,
                     cmap='magma_r',
                     vmin=0, alpha=alpha)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'10 m Wind Speed (m s$\mathregular{^{-1}}$)')

    if '10mWind_Shade' in plotcode:
        m.contourf(gridlon, gridlat, H_UV['SPEED'],
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
            H_UV['UGRD'] = H_UV['UGRD'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            H_UV['VGRD'] = H_UV['VGRD'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        else:
            Cgridlat = gridlat
            Cgridlon = gridlon

        thin = barb_thin
        # Add to plot
        if '10mWind_Barb' in plotcode:
            m.barbs(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                    H_UV['UGRD'][::thin,::thin], H_UV['VGRD'][::thin,::thin],
                    zorder=200, length=5.5,
                    barb_increments={'half':2.5, 'full':5,'flag':25},
                    latlon=True)
        if '10mWind_Quiver' in plotcode:
            Q = m.quiver(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                         H_UV['UGRD'][::thin,::thin], H_UV['VGRD'][::thin,::thin],
                         zorder=350,
                         units='inches',
                         scale=40,
                         latlon=True)
    
            qk = plt.quiverkey(Q, .92, 0.07, 10, r'10 m s$^{-1}$',
                            labelpos='S',
                            coordinates='axes',
                            color='magenta')
            qk.text.set_backgroundcolor('w')
    
    if '10mWind_p95_fill' in plotcode:
        DIR = '/uufs/chpc.utah.edu/common/home/horel-group2/blaylock/HRRR_OSG/hourly30/UVGRD_10_m/'
        FILE = 'OSG_HRRR_%s_m%02d_d%02d_h%02d_f00.h5' % (('UVGRD_10_m', VALIDDATE.month, VALIDDATE.day, VALIDDATE.hour))
        with h5py.File(DIR+FILE, 'r') as f:
            spd_p95 = f["p95"][:]
        masked = H_UV['SPEED']-spd_p95
        masked = np.ma.array(masked)
        masked[masked < 0] = np.ma.masked
        
        m.pcolormesh(gridlon, gridlat, masked,
             vmax=10, vmin=0,
             latlon=True,
             cmap='viridis',
             alpha=alpha)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'10 m Wind Speed exceeding 95th Percentile (m s$\mathregular{^{-1}}$)')

if '80mWind_Fill' in plotcode or '80mWind_Shade' in plotcode or '80mWind_Barb' in plotcode or '80mWind_Quiver' in plotcode:
        # Get data
    #H_u = get_hrrr_variable(DATE, 'UGRD:80 m',
    #                        model=model, fxx=fxx,
    #                        outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
    #                        verbose=False, value_only=True)
    #H_v = get_hrrr_variable(DATE, 'VGRD:80 m',
    #                        model=model, fxx=fxx,
    #                        outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
    #                        verbose=False, value_only=True)
    #spd = wind_uv_to_spd(H_u['value'], H_v['value'])
    H_UV = get_hrrr_variable(DATE, 'UVGRD:80 m',
                             model=model, fxx=fxx,
                             outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                             verbose=False, value_only=True)

    if '80mWind_Fill' in plotcode:
        m.pcolormesh(gridlon, gridlat, H_UV['SPEED'],
                     latlon=True,
                     cmap='magma_r',
                     vmin=0, alpha=alpha)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'10 m Wind Speed (m s$\mathregular{^{-1}}$)')

    if '80mWind_Shade' in plotcode:
        m.contourf(gridlon, gridlat, H_UV['SPEED'],
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
            H_UV['UGRD'] = H_UV['UGRD'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            H_UV['VGRD'] = H_UV['VGRD'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        else:
            Cgridlat = gridlat
            Cgridlon = gridlon

        # Add to plot
        thin = barb_thin
        if '80mWind_Barb' in plotcode:
            m.barbs(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                    H_UV['UGRD'][::thin,::thin], H_UV['VGRD'][::thin,::thin],
                    zorder=200, length=5.5, color='darkred',
                    barb_increments={'half':2.5, 'full':5,'flag':25},
                    latlon=True)
        if '80mWind_Quiver' in plotcode:
            Q = m.quiver(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                         H_UV['UGRD'][::thin,::thin], H_UV['VGRD'][::thin,::thin],
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
                               model=model, fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)

    # Add to plot
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


if 'dBZ_Fill' in plotcode or 'dBZ_Contour' in plotcode or 'dBZ20_Contour' in plotcode or 'dBZ30_Contour' in plotcode or 'dBZ40_Contour' in plotcode:
    from BB_cmap.reflectivity_colormap import reflect_ncdc
    # Get Data
    if model == 'hrrr':
        REFC = 'REFC:entire'
    elif model == 'hrrrX' or model == 'hrrrAK':
        REFC = 'var discipline=0 center=59 local_table=1 parmcat=16 parm=196'
    H_ref = get_hrrr_variable(DATE, REFC,
                              model=model, fxx=fxx,
                              outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                              verbose=False, value_only=True)

    # Mask values
    dBZ = H_ref['value']
    dBZ = np.ma.array(dBZ)
    dBZ[dBZ == -10] = np.ma.masked
    
    # Add Contour to plot
    if 'dBZ_Contour' in plotcode:
        cREF = m.contour(gridlon, gridlat, dBZ,
                         cmap=reflect_ncdc(),
                         levels=range(10, 80, 10),
                         latlon=True,
                         zorder=50)
        plt.clabel(cREF, cREF.levels[::2], fmt='%2.0f', colors='k', fontsize=9)

    if 'dBZ20_Contour' in plotcode:
        cREF = m.contour(gridlon, gridlat, dBZ,
                         levels=[20],
                         colors='green',
                         latlon=True,
                         zorder=50)
    if 'dBZ30_Contour' in plotcode:
        cREF = m.contour(gridlon, gridlat, dBZ,
                         levels=[30],
                         colors='yellowgreen',
                         latlon=True,
                         zorder=50)    
    if 'dBZ40_Contour' in plotcode:
        cREF = m.contour(gridlon, gridlat, dBZ,
                         levels=[40],
                         colors='darkorange',
                         latlon=True,
                         zorder=50)

    # Add fill to plot
    if 'dBZ_Fill' in plotcode:
        m.pcolormesh(gridlon, gridlat, dBZ,
                     cmap=reflect_ncdc(),
                     vmax=80, vmin=0,
                     alpha=alpha,
                     latlon=True)
        cb2 = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cb2.set_label('Simulated Composite Reflectivity (dBZ)')


if '2mDPT_p95p05_fill' in plotcode:
    H_dpt = get_hrrr_variable(DATE, 'DPT:2 m',
                            model=model, fxx=fxx,
                            outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                            verbose=False, value_only=True)

    DIR = '/uufs/chpc.utah.edu/common/home/horel-group2/blaylock/HRRR_OSG/hourly30/DPT_2_m/'
    FILE = 'OSG_HRRR_%s_m%02d_d%02d_h%02d_f00.h5' % (('DPT_2_m', VALIDDATE.month, VALIDDATE.day, VALIDDATE.hour))

    ### Plot Dew Point Depression
    with h5py.File(DIR+FILE, 'r') as f:
        dpt_p05 = f["p05"][:]
    masked = H_dpt['value']-dpt_p05 # both these datasets are in Kelvin, but when we take the difference it is in Celsius
    masked = np.ma.array(masked)
    masked[masked > 0] = np.ma.masked
    
    mesh_depression = m.pcolormesh(gridlon, gridlat, masked,
                                   vmax=10, vmin=-10,
                                   latlon=True,
                                   cmap='BrBG')
    
    ### Plot Dew Point Exceedance
    with h5py.File(DIR+FILE, 'r') as f:
        dpt_p95 = f["p95"][:]
    masked = H_dpt['value']-dpt_p95 # both these datasets are in Kelvin, but when we take the difference it is in Celsius
    masked = np.ma.array(masked)
    masked[masked < 0] = np.ma.masked

    mesh_exceedance = m.pcolormesh(gridlon, gridlat, masked,
                                   vmax=10, vmin=-10,
                                   latlon=True,
                                   cmap='BrBG')

if '2mTemp_Fill' in plotcode or '2mTemp_Freeze' in plotcode or '2mTemp_p95p05_fill' in plotcode:
    # Get Data
    H_temp = get_hrrr_variable(DATE, 'TMP:2 m',
                               model=model, fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    
    TMP = H_temp['value']-273.15

    # Add fill to plot
    if '2mTemp_Fill' in plotcode:
        m.pcolormesh(gridlon, gridlat, TMP,
                       cmap="Spectral_r",
                       alpha=alpha,
                       zorder=3, latlon=True)
        cbT = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cbT.set_label('2 m Temperature (C)')
    # Add freezing contour to plot
    if '2mTemp_Freeze' in plotcode:
        m.contour(gridlon, gridlat, TMP,
                  colors='b',
                  levels=[0],
                  zorder=400,
                  latlon=True)
    
    if '2mTemp_p95p05_fill' in plotcode:
        DIR = '/uufs/chpc.utah.edu/common/home/horel-group2/blaylock/HRRR_OSG/hourly30/TMP_2_m/'
        FILE = 'OSG_HRRR_%s_m%02d_d%02d_h%02d_f00.h5' % (('TMP_2_m', VALIDDATE.month, VALIDDATE.day, VALIDDATE.hour))

        ### Plot Temperature Depression
        with h5py.File(DIR+FILE, 'r') as f:
            tmp_p05 = f["p05"][:]
        masked = H_temp['value']-tmp_p05 # both these datasets are in Kelvin, but when we take the difference it is in Celsius
        masked = np.ma.array(masked)
        masked[masked > 0] = np.ma.masked
        
        mesh_depression = m.pcolormesh(gridlon, gridlat, masked,
                                    vmax=10, vmin=-10,
                                    latlon=True,
                                    cmap='bwr')
        
        ### Plot Temperature Exceedance
        with h5py.File(DIR+FILE, 'r') as f:
            tmp_p95 = f["p95"][:]
        masked = H_temp['value']-tmp_p95 # both these datasets are in Kelvin, but when we take the difference it is in Celsius
        masked = np.ma.array(masked)
        masked[masked < 0] = np.ma.masked

        mesh_exceedance = m.pcolormesh(gridlon, gridlat, masked,
                                    vmax=10, vmin=-10,
                                    latlon=True,
                                    cmap='bwr')
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'5$\mathregular{^{th}}$/95$\mathregular{^{th}}$ percentile 2 m Temperature Depression/Exceedance (C)')


if '2mRH_Fill' in plotcode:
    # Get Data
    try:
        H_RH = get_hrrr_variable(DATE, 'RH:2 m',
                                 model=model, fxx=fxx,
                                 outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                                 verbose=False, value_only=True)
        ''' RH Calculated
        H_DPT = get_hrrr_variable(DATE, 'DPT:2 m',
                                    model=model, fxx=fxx,
                                    outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                                    verbose=False, value_only=True)
        H_TMP = get_hrrr_variable(DATE, 'TMP:2 m',
                                model=model, fxx=fxx,
                                outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                                verbose=False, value_only=True)
        H_rh = Tempdwpt_to_RH(H_TMP['value']-273.15, H_DPT['value']-273.15)
        '''
        # Add fill to plot
        m.pcolormesh(gridlon, gridlat, H_RH['value'], cmap="BrBG",
                     vmin=0, vmax=100,
                     zorder=3,
                     latlon=True)
        cbT = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cbT.set_label('2 m Relative Humidity (%)')

    except:
        print "!! Some errors getting the RH value."
        print "!! If you requested an old date, from HRRR version 1, there isn't a RH variable,"
        print "!! and this code doesn't get the dwpt and convert it to RH yet."

if '700Temp_Fill' in plotcode or '700Temp_-12c' in plotcode:
    # Get Data
    H_temp = get_hrrr_variable(DATE, 'TMP:700 mb',
                               model=model, fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)

    TMP = H_temp['value']-273.15

    # Add fill to plot
    if '700Temp_Fill' in plotcode:
        m.pcolormesh(gridlon, gridlat, TMP,
                     cmap="Spectral_r",
                     alpha=alpha,
                     zorder=3, latlon=True)
        cbT = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cbT.set_label('700 mb Temperature (C)')
    # Add -12 C contour to plot
    if '700Temp_-12c' in plotcode:
        m.contour(gridlon, gridlat, TMP,
                  colors='b',
                  levels=[-12],
                  latlon=True,
                  zorder=400)

if '700RH_Fill' in plotcode:
    # Get Data and calculate RH from temperature and dew point
    H_DPT = get_hrrr_variable(DATE, 'DPT:700 mb',
                              model=model, fxx=fxx,
                              outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                              verbose=False, value_only=True)
    H_TMP = get_hrrr_variable(DATE, 'TMP:700 mb',
                              model=model, fxx=fxx,
                              outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                              verbose=False, value_only=True)
    H_rh = Tempdwpt_to_RH(H_TMP['value']-273.15, H_DPT['value']-273.15)
    
    # Add fill to plot
    m.pcolormesh(gridlon, gridlat, H_rh, cmap="BrBG",
                 vmin=0, vmax=100,
                 zorder=3,
                 latlon=True)
    cbT = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
    cbT.set_label('700 mb Relative Humidity (%)')


if '500HGT_Contour' in plotcode:
    H_500 = get_hrrr_variable(DATE, 'HGT:500 mb',
                              model=model, fxx=fxx,
                              outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                              verbose=False, value_only=True)

    CS = m.contour(gridlon, gridlat, H_500['value'], 
                    levels=range(5040, 6181, 60),
                    linewidths=1.7,
                    colors='k', 
                    latlon=True,
                    zorder=400)
    plt.clabel(CS, inline=1, fmt='%2.f')


if '500Wind_Fill' in plotcode or '500Wind_Barb' in plotcode or '500Vort_Fill' in plotcode or '500Conv_Fill' in plotcode or '500Wind_Quiver' in plotcode:
    H_u = get_hrrr_variable(DATE, 'UGRD:500 mb',
                            model=model, fxx=fxx,
                            outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                            verbose=False, value_only=True)
    H_v = get_hrrr_variable(DATE, 'VGRD:500 mb',
                            model=model, fxx=fxx,
                            outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                            verbose=False, value_only=True)

    if '500Wind_Fill' in plotcode:
        spd = wind_uv_to_spd(H_u['value'], H_v['value'])

        m.pcolormesh(gridlon, gridlat, spd,
                    latlon=True, cmap='BuPu', vmin=0)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'500 mb Wind Speed (m s$\mathregular{^{-1}}$)')

    if '500Conv_Fill' in plotcode or '500Vort_Fill' in plotcode:
        dudx, dudy = np.gradient(H_u['value'], 3, 3)
        dvdx, dvdy = np.gradient(H_v['value'], 3, 3)
        if '500Vort_Fill' in plotcode:    
            vorticity = dvdx - dudy
            # Mask values
            vort = vorticity
            vort = np.ma.array(vort)
            vort[np.logical_and(vort < .05, vort > -.05) ] = np.ma.masked

            m.pcolormesh(gridlon, gridlat, vort,
                        latlon=True, cmap='bwr',
                        vmax=np.max(vort),
                        vmin=-np.max(vort))
            cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
            cb.set_label(r'500 mb Vorticity (s$\mathregular{^{-1}}$)')
        if '500Conv_Fill' in plotcode:
            convergence = dudx + dvdy
            # Mask values
            conv = convergence
            conv = np.ma.array(conv)
            conv[np.logical_and(conv < .05, conv > -.05) ] = np.ma.masked

            m.pcolormesh(gridlon, gridlat, conv,
                        latlon=True, cmap='bwr',
                        vmax=np.max(conv),
                        vmin=-np.max(conv))
            cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
            cb.set_label(r'500 mb Convergence (s$\mathregular{^{-1}}$)')

    if '500Wind_Barb' in plotcode or '500Wind_Quiver' in plotcode:        
        # For small domain plots, trimming the edges significantly reduces barb plotting time
        if barb_thin < 20:
            cut_v, cut_h = pluck_point_new(lat, lon, gridlat, gridlon)
            Cgridlat = gridlat[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            Cgridlon = gridlon[cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            H_u['value'] = H_u['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
            H_v['value'] = H_v['value'][cut_v-bfr:cut_v+bfr, cut_h-bfr:cut_h+bfr]
        else:
            Cgridlat = gridlat
            Cgridlon = gridlon
        thin = barb_thin
        if '500Wind_Barb' in plotcode:
            m.barbs(Cgridlon[::thin, ::thin], Cgridlat[::thin, ::thin], H_u['value'][::thin, ::thin], H_v['value'][::thin, ::thin],
                    zorder=200, length=6, color='navy',
                    barb_increments={'half':2.5, 'full':5,'flag':25},
                    latlon=True)
            #plt.ylabel(r'Barbs: half=2.5, full=5, flag=25 (ms$\mathregular{^{-1}}$)')
        if '500Wind_Quiver' in plotcode:
            Q = m.quiver(Cgridlon[::thin,::thin], Cgridlat[::thin,::thin],
                         H_u['value'][::thin,::thin], H_v['value'][::thin,::thin],
                         zorder=350,
                         color='navy',
                         latlon=True)
    
            qk = plt.quiverkey(Q, .92, 0.07, 30, r'30 m s$\mathregular{^{-1}}$',
                            labelpos='S',
                            coordinates='axes',
                            color='darkgreen')
            qk.text.set_backgroundcolor('w')

if 'MSLP_Contour' in plotcode or 'MSLP_Fill' in plotcode:
    H = get_hrrr_variable(DATE, 'MSLMA:mean sea level',
                          model=model, fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)

    if 'MSLP_Contour' in plotcode:
        CS = m.contour(gridlon, gridlat, H['value']/100., 
                       latlon=True,
                       levels=range(952, 1200, 4),
                       colors='k',
                       zorder=400)
        CS.clabel(inline=1, fmt='%2.f',
                  zorder=400)

    if 'MSLP_Fill' in plotcode:
        m.pcolormesh(gridlon, gridlat, H['value']/100., 
               latlon=True, cmap='viridis')

        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label('Mean Sea Level Pressure (hPa)')


if '2mPOT_Fill' in plotcode:
    # Get Data
    H_temp = get_hrrr_variable(DATE, 'POT:2 m',
                               model=model, fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    
    TMP = H_temp['value']-273.15

    m.pcolormesh(gridlon, gridlat, TMP,
                    cmap="Oranges",
                    alpha=alpha,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label('2 m Potential Temperature (C)')

if 'SkinTemp_Fill' in plotcode:
    # Get Data
    H_temp = get_hrrr_variable(DATE, 'TMP:surface',
                               model=model, fxx=fxx,
                               outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                               verbose=False, value_only=True)
    
    TMP = H_temp['value']-273.15

    m.pcolormesh(gridlon, gridlat, TMP,
                    cmap="Spectral_r",
                    alpha=alpha,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label('Skin Temperature (C)')


if 'AccumPrecip_Fill' in plotcode or '1hrPrecip_Fill' in plotcode:
    #import matplotlib.colors
    #cmap = matplotlib.colors.LinearSegmentedColormap.from_list("Precip", ["#00db16", "blue", "#d10000", 'black'])
    cdict3 = {'red':  ((0.0, 0.0, 0.0),
                   (0.25, 1.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),
            'green': ((0.0, 0.7, 0.7),
                    (0.25, 1.0, 1.0),
                    (0.5, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

            'blue':  ((0.0, 0.18, 0.18),
                    (0.25, 1.0, 1.0),
                    (0.5, 1.0, 1.0),
                    (1.0, 0.0, 0.0))
            }
    plt.register_cmap(name='BlueRed3', data=cdict3)
    cmap = 'BlueRed3'
    
    if 'AccumPrecip_Fill' in plotcode:
        # Get Data
        H = get_hrrr_variable(DATE, 'APCP:surface:0',
                                model=model, fxx=fxx,
                                outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                                verbose=False, value_only=True)
        # Mask values
        prec = H['value']
        prec = np.ma.array(prec)
        prec[prec == 0] = np.ma.masked

        m.pcolormesh(gridlon, gridlat, prec,
                        cmap='BlueRed3',
                        alpha=alpha,
                        vmin=.25,
                        zorder=3, latlon=True)
        cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
        cbS.set_label('Accumulated Precipitation since F00 (mm)')

    if '1hrPrecip_Fill' in plotcode:
        # Get Data
        H = get_hrrr_variable(DATE, 'APCP:surface',
                                model=model, fxx=fxx,
                                outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                                verbose=False, value_only=True)
        # Mask values
        prec = H['value']
        prec = np.ma.array(prec)
        prec[prec == 0] = np.ma.masked

        m.pcolormesh(gridlon, gridlat, prec,
                        cmap='BlueRed3',
                        alpha=alpha,
                        vmin=.25, vmax=20,
                        zorder=3, latlon=True)
        cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad, extend="max",)
        cbS.set_label('1 hour Accumulated Precipitation (mm)')

if 'SnowCover_Fill' in plotcode:
    # Get Data
    H = get_hrrr_variable(DATE, 'SNOWC',
                          model=model, fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)

    # Mask values
    snow = H['value']
    snow = np.ma.array(snow)
    snow[snow == 0] = np.ma.masked

    m.pcolormesh(gridlon, gridlat, snow,
                    cmap="Blues",
                    alpha=alpha,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label('Snow Cover (%)')

if 'PWAT_Fill' in plotcode:
    # Get Data
    H = get_hrrr_variable(DATE, 'PWAT:entire',
                          model=model, fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)

    m.pcolormesh(gridlon, gridlat, H['value'],
                    cmap="RdYlGn",
                    alpha=alpha,
                    vmin=0,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'Vertically Integrated Liquid Water (kg m$\mathregular{^{-2}}$)')

if 'CAPE_Fill' in plotcode:
    # Get Data
    H = get_hrrr_variable(DATE, 'CAPE:surface',
                          model=model, fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)

    # Mask values
    cape = H['value']
    cape = np.ma.array(cape)
    cape[cape == 0] = np.ma.masked

    m.pcolormesh(gridlon, gridlat, cape,
                    cmap="Oranges",
                    alpha=alpha,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'Surface CAPE (J kg$\mathregular{^{-1}}$)')

if 'CIN_Fill' in plotcode:
    # Get Data
    H = get_hrrr_variable(DATE, 'CIN:surface',
                          model=model, fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)

    # Mask values
    cin = H['value']
    cin = np.ma.array(cin)
    cin[cin == 0] = np.ma.masked

    m.pcolormesh(gridlon, gridlat, cin,
                    cmap="BuPu",
                    alpha=alpha,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(r'Surface CIN (J kg$\mathregular{^{-1}}$)')

if 'RedFlag_Fill' in plotcode or 'RedFlag_Contour' in plotcode or 'RedFlagPot_Fill' in plotcode:
    # generalized criteria for red flag warning
    # Winds (gusts) greater than 6.7 m/s and RH < 25%
    rf_RH = 25
    rf_WIND = 6.7

    # Get Data
    H_gust = get_hrrr_variable(DATE, 'GUST:surface',
                          model=model, fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    H_rh = get_hrrr_variable(DATE, 'RH:2 m',
                          model=model, fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    
    RedFlag = np.logical_and(H_gust['value'] >rf_WIND, H_rh['value'] < rf_RH)
    if 'RedFlag_Contour' in plotcode:
        try:
            CS = m.contour(gridlon, gridlat, RedFlag, 
                            latlon=True,
                            colors='maroon',
                            zorder=400)
        except:
            # maybe there isn't any contours in this domain
            pass

    if 'RedFlag_Fill' in plotcode:
        RedFlag = np.ma.array(RedFlag)
        RedFlag[RedFlag == 0] = np.ma.masked 
        m.pcolormesh(gridlon, gridlat, RedFlag,
                    cmap="YlOrRd_r",
                    alpha=alpha,
                    zorder=4, latlon=True)

    if 'RedFlagPot_Fill' in plotcode:
        cdict3 = {'red':  ((0.0,  1.0, 1.0),
                           (0.5,  0.5, 0.5),
                           (0.5,  1.0, 1.0),
                           (1.0,  0.4, 0.4)),

                'green': ((0.0,  1.0, 1.0),
                          (0.5,  0.5, 0.5),
                          (0.5,  0.4, 0.4),
                          (1.0,  0.0, 0.0)),

                'blue':  ((0.0,  1.0, 1.0),
                          (0.5,  0.5, 0.5),
                          (0.5,  0.0, 0.0),
                          (1.0,  0.0, 0.0))
                }

        plt.register_cmap(name='FirePot', data=cdict3)
        
        # Definate Red Flag Area:
        RED_FLAG = np.logical_and(H_rh['value'] < rf_RH,
                                  H_gust['value'] > rf_WIND)
        # Linear Equation
        b = (rf_RH-rf_WIND)*(rf_RH/rf_WIND)
        z = -(rf_RH/rf_WIND)*(H_rh['value']-H_gust['value'])+b
        
        m.pcolormesh(gridlon, gridlat, z,
                     cmap="FirePot",
                     alpha=alpha,
                     vmax=200, vmin=-200,
                     zorder=3,
                     latlon=True)
        cb = plt.colorbar(orientation='horizontal', pad=pad, shrink=shrink)
        cb.set_label(r'Red Flag Potential')

        m.contour(gridlon, gridlat, z,
                  colors='k',
                  levels=[0],
                  zorder=3,
                  latlon=True)
        m.contour(gridlon, gridlat, RED_FLAG,
                  colors='darkred',
                  levels=[0],
                  zorder=3,
                  latlon=True)
        
    
    plt.xlabel(r'Red Flag Criteria: Winds > 6.7 m s$\mathregular{^{-1}}$ and RH < 25%')


# =============================================================================
# Hack! Plot an extra HRRR variable not listed on the webpage hrrr_custom.html
# This extra argument will let you attempt to plot a different variable for
# a quicklook.
try:
    # Must be a variable from a line in the .idx file
    hrrrVAR = form['extraVAR'].value
    extraHRRR = get_hrrr_variable(DATE, hrrrVAR,
                          model=model, fxx=fxx,
                          outDIR='/uufs/chpc.utah.edu/common/home/u0553130/temp/',
                          verbose=False, value_only=True)
    m.pcolormesh(gridlon, gridlat, extraHRRR['value'],
                    cmap='viridis',
                    alpha=alpha,
                    zorder=3, latlon=True)
    cbS = plt.colorbar(orientation='horizontal', shrink=shrink, pad=pad)
    cbS.set_label(hrrrVAR+' (units)')
except:
    pass
# =============================================================================

#plt.ylabel('Section Timer:%s\nFull Timer:%s' % (t2-t1, datetime.now()-firsttimer))

plt.savefig(sys.stdout)	# Plot standard output.
