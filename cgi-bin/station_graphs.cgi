#!/usr/bin/python

#if this doesn't work try /usr/local/bin/python

import sys
import cgi, cgitb
import time
import datetime
cgitb.enable()

form = cgi.FieldStorage()

current = datetime.datetime.now()
onedayago = datetime.datetime.now()-datetime.timedelta(days=1)

try:
   id = form['id'].value
except:
   id = 'ukbkb'

try:
   plot_max = form['plot_max'].value
except:
   plot_max = '25'

try:
   rose_type = form['rose_type'].value
except:
   rose_type = 'wspd'
   
try:
   time_option = form['time_option'].value
except:
   time_option = 'local'
try:
   units = form['units'].value
except:
   units = 'english'
  
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

   syr = ("%04d" % onedayago.year)
   smo = ("%02d" % onedayago.month)
   sdy = ("%02d" % onedayago.day)
   shr = ("%02d" % onedayago.hour)
   
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
<title>Station Graphs</title>
</head>'''

print '''
<body link="#FFFFFF">

<script src="js/site/sitemenu.js"></script>
</div>'''

print''' 

<br>
<h1 align="center">Station WX Graphs</h1>
<br>

<div style="background-color:#f5f5f5; width:85%; max-width:1000px; margin-left:auto; margin-right:auto;">	
	<div style="background-color:#d40000;">
		<br><p style="color:white;"> <font size="4"><b>Instructions:</b></font>
		  Choose a station, time option, and rose type.
		  Then Choose the start and end time for the period you are interested. 
		  Clicking "Change Data Options"
		  will create your new plot. Hover mouse over blue text for additional 'tooltips'.
		<p style="color:white;"> Note: Requesting many days increases the time it takes to create the graphs.
		Please only make graphs for short time periods. Less than 15 days would be good :)
		<br><br>  
	</div>			
	

       
<div class="contentBox">
<div class="innerBox">
   <br>
   <div class="contentText">
      <form method="GET" action="cgi-bin/station_graphs.cgi">
	  
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

<!---ROSE TYPE ----------------------->	  
      <tr>
      <td><a title="'Wind Speed' plots wind speed frequency as a function of wind direction. 
	  'Speed Clock' plots concentration or speed as a function of hour of the day.">
	  Rose Type:</a>
	  </td>
      <td>
         <select name="rose_type">'''

disp_int = ['Wind Speed', 'Speed Clock']
true_int = ['wspd','spd_clock']

for i in range(0,len(true_int)):
   if str(rose_type) == str(true_int[i]):
      print'''<option selected="selected" value="'''+str(true_int[i])+'''">'''+disp_int[i]+'''</option>'''
   else:
      print'''<option value="'''+str(true_int[i])+'''">'''+disp_int[i]+'''</option>'''
print''' </select>
      </td>
	  </tr>
<!---(rose type) ----------------------->	 

<!---Units ----------------------------->	  
      <tr>
      <td>
	  Units: 
	  </td>
      <td>
         <select name="units">'''

disp_int = ['English', 'Metric']
true_int = ['english','metric']

for i in range(0,len(true_int)):
   if str(units) == str(true_int[i]):
      print'''<option selected="selected" value="'''+str(true_int[i])+'''">'''+disp_int[i]+'''</option>'''
   else:
      print'''<option value="'''+str(true_int[i])+'''">'''+disp_int[i]+'''</option>'''
print''' </select>
      </td>
	  </tr>
<!---(units) ---------------------------->

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
         <select name="syr">'''
for i in range(2015,current.year+1):
   if syr == ("%04d" % i):
      print'''<option selected="selected">'''+"%04d" % i+'''</option>'''
   else:
      print'''<option>'''+"%04d" % i+'''</option>'''
print''' </select>
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
         <select name="eyr">'''
for i in range(2015,current.year+1):
   if eyr == ("%04d" % i):
      print'''<option selected="selected">'''+"%04d" % i+'''</option>'''
   else:
      print'''<option>'''+"%04d" % i+'''</option>'''
print''' </select>
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
<!--Temperature/Humidity Graph-->
<div class="imageText">
   <a href="cgi-bin/plot_station_graph.cgi?id='''+id+\
   '''&plot_type=temp_RH'''+\
   '''&time_option='''+time_option+\
   '''&rose_type='''+str(rose_type)+\
   '''&plot_max='''+str(plot_max)+\
   '''&smo='''+str(smo)+\
   '''&sdy='''+str(sdy)+\
   '''&syr='''+str(syr)+\
   '''&shr='''+str(shr)+\
   '''&emo='''+str(emo)+\
   '''&edy='''+str(edy)+\
   '''&eyr='''+str(eyr)+\
   '''&ehr='''+str(ehr)+\
   '''">
      <img alt="Error: Temp/RH graph not available for some reason" class="style1" width=85% 
	  src="cgi-bin/plot_station_graph.cgi?id='''+id+\
	  '''&plot_type=temp_RH'''+\
	  '''&time_option='''+time_option+\
	  '''&rose_type='''+str(rose_type)+\
	  '''&plot_max='''+str(plot_max)+\
	  '''&units='''+str(units)+\
	  '''&smo='''+str(smo)+\
	  '''&sdy='''+str(sdy)+\
	  '''&syr='''+str(syr)+\
	  '''&shr='''+str(shr)+\
	  '''&emo='''+str(emo)+\
	  '''&edy='''+str(edy)+\
	  '''&eyr='''+str(eyr)+\
	  '''&ehr='''+str(ehr)+\
	  '''" width="100%">
   </a>
   <br>
</div>

<!--Wind Speed/Direction Graph-->
<br>
<div class="imageText">
   <a href="cgi-bin/plot_station_graph.cgi?id='''+id+\
   '''&plot_type=wind'''+\
   '''&time_option='''+time_option+\
   '''&rose_type='''+str(rose_type)+\
   '''&plot_max='''+str(plot_max)+\
   '''&smo='''+str(smo)+\
   '''&sdy='''+str(sdy)+\
   '''&syr='''+str(syr)+\
   '''&shr='''+str(shr)+\
   '''&emo='''+str(emo)+\
   '''&edy='''+str(edy)+\
   '''&eyr='''+str(eyr)+\
   '''&ehr='''+str(ehr)+\
   '''">
      <img alt="Error: Wind graph not available for some reason" class="style1" width=85% 
	  src="cgi-bin/plot_station_graph.cgi?id='''+id+\
	  '''&plot_type=wind'''+\
	  '''&time_option='''+time_option+\
	  '''&rose_type='''+str(rose_type)+\
	  '''&plot_max='''+str(plot_max)+\
	  '''&units='''+str(units)+\
	  '''&smo='''+str(smo)+\
	  '''&sdy='''+str(sdy)+\
	  '''&syr='''+str(syr)+\
	  '''&shr='''+str(shr)+\
	  '''&emo='''+str(emo)+\
	  '''&edy='''+str(edy)+\
	  '''&eyr='''+str(eyr)+\
	  '''&ehr='''+str(ehr)+\
	  '''" width="100%">
   </a>
   <br>
</div>

<!--Wind Rose-->
<br>
<div class="imageText">
   <a href="cgi-bin/plot_wind_rose.cgi?id='''+id+'''&time_option='''+time_option+'''&rose_type=wspd&plot_max='''+str(plot_max)+'''&smo='''+str(smo)+'''&sdy='''+str(sdy)+'''&syr='''+str(syr)+'''
   &shr='''+str(shr)+'''&emo='''+str(emo)+'''&edy='''+str(edy)+'''&eyr='''+str(eyr)+'''&ehr='''+str(ehr)+'''">
      <img alt="Error: Wind Rose not available for some reason" class="style1" width=500px src="cgi-bin/plot_ozone_rose.cgi?id='''+id+'''&time_option='''+time_option+'''&rose_type='''+str(rose_type)+'''&plot_max='''+str(plot_max)+'''&smo='''+str(smo)+'''&sdy='''+str(sdy)+'''&syr='''+str(syr)+'''
      &shr='''+str(shr)+'''&emo='''+str(emo)+'''&edy='''+str(edy)+'''&eyr='''+str(eyr)+'''&ehr='''+str(ehr)+'''" width="100%">
   </a>
   <br>
</div>


<br<br><p align=center>Powered By:<br>
<a href="http://mesowest.utah.edu/"><img class="style1" src="https://pbs.twimg.com/profile_images/938726763/mesowest_logo_red_square_bigger.png"></a>
   <br>
   <br>
   
</div>
</div>
</div>

<script src="js/site/siteclose.js"></script>
</body>
</html>
'''

