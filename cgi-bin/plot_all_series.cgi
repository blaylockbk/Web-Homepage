#!/usr/local/bin/python

import numpy as np
import cgi, cgitb
cgitb.enable()
import matplotlib as mpl
mpl.use('Agg')
import gzip, os, sys, datetime, re, time, urllib2, json, calendar
from matplotlib import pyplot
import tables as pytbls
from scipy import signal as sig

print "Content-Type: image/png\n"
# print "Content-Type: text/plain\n"

## Get arguments from storage or use default if any errors are thrown

form = cgi.FieldStorage()

try:
	stidstringlist = form["stids"].value
except:
	stidstringlist = ''

try:
	mytzone = form["tz"].value
except:
	mytzone = 'local'
	
if(mytzone != 'utc'):
	mytzone = 'local'

try:
	mystat = form["stat"].value
except:
	mystat = 'obs'
	
if(mystat != '8hr'):
	mystat = 'obs'
	
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
except:
	if(mytzone == 'utc'):
		yr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y')
		mo = datetime.datetime.strftime(datetime.datetime.utcnow(),'%m')
		dy = datetime.datetime.strftime(datetime.datetime.utcnow(),'%d')
		# hr = datetime.datetime.strftime(datetime.datetime.utcnow(),'%H')
		# mm = datetime.datetime.strftime(datetime.datetime.utcnow(),'%M')
	else:
		yr = datetime.datetime.strftime(datetime.datetime.now(),'%Y')
		mo = datetime.datetime.strftime(datetime.datetime.now(),'%m')
		dy = datetime.datetime.strftime(datetime.datetime.now(),'%d')
		# hr = datetime.datetime.strftime(datetime.datetime.now(),'%H')
		# mm = datetime.datetime.strftime(datetime.datetime.now(),'%M')			

try:
	stidstringlistarray = stidstringlist.split(',')
except:
	stidstringlistarray = []

## Define data type choice dictionaries

varoptions = {'TMPC': 'Temperature',
'RELH': 'Relative Humidity',
'PM25': 'PM2.5 Concentration',
'VOLT': 'Battery Voltage',
'OZNE': 'Ozone Concentration'}

varunits = {'TMPC': 'Temperature (C)',
'RELH': 'Humidity (%)',
'PM25': 'PM2.5 (ug/m3)',
'VOLT': 'Battery (volts)',
'OZNE': 'Ozone (ppbv)'
}

varapi = {'TMPC': 'air_temp',
'RELH': 'relative_humidity',
'PM25': 'PM_25_concentration',
'VOLT': 'volt',
'OZNE': 'ozone_concentration'}

try:
	leftvarchoice = form["leftvar"].value
except:
	leftvarchoice = 'OZNE'

if(leftvarchoice not in varoptions):
	leftvarchoice = 'OZNE'

rightvarchoice = 'None'
if(rightvarchoice not in varoptions):
	rightvarchoice = 'None'

try:
	minback = int(form["min"].value)
except:
	minback = 1440
if(minback > 43200):
	minback = 43200
if(minback < 1440):
	minback = 1440

try:
	epochend = int(time.mktime(time.strptime(yr+mo+dy+'0000','%Y%m%d%H%M')))+86400
except:
	epochend = ((int(time.mktime(time.localtime()))/86400)*86400)+86400

if(mystat == '8hr'):
	epochstart = int(epochend-(60.*minback)-(8*3600))
else:
	epochstart = int(epochend-(60.*minback))

currtimestring = time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochend))
pasttimestring = time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochstart))

apitimeend = time.strftime('%Y%m%d%H%M',time.gmtime(epochend))
apitimestart = time.strftime('%Y%m%d%H%M',time.gmtime(epochstart))
epochstartstat = int(epochend-(60.*minback))

# print apitimestart,apitimeend

if(time.localtime(epochend).tm_isdst == 1):
	utctzoff = utctzoff-3600

# print utctzoff
	
## Define MesoWest V2 API Parsing Function and Defaults

apitoken = 'a94df50babad4344bd7e183c5688c5e6'
apivarlist = varapi[leftvarchoice]
vardatalistv2 = [str(varapi[leftvarchoice])+'_set_1']

stidlist = []
insitustnlat = {}
insitustnlon = {}
insitutimelist = {}
insitudatalist = {}

def ParseDataV2(jsondata):
	for station in jsondata['STATION']:
		insitustnlat[station['STID']] = station['LATITUDE']
		insitustnlon[station['STID']] = station['LONGITUDE']
		insitudatalist[station['STID']] = ''
		if(station['STID'] == 'QH3' or station['STID'] == 'QHW'):
			vardatalistv2 = [str(varapi[leftvarchoice])+'_set_2']
		else:
			vardatalistv2 = [str(varapi[leftvarchoice])+'_set_1']
		try:
			if(len(stidstringlistarray[0]) > 0):
				if(int(station['MNET_ID']) < 2000 and station['STID'] in stidstringlistarray):
					for key in station['OBSERVATIONS']:
						if key in vardatalistv2:
							temptimelist = ''
							templist = ''
							temptimelist_filter1 = ''
							templist_filter1 = ''
							temptimelist_filter2 = ''
							templist_filter2 = ''
							temptimelist = station['OBSERVATIONS']['date_time']					
							templist = station['OBSERVATIONS'][key]
							templist_filter1 = [v for v in templist if v is not None]
							temptimelist_filter1 = [v for v,w in zip(temptimelist,templist) if w is not None]
							templist_filter2 = [v for v in templist_filter1 if v != '']
							temptimelist_filter2 = [v for v,w in zip(temptimelist_filter1,templist_filter1) if w != '']
							temptimelist_filter2 = [int(calendar.timegm(time.strptime(v,'%Y-%m-%dT%H:%M:%SZ'))) for v in temptimelist_filter2]
							if(mystat == '8hr'):
								new8hrtimelist = []
								new8hrdatalist = []
								for k in range(0,len(temptimelist_filter2)):
									if(temptimelist_filter2[k] >= epochstartstat):
										temp8hrtime = [v for v,w in zip(temptimelist_filter2,templist_filter2) if (temptimelist_filter2[k]-v) >= 0 and (temptimelist_filter2[k]-v) < (8*3600)]
										temp8hrdata = [w for v,w in zip(temptimelist_filter2,templist_filter2) if (temptimelist_filter2[k]-v) >= 0 and (temptimelist_filter2[k]-v) < (8*3600)]										
										temp8hrtimecheck = temp8hrtime[-1] - temp8hrtime[0]
										if(temp8hrtimecheck > (5*3600)):
											new8hrtimelist.append(temptimelist_filter2[k])
											new8hrdatalist.append(np.mean(temp8hrdata))
								temptimelist_filter2 = new8hrtimelist
								templist_filter2 = new8hrdatalist
							if(mytzone == 'local'):
								temptimelist_filter2 = [x-utctzoff for x in temptimelist_filter2]
							insitutimelist[station['STID']] = temptimelist_filter2
							insitudatalist[station['STID']] = templist_filter2
							if(len(insitudatalist[station['STID']]) > 0):
								stidlist.append(station['STID'])				
			else:
				if(int(station['MNET_ID']) < 2000):
					for key in station['OBSERVATIONS']:
						if key in vardatalistv2:
							temptimelist = ''
							templist = ''
							temptimelist_filter1 = ''
							templist_filter1 = ''
							temptimelist_filter2 = ''
							templist_filter2 = ''
							temptimelist = station['OBSERVATIONS']['date_time']					
							templist = station['OBSERVATIONS'][key]
							templist_filter1 = [v for v in templist if v is not None]
							temptimelist_filter1 = [v for v,w in zip(temptimelist,templist) if w is not None]
							templist_filter2 = [v for v in templist_filter1 if v != '']
							temptimelist_filter2 = [v for v,w in zip(temptimelist_filter1,templist_filter1) if w != '']
							temptimelist_filter2 = [int(calendar.timegm(time.strptime(v,'%Y-%m-%dT%H:%M:%SZ'))) for v in temptimelist_filter2]
							if(mystat == '8hr'):
								new8hrtimelist = []
								new8hrdatalist = []
								for k in range(0,len(temptimelist_filter2)):
									if(temptimelist_filter2[k] >= epochstartstat):
										temp8hrtime = [v for v,w in zip(temptimelist_filter2,templist_filter2) if (temptimelist_filter2[k]-v) >= 0 and (temptimelist_filter2[k]-v) < (8*3600)]
										temp8hrdata = [w for v,w in zip(temptimelist_filter2,templist_filter2) if (temptimelist_filter2[k]-v) >= 0 and (temptimelist_filter2[k]-v) < (8*3600)]
										temp8hrtimecheck = temp8hrtime[-1] - temp8hrtime[0]
										if(temp8hrtimecheck >= (5*3600)):
											new8hrtimelist.append(temptimelist_filter2[k])
											new8hrdatalist.append(np.mean(temp8hrdata))
								temptimelist_filter2 = new8hrtimelist
								templist_filter2 = new8hrdatalist
							if(mytzone == 'local'):
								temptimelist_filter2 = [x-utctzoff for x in temptimelist_filter2]
							insitutimelist[station['STID']] = temptimelist_filter2
							insitudatalist[station['STID']] = templist_filter2
							if(len(insitudatalist[station['STID']]) > 0):
								stidlist.append(station['STID'])				
		except:
			skip = 1

## Now request in-situ data from MesoWest API and store in lists as well

stnstidlist = []
stntimelist = []
stnlatlist = []
stnlonlist = []
stndatalist = []
stncolorlist = []

mwtimestring = time.strftime('&day1=%d&month1=%m&year1=%Y&hour1=%H',time.localtime(epochend+3600))

try:
	#if(len(stidstringlist) > 0):
		#initialurl = 'http://api.mesowest.net/v2/stations/timeseries?stid='+stidstringlist+'&start='+apitimestart+'&end='+apitimeend+'&vars='+apivarlist+'&obtimezone=UTC&token='+apitoken
	#else:
	initialurl = 'http://api.mesowest.net/v2/stations/timeseries?bbox=-114,40,-111,43&network=9,153,1011&start='+apitimestart+'&end='+apitimeend+'&vars='+apivarlist+'&obtimezone=UTC&token='+apitoken
	urlrequest = urllib2.Request(initialurl)
	urlopener = urllib2.build_opener()
	urldata = urlopener.open(urlrequest,timeout=90)
	readdata = urldata.read()
	data = json.loads(readdata)
	ParseDataV2(data)
except:
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
		try:
			filterrawtimes[stid] = sorted(insitutimelist[stid])
			filterrawdata[stid] = [x for (y,x) in sorted(zip(insitutimelist[stid],insitudatalist[stid]))]
			havedata = havedata + len(filterrawtimes[stid])
		except:
			filterrawtimes[stid] = []
			filterrawdata[stid] = []			
			
# if(havedata > 0):
datelocater = mpl.dates.AutoDateLocator()
dateaxisfmt = mpl.dates.DateFormatter('%m-%d %H:%M:%S')
mpl.rc('xtick',labelsize=8)
datepresfmt = mpl.ticker.ScalarFormatter(useOffset=False)
datepresfmt.set_scientific(False)
mpl.rc('ytick',labelsize=8)
color=iter(mpl.cm.jet(np.linspace(0,1,len(stidlist))))

fig = pyplot.figure(figsize=(10,5))
myp = fig.add_subplot(111)

if(mystat == '8hr'):
	pyplot.suptitle('8-hr Average Ozone Time Series from '+time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochstartstat))+' - '+time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochend)))
else:
	pyplot.suptitle('Ozone Time Series from '+time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochstart))+' - '+time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochend)))
	
lineset = []
for stid in sorted(stidlist):
	# try:
	nextcol=next(color)
	mpldates = mpl.dates.epoch2num(filterrawtimes[stid])	
	if(len(mpldates) > 0):
		curline = pyplot.plot(mpldates,filterrawdata[stid],color=nextcol,label=stid)
		lineset = lineset+curline
	# except:
		# skip = 1
myp.set_ylabel(varunits[leftvarchoice])
myp.set_xlabel('Time ('+tzout+')')
myp.xaxis.set_major_locator(datelocater)
myp.xaxis.set_major_formatter(dateaxisfmt)
myp.yaxis.set_major_formatter(datepresfmt)
if(mystat == '8hr'):
	myp.plot([mpl.dates.epoch2num(epochstartstat-utctzoff),mpl.dates.epoch2num(epochend-utctzoff)],[75,75],'0.5',ls='--')
	myp.plot([mpl.dates.epoch2num(epochstartstat-utctzoff),mpl.dates.epoch2num(epochend-utctzoff)],[65,65],'0.5',ls=':')
	myp.set_xlim(mpl.dates.epoch2num(epochstartstat-utctzoff),mpl.dates.epoch2num(epochend-utctzoff))
else:
	myp.set_xlim(mpl.dates.epoch2num(epochstart-utctzoff),mpl.dates.epoch2num(epochend-utctzoff))	
myp.set_ylim(bottom=0)
box = myp.get_position()
myp.set_position([box.x0, box.y0, box.width * 0.8, box.height])
myp.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':8})
fig.autofmt_xdate()
pyplot.savefig(sys.stdout, format='png')
# else:
	# fig = pyplot.figure(figsize=(10,0.5))
	# pyplot.suptitle('Observations from '+time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochstart))+' - '+time.strftime('%Y-%m-%d %H:%M '+tzout,time.localtime(epochend))+' could not be generated')
	# pyplot.savefig(sys.stdout, format='png')

sys.exit()
