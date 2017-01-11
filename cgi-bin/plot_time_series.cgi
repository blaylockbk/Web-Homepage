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

print "Content-Type: image/png\n"
# print "Content-Type: text/html\n"

## Get arguments from storage or use default if any errors are thrown

form = cgi.FieldStorage()

try:
	mytzone = form["tz"].value
except:
	mytzone = 'local'
	
if(mytzone != 'utc'):
	mytzone = 'local'

## Set timezone first

if(mytzone == 'utc'):
	os.environ['TZ'] = 'Etc/Greenwich'
	time.tzset()
	tzout = 'UTC'
else:
	tzout = 'Local'	

currtime = datetime.datetime.utcnow()
pasttime = currtime-datetime.timedelta(days=1)
curyr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y')

## Cheap way of getting timezone offsets

utctzoff = int(time.mktime(time.gmtime())) - int(time.mktime(time.localtime()))

try:
	paston = int(form["past"].value)
except:
	paston = 0
	
if(paston != 1):
	paston = 0

try:
	yr = form["yr"].value
	mo = form["mo"].value
	dy = form["dy"].value
	hr = form["hr"].value
	mm = form["mm"].value
except:
	if(mytzone == 'utc'):
		yr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y')
		mo = datetime.datetime.strftime(datetime.datetime.utcnow(),'%m')
		dy = datetime.datetime.strftime(datetime.datetime.utcnow(),'%d')
		hr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%H')
		mm = datetime.datetime.strftime(datetime.datetime.utcnow(),'%M')
	else:
		yr = datetime.datetime.strftime(datetime.datetime.now(),'%Y')
		mo = datetime.datetime.strftime(datetime.datetime.now(),'%m')
		dy = datetime.datetime.strftime(datetime.datetime.now(),'%d')
		hr = datetime.datetime.strftime(datetime.datetime.now(),'%H')
		mm = datetime.datetime.strftime(datetime.datetime.now(),'%M')			

## Define listing of train IDs and line styles

traxstidlist = ['TRX01']
stidlist = ['TRX01','UUTK1','UUTK2','KSL5','UNERD','UUTK3']
stylelist = ['','--']
stnstyle = {}
showstn = {}
mobiledatadir = {}
showanystns = 0
for stid in stidlist:
	showstn[stid] = 0
	try:
		if(form[stid].value == 'on'):
			showstn[stid] = 1
			stnstyle[stid] = stylelist[showanystns]
			showanystns = showanystns + 1
	except:
		skip = 1
	if(stid in traxstidlist):
		mobiledatadir[stid] = '/uufs/chpc.utah.edu/common/home/horel-group4/mesotrax/'
	else:
		mobiledatadir[stid] = '/uufs/chpc.utah.edu/common/home/horel-group4/gslso3s/data/mobile/'

if(showanystns < 1):
	showstn['TRX01'] = 1
	
## Define data type choice dictionaries

varoptions = {'TMPC': 'Temperature',
'RELH': 'Relative Humidity',
'PRES': 'Barometric Pressure',
'TICC': 'CR1000 Logger Temperature',
'VOLT': 'CR1000 Voltage',
'PM25': 'PM2.5 Concentration',
'FLOW': 'ESampler Flow Rate',
'ITMP': 'ESampler Temperature',
'INRH': 'ESampler Relative Humidity',
'None': 'None',
'TTD': 'Temperature and Moisture',
'NSAT': 'GPS Satellites',
'THTA': 'Potential Temperature',
'GLAT': 'GPS Latitude',
'GLON': 'GPS Longitude',
'GELV': 'GPS Elevation',
'ANBC': 'Black Carbon (Analog)',
'OZNE': 'Ozone',
'TC2B': '2B Temperature',
'PS2B': '2B Pressure',
'FL2B': '2B Flow Rate'
}

varfilename = {'TMPC': 'cr1000',
'RELH': 'cr1000',
'PRES': 'cr1000',
'TICC': 'cr1000',
'VOLT': 'cr1000',
'PM25': 'esampler',
'FLOW': 'esampler',
'ITMP': 'esampler',
'INRH': 'esampler',
'NSAT': 'cr1000',
'GLAT': 'cr1000',
'GLON': 'cr1000',
'GELV': 'cr1000',
'ANBC': 'aeth',
'OZNE': '2b',
'TC2B': '2b',
'PS2B': '2b',
'FL2B': '2b'
}

varcolordict = {'TMPC': 'r',
'RELH': 'g',
'PRES': 'c',
'TICC': '#ff9900',
'VOLT': 'y',
'PM25': 'm',
'FLOW': 'b',
'ITMP': '#660000',
'INRH': '#006600',
'NSAT': 'b',
'GLAT': 'c',
'GLON': 'c',
'GELV': 'c',
'ANBC': '0.7',
'OZNE': '#009900',
'TC2B': '#660000',
'PS2B': 'c',
'FL2B': 'b'
}

varunits = {'TMPC': 'Temperature (C)',
'RELH': 'Humidity (%)',
'PRES': 'Pressure (hPa)',
'TICC': 'Temperature (C)',
'VOLT': 'Voltage (volts)',
'PM25': 'PM2.5 (ug/m3)',
'FLOW': 'Flow Rate (L/min)',
'ITMP': 'Temperature (C)',
'INRH': 'Humidity (%)',
'NSAT': 'Number Satellites',
'GLAT': 'Latitude (degrees)',
'GLON': 'Longitude (degrees)',
'GELV': 'Elevation (m)',
'ANBC': 'Black Carbon (ug/m3)',
'OZNE': 'Ozone (ppbv)',
'TC2B': 'Temperature (C)',
'PS2B': 'Pressure (hPa)',
'FL2B': 'Flow Rate (cc/min)'
}

try:
	leftvarchoice = form["leftvar"].value
except:
	leftvarchoice = 'PM25'

if(leftvarchoice not in varoptions):
	leftvarchoice = 'PM25'

try:
	rightvarchoice = form["rightvar"].value
except:
	rightvarchoice = 'None'

if(rightvarchoice not in varoptions):
	rightvarchoice = 'None'
	
try:
	minback = int(form["min"].value)
except:
	minback = 60

if(minback > 43200):
	minback = 43200

try:
	epochend = int(time.mktime(time.strptime(yr+mo+dy+hr+mm,'%Y%m%d%H%M')))
except:
	epochend = int(time.mktime(time.localtime()))
	
epochstart = int(epochend-(60.*minback))

currtimestring = time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochend))
pasttimestring = time.strftime('%Y-%m-%d %H:%M'+tzout,time.localtime(epochstart))

if(time.localtime(epochend).tm_isdst == 1):
	utctzoff = utctzoff-3600

yearmo_now = time.strftime('%Y_%m',time.gmtime(epochend))
yearmo_before = time.strftime('%Y_%m',time.gmtime(epochstart))

## Define HDF5 data folder!

datachoicelist = []

for choice in [leftvarchoice,rightvarchoice]:
	if choice == 'TTD':
		datachoicelist.append('TMPC')
		datachoicelist.append('RELH')
	elif choice == 'THTA':
		datachoicelist.append('TMPC')
		datachoicelist.append('PRES')
	elif choice == 'None':
		skip = 1
	else:
		datachoicelist.append(choice)

datadict = {}
for stid in stidlist:
	datadict[stid] = {}
	for type in datachoicelist:
		datadict[stid][varfilename[type]] = {}
		hdf5dir = mobiledatadir[stid]+varfilename[type]+'/'
		if(yearmo_now == yearmo_before):
			hdf5files = [hdf5dir+stid+'_'+yearmo_now+'_'+varfilename[type]+'.h5']
		else:
			hdf5files = [hdf5dir+stid+'_'+yearmo_before+'_'+varfilename[type]+'.h5', hdf5dir+stid+'_'+yearmo_now+'_'+varfilename[type]+'.h5']
		for file in hdf5files:
			try:
				h5stnhandle = pytbls.openFile(file, mode = "r")
				selectedtable = h5stnhandle.root.obsdata.observations
			
# Now select all data and convert -9999 to NAN...

				for column in selectedtable.colnames:
					try:
						datadict[stid][varfilename[type]][column] = datadict[stid][varfilename[type]][column]
					except:
						datadict[stid][varfilename[type]][column] = []
					
				mydata = selectedtable.readWhere("(EPOCHTIME >= "+str(epochstart)+") & (EPOCHTIME <= "+str(epochend)+")")
				for key in datadict[stid][varfilename[type]]:
					x = np.array(mydata[key],dtype='float')
					x[x == -9999.] = np.nan
					if key == 'ITMP':
						x = (x-32)/1.8			
					datadict[stid][varfilename[type]][key].extend(x)
				h5stnhandle.close()
				
			except IOError:
				skip = 1


filterrawtimes = {}
filterrawdata = {}
tmptime = {}
tmpdata = {}
havedata = 0
if(leftvarchoice != 'None'):
	for stid in stidlist:
		filterrawtimes[stid] = {}
		filterrawdata[stid] = {}
		for type in datachoicelist:
			try:
				tmptime[stid] = np.array(datadict[stid][varfilename[type]]['EPOCHTIME'])
				tmpdata[stid] = np.array(datadict[stid][varfilename[type]][type])
				tmpdata[stid] = tmpdata[stid][~np.isnan(tmptime[stid])]		
				tmptime[stid] = tmptime[stid][~np.isnan(tmptime[stid])]
				tmptime[stid] = [int(x) - utctzoff if ~np.isnan(x) else np.nan for x in tmptime[stid]]
				filterrawtimes[stid][type] = sorted(tmptime[stid])
				filterrawdata[stid][type] = [x for (y,x) in sorted(zip(tmptime[stid],tmpdata[stid]))]
				havedata = havedata + len(filterrawtimes[stid][type])
			except:
				filterrawtimes[stid][type] = []
				filterrawdata[stid][type] = []

if(havedata > 0):
	datelocater = mpl.dates.AutoDateLocator()
	dateaxisfmt = mpl.dates.DateFormatter('%m-%d %H:%M:%S')
	mpl.rc('xtick',labelsize=8)
	datepresfmt = mpl.ticker.ScalarFormatter(useOffset=False)
	datepresfmt.set_scientific(False)
	mpl.rc('ytick',labelsize=8)

	fig = pyplot.figure(figsize=(10,5))
	myp = fig.add_subplot(111)
	pyplot.suptitle('Observations from '+time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochstart))+' - '+time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochend)))
	
	lineset = []
	if(leftvarchoice == 'TTD'):
		for stid in stidlist:
			if(showstn[stid] == 1):
				try:
					es = 6.11*(10**((7.5*np.array(filterrawdata[stid]['TMPC']))/(237.7+np.array(filterrawdata[stid]['TMPC']))))
					e = es*(np.array(filterrawdata[stid]['RELH'])/100.)
					e[e==0] = np.nan
					alogs = 0.43429*np.log(e) - 0.43429*np.log(6.11)
					dwpc = (237.7*alogs)/(7.5-alogs)
					mpldates = mpl.dates.epoch2num(filterrawtimes[stid]['TMPC'])
					if(len(mpldates) > 0):
						curline = pyplot.plot(mpldates,filterrawdata[stid]['TMPC'],stnstyle[stid],color=varcolordict['TMPC'],label=stid+' '+varoptions['TMPC'])
						lineset = lineset+curline
						curline = pyplot.plot(mpldates,dwpc,stnstyle[stid],color=varcolordict['RELH'],label=stid+' Dewpoint')
						lineset = lineset+curline
				except:
					skip = 1
		myp.set_ylabel('Temperature and Dewpoint (C)')		
	elif(leftvarchoice == 'THTA'):
		for stid in stidlist:
			if(showstn[stid] == 1):
				try:
					kappa = (287./1004.)
					tmpk = np.array(filterrawdata[stid]['TMPC']) + 287.15
					thtak = tmpk * ((1000./np.array(filterrawdata[stid]['PRES']))**kappa)
					mpldates = mpl.dates.epoch2num(filterrawtimes[stid]['TMPC'])
					if(len(mpldates) > 0):
						curline = pyplot.plot(mpldates,thtak,'y'+stnstyle[stid],label=stid+' Potential Temperature')
						lineset = lineset+curline
				except:
					skip = 1
		myp.set_ylabel('Temperature (K)')
	else:
		for stid in stidlist:
			if(showstn[stid] == 1):
				try:
					mpldates = mpl.dates.epoch2num(filterrawtimes[stid][leftvarchoice])
					if(len(mpldates) > 0):
						curline = pyplot.plot(mpldates,filterrawdata[stid][leftvarchoice],stnstyle[stid],color=varcolordict[leftvarchoice],label=stid+' '+varoptions[leftvarchoice])
						lineset = lineset+curline
				except:
					skip = 1
		myp.set_ylabel(varunits[leftvarchoice])
		if(leftvarchoice == 'RELH' or leftvarchoice == 'INRH'):
			myp.set_ylim(0,100)
	if(rightvarchoice == 'None'):
		skip = 1
	elif(rightvarchoice == 'TTD'):
		for stid in stidlist:
			if(showstn[stid] == 1):
				try:
					myp2 = myp.twinx()
					es = 6.11*(10**((7.5*np.array(filterrawdata[stid]['TMPC']))/(237.7+np.array(filterrawdata[stid]['TMPC']))))
					e = es*(np.array(filterrawdata[stid]['RELH'])/100.)
					e[e==0] = np.nan
					alogs = 0.43429*np.log(e) - 0.43429*np.log(6.11)
					dwpc = (237.7*alogs)/(7.5-alogs)
					mpldates2 = mpl.dates.epoch2num(filterrawtimes[stid]['TMPC'])
					if(len(mpldates2) > 0):
						curline = myp2.plot(mpldates2,filterrawdata[stid]['TMPC'],stnstyle[stid],color=varcolordict['TMPC'],label=stid+' '+varoptions['TMPC'])
						lineset = lineset+curline
						curline = myp2.plot(mpldates2,dwpc,stnstyle[stid],color=varcolordict['RELH'],label=stid+' Dewpoint')
						lineset = lineset+curline
				except:
					skip = 1
		myp2.set_ylabel('Temperature and Dewpoint (C)')
		myp2.yaxis.set_major_formatter(datepresfmt)
	elif(rightvarchoice == 'THTA'):
		for stid in stidlist:
			if(showstn[stid] == 1):
				try:
					myp2 = myp.twinx()
					kappa = (287./1004.)
					tmpk = np.array(filterrawdata[stid]['TMPC']) + 287.15
					thtak = tmpk * ((1000./np.array(filterrawdata[stid]['PRES']))**kappa)
					mpldates2 = mpl.dates.epoch2num(filterrawtimes[stid]['TMPC'])
					if(len(mpldates2) > 0):
						curline = myp2.plot(mpldates2,thtak,'y'+stnstyle[stid],label=stid+' Potential Temperature')
						lineset = lineset+curline
				except:
					skip = 1
		myp2.set_ylabel('Temperature (K)')
		myp2.yaxis.set_major_formatter(datepresfmt)
	else:
		for stid in stidlist:
			if(showstn[stid] == 1):
				try:
					myp2 = myp.twinx()		
					mpldates2 = mpl.dates.epoch2num(filterrawtimes[stid][rightvarchoice])
					if(len(mpldates2) > 0):
						curline = myp2.plot(mpldates2,filterrawdata[stid][rightvarchoice],stnstyle[stid],color=varcolordict[rightvarchoice],label=stid+' '+varoptions[rightvarchoice])
						lineset = lineset+curline
				except:
					skip = 1
		myp2.set_ylabel(varunits[rightvarchoice])
		if(rightvarchoice == 'RELH' or rightvarchoice == 'INRH'):
			myp2.set_ylim(0,100)
		myp2.yaxis.set_major_formatter(datepresfmt)
	myp.set_xlabel('Time ('+tzout+')')
	myp.xaxis.set_major_locator(datelocater)
	myp.xaxis.set_major_formatter(dateaxisfmt)
	myp.yaxis.set_major_formatter(datepresfmt)
	myp.set_xlim(mpl.dates.epoch2num(epochstart-utctzoff),mpl.dates.epoch2num(epochend-utctzoff))
	fig.autofmt_xdate()	
	labelset = [l.get_label() for l in lineset]
	try:
		myp2.legend(lineset,labelset,loc=3,prop={'size':8})
	except:
		myp.legend(lineset,labelset,loc=3,prop={'size':8})
	pyplot.savefig(sys.stdout, format='png')
else:
	fig = pyplot.figure(figsize=(10,0.5))
	pyplot.suptitle('Observations from '+time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochstart))+' - '+time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochend))+' could not be generated')
	pyplot.savefig(sys.stdout, format='png')

sys.exit()
