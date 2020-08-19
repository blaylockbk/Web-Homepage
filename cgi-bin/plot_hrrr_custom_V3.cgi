#!/uufs/chpc.utah.edu/common/home/u0553130/anaconda3/envs/pyBKB_v3/bin/python

# Brian Blaylock
# June 8, 2017     # I accidentally made beef jerky in the crock pot last night


"""
Generates a custom figure of desired HRRR variables

Note: For CGI, cannot print anything to screen when outputting a .png file
"""

import numpy as np
from datetime import datetime, timedelta


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

import sys, os
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v3')
sys.path.append('/uufs/chpc.utah.edu/sys/pkg/python/2.7.3_rhel6/lib/python2.7/site-packages/mpl_toolkits')
#sys.path.append('/uufs/chpc.utah.edu/sys/pkg/python/2.7.3_rhel6/lib/python2.7/site-packages/')
from BB_MesoWest.get_MesoWest import get_mesowest_stninfo
from BB_HRRR.plot_HRRR_custom import *
#from BB_GOES16.get_ABI import get_GOES16_truecolor, get_GOES16_firetemperature, file_nearest
#from BB_GOES16.get_GLM import get_GLM_files_for_ABI, accumulate_GLM

import cgi
import cgitb
cgitb.enable()	# Spits out error to browser in coherent format.


# == Debugging ================================================================
# =============================================================================

debug_mode = True

if debug_mode:
    # Prints text to screen with errors
    print("Content-Type: text/html\n")
    print('Current working directory', os.getcwd())
    print('\nPath:')
    for i in sys.path:
        print(i)
    #print sys.modules.keys()
    print('')
    print('matplitlib version', mpl.__version__)
    import mpl_toolkits.basemap
    print('mpl_toolkits:', dir(mpl_toolkits))
    print('mpl_toolkits:', mpl_toolkits.__path__)
else:
    # Output is a png image
    print("Content-Type: image/png\n")


debug_plot_code = 'POT_2-m_Fill'

# =============================================================================
# =============================================================================

'''


# === Load Form Input =========================================================
form = cgi.FieldStorage()	# CGI function takes in web arguments

try:
    model = cgi.escape(form['model'].value)
except:
    model = 'hrrr'

try:
    date = cgi.escape(form['valid'].value)
    DATE = datetime.strptime(date,'%Y-%m-%d_%H%M') # convert to datetime
except:
    DATE = datetime(2019, 1, 1)
    #plt.figure(1)
    #plt.title('Something wrong with date')
    #plt.savefig(sys.stdout)	# Plot standard output.

try:
    fxx = int(cgi.escape(form['fxx'].value))
except:
    fxx = 0

try:
    dsize = cgi.escape(form['dsize'].value)
except:
    dsize = 'full'
    #plt.figure(1)
    #plt.title('Something wrong with the domain size\noptions: small, medium, large, xlarge, xxlarge, xxxlarge, conus')
    #plt.savefig(sys.stdout)	# Plot standard output.


if dsize != 'full':
    try:
        location = cgi.escape(form['location'].value)
    except:
        #plt.figure(1)
        #plt.title('Something wrong with Location\nUse a valid MesoWest Station ID\nor input a lat/lon (ex: 40.5,-111.5)')
        #plt.savefig(sys.stdout)	# Plot standard output.
        location = 'WBB'
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
            stninfo = get_mesowest_stninfo([location])
            lat = stninfo[location]['latitude']
            lon = stninfo[location]['longitude']
    except:
        plt.figure(1)
        plt.title('Something wrong with Location\nUse a valid MesoWest Station ID\nor iput a lat/lon (ex: 40.5,-111.5')
        plt.savefig(sys.stdout)	# Plot standard output.
else:
    lon=None
    lat=None
    location=None

try:
    plotcode = cgi.escape(form['plotcode'].value)
except:
    if debug_mode:
        plotcode = debug_plot_code
    else:
        plotcode = 'none,here'

try:
    background = cgi.escape(form['background'].value)
except:
    #plt.figure(1)
    #plt.title('Something wrong with the background, options: arcgis, arcgisRoad, arcgisSat, terrain, landuse, none')
    #plt.savefig(sys.stdout)	# Plot standard output.
    background = 'arcgis'

try:
    GOES_TC = cgi.escape(form['goes_tc'].value)
except:
    GOES_TC = False
try:
    GOES_FT = cgi.escape(form['goes_ft'].value)
except:
    GOES_FT = False
try:
    GOES_GLM = cgi.escape(form['goes_glm'].value)
except:
    GOES_GLM = False



## ============================================================================
## ============================================================================


VALIDDATE = DATE
RUNDATE = VALIDDATE - timedelta(hours=fxx)


lats, lons = load_lats_lons(model)

# Draw map base elements
m, alpha, half_box, barb_thin = draw_map_base(model, dsize, background,
                                              location, lat, lon,
                                              RUNDATE, VALIDDATE, fxx)


a = plotcode.split(',')
unique_vars = np.unique([i.split('_')[0] for i in a])
PLOTCODES={}
for U in unique_vars:
    PLOTCODES[U]={}
    var_codes = [i for i in a if i.split('_')[0]==U]
    unique_levels = np.unique([i.split('_')[1] for i in var_codes])
    #
    for L in unique_levels:
        PLOTCODES[U][L] = {}
        plot_codes = [i for i in a if i.split('_')[1]==L]
        unique_plot = np.unique([i.split('_')[2] for i in plot_codes])
        #
        PLOTCODES[U][L]['Fill']=False
        PLOTCODES[U][L]['Contour']=False
        PLOTCODES[U][L]['Shade']=False
        PLOTCODES[U][L]['Barbs']=False
        PLOTCODES[U][L]['Quiver']=False
        PLOTCODES[U][L]['p95']=False
        PLOTCODES[U][L]['p05p95']=False
        PLOTCODES[U][L]['Convergence']=False
        PLOTCODES[U][L]['Vorticity']=False
        PLOTCODES[U][L]['Fill-Potential']=False
        PLOTCODES[U][L]['masked']=False
        PLOTCODES[U][L]['Crossover']=False
        for P in unique_plot:
            if P == 'Contour':
                try:
                    contours = [i.split('_')[3] for i in a if i.split('_')[2]==P][0].split('c')
                    PLOTCODES[U][L][P]=[int(i) for i in contours]
                except:
                    PLOTCODES[U][L][P]=True
            else:
                PLOTCODES[U][L][P]=True

# Draw Winds:
if 'Wind' in PLOTCODES:
    for L in PLOTCODES['Wind']:
        level=L.replace('-',' ')
        Fill=PLOTCODES['Wind'][L]['Fill']
        Shade=PLOTCODES['Wind'][L]['Shade']
        Barbs=PLOTCODES['Wind'][L]['Barbs']
        Quiver=PLOTCODES['Wind'][L]['Quiver']
        p95=PLOTCODES['Wind'][L]['p95']
        Convergence=PLOTCODES['Wind'][L]['Convergence']
        Vorticity=PLOTCODES['Wind'][L]['Vorticity']

        draw_wind(m, lons, lats,
                  model, dsize, background,
                  location, lat, lon,
                  RUNDATE, VALIDDATE, fxx,
                  alpha, half_box, barb_thin,
                  level=level,
                  Fill=Fill,
                  Shade=Shade,
                  Barbs=Barbs,
                  Quiver=Quiver,
                  p95=p95,
                  Convergence=Convergence,
                  Vorticity=Vorticity)

# Draw Gusts
if 'Gust' in PLOTCODES:
    draw_gust(m, lons, lats,
              model, dsize, background,
              location, lat, lon,
              RUNDATE, VALIDDATE, fxx,
              alpha, half_box, barb_thin)

# Draw Simulated Radar
if 'dBZ' in PLOTCODES:
    for L in PLOTCODES['dBZ']:
        level=L.replace('-',' ')
        Fill=PLOTCODES['dBZ'][L]['Fill']
        Contour=PLOTCODES['dBZ'][L]['Contour']
        contours = range(10, 81, 10)
        if type(Contour) is list:
            contours=Contour
            Contour=True
        draw_refc(m, lons, lats,
                  model, dsize, background,
                  location, lat, lon,
                  RUNDATE, VALIDDATE, fxx,
                  alpha, half_box, barb_thin,
                  Fill=Fill,
                  Contour=Contour, contours = contours)

# Temperature
if 'TMP' in PLOTCODES:
    for L in PLOTCODES['TMP']:
        VAR = 'TMP:%s' % L.replace('-', ' ')
        Fill=PLOTCODES['TMP'][L]['Fill']
        Contour=PLOTCODES['TMP'][L]['Contour']
        p05p95=PLOTCODES['TMP'][L]['p05p95']
        contours = [0]
        if type(Contour) is list:
            contours=Contour
            Contour=True

        draw_tmp_dpt(m, lons, lats,
                    model, dsize, background,
                    location, lat, lon,
                    RUNDATE, VALIDDATE, fxx,
                    alpha, half_box, barb_thin,
                    variable=VAR,
                    Fill=Fill,
                    Contour=Contour, contours = [0],
                    p05p95=p05p95)

# Potential Temperature
if 'POT' in PLOTCODES:
    for L in PLOTCODES['POT']:
        VAR = 'POT:%s' % L.replace('-', ' ')
        Fill=PLOTCODES['POT'][L]['Fill']
        Contour=PLOTCODES['POT'][L]['Contour']
        p05p95=PLOTCODES['POT'][L]['p05p95']
        contours = [0]
        if type(Contour) is list:
            contours=Contour
            Contour=True

        draw_pot(m, lons, lats,
                 model, dsize, background,
                 location, lat, lon,
                 RUNDATE, VALIDDATE, fxx,
                 alpha, half_box, barb_thin)

# Dew Point Temperature
if 'DPT' in PLOTCODES:
    for L in PLOTCODES['DPT']:
        
        VAR = 'DPT:%s' % L.replace('-', ' ')
        Fill=PLOTCODES['DPT'][L]['Fill']
        Contour=PLOTCODES['DPT'][L]['Contour']
        p05p95=PLOTCODES['DPT'][L]['p05p95']
        contours = [0]
        if type(Contour) is list:
            contours=Contour
            Contour=True

        draw_tmp_dpt(m, lons, lats,
                 model, dsize, background,
                 location, lat, lon,
                 RUNDATE, VALIDDATE, fxx,
                 alpha, half_box, barb_thin,
                 variable=VAR,
                 Fill=Fill,
                 Contour=Contour, contours = [0],
                 p05p95=p05p95)

# Relative Humidity
if 'RH' in PLOTCODES:
    for L in PLOTCODES['RH']:
        level = L.replace('-', ' ')
        draw_rh(m, lons, lats,
                model, dsize, background,
                location, lat, lon,
                RUNDATE, VALIDDATE, fxx,
                alpha, half_box, barb_thin,
                level=level)

# Vapor Pressure Deficit
if 'VPD' in PLOTCODES:
    for L in PLOTCODES['VPD']:
        Fill=PLOTCODES['VPD'][L]['Fill']
        Crossover=PLOTCODES['VPD'][L]['Crossover']
        level = L.replace('-', ' ')
        draw_vpd(m, lons, lats,
                model, dsize, background,
                location, lat, lon,
                RUNDATE, VALIDDATE, fxx,
                alpha, half_box, barb_thin,
                level=level,
                Fill=Fill,
                Crossover=Crossover)

# Geopotential Height
if 'HGT' in PLOTCODES:
    for L in PLOTCODES['HGT']:
        level = L.replace('-', ' ')
        Contour=PLOTCODES['HGT'][L]['Contour']
        p05p95=PLOTCODES['HGT'][L]['p05p95']
        draw_hgt(m, lons, lats,
            model, dsize, background,
            location, lat, lon,
            RUNDATE, VALIDDATE, fxx,
            alpha, half_box, barb_thin,
            level=level,
            Contour=Contour,
            p05p95=p05p95)

# Mean Sea Level Pressure
if 'MSLP' in PLOTCODES:
    for L in PLOTCODES['MSLP']:
        Fill=PLOTCODES['MSLP'][L]['Fill']
        Contour=PLOTCODES['MSLP'][L]['Contour']
        draw_mslp(m, lons, lats,
                model, dsize, background,
                location, lat, lon,
                RUNDATE, VALIDDATE, fxx,
                alpha, half_box, barb_thin,
                Fill=Fill,
                Contour=Contour)

# Red Flag Conditions
if 'REDFLAG' in PLOTCODES:
    for L in PLOTCODES['REDFLAG']:
        Fill=PLOTCODES['REDFLAG'][L]['Fill']
        Contour=PLOTCODES['REDFLAG'][L]['Contour']
        Fill_Potential=PLOTCODES['REDFLAG'][L]['Fill-Potential']
        draw_redflag(m, lons, lats,
                     model, dsize, background,
                     location, lat, lon,
                     RUNDATE, VALIDDATE, fxx,
                     alpha, half_box, barb_thin,
                     RH=25, SPEED=6.7,
                     Fill=Fill,
                     Contour=Contour,
                     Fill_Potential=Fill_Potential)

if 'GOES_ABI' in PLOTCODES:
    print('future')

if 'GOES_GLM' in PLOTCODES:
    print('future')

# All other variables
OTHER = [i for i in PLOTCODES.keys() if i not in ['TMP', 'DPT', 'Wind', 'Gust', 'dBZ', 'RH', 'HGT', 'MSLP','REDFLAG', 'VPD', 'POT']]

for i in OTHER:
    for L in PLOTCODES[i]:
        variable = '%s:%s' % (i, L)

        masked=PLOTCODES[i][L]['masked']

        draw_variable(m, lons, lats,
                      model, dsize, background,
                      location, lat, lon,
                      RUNDATE, VALIDDATE, fxx,
                      alpha, half_box, barb_thin,
                      variable=variable,
                      masked=masked)

if debug_mode:
    print("looks like the plotting script made it to the end :)")
else:
    plt.savefig(sys.stdout)	# Plot standard output.


# http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/plot_hrrr_custom.cgi?model=hrrrak&valid=2018-05-01_0000&fxx=0&plotcode=dBZ_Fill&dsize=conus&background=none
'''