#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
June 23, 2017
"""
import numpy as np
import cgi, cgitb

cgitb.enable()

form = cgi.FieldStorage()

try:
    fire = cgi.escape(form['fire'].value)
except:
    fire = 'BRIANHEAD'


alert_file = '/uufs/chpc.utah.edu/common/home/u0553130/oper/HRRR_fires/HRRR_fires_alerts.csv'

alerts = np.genfromtxt(alert_file, names=True, dtype=None, delimiter=',')
fires = np.unique(alerts['Fire'])

print "Content-Type: text/html\n"
print'''<!DOCTYPE html>
<html>
<head>
<title>HRRR Fire Wind Events</title>
<link rel="stylesheet" href="./css/brian_style.css" />
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
</head>
<!--This page is created dynamically in the scirpt /oper/HRRR_fires/HRRR_fires_alerts.py-->
<body>
<a name="TOP"></a>
<script src="./js/site/sitemenu.js"></script>	
<h1 align="center"><i class="fa fa-fire-extinguisher"></i> HRRR Fires Alert <i class="fas fa-exclamation-triangle"></i></h1>

<center>
    <div class="row" id="content">
        <div class=" col-md-1">
        </div>
        <div class=" col-md-2">
    <a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_golf.html" style="width:100%"> <i class="fa fa-map-marker-alt"></i> Point Forecast</a>      
        </div>
        <div class="col-md-2">
    <a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_fires.html" style="width:100%"><i class="fa fa-fire-extinguisher"></i> Fires Forecast</a>
        </div>
        <div class="col-md-2">
    <a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_custom.html" style="width:100%"> <i class="far fa-map"></i> Custom Maps</a>
        </div>
        <div class="col-md-2">
    <a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrrX-hrrr.cgi" style="width:100%"> <i class="fa fa-map"></i> Compare Maps</a>
        </div>
        <div class="col-md-2">
    <a class='btn btn-danger' role='button' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html" style="width:100%"> <i class="fa fa-database"></i> HRRR Archive</a>
        </div>
    </div>
</center>
    
<center>
    <div id="container" style="max-width:900px">
    <br>
    <div class="well well-sm">
    <p>Criteria: Maximum HRRR 10m wind for 90x90 km<sup>2</sup> box at fire initalization point is greater than 15 ms<sup>-1</sup>
    <p>The maximum wind gust for the same 90x90 km<sup>2</sup> box and the maximum composite reflectivity for a 150x150 km<sup>2</sup> box is also given.
    </div>
'''

print '''
<!---Fire Name -----------------------> 
    <div class="form-group">
      <label class="control-label col-md-2" for="model">Fire Name:</label>
      <div class="col-md-4">      
         <select class="form-control" id="fire" name="model" onchange="changeFire();">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = fires
value = fires

for i in range(0,len(value)):
   if fire == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>

      </div>
      
    </div>
<!---(Fire Name) ----------------------->
'''

print '''
    <table class="table sortable">
    <tr><th>Valid DateTime (UTC)</th> <th>Forecast Hour</th> <th>Fire</th> <th>State</th> <th>Size (acres)</th> <th>10m Wind (ms-1)</th> <th>Surface Gust (ms-1)</th> <th>Composite Reflectivity (dBZ)</th> <th>View Area Snapshot</th><th>Download Grib2 CONUS*</th></tr>
'''
line = ''
for a in alerts:
    if a[1] == fire:
        line += "<tr><td>%s</td>" % a[0]
        line += "<td>%s</td>" % a[7][25:28]
        line += "<td>%s</td>" % a[1]
        line += "<td>%s</td>" % a[2]
        line += "<td>%s</td>" % '{:,}'.format(a[3])
        line += "<td>%.1f</td>" % a[4]
        line += "<td>%.1f</td>" % a[5]
        line += "<td>%.1f</td>" % a[6]
        line += "<td><a class='btn btn-default' role='button' href='http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/plot_hrrr_custom.cgi?model=hrrr&valid=%s&fxx=%s&location=%s,%s&plotcode=10mWind_Barb,10mWind_Shade,dBZ_Contour&dsize=medium&background=arcgis' target='_blank'><i class='far fa-image' aria-hidden='true'></i> Sample</a></td>" % (a[0], a[7][26:28], a[8], a[9])
        line += "<td><a class='btn btn-default' role='button' href='https://pando-rgw01.chpc.utah.edu/HRRR/oper/sfc/%s' target='_blank'><i class='fa fa-download' aria-hidden='true'></i> GRIB2</a></td></tr>" % a[7]
print line
print '''
    </table>

    <p>*Note: Grib2 files are available for download on Pando archive one day after HRRR run time.
    <p>*Note: Map sample script can be found on <a href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/hrrr_sample_fire.cgi"><i class="fa fa-github"></i> GitHub</a>
    </div>
</center>

<script src="./js/site/siteclose.js"></script>
<script>
function changeFire() {
    var x = document.getElementById("fire").value;
    window.location.href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrr_fires_alert.cgi?fire="+x;
}
</script>
</body>
</html>
'''
