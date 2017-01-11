#!/usr/local/bin/python

import numpy as np
import cgi, cgitb
cgitb.enable()
import matplotlib as mpl
mpl.use('Agg')
import gzip, os, sys, datetime, re, time
from matplotlib import pyplot
import tables as pytbls
from scipy import signal as sig

## Set timezone first

os.environ['TZ'] = 'Etc/Greenwich'
time.tzset()

print "Content-Type: text/plain\n"

## Get arguments from storage or use default if any errors are thrown

form = cgi.FieldStorage()

currtime = datetime.datetime.utcnow()
pasttime = currtime-datetime.timedelta(days=1)
curyr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y')

try:
	yr = form["yr"].value
	mo = form["mo"].value
	dy = form["dy"].value
	hr = form["hr"].value
	mm = form["mm"].value
except:
	yr = datetime.datetime.strftime(datetime.datetime.now(),'%Y')
	mo = datetime.datetime.strftime(datetime.datetime.now(),'%m')
	dy = datetime.datetime.strftime(datetime.datetime.now(),'%d')
	hr = datetime.datetime.strftime(datetime.datetime.now(),'%H')
	mm = datetime.datetime.strftime(datetime.datetime.now(),'%M')			

## Define listing of train IDs and line styles

traxstidlist = ['TRX01']
stidlist = ['TRX01','UUTK1','UUTK2','KSL5','UNERD','UUTK3']
mobiledatadir = {}
for stid in stidlist:
	if(stid in traxstidlist):
		mobiledatadir[stid] = '/uufs/chpc.utah.edu/common/home/horel-group4/mesotrax/'
	else:
		mobiledatadir[stid] = '/uufs/chpc.utah.edu/common/home/horel-group4/gslso3s/data/mobile/'

mobilestnname = {
	'TRX01': 'UTA TRAX',
	'UUTK1': 'UofU ATMOS Mobile',
	'UUTK2': 'UofU ATMOS Mobile',
	'UUTK3': 'UofU ATMOS Mobile',
	'UNERD': 'UofU NerdMobile',
	'KSL5': 'KSL Chopper 5'
}
		
## Define data type choice dictionaries

varnames = {'TMPC': 'airtemp_C','RELH': 'rh_pcent','PRES': 'pres_hpa','TICC': 'loggertemp_C','VOLT': 'voltage','OZNE': 'ozone_ppbv','PM25': 'pm25_ugm3','FLOW': 'flow_Lmin','ITMP': 'temp_C','INRH': 'rh_pcent', 'NSAT': 'gpsnumsat', 'GLAT': 'gpslat_dd', 'GLON': 'gpslon_dd', 'GELV': 'gpselev_m','ANBC': 'black_carbon','FL2B': '2bflow_Lmin','TC2B': '2btemp_C','PS2B': '2bpres_hpa'}
varorder = ['GLAT','GLON','GELV','NSAT','PM25','FLOW','ITMP','INRH','TMPC','RELH','PRES','TICC','VOLT','ANBC','OZNE','FL2B','TC2B','PS2B']

try:
	inputstid = form["stid"].value
except:
	inputstid = 'TRX01'

if(inputstid in stidlist):
	reqstidlist = [inputstid]
else:
	reqstidlist = []
	
try:
	minback = int(form["min"].value)
except:
	minback = 60

if(minback > 2880):
	minback = 2880

try:
	epochend = int(time.mktime(time.strptime(yr+mo+dy+hr+mm,'%Y%m%d%H%M')))
except:
	epochend = int(time.mktime(time.localtime()))
	
epochstart = int(epochend-(60.*minback))

showtimeend = time.strftime('%Y-%m-%d %H:%M UTC',time.gmtime(epochend))
showtimestart = time.strftime('%Y-%m-%d %H:%M UTC',time.gmtime(epochstart))

yearmo_now = time.strftime('%Y_%m',time.gmtime(epochend))
yearmo_before = time.strftime('%Y_%m',time.gmtime(epochstart))

print '#'+inputstid+' '+mobilestnname[inputstid]+' observations from '+showtimestart+' to '+showtimeend

## Define HDF5 data folder!

filetypelist = ['cr1000','esampler','aeth','2b']
datadict = {}
stnvarlist = {}

for stid in reqstidlist:
	datadict[stid] = {}
	for type in filetypelist:
		datadict[stid][type] = {}
		hdf5dir = mobiledatadir[stid]+type+'/'
		if(yearmo_now == yearmo_before):
			hdf5files = [hdf5dir+stid+'_'+yearmo_now+'_'+type+'.h5']
		else:
			hdf5files = [hdf5dir+stid+'_'+yearmo_before+'_'+type+'.h5', hdf5dir+stid+'_'+yearmo_now+'_'+type+'.h5']
		for file in hdf5files:
			try:
				h5stnhandle = pytbls.openFile(file, mode = "r")
				selectedtable = h5stnhandle.root.obsdata.observations
			
# Now select all data and convert -9999 to NAN...

				for column in selectedtable.colnames:
					try:
						datadict[stid][type][column] = datadict[stid][type][column]
					except:
						datadict[stid][type][column] = []
					
				mydata = selectedtable.readWhere("(EPOCHTIME >= "+str(epochstart)+") & (EPOCHTIME <= "+str(epochend)+")")
				for key in datadict[stid][type]:
					x = np.array(mydata[key],dtype='float')			
					if key == 'ITMP':
						x = (x-32)/1.8			
					datadict[stid][type][key].extend(x)

				for key in datadict[stid][type]:
					checknodata = datadict[stid][type][key]
					try:
						datalength = len(checknodata[checknodata != -9999.])
					except:
						datalength = len(checknodata)
					if(datalength > 0):
						try:
							stnvarlist[type][key] = column
						except:
							stnvarlist[type] = {}
							stnvarlist[type][key] = column
							
				h5stnhandle.close()

			except IOError:
				skip = 1

headerline = 'Station_ID,Date,TimeUTC'
oblist = []

try:
	for type in stnvarlist:
		for var in varorder:
			if var != 'EPOCHTIME' and var in stnvarlist[type]:
				try:
					headerline = headerline+','+type+'_'+varnames[var]
				except:
					headerline = headerline+','+type+'_'+var

	print headerline
	for stid in reqstidlist:
		for epochtime in datadict[stid]['cr1000']['EPOCHTIME']:
			obline = stid+','+time.strftime('%Y-%m-%d,%H:%M:%S',time.localtime(int(epochtime)))
			for type in stnvarlist:
				for var in varorder:
					if var != 'EPOCHTIME' and var != 'GTIM' and var in stnvarlist[type]:
						vartmp = ("%.2f" % -9999)
						try:
							if var == 'GLAT' or var == 'GLON':
								vartmp = ("%.5f" % datadict[stid][type][var][np.where(datadict[stid][type]['EPOCHTIME'] == epochtime)[0][0]])
							else:
								vartmp = ("%.2f" % datadict[stid][type][var][np.where(datadict[stid][type]['EPOCHTIME'] == epochtime)[0][0]])
						except:
							vartmp = ("%.2f" % -9999)
						obline = obline+','+str(vartmp)
			print obline
except:
	print 'Could not generate observations for '+inputstid+' from '+showtimestart+' to '+showtimeend

sys.exit()
