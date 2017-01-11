#!/usr/bin/python

#if this doesn't work try /usr/local/bin/python

import sys
import cgi, cgitb
import time
import datetime
cgitb.enable()

form = cgi.FieldStorage()

current = datetime.datetime.now()
tendaysago = datetime.datetime.now()-datetime.timedelta(days=10)

try:
   id = form['id'].value
except:
   id = 'mtmet'

try:
   plot_max = form['plot_max'].value
except:
   plot_max = '25'

try:
   rose_type = form['rose_type'].value
except:
   rose_type = 'ozone'

try:
   threshold = form['threshold'].value
except:
   threshold = '00'
   
try:
   time_option = form['time_option'].value
except:
   time_option = 'local'
   
try:
   HI = form['HI'].value #hour interval
except:
   HI = 'All Day'  
  
try:
   eyr = form['eyr'].value
   emo = form['emo'].value
   edy = form['edy'].value
   ehr = form['ehr'].value

   syr = form['syr'].value
   smo = form['smo'].value
   sdy = form['sdy'].value
   shr = form['shr'].value

except:
   eyr = ("%04d" % current.year)
   emo = ("%02d" % current.month)
   edy = ("%02d" % current.day)
   ehr = ("%02d" % current.hour)

   syr = ("%04d" % tendaysago.year)
   smo = ("%02d" % tendaysago.month)
   sdy = ("%02d" % tendaysago.day)
   shr = ("%02d" % tendaysago.hour)
   
   #syr = ('2015')
   #smo = ('06')
   #sdy = ('01')
   #shr = ('00')

# Get epoch time stamps for plotting ceilometer data.

beg_date = datetime.datetime(int(syr),int(smo),int(sdy),int(shr),00,00)
end_date = datetime.datetime(int(eyr),int(emo),int(edy),int(ehr),00,00)
beg_epoch = time.mktime(beg_date.timetuple())
end_epoch = time.mktime(end_date.timetuple())

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>Ozone Rose</title>
</head>'''

print '''
<body link="#FFFFFF">

<script src="js/site/sitemenu.js"></script>
</div>'''

print''' 

<br>
<h1 align="center">Ozone and Wind Roses</h1>
<br>

<div style="background-color:#f5f5f5; width:85%; max-width:1000px; margin-left:auto; margin-right:auto;">	
	<div style="background-color:#d40000;">
		<br><p style="color:white;"> <font size="4"><b>Instructions:</b></font>
		  Choose a station, rose type, time zone, and hour interval.
		  Adjust the plot range to zoom in and out of the polar plot. Then Choose
		  the start and end time for the period you are interested. Clicking "Change Data Options"
		  will create your new plot. Hover mouse over blue text for additional 'tooltips'.
		  More info and examples <a style="color:white;" href="https://gslso3s.wordpress.com/2015/07/01/ozone-and-wind-roses/">here</a>.
		<br><br><p style="color:white;"> Note: Not all stations have ozone sensors and will not be able to create a plot. 
		Some station IDs you might like to try are 
		<a style="color:orange;" href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/ozone_rose.cgi?id=mtmet">mtmet</a> (University of Utah),
		<a style="color:orange;" href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/ozone_rose.cgi?id=naa">naa</a> (Neil Armstrong Academy West Valley), 
		<a style="color:orange;" href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/ozone_rose.cgi?id=qhw">qhw</a> (Hawthorne, Salt Lake City),
		<a style="color:orange;" href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/ozone_rose.cgi?id=qnp">qnp</a> (Provo Airport), 
		and <a style="color:orange;" href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/ozone_rose.cgi?id=qsf">qsf</a> (Spanish Fork). 
		For a complete list of ozone stations click <a style="color:lightblue;" href="http://meso2.chpc.utah.edu/gslso3s/cgi-bin/site_metadata.cgi">here</a>. Also, "Min Ozone" is only useful for the traditional ozone roses. 
		<br><br>  
	</div>			
	

       
<div class="contentBox">
<div class="innerBox">
   <br>
   <div class="contentText">
      <form method="GET" action="cgi-bin/ozone_rose.cgi">
	  
      <table class="center">
      
<!---STATION ----------------------->	  
	  <tr>
         <td><a title="Station ID used by mesowest.utah.edu">
		 Station ID: 
		 </a></td>
      <td>
	  <!-- USE IF YOU WANT TO SELECT SPECIFIC STATIONS
         <select name="id">'''

stn_ids = ['bgrut','fwp','gslm','lms','mtmet','naa','o3s01','o3s02','o3s03','o3s04','o3s05','o3s06','o3s07','o3s08','qbr','qbv','qed','qh3','qhv','qhw','qo2','qsa','qsy','snx']
stn_ids = ['bgrut','qbv','qbr','fwp','o3s08','gslm','qhv','qhw','qh3','lms','ql4','naa','qnp','qo2','qsa','qsf','mtmet']

for i in range(0,len(stn_ids)):
   if str(id) == str(stn_ids[i]):
      print'''<option selected="selected">'''+stn_ids[i]+'''</option>'''
   else:
      print'''<option>'''+stn_ids[i]+'''</option>'''
print''' </select>
	  -->
	  <!--OTHERWISE, USE A TEXT INPUT-->
	  '''
if id == 'mtmet':
	print '''<input type="text" name="id" value="mtmet">'''
else: 
	print '''<input type="text" name="id" value="'''+str(id)+'''">'''
print'''
      </td>
	  <td><a href="http://mesowest.utah.edu/" target="_blank">Find a Station ID</a>
	  </td>
	  </tr>
<!---(station) ----------------------->	  
	  
<!---ROSE TYPE ----------------------->	  
      <tr>
      <td><a title="'Ozone' plots ozone concentration frequency as a function of wind direction. 
	  'Wind Speed' plots wind speed frequency as a function of wind direction. 
	  'Ozone Clock' and 'Speed Clock' plots concentration or
	  speed as a function of hour of the day.">
	  Rose Type:</a>
	  </td>
      <td>
         <select name="rose_type">'''

disp_int = ['Ozone', 'Wind Speed', 'Ozone Clock', 'Speed Clock']
true_int = ['ozone','wspd', 'ozone_clock','spd_clock']

for i in range(0,len(true_int)):
   if str(rose_type) == str(true_int[i]):
      print'''<option selected="selected" value="'''+str(true_int[i])+'''">'''+disp_int[i]+'''</option>'''
   else:
      print'''<option value="'''+str(true_int[i])+'''">'''+disp_int[i]+'''</option>'''
print''' </select>
      </td>
	  </tr>
<!---(rose type) ----------------------->	  
	  
<!---TIME OPTION ----------------------->  
	  <tr>
      <td>Time Option:</td>
      <td>
         <select name="time_option">'''

disp_int = ['Local', 'UTC']
true_int = ['local','utc']

for i in range(0,len(true_int)):
   if str(time_option) == str(true_int[i]):
      print'''<option selected="selected" value="'''+str(true_int[i])+'''">'''+disp_int[i]+'''</option>'''
   else:
      print'''<option value="'''+str(true_int[i])+'''">'''+disp_int[i]+'''</option>'''
print''' </select>
      </td>
	  </tr>
<!---(time option) ----------------------->

	 
<!---HOUR INTERVAL ----------------------->		  
      <tr>
         <td>Hour Interval:</td>
      <td>
         <select name="HI">'''

intervals = ['All Day','00-03','03-06','06-09','09-12','12-15','15-18','18-21','21-24']

for i in range(0,len(intervals)):
   if str(HI) == str(intervals[i]):
      print'''<option selected="selected">'''+intervals[i]+'''</option>'''
   else:
      print'''<option>'''+intervals[i]+'''</option>'''
print''' </select>
      </td>
	  </tr>
	       
<!---(hour interval) ----------------------->

<!---THRESHOLD ----------------------->	  	  
	  <tr>
         <td>
		 <a title="The minimum ozone values to include in the plot.
		 This makes it possible to only look at the  most polluted days.">
		 Min Ozone:
		 </a>
		 </td>
		 
		 <td>
         <select name="threshold">'''
for i in (00, 50, 55, 60, 65, 70, 75, 80):
   if threshold == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>
      </td>
      </tr>
<!---(threshold) ----------------------->

<!---PLOT RANGE ----------------------->	  	  
	  <tr>
         <td>
		 <a title="Changes the value of the outermost circle. 
		 For 'clock' plots the default is automatically set to 4.4%
		 because the expected occurrence for each hour is 4.2%.">
		 Plot Range:
		 </a>
		 </td>
		 
		 <td>
         <select name="plot_max">'''
for i in range(5,50,5):
   if plot_max == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>
      </td>
      </tr>
<!---(plot range) ----------------------->	

	  </table>
   </div>

      <br>
      <table class="center">
      <tr>
         <td></td>
         <td>Month</td>
         <td>Day</td>
         <td>Year</td>
         <td>Hour</td>
      </tr>
	  

<!---BEGIN TIME ----------------------->	  
      <tr>
         <td>
         Begin Time:
         </td>

         <td>
         <select name="smo">'''
for i in range(1,13):
   if smo == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>

         <td>
         <select name="sdy">'''
for i in range(1,32):
   if sdy == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>

         <td>
         <select name ="syr">
            <option>2015</option>
         </select>
         </td>

         <td>
         <select name="shr">'''
for i in range(0,24):
   if shr == str("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>
      </tr>
<!---(begin time) ----------------------->	  
	  
<!---END TIME ----------------------->		  
      <tr>
         <td>
         End Time:
         </td>

         <td>
         <select name="emo">'''
for i in range(1,13):
   if emo == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>

         <td>
         <select name="edy">'''
for i in range(1,32):
   if edy == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>

         <td>
         <select name ="eyr">
            <option>2015</option>
         </select>
         </td>

         <td>
         <select name="ehr">'''
for i in range(0,24):
   if ehr == ("%02d" % i):
      print'''<option selected="selected">'''+"%02d" % i+'''</option>'''
   else:
      print'''<option>'''+"%02d" % i+'''</option>'''
print''' </select>
         </td>
		</tr>
    
<!---(end time) ----------------------->	


<!---SUBMIT BUTTON ----------------------->
  <tr>
   <td colspan=5 align="center">
      <input type="submit" value="Change Data Options" class="myButton">
	</td>
   </tr>
   </table>
   </form>
   </div>
<!---(submit button) ----------------------->   

<br>
<div class="imageText">
   <a href="cgi-bin/plot_ozone_rose.cgi?id='''+id+'''&time_option='''+time_option+'''&rose_type='''+str(rose_type)+'''&threshold='''+str(threshold)+'''&plot_max='''+str(plot_max)+'''&smo='''+str(smo)+'''&sdy='''+str(sdy)+'''&syr='''+str(syr)+'''
   &shr='''+str(shr)+'''&emo='''+str(emo)+'''&edy='''+str(edy)+'''&eyr='''+str(eyr)+'''&ehr='''+str(ehr)+'''&HI='''+str(HI)+'''">
      <img class="style1" width=500px src="cgi-bin/plot_ozone_rose.cgi?id='''+id+'''&time_option='''+time_option+'''&rose_type='''+str(rose_type)+'''&threshold='''+str(threshold)+'''&plot_max='''+str(plot_max)+'''&smo='''+str(smo)+'''&sdy='''+str(sdy)+'''&syr='''+str(syr)+'''
      &shr='''+str(shr)+'''&emo='''+str(emo)+'''&edy='''+str(edy)+'''&eyr='''+str(eyr)+'''&ehr='''+str(ehr)+'''&HI='''+str(HI)+'''" width="100%">
   </a>
   <br>
</div>


<!--Legends-->
<table class="center">
<tr>
	<td>Ozone Concentration (ppb)</td>
	<td>Wind Speed (m/s)</td>
</tr>
<tr>
<td><img class="style1" src="images/ozone_legend.jpg"></td>
<td><img class="style1" src="images/wspd_legend.jpg"></td>
</tr>
</table>


   <br>
   <br>
   
</div>
</div>
</div>

<script src="js/site/siteclose.js"></script>
</body>
</html>
'''