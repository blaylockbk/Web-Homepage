#!/usr/local/bin/python

import numpy as np
import cgi, cgitb
cgitb.enable()
import gzip, os, sys, datetime, re, time, urllib2, collections, calendar, json
from operator import itemgetter
import tables as pytbls

# print "Content-Type: text/html\n"

## Get arguments from storage or use default if any errors are thrown

form = cgi.FieldStorage()

regionlist = ['GSL','SYR','SLC']
try:
	myregion = form["region"].value
except:
	myregion = 'GSL'

if(myregion not in regionlist):
	myregion = 'GSL'

try:
	mytzone = form["tz"].value
except:
	mytzone = 'local'
	
if(mytzone != 'utc'):
	mytzone = 'local'
	
## Cheap way of getting timezone offsets

utctzoff = int(time.mktime(time.gmtime())) - int(time.mktime(time.localtime()))
	
## Set timezone first

if(mytzone == 'utc'):
	os.environ['TZ'] = 'Etc/Greenwich'
	time.tzset()
	tzout = ' UTC'
	mwtzlink = 'GMT'
	utctzoff = 0
else:
	tzout = ' Local'
	mwtzlink = 'LOCAL'
	
## Figure out current time and get current year
	
currtime = datetime.datetime.utcnow()
pasttime = currtime-datetime.timedelta(days=1)
curyr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y')

## Read and determine what time period we are looking at!

try:
	paston = int(form["past"].value)
except:
	paston = 0
	
if(paston != 1):
	paston = 0

try:
	if(paston == 1):
		yr = form["yr"].value
		mo = form["mo"].value
		dy = form["dy"].value
		hr = form["hr"].value
		mm = form["mm"].value
	else:
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

## Define a listing of mobile station IDs (remember these are HDF5 files that have different names for each ID)

traxstidlist = ['TRX01']
mobilestidlist = ['TRX01','UUTK1','UUTK2','KSL5','UNERD','UUTK3']
showstn = {}
mobiledatadir = {}
for stid in mobilestidlist:
	showstn[stid] = 1
	if(stid in traxstidlist):
		mobiledatadir[stid] = '/uufs/chpc.utah.edu/common/home/horel-group4/mesotrax/'
	else:
		mobiledatadir[stid] = '/uufs/chpc.utah.edu/common/home/horel-group4/gslso3s/data/mobile/'
	try:
		if(form[stid].value == 'off'):
			showstn[stid] = 0
	except:
		skip = 1

mobilestnname = {
	'TRX01': 'UTA TRAX',
	'UUTK1': 'UofU ATMOS Mobile',
	'UUTK2': 'UofU ATMOS Mobile',
	'UUTK3': 'UofU ATMOS Mobile',
	'UNERD': 'UofU NerdMobile',
	'KSL5': 'KSL Chopper 5'
}
		
## Define some default dictionaries for HDF5 files to query, variables, and display methods

filetypelist = ['cr1000','esampler','2b']
varoptionlist = ['OZNE','PM25','TMPC','RELH','VOLT']

varoptions = {'TMPC': 'Temperature',
'RELH': 'Relative Humidity',
'PM25': 'PM2.5 Concentration',
'VOLT': 'Battery Voltage',
'OZNE': 'Ozone Concentration'}

varfilename = {'TMPC': 'cr1000',
'RELH': 'cr1000',
'PM25': 'esampler',
'VOLT': 'cr1000',
'OZNE': '2b'}

varunits = {'TMPC': 'deg C',
'RELH': '%',
'PM25': 'ug/m<sup>3</sup>',
'VOLT': 'volts',
'OZNE': 'ppbv'}

varapi = {'TMPC': 'air_temp',
'RELH': 'relative_humidity',
'PM25': 'PM_25_concentration',
'VOLT': 'volt',
'OZNE': 'ozone_concentration'}

varmoped = {'TMPC': 8,
'RELH': 10,
'PM25': 0,
'VOLT': 0,
'OZNE': 24}

mwvarlink = {'TMPC': 'TMPF',
'RELH': 'RELH',
'PM25': 'PM25',
'VOLT': 'VOLT',
'OZNE': 'OZNE'}

vartemplist = ['TMPC','TICC','ITMP']
varrhlist = ['RELH','INRH']
varotherlist = ['FLOW']

opacoptionlist = ['On','Off']

tzoptions = {'local': 'Local','utc': 'UTC'}
tzoptionlist = ['local','utc']

regionmap = {'GSL': '41.021070,-112.355132,10',
'SYR': '41.005733,-112.258307,10',
'SLC': '40.686562,-112.167544,10',
}

regionmapzoom = {'GSL': '9',
'SYR': '10',
'SLC': '10',
}

## Define defaults for the home page rendering if not chosen

try:
	varchoice = form["var"].value
except:
	varchoice = 'OZNE'

if(varchoice not in varoptions):
	varchoice = 'OZNE'

try:
	opacchoice = form["opacchange"].value
except:
	opacchoice = 'Off'

if(opacchoice not in opacoptionlist):
	opacchoice = 'Off'

try:
	minback = int(form["min"].value)
except:
	minback = 120

if(minback > 1440):
	minback = 1440

## Figure out timestamps for HDF5 querying, API querying, and displays

try:
	epochend = int(time.mktime(time.strptime(yr+mo+dy+hr+mm,'%Y%m%d%H%M')))
except:
	epochend = int(time.mktime(time.localtime()))

epochstart = int(epochend-(60.*minback))

currtimestring = time.strftime('%Y-%m-%d %H:%M'+tzout,time.localtime(epochend))
currtimestringutc = time.strftime('%Y-%m-%d %H:%M UTC',time.gmtime(epochend))
pasttimestring = time.strftime('%Y-%m-%d %H:%M'+tzout,time.localtime(epochstart))

apitimeend = time.strftime('%Y%m%d%H%M',time.gmtime(epochend))
apitimestart = time.strftime('%Y%m%d%H%M',time.gmtime(epochstart))

yearmo_now = time.strftime('%Y_%m',time.gmtime(epochend))
yearmo_before = time.strftime('%Y_%m',time.gmtime(epochstart))

## Define MesoWest V2 API Parsing Function and Defaults

apitoken = 'a94df50babad4344bd7e183c5688c5e6'
apivarlist = varapi[varchoice]
vardatalistv2 = [str(varapi[varchoice])+'_set_1']

insitustnname = {}
insitustnlat = {}
insitustnlon = {}
insitulasttime = {}
insitulastdata = {}
def ParseDataV2(jsondata):
	for station in jsondata['STATION']:
		insitustnname[station['STID']] = station['NAME']
		insitustnlat[station['STID']] = station['LATITUDE']
		insitustnlon[station['STID']] = station['LONGITUDE']
		insitulastdata[station['STID']] = ''
		try:
			if(int(station['MNET_ID']) < 2000):
				for key in station['OBSERVATIONS']:
					if key in vardatalistv2:
						templist1 = station['OBSERVATIONS'][key]
						templist = [v for v in templist1 if v is not None]
						temptimelist = [v for v,w in zip(station['OBSERVATIONS']['date_time'],templist1) if w is not None]
						temptime = int(time.mktime(time.strptime(temptimelist[len(temptimelist)-1],'%Y-%m-%dT%H:%M:%SZ')))
						if(mytzone == 'local'):
							temptime = temptime-utctzoff
						if(time.localtime(temptime).tm_isdst == 1):
							temptime = temptime+3600
						temptimestring = time.strftime('%Y-%m-%d %H:%M'+tzout,time.localtime(temptime))
						insitulasttime[station['STID']] = temptimestring
						insitulastdata[station['STID']] = templist[-1]
		except:
			skip = 1

mopedstidlist = []
def ParseMOPED(mopedfile):
	borderurlat = 41.81
	borderurlon = -110.95
	borderlllat = 40.06
	borderlllon = -114.14
	if(os.path.exists(mopedfile)):
		mopedhandle = gzip.open(mopedfile,'rb')
		mopedlist = mopedhandle.read().splitlines()[1:]
		for mopedob in mopedlist:
			mopedobarray = mopedob.split(',')
			temptime = int(time.mktime(time.strptime(mopedobarray[1],'%Y%m%d%H%M')))
			if(mytzone == 'local'):
				temptime = temptime-utctzoff
			if(time.localtime(temptime).tm_isdst == 1):
				temptime = temptime+3600
			temptimestring = time.strftime('%Y-%m-%d %H:%M'+tzout,time.localtime(temptime))
			mopedtime = temptimestring
			mopedlat = float(mopedobarray[2])
			mopedlon = float(mopedobarray[4])
			mopeddata = float(mopedobarray[varmoped[varchoice]])
			if(varchoice == 'TMPC' and mopeddata != -9999):
				mopeddata = (mopeddata-32.)/1.8
			if(mopedlat > borderlllat and mopedlat < borderurlat and mopedlon > borderlllon and mopedlon < borderurlon and temptime > epochstart and temptime <= epochend):
				try:
					if(showstn[mopedobarray[0]] == 0):
						showstn[mopedobarray[0]] = 1
					else:
						skip = 1
				except:
					mobilestidlist.append(mopedobarray[0])
					mopedstidlist.append(mopedobarray[0])
					showstn[mopedobarray[0]] = 1
				try:
					timelist[mopedobarray[0]].append(mopedtime)
					latlist[mopedobarray[0]].append(mopedlat)
					lonlist[mopedobarray[0]].append(mopedlon)
					elevlist[mopedobarray[0]].append('')
					datamarkerlist[mopedobarray[0]].append("%.2f" % mopeddata)
					for j in range(0,len(colorlist)):
						if(mopeddata >= colorminlist[j]):
							tmpcolor = colorlist[j]
							tablecolor[mopedobarray[0]] = colorlist[j]
							tabletextcolor[mopedobarray[0]] = colortextlist[j]
					pm25colorlist[mopedobarray[0]].append(tmpcolor)					
				except:
					timelist[mopedobarray[0]] = []
					latlist[mopedobarray[0]] = []
					lonlist[mopedobarray[0]] = []
					elevlist[mopedobarray[0]] = []
					datamarkerlist[mopedobarray[0]] = []
					pm25colorlist[mopedobarray[0]] = []
					timelist[mopedobarray[0]].append(mopedtime)
					latlist[mopedobarray[0]].append(mopedlat)
					lonlist[mopedobarray[0]].append(mopedlon)
					elevlist[mopedobarray[0]].append('')
					datamarkerlist[mopedobarray[0]].append("%.2f" % mopeddata)
					for j in range(0,len(colorlist)):
						if(mopeddata >= colorminlist[j]):
							tmpcolor = colorlist[j]
							tablecolor[mopedobarray[0]] = colorlist[j]
							tabletextcolor[mopedobarray[0]] = colortextlist[j]
					pm25colorlist[mopedobarray[0]].append(tmpcolor)
				tablevalue[mopedobarray[0]] = "%.2f" % mopeddata
		mopedhandle.close()
			
## Query data out of HDF5 files for mobile sensors

datadict = {}
tablecolor = {}
tabletextcolor = {}
tablevalue = {}
tablelink = {}

for stid in mobilestidlist:
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
			
## Now select all data and convert -9999 to NAN...

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
				h5stnhandle.close()
				
			except IOError:
				skip = 1

## Define color lists for map plotting legends

colorlist = ['#FF0000','#FFFF00','#0000FF','#00FFFF','#00FF00']
colortextlist = ['#FFFFFF','#000000','#FFFFFF','#000000','#000000']
colormaxlist = [1,2,3,4,10]
colorminlist = [0,1,2,3,4]

if(varchoice == 'PM25'):
	colorlist = ['#00FFFF','#00CCFF','#0099FF','#00FF00','#009900','#006600','#FFFF00','#FFE600','#FFCD00','#FF7E00','#FF5000','#FF0000','#990000','#CC0033','#FF00FF']
	colortextlist = ['#000000','#000000','#FFFFFF','#000000','#FFFFFF','#FFFFFF','#000000','#000000','#000000','#000000','#000000','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF']
	colormaxlist = [2,4,6,8,10,12,20,28,35.5,45.5,55.5,85.5,115.5,150.5,  300]
	colorminlist = [0,2,4,6, 8,10,12,20,  28,35.5,45.5,55.5, 85.5,115.5,150.5]

if(varchoice == 'VOLT'):
	colorlist = ['#003300','#006600','#009900','#00CC00','#00FF00','#999900','#CCCC00','#FFFF00','#FF6600','#FF0000']
	colortextlist = ['#FFFFFF','#FFFFFF','#FFFFFF','#000000','#000000','#000000','#000000','#000000','#000000','#FFFFFF']
	colormaxlist = [5,8,9,10,11,12,13,14,15,100]
	colorminlist = [0,5,8, 9,10,11,12,13,14, 15]

if(varchoice == 'OZNE'):
	colorlist = ['#00FFFF','#00CCFF','#0099FF','#00FF00','#009900','#006600','#FFFF00','#FFE600','#FFCD00','#FF7E00','#FF5000','#FF0000','#990000','#CC0033','#FF00FF']
	colortextlist = ['#000000','#000000','#FFFFFF','#000000','#FFFFFF','#FFFFFF','#000000','#000000','#000000','#000000','#000000','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF']
	colormaxlist = [10,20,30,40,50,60,65,70,75,85,95,105,110,115,500]
	colorminlist = [ 0,10,20,30,40,50,60,65,70,75,85, 95,105,110,115]

if(varchoice in vartemplist):
	colorlist = ['#330033','#990099','#3300CC','#00FFFF','#00CCFF','#0066CC','#0000FF','#003333','#006600','#FFFF00','#FF6600','#FF0000','#FF0066','#FF00FF','#FF99FF','#FFFFFF']
	colortextlist = ['#FFFFFF','#FFFFFF','#FFFFFF','#000000','#000000','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#000000','#000000','#FFFFFF','#FFFFFF','#FFFFFF','#000000','#000000']
	colormaxlist = [-20,-15,-10, -5, 0,5,10,15,20,25,30,35,40,45,50,100]
	colorminlist = [-25,-20,-15,-10,-5,0,5,10,15,20,25,30,35,40,45,50]

if(varchoice in varrhlist):
	colorlist = ['#660000','#990000','#993300','#996600','#663300','#333300','#003300','#006600','#00CC00','#00FF00']
	colortextlist = ['#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#FFFFFF','#000000','#000000']
	colormaxlist = [10,20,30,40,50,60,70,80,90,100]
	colorminlist = [0,10,20,30,40,50,60,70,80,90]
	
legendcolorlist = []
legendlist = []		
for i in range(0,len(colorlist)):
	legendcolorlist.append(colorlist[i])
	if i == 0:
		legendlist.append('< '+"%.2f" % colormaxlist[i])
	elif i == len(colorlist)-1:
		legendlist.append("%.2f" % colorminlist[i]+'+')
	else:
		legendlist.append("%.2f" % colorminlist[i]+' - '+"%.2f" % colormaxlist[i])

## Now start putting lists together for mobile stations, matching up GPS data to data in other queried files
		
timelist = {}
latlist = {}
lonlist = {}
elevlist = {}
datamarkerlist = {}
pm25opacitylist = {}
pm25sizelist = {}
pm25edgelist = {}
pm25edgecolorlist = {}
pm25colorlist = {}

mobiletimestring = time.strftime('yr=%Y&mo=%m&dy=%d&hr=%H&mm=%M',time.localtime(epochend))

nogps = 0
totalgps = 0
for stid in mobilestidlist:
	try:
		checkgps = [x for x in datadict[stid]['cr1000']['GLAT'] if x != -9999.]
	except:
		checkgps = []
	if(len(checkgps) > 0):
		totalgps = totalgps + len(checkgps)
		timelist[stid] = datadict[stid]['cr1000']['EPOCHTIME']
		if(varchoice == 'NSAT' or stid not in traxstidlist):
			latlist[stid] = datadict[stid]['cr1000']['GLAT']
			lonlist[stid] = datadict[stid]['cr1000']['GLON']
			if(stid == 'KSL5'):
				elevlist[stid] = [("%.1f" % x) for x in datadict[stid]['cr1000']['GELV']]
			else:
				elevlist[stid] = [''] * len(datadict[stid]['cr1000']['GELV'])
		else:
			latlist[stid] = [x if y >= 3 else -9999. for (x,y) in zip(datadict[stid]['cr1000']['GLAT'],datadict[stid]['cr1000']['NSAT'])]
			lonlist[stid] = [x if y >= 3 else -9999. for (x,y) in zip(datadict[stid]['cr1000']['GLON'],datadict[stid]['cr1000']['NSAT'])]
			if(stid == 'KSL5'):
				elevlist[stid] = [("%.1f" % x) if y >= 3 else -9999. for (x,y) in zip(datadict[stid]['cr1000']['GELV'],datadict[stid]['cr1000']['NSAT'])]
			else:
				elevlist[stid] = [''] * len(datadict[stid]['cr1000']['GELV'])
		datamarkerlist[stid] = []
		pm25colorlist[stid] = []
		for epochtime in timelist[stid]:
			tmpcolor = '#000000'
			tablecolor[stid] = '#000000'
			tabletextcolor[stid] = '#FFFFFF'
			if(varchoice == 'THTA'):		
				kappa = (287./1004.)
				tmpk = datadict[stid][varfilename['TMPC']]['TMPC'][np.where(datadict[stid][varfilename['TMPC']]['EPOCHTIME'] == epochtime)[0][0]] + 287.15
				tmppres = datadict[stid][varfilename['PRES']]['PRES'][np.where(datadict[stid][varfilename['PRES']]['EPOCHTIME'] == epochtime)[0][0]]
				try:
					thtak = tmpk * ((1000./tmppres)**kappa)
					datamarkerlist[stid].append("%.2f" % thtak)
					for j in range(0,len(colorlist)):
						if(thtak >= colorminlist[j]):
							tmpcolor = colorlist[j]
							tablecolor[stid] = colorlist[j]
							tabletextcolor[stid] = colortextlist[j]
					pm25colorlist[stid].append(tmpcolor)					
					tablevalue[stid] = ("%.2f" % thtak)					
				except:
					datamarkerlist[stid].append(-9999.)
					pm25colorlist[stid].append('#000000')
					tablecolor[stid] = '#000000'
					tabletextcolor[stid] = '#FFFFFF'
					tablevalue[stid] = 'N/A'
				if(stid in traxstidlist):
					rightplotvar = 'GLAT'
				else:
					rightplotvar = 'GELV'
				tablelink[stid] = '/gslso3s/cgi-bin/plot_time_series.cgi?'+mobiletimestring+'&min=1440&tz='+mytzone+'&leftvar='+varchoice+'&rightvar='+rightplotvar+'&'+stid+'=on'
			else:
				try:
					datamarkertmp = datadict[stid][varfilename[varchoice]][varchoice][np.where(datadict[stid][varfilename[varchoice]]['EPOCHTIME'] == epochtime)[0][0]]
					datamarkerlist[stid].append("%.2f" % datamarkertmp)
					for j in range(0,len(colorlist)):
						if(datamarkertmp >= colorminlist[j]):
							tmpcolor = colorlist[j]
							tablecolor[stid] = colorlist[j]
							tabletextcolor[stid] = colortextlist[j]
					pm25colorlist[stid].append(tmpcolor)
					tablevalue[stid] = ("%.2f" % datamarkertmp)
				except:
					datamarkerlist[stid].append(-9999.)
					pm25colorlist[stid].append('#000000')
					tablecolor[stid] = '#000000'
					tabletextcolor[stid] = '#FFFFFF'
					tablevalue[stid] = 'N/A'
				if(stid in traxstidlist):
					rightplotvar = 'GLAT'
				else:
					rightplotvar = 'GELV'
				tablelink[stid] = '/gslso3s/cgi-bin/plot_time_series.cgi?'+mobiletimestring+'&min=1440&tz='+mytzone+'&leftvar='+varchoice+'&rightvar='+rightplotvar+'&'+stid+'=on'
		timelist[stid] = [time.strftime('%Y-%m-%d %H:%M'+tzout,time.localtime(int(x))) for x in timelist[stid]]
		if(opacchoice == 'On' and len(latlist[stid]) > 1):
			pm25opacitylist[stid] = np.linspace(0.3,0.99,len(latlist[stid])).tolist()
		else:
			pm25opacitylist[stid] = np.linspace(1.0,1.0,len(latlist[stid])).tolist()
		pm25sizelist[stid] = [4] * len(latlist[stid])
		pm25edgelist[stid] = [1] * len(latlist[stid])
		pm25edgecolorlist[stid] = ['black'] * len(latlist[stid])	
		if(paston != 1):
			pm25sizelist[stid][-1] = 6
			pm25edgelist[stid][-1] = 2
			pm25edgecolorlist[stid][-1] = 'black'		
	else:
		skip = 1
		
if(totalgps > 0):
	skip = 1
else:
	nogps = 1

## Now request in-situ data from MesoWest API and store in lists as well

stnstidlist = []
stntimelist = []
stnlatlist = []
stnlonlist = []
stndatalist = []
stncolorlist = []

mwtimestring = time.strftime('&day1=%d&month1=%m&year1=%Y&hour1=%H',time.localtime(epochend+3600))

try:
	initialurl = 'http://api.mesowest.net/v2/stations/timeseries?bbox=-114,40,-111,43&network=9,153,1011&start='+apitimestart+'&end='+apitimeend+'&vars='+apivarlist+'&obtimezone=UTC&token='+apitoken
	urlrequest = urllib2.Request(initialurl)
	urlopener = urllib2.build_opener()
	urldata = urlopener.open(urlrequest,timeout=20)
	readdata = urldata.read()
	data = json.loads(readdata)
	ParseDataV2(data)
	for stid in insitustnlat:
		tablecolor[stid] = '#000000'
		tabletextcolor[stid] = '#FFFFFF'
		if(insitulastdata[stid] != ''):
			stnstidlist.append(str(stid))
			stntimelist.append(str(insitulasttime[stid]))
			stnlatlist.append("%.5f" % np.float(insitustnlat[stid]))
			stnlonlist.append("%.5f" % np.float(insitustnlon[stid]))
			stndatalist.append("%.2f" % np.float(insitulastdata[stid]))
			for j in range(0,len(colorlist)):
				if(np.float(insitulastdata[stid]) >= colorminlist[j]):
					tmpcolor = colorlist[j]
					tablecolor[stid] = colorlist[j]
					tabletextcolor[stid] = colortextlist[j]
			stncolorlist.append(tmpcolor)
			tablevalue[stid] = "%.2f" % np.float(insitulastdata[stid])
			tablelink[stid] = 'http://mesowest.utah.edu/cgi-bin/droman/time_chart_dyn.cgi?stn='+str(stid)+'&unit=1&hours=24&past='+str(paston)+mwtimestring+'&time='+mwtzlink+'&var='+mwvarlink[varchoice]+'&level=All'
except:
	skip = 1

## Now request MOPED Data

if(minback <= 180 and varmoped[varchoice] > 0):
	mopedarchivedir = "/uufs/chpc.utah.edu/common/home/horel-group/archive/"
	mopedhrlist = np.arange((-1*minback),90,60)
	for mopedhr in mopedhrlist:
		currmopedfile = mopedarchivedir+time.strftime('%Y%m%d',time.gmtime(epochend+(mopedhr*60)))+'/moped_data/'+time.strftime('%Y%m%d%H',time.gmtime(epochend+(mopedhr*60)))+'00_uu2dvar_moped_5min.csv.gz'
		ParseMOPED(currmopedfile)
	for stid in mopedstidlist:
		mobilestnname[stid] = 'Freight Truck'
		nogps = 0
		if(opacchoice == 'On' and len(latlist[stid]) > 1):
			pm25opacitylist[stid] = np.linspace(0.3,0.99,len(latlist[stid])).tolist()
		else:
			pm25opacitylist[stid] = np.linspace(1.0,1.0,len(latlist[stid])).tolist()
		pm25sizelist[stid] = [4] * len(latlist[stid])
		pm25edgelist[stid] = [1] * len(latlist[stid])
		pm25edgecolorlist[stid] = ['black'] * len(latlist[stid])	
		if(paston != 1):
			pm25sizelist[stid][-1] = 6
			pm25edgelist[stid][-1] = 2
			pm25edgecolorlist[stid][-1] = 'black'
		tablelink[stid] = ''
	
## Begin HTML content
	
print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<title>Ozone Study Map Archive</title>
<script src="/gslso3s/js/site/siteopen.js"></script>
</head>
<body>
<script src="/gslso3s/js/site/sitemenu.js"></script>
<br>
<b><font COLOR="#0000DD" SIZE=+3>Great Salt Lake Summer Ozone Study - Map Interface</font></b>
<br><br>
<div style="width:900px">
This page provides access to observations that were collected as part of the Great Salt Lake Summer 2015 Ozone Study.  To choose a different time period or different variables, please use the options given below.
<br><br>

<form method="GET" action="map.cgi">
	<b>Final Observation Time:</b><span style="padding-left:20px">
	Year:
	<select name="yr">'''
for i in range(2014,int(curyr)+1):
	if yr == ("%04d" % i):
		print '''		<option selected="selected">'''+"%04d" % i+'''</option>'''
	else:
		print '''		<option>'''+"%04d" % i+'''</option>'''
print'''	</select>
	<span style="padding-left:10px">
	Month:
	<select name="mo">'''
for i in range(1,13):
	if mo == ("%02d" % i):
		print '''		<option selected="selected">'''+"%02d" % i+'''</option>'''
	else:
		print '''		<option>'''+"%02d" % i+'''</option>'''
print'''	</select>	
	<span style="padding-left:10px">
	Day:
	<select name="dy">'''	
for i in range(1,32):
	if dy == ("%02d" % i):
		print '''		<option selected="selected">'''+"%02d" % i+'''</option>'''
	else:
		print '''		<option>'''+"%02d" % i+'''</option>'''
print'''	</select>
	<span style="padding-left:10px">
	Hour:
	<select name="hr">'''	
for i in range(0,24):
	if hr == ("%02d" % i):
		print '''		<option selected="selected">'''+"%02d" % i+'''</option>'''
	else:
		print '''		<option>'''+"%02d" % i+'''</option>'''
print'''	</select>
	<span style="padding-left:10px">
	Minute:
	<select name="mm">'''	
for i in range(0,60):
	if mm == ("%02d" % i):
		print '''		<option selected="selected">'''+"%02d" % i+'''</option>'''
	else:
		print '''		<option>'''+"%02d" % i+'''</option>'''
print'''	</select>
	<br><br>
	<b>Primary Options:</b><span style="padding-left:20px">
	Timezone:
	<select name="tz">'''

for option in tzoptionlist:
	if mytzone == option:
		print '''		<option selected="selected" value="'''+option+'''">'''+tzoptions[option]+'''</option>'''
	else:
		print '''		<option value="'''+option+'''">'''+tzoptions[option]+'''</option>'''
print'''	</select>	
	<span style="padding-left:10px">
	Period:
	<select name="min">'''

minint = [30,60,120,180,360,720,1440]
timeint = ['30 min','1 hr','2 hr','3 hr','6 hr','12 hr','1 day']

for i in range(0,len(minint)):
	if str(minback) == str(minint[i]):
		print '''		<option selected="selected" value="'''+str(minint[i])+'''">'''+timeint[i]+'''</option>'''
	else:
		print '''		<option value="'''+str(minint[i])+'''">'''+timeint[i]+'''</option>'''
print'''	</select>
	<span style="padding-left:10px">	
	Variable:
	<select name="var">'''

for option in varoptionlist:
	if varchoice == option:
		print '''		<option selected="selected" value="'''+option+'''">'''+varoptions[option]+'''</option>'''
	else:
		print '''		<option value="'''+option+'''">'''+varoptions[option]+'''</option>'''
print'''	</select>
	<span style="padding-left:10px">	
	Opacity by Time:
	<select name="opacchange">'''

for option in opacoptionlist:
	if opacchoice == option:
		print '''		<option selected="selected" value="'''+option+'''">'''+option+'''</option>'''
	else:
		print '''		<option value="'''+option+'''">'''+option+'''</option>'''
print'''	</select>
<br><br>
<input type="hidden" name="past" value="1">
<input type="hidden" name="region" value="'''+myregion+'''">
<input type="submit" value="Update Time and Primary Options">
</form><br><br>
<b>Map Layer Controls:</b><span style="padding-left:20px">
<input type="button" id="showmopedlink" value="Show Freight Truck Obs">
<input type="button" id="hidemopedlink" value="Hide Freight Truck Obs">
<input type="button" id="showmobilelink" value="Show Other Mobile Obs">
<input type="button" id="hidemobilelink" value="Hide Other Mobile Obs">
<input type="button" id="showsfclink" value="Show In-Situ Obs">
<input type="button" id="hidesfclink" value="Hide In-Situ Obs">
<input type="button" id="showobs" value="Load Weather Obs">
<span id="obsloading">Observations now loading...</span>
<input type="button" id="hideobs" value="Hide Weather Obs">
<br><br>
<b>Map View Options:</b><span style="padding-left:20px">
<input type="button" onClick="parent.location='/gslso3s/cgi-bin/map.cgi?tz='''+mytzone+'''&region=GSL&yr='''+str(yr)+'''&mo='''+str(mo)+'''&dy='''+str(dy)+'''&hr='''+str(hr)+'''&mm='''+str(mm)+'''&min='''+str(minback)+'''&var='''+varchoice+'''&opacchange='''+opacchoice+'''&past='''+str(paston)+''''" value="View Great Salt Lake">
<input type="button" onClick="parent.location='/gslso3s/cgi-bin/map.cgi?tz='''+mytzone+'''&region=SYR&yr='''+str(yr)+'''&mo='''+str(mo)+'''&dy='''+str(dy)+'''&hr='''+str(hr)+'''&mm='''+str(mm)+'''&min='''+str(minback)+'''&var='''+varchoice+'''&opacchange='''+opacchoice+'''&past='''+str(paston)+''''" value="View Antelope Island">
<input type="button" onClick="parent.location='/gslso3s/cgi-bin/map.cgi?tz='''+mytzone+'''&region=SLC&yr='''+str(yr)+'''&mo='''+str(mo)+'''&dy='''+str(dy)+'''&hr='''+str(hr)+'''&mm='''+str(mm)+'''&min='''+str(minback)+'''&var='''+varchoice+'''&opacchange='''+opacchoice+'''&past='''+str(paston)+''''" value="View Salt Lake and Tooele Valleys">
<br><br>
<div id="map" style="width: 900px; height: 600px"></div>
<br>
Diamond markers represent data from available freight trucks.  Circle markers represent data from Utah Transportation Authority TRAX light rail cars and other mobile sources.  Square markers are observations collected from deployed in-situ stations.  Marker color is based on observation value according to the legend on the map.
<br><br>
Weather observations from of the <a href='http://mesowest.org/api' target="_blank">MesoWest API Services</a> can be plotted by clicking the "Load Weather Obs" button above the map.  Observations will be plotted in wind barb format similar to <a href='http://mesowest.utah.edu' target="_blank">MesoWest</a>.  Red numbers indicate temperature in degrees Celsius.  Green numbers indicate relative humidity.  Wind barbs show wind speed in meters per second (one full barb is 5 meters per second).  Wind gust values larger than 5 meters per second are also shown in yellow if available.
<br><br>
The table below provides the last '''+str(varoptions[varchoice].lower())+''' observation collected from each platform available on the map for the time period selected, with links to time series graphs available as well to show data over the previous 24 hours.  Rows can be sorted by clicking on the table headers.
<br>
<script>'''

## Beginning of mapping section, create javascript lists using lists from earlier querying

for stid in mobilestidlist:
	try:
		if(showstn[stid] == 1):
			print '''	var alltimes'''+stid+''' = '''+str(timelist[stid])+'''
	var alllats'''+stid+''' = '''+str(latlist[stid])+'''
	var alllons'''+stid+''' = '''+str(lonlist[stid])+'''
	var allelevs'''+stid+''' = '''+str(elevlist[stid])+'''
	var alldata'''+stid+''' = '''+str(datamarkerlist[stid])+'''
	var allopac'''+stid+''' = '''+str(pm25opacitylist[stid])+'''
	var allsize'''+stid+''' = '''+str(pm25sizelist[stid])+'''
	var alledge'''+stid+''' = '''+str(pm25edgelist[stid])+'''
	var alledgecolor'''+stid+''' = '''+str(pm25edgecolorlist[stid])+'''
	var allcolors'''+stid+''' = '''+str(pm25colorlist[stid])
	except:
		skip = 1
	
print '''	var stnstids = '''+str(stnstidlist)+'''
	var stntimes = '''+str(stntimelist)+'''
	var stnlats = '''+str(stnlatlist)+'''
	var stnlons = '''+str(stnlonlist)+'''
	var stndata = '''+str(stndatalist)+'''
	var stncolor = '''+str(stncolorlist)

## Draw map, extra layers, and legend
	
print'''	var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/3eb45b95929d472d8fe4a2a5dafbd314/998/256/{z}/{x}/{y}.png',
		cloudmadeUrl = 'http://{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png',
		subDomains = ['otile1','otile2','otile3','otile4'],
		cloudmadeAttribution = 'Map data &copy; '''+str(curyr)+''' OpenStreetMap contributors, Imagery &copy; '''+str(curyr)+''' MapQuest',
		cloudmade = new L.TileLayer(cloudmadeUrl, {
			maxZoom: 18, 
			attribution: cloudmadeAttribution, 
			subdomains: subDomains, 
			unloadInvisibleTiles: true,
			updateWhenIdle:false
		});
	map = new L.Map('map', {
		center: new L.LatLng('''+regionmap[myregion]+'''), 
		zoom: '''+regionmapzoom[myregion]+''', 
		layers: [cloudmade]
	});
	var nexradurl = 'http://mesonet.agron.iastate.edu/cache/tile.py/1.0.0/nexrad-n0r/{z}/{x}/{y}.png?'+(new Date()).getTime(),
	nexradAttribution = 'Radar data &copy; '''+str(curyr)+''' Iowa Environmental Mesonet'
	nexrad = new L.TileLayer(nexradurl, {
		opacity: 0.6,
		attribution: nexradAttribution
	}).addTo(map);
	
	var legend = L.control({position: 'bottomleft'});	
	legend.onAdd = function (map) {
		var div = L.DomUtil.create('div', 'legendinfo legend'),
			legendbg = '''+str(legendcolorlist)+''',
			legendtxt = '''+str(legendlist)+''',
			labels = ['<b>Legend ('''+varunits[varchoice]+''')</b>'];
		for (var i = 0; i < legendbg.length; i++) {
			labels.push('<i style="background:'+legendbg[i]+'"></i> '+legendtxt[i]+'');
		}
		div.innerHTML = labels.join('<br>');
		return div;
	};
	legend.addTo(map);'''

print'''	var topinfo = L.control();
	topinfo.onAdd = function (map) {
		this._div = L.DomUtil.create('div','legendinfo');
		this.update();
		return this._div;
	};
	topinfo.update = function (props) {
		this._div.innerHTML = '<font color="black">Data from '''+pasttimestring+'''<br>to '''+currtimestring+'''</font>';		
	};
	topinfo.addTo(map);'''

## Plot mobile obs

if(nogps == 0):
	print '''	var datamarkerlist = [];
	var mopedmarkerlist = [];'''
	for stid in mobilestidlist:
		if stid in mopedstidlist:
			shape = 'Diamond'
		else:
			shape = 'Circle'
		try:
			if(showstn[stid] == 1):
				testtime = timelist[stid][-1]
			print'''	for (var j=0;j<alltimes'''+stid+'''.length;j++) {
		if(alllons'''+stid+'''[j] != -9999) {'''
			if(stid == 'KSL5'):
				print'''			iconHTML = '<font color="black"><b>'''+stid+'''<br>'+alltimes'''+stid+'''[j]+'</b><br>'+alldata'''+stid+'''[j]+' '''+varunits[varchoice]+''' ('+allelevs'''+stid+'''[j]+' m ASL)</sup></font>\''''
			else:
				print'''			iconHTML = '<font color="black"><b>'''+stid+'''<br>'+alltimes'''+stid+'''[j]+'</b><br>'+alldata'''+stid+'''[j]+' '''+varunits[varchoice]+'''</sup></font>\''''
			print'''			var mystnplot = new L.'''+shape+'''Marker(new L.LatLng(alllats'''+stid+'''[j],alllons'''+stid+'''[j]), {
				radius: allsize'''+stid+'''[j],
				color: alledgecolor'''+stid+'''[j],
				weight: alledge'''+stid+'''[j],
				opacity: allopac'''+stid+'''[j],
				fillColor: allcolors'''+stid+'''[j],
				fillOpacity: allopac'''+stid+'''[j]
			});
			mystnplot.bindPopup(iconHTML);'''	
			if stid in mopedstidlist:
				print'''			mopedmarkerlist.push(mystnplot);'''
			else:
				print'''			datamarkerlist.push(mystnplot);'''
			print'''		}
	}'''
		except:
			skip = 1
	print'''	mobileobslayer = L.layerGroup(datamarkerlist);
	mopedobslayer = L.layerGroup(mopedmarkerlist);'''

## Plot in-situ obs

print '''	var stnmarkerlist = [];
for (var j=0;j<stntimes.length;j++) {
	if(stnlons[j] != -9999) {
		iconHTML = '<font color="black"><b><a href="http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn='+stnstids[j]+'&past='''+str(paston)+'''&unit=1'''+mwtimestring+'''&time='''+mwtzlink+'''" target="_blank">'+stnstids[j]+'</a><br>'+stntimes[j]+'</b><br>'+stndata[j]+' '''+varunits[varchoice]+'''</sup></font>'
		var mystaticstnplot = new L.SquareMarker(new L.LatLng(stnlats[j],stnlons[j]), {
			radius: 4,
			color: 'black',
			weight: 1,
			opacity: 1,
			fillColor: stncolor[j],
			fillOpacity: 1
		});
		mystaticstnplot.bindPopup(iconHTML);
		stnmarkerlist.push(mystaticstnplot);
	}
}
stnobslayer = L.layerGroup(stnmarkerlist);'''

## JQuery section for buttons to show/hide layers

print '''</script>
<script>
$(document).ready(function() {
	$("#obsloading").hide();
	$("#hideobs").hide();
	$("#hideradlink").hide();
	map.removeLayer(nexrad);
	$("#showsfclink").hide();
	$("#showmopedlink").hide();
	stnobslayer.addTo(map);
	$("#showmobilelink").hide();'''
	
if(nogps == 0):
	print '''	mobileobslayer.addTo(map);
	mopedobslayer.addTo(map);'''

print'''	$("#hideradlink").click(function(){
		$("#showradlink").show();
		$("#hideradlink").hide();
		map.removeLayer(nexrad);
	});
	$("#showradlink").click(function(){
		$("#showradlink").hide();
		$("#hideradlink").show();
		nexrad.addTo(map);
	});	
	$("#hidemopedlink").click(function(){
		$("#showmopedlink").show();
		$("#hidemopedlink").hide();
		map.removeLayer(mopedobslayer);
	});
	$("#showmopedlink").click(function(){
		$("#showmopedlink").hide();
		$("#hidemopedlink").show();
		mopedobslayer.addTo(map);
	});
	$("#hidemobilelink").click(function(){
		$("#showmobilelink").show();
		$("#hidemobilelink").hide();'''
		
if(nogps == 0):
	print'''		map.removeLayer(mobileobslayer);'''

print'''	});
	$("#showmobilelink").click(function(){
		$("#showmobilelink").hide();
		$("#hidemobilelink").show();'''
		
if(nogps == 0):
	print'''		mobileobslayer.addTo(map);'''

print'''	});
	$("#hidesfclink").click(function(){
		$("#showsfclink").show();
		$("#hidesfclink").hide();
		map.removeLayer(stnobslayer);
	});
	$("#showsfclink").click(function(){
		$("#showsfclink").hide();
		$("#hidesfclink").show();
		stnobslayer.addTo(map);
	});
	$("#obsloading").hide();
	$("#hideobs").click(function(){
		obslayer.clearLayers();
		$("#showobs").show();
		$("#hideobs").hide();
	});'''
	
## JQuery which queries MesoWest API for meteorological obs layer
	
print'''	$("#showobs").click(function(){
		$("#showobs").hide();
		$("#obsloading").show();
		args = {
			radius: map.getCenter().lat+','+map.getCenter().lng+',70',
			vars: 'air_temp,relative_humidity,wind_speed,wind_direction,wind_gust',
			start: '''+apitimestart+''',
			end: '''+apitimeend+''',
			token: mytoken,
			obtimezone: 'UTC',
			units: 'METRIC',
		};
		$.getJSON('http://api.mesowest.net/v2/stations/timeseries?callback=?', args, function( data ) {
			var apimarkerlist = [];
			for (stnindex in data.STATION) {
				stndata = data.STATION[stnindex]
				tmpc = stndata.OBSERVATIONS['air_temp_set_1']
				dwpc = stndata.OBSERVATIONS['relative_humidity_set_1']
				sknt = stndata.OBSERVATIONS['wind_speed_set_1']
				drct = stndata.OBSERVATIONS['wind_direction_set_1']
				gust = stndata.OBSERVATIONS['wind_gust_set_1']
				dattim = stndata.OBSERVATIONS['date_time']
				iconHTML = '<b><a href="http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn='+stndata.STID+'&past='''+str(paston)+'''&unit=1'''+mwtimestring+'''&time='''+mwtzlink+'''" target="_blank">'+stndata.STID+'</a>'
				try {
					dattimarray = dattim[sknt.length-1].split("T");
					var apimarker = L.marker([stndata.LATITUDE,stndata.LONGITUDE], {
						icon: L.icon({iconUrl: '/gslso3s/css/barbs/barb_0.png',iconSize: [80, 80],iconAnchor: [40, 40],}),
						iconAngle: drct[sknt.length-1],
					});
					iconHTML += '<br>'+dattimarray[0]+' '+dattimarray[1].slice(0,-1)+' UTC</b>'					
					try {
						tmpcplot = tmpc[sknt.length-1]
						if(tmpcplot !== null) {
							tmpcplot = Math.round(tmpcplot)
							var apitmpcmarker = L.marker([stndata.LATITUDE,stndata.LONGITUDE], {
								icon: L.divIcon({html: '<div class="tmpflabel">'+tmpcplot+'</div>',iconAnchor:[20,20]})
							});
							iconHTML += '<br>Temp: '+tmpc[sknt.length-1]+' C'
							apimarkerlist.push(apitmpcmarker);
						}
					} catch(err) {
						var tmpcskip = 1;
					}				
					try {
						dwpcplot = dwpc[sknt.length-1]
						if(dwpcplot > 0) {
							dwpcplot = Math.round(dwpcplot)
							var apidwpcmarker = L.marker([stndata.LATITUDE,stndata.LONGITUDE], {
								icon: L.divIcon({html: '<div class="dwpflabel">'+dwpcplot+'%</div>',iconAnchor:[20,-3]})
							});
							iconHTML += '<br>RH: '+dwpc[sknt.length-1]+'%'
							apimarkerlist.push(apidwpcmarker);
						}
					} catch(err) {
						var dwpcskip = 1;
					}
					try {
						if(sknt[sknt.length-1] > 0 && sknt[sknt.length-1] < 2.5) {
							skntint = 1
						}
						else {
							skntint = Math.floor(2*sknt[sknt.length-1]/5)*5
						}
						apimarker = L.marker([stndata.LATITUDE,stndata.LONGITUDE], {
							icon: L.icon({iconUrl: '/gslso3s/css/barbs/barb_'+skntint+'.png',iconSize: [80, 80],iconAnchor: [40, 40],}),
							iconAngle: drct[sknt.length-1],
						});
					} catch(err) {
						var plotskip = 1;
					}
					if(sknt[sknt.length-1] > 0) {
						if(drct[sknt.length-1] >= 348.75 || drct[sknt.length-1] < 11.25) {
							iconHTML += '<br>N at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 11.25 && drct[sknt.length-1] < 33.75) {
							iconHTML += '<br>NNE at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 33.75 && drct[sknt.length-1] < 56.25) {
							iconHTML += '<br>NE at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 56.25 && drct[sknt.length-1] < 78.75) {
							iconHTML += '<br>ENE at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 78.75 && drct[sknt.length-1] < 101.25) {
							iconHTML += '<br>E at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 101.25 && drct[sknt.length-1] < 123.75) {
							iconHTML += '<br>ESE at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 123.75 && drct[sknt.length-1] < 146.25) {
							iconHTML += '<br>SE at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 146.25 && drct[sknt.length-1] < 168.75) {
							iconHTML += '<br>SSE at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 168.75 && drct[sknt.length-1] < 191.25) {
							iconHTML += '<br>S at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 191.25 && drct[sknt.length-1] < 213.75) {
							iconHTML += '<br>SSW at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 213.75 && drct[sknt.length-1] < 236.25) {
							iconHTML += '<br>SW at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 236.25 && drct[sknt.length-1] < 258.75) {
							iconHTML += '<br>WSW at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 258.75 && drct[sknt.length-1] < 281.25) {
							iconHTML += '<br>W at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 281.25 && drct[sknt.length-1] < 303.75) {
							iconHTML += '<br>WNW at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 303.75 && drct[sknt.length-1] < 326.25) {
							iconHTML += '<br>NW at '+sknt[sknt.length-1]+' m/s'
						}
						else if(drct[sknt.length-1] >= 326.25 && drct[sknt.length-1] < 348.75) {
							iconHTML += '<br>NNW at '+sknt[sknt.length-1]+' m/s'
						}
						else {
							iconHTML += '<br>Speed '+sknt[sknt.length-1]+' m/s'
						}
					}
					else {
						iconHTML += '<br>CALM'
					}
					try {
						if(gust[sknt.length-1] >= 5) {
							gustplot = gust[sknt.length-1]
							gustplot = Math.round(gustplot)
							var apigustmarker = L.marker([stndata.LATITUDE,stndata.LONGITUDE], {
								icon: L.divIcon({html: '<div class="gustlabel">'+gustplot+'</div>',iconAnchor:[-5,20]})
							});
							iconHTML += '<br>Gusting to '+gust[sknt.length-1]+' m/s'
							apimarkerlist.push(apigustmarker);
						}
					} catch(err) {
						var gustskip = 1;
					}						
					apimarker.bindPopup(iconHTML);
					apimarkerlist.push(apimarker);
				} catch(err) {
					var skip = 1;
				}
			}
			obslayer = L.layerGroup(apimarkerlist).addTo(map);
			$("#obsloading").hide();
			$("#hideobs").show();
		});
	});
});	
</script><br>'''

## Finally, the tabular section below the map

print'''</div>'''

if(mytzone == 'local'):
	print'''<b><font SIZE=+1 color="#0000CC">Final Time '''+currtimestring+''' ('''+currtimestringutc+''')</font></b><br>'''
else:
	print'''<b><font SIZE=+1 color="#0000CC">Final Time '''+currtimestring+'''</font></b><br>'''

print'''<table id="table1" class="sortable" width="1000">'''
print'''<tr><th class="table1" width="100"><font SIZE=+1><b>Type</b></font></th><th class="table1"><font SIZE=+1><b>Station</b></font></th><th class="table1"><font SIZE=+1><b>Last Record Available</b></font></th><th class="table1"><font SIZE=+1><b>'''+varoptions[varchoice]+'''</b></font></th><th class="table1" ><b><font SIZE=+1>Additional Links</font></b></th></tr>'''	
for stid in sorted(mobilestidlist):
	try:
		if(len(tablelink[stid]) > 5):
			print'''<tr><td class="table1"><font><b>Mobile</b></font></td><td class="table1"><font><b>'''+("%s (%s)" % (mobilestnname[stid],stid))+'''</b></font></td><td class="table1"><font><b>'''+timelist[stid][-1]+'''</b></font></td><td class="table1" sorttable_customkey="'''+("%d" % (float(tablevalue[stid])*100))+'''" bgcolor="'''+tablecolor[stid]+'''"><font color="'''+tabletextcolor[stid]+'''"><b>'''+tablevalue[stid]+''' '''+varunits[varchoice]+'''</font></b></td><td class="table1"><font><b><a href="'''+tablelink[stid]+'''" target="_blank">24hr Graph</a></b></font></td></tr>'''
		else:
			print'''<tr><td class="table1"><font><b>Mobile</b></font></td><td class="table1"><font><b>'''+("%s (%s)" % (mobilestnname[stid],stid))+'''</b></font></td><td class="table1"><font><b>'''+timelist[stid][-1]+'''</b></font></td><td class="table1" sorttable_customkey="'''+("%d" % (float(tablevalue[stid])*100))+'''" bgcolor="'''+tablecolor[stid]+'''"><font color="'''+tabletextcolor[stid]+'''"><b>'''+tablevalue[stid]+''' '''+varunits[varchoice]+'''</font></b></td><td class="table1"><font><b>-</b></font></td></tr>'''			
	except:
		try:
			print'''<tr><td class="table1"><font SIZE=+1><b>Mobile</b></font></td><td class="table1"><font SIZE=+1><b>'''+("%s (%s)" % (mobilestnname[stid],stid))+'''</b></font></td><td class="table1" colspan="2"><b><font SIZE=+1>No real-time data within '''+str(minback)+''' minutes</font></b></td><td class="table1"><font SIZE=+1><b><a href="'''+tablelink[stid]+'''" target="_blank">24hr Graph</a></b></font></td></tr>'''
		except:
			skip = 1
for stid in sorted(insitulasttime,key=insitulasttime.get,reverse=True):
	try:
		print'''<tr><td class="table1"><font><b>In-Situ</b></font></td><td class="table1"><font><b>'''+("%s (%s)" % (insitustnname[stid],stid))+'''</b></font></td><td class="table1"><font><b>'''+insitulasttime[stid]+'''</b></font></td><td class="table1" sorttable_customkey="'''+("%d" % (float(tablevalue[stid])*100))+'''" bgcolor="'''+tablecolor[stid]+'''"><font color="'''+tabletextcolor[stid]+'''"><b>'''+tablevalue[stid]+''' '''+varunits[varchoice]+'''</font></b></td><td class="table1"><font><b><a href="'''+tablelink[stid]+'''" target="_blank">24hr Graph</a></b></font></td></tr>'''
	except:
		skip = 1
print'''</table>'''

print'''<script src="/gslso3s/js/site/siteclose.js"></script>
</body>
</html>
'''

sys.exit()
