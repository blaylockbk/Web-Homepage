#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

"""
Brian Blaylock
December 14, 2017

GOES16 and NEXRAD File Explorer for AWS

Interactive web interface for viewing GOES-16 files available on the Amazon
noaa-goes16 public bucket. Click button to download files.

Details of GOES-16 data
http://www.goes-r.gov/products/images/productFileSize8ColorPng8-1600px.png

Updates/To Do:
    [X] Bootstrap style: Dec 13, 2017
    [X] Differentiate between directories and files for navigation Dec 13, 2017
    [X] Added a back button. Dec 13, 2017
"""

import subprocess
import cgi, cgitb
from collections import OrderedDict
cgitb.enable()

form = cgi.FieldStorage()


sets = OrderedDict()
sets['noaa-goes16'] = {'name': 'GOES-16 (East)',
                      'docs': 'https://registry.opendata.aws/noaa-goes/'}
sets['noaa-goes17'] = {'name': 'GOES-17 (West)',
                       'docs': 'https://registry.opendata.aws/noaa-goes/'}
sets['noaa-nexrad-level2'] = {'name': 'NEXRAD Level2',
                               'docs': 'https://registry.opendata.aws/noaa-nexrad/'}
sets['noaa-gfs-pds'] = {'name': 'Global Forecast System (GFS)',
                        'docs': 'https://registry.opendata.aws/noaa-gfs-pds/'}
sets['noaa-hrrr-bdp-pds'] = {'name': 'High-Resolution Rapid Refresh (HRRR)',
                         'docs': 'https://registry.opendata.aws/noaa-hrrr-bdp-pds/'}
sets['noaa-gefs-pds'] = {'name': 'Global Ensemble Forecast System',
                         'docs': 'https://registry.opendata.aws/noaa-gefs/'}                       
sets['noaa-nwm-pds']= {'name': 'National Water Model Short-Range Forecasts',
                       'docs': 'https://registry.opendata.aws/noaa-nwm-pds/'}
sets['nwm-archive'] = {'name': 'National Water Model Archive',
                       'docs': 'https://registry.opendata.aws/nwm-archive/'}
sets['era5-pds'] = {'name': 'ECMWF ERA5 Reanalysis',
                    'docs': 'https://registry.opendata.aws/exmwf-ara5/'}


HRRR_pando_btn = '<a class="btn btn-warning" href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrr_download.cgi">HRRR on Pando Archive</a>'
GOES_pando_btn = '<a class="btn btn-warning" href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_pando.cgi">GOES on Pando Archive</a>'
GOES_alt_btn = '<a class="btn btn-warning" href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi">Alternative GOES Download</a>'

## Get Bucket name from the form, or set default
try:
    dataset = cgi.escape(form['DATASET'].value)
except:
    # Demo, default bucket
    dataset = 'noaa-goes16'
try:
    bucket = cgi.escape(form['BUCKET'].value)
except:
    # Demo, default bucket
    bucket = ''


## You must have a / at the end of the bucket name
if len(bucket) > 1 and bucket[-1] != '/':
    bucket = bucket+'/'


## Pando URL
baseURL = 'https://%s.s3.amazonaws.com/' % (dataset)

## Begin the HTML document
print "Content-Type: text/html\n"

print'''<!DOCTYPE html>'''
print'''
<html>
<head>
'''
print '<title>Download %s from AWS</title>' % dataset
print '''
<script src="../js/site/siteopen.js"></script>
</head>

<body>
<script src="js/site/sitemenu.js"></script>
<div class='container'>
<h1 align=center><i class="fab fa-aws"></i> Download from Amazon</h1>
<h1 align=center>

</h1>
'''


print '''
<hr>
<form class="form-horizontal"  style='font-size:20px'>
  <div class="form-group">
    <label class="control-label col-sm-2" for="email">Dataset:</label>
    <div class="col-sm-4">
      <select class="form-control" id="DATASET" name="DATASET" style='display:inline;font-size:17px' onchange="this.form.submit()">'''
# display is the variable name as it will display on the webpage
# value is the value used
display = [sets[i]['name'] for i in sets.keys()]
value = sets.keys()

for i in range(0,len(value)):
   if dataset == value[i]:
      print'''<option selected="selected" value="'''+value[i]+'''">'''+display[i]+'''</option>'''
   else:
      print'''<option value="'''+value[i]+'''">'''+display[i]+'''</option>'''
print''' </select>
    </div>
  </div>

  <div class="form-group">
    <label class="control-label col-sm-2" for="pwd">URL:</label>
    <div class="col-sm-10"> 
      https://%s.s3.amazonaws.com/%s''' % (dataset, bucket)
print '''
    </div>
  </div>

  <div class="form-group">
    <label class="control-label col-sm-2" for="pwd">Resources:</label>
    <div class="col-sm-10"> 
      <a class='btn btn-default' href='%s' target=_blank>Documentation</a>''' % (sets[dataset]['docs'])
if dataset == 'noaa-hrrr-bdp-pds':
    print HRRR_pando_btn
if dataset in ['noaa-goes16', 'noaa-goes17']:
    print GOES_alt_btn
    print GOES_pando_btn
print '''
    </div>
  </div>
</form>
'''

print '<hr>'


## === rclone directories =====================================================
## Create list of directories and files in the bucket with rclone
# 1) The location of the rclone command
#rclone = '/uufs/chpc.utah.edu/sys/installdir/rclone/1.29/bin/rclone'
#rclone = '/uufs/chpc.utah.edu/common/home/horel-group/archive_s3/rclone-beta/rclone --config /uufs/chpc.utah.edu/common/home/u0553130/.rclone.conf'
rclone = '/uufs/chpc.utah.edu/common/home/horel-group7/Pando_Scripts/rclone-v1.39-linux-386/rclone --config /uufs/chpc.utah.edu/common/home/u0553130/.rclone.conf'

# 2) The rclone comand to list files in this bucket
#    'horelS3' is the bucket named I configured rclone to access the Pando.
ls = ' ls --max-depth 1 AWS:%s/%s' % (dataset, bucket)
lsd = ' lsd AWS:%s/%s' % (dataset, bucket)

# 3) Execute the rclone lsd command to list directories
## Check if there are directories in the requestd bucket
rclone_lsd = subprocess.check_output(rclone + lsd, shell=True)

# 4) Split the directory names to a list
dlist = rclone_lsd.split('\n')

# 5) Remove empty elements. There is always one at the end.
dlist.remove('')

# 6) Order the files
dlist.sort() 


## === Back Button ============================================================
dirs = bucket.split('/')
if len(dirs) > 1:
    back_bucket = '/'.join(bucket.split('/')[:-2])
    URL = 'https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_AWS_download.cgi?DATASET=%s&BUCKET=%s' % (dataset, back_bucket)
    print '''<a href="%s"><i class="fas fa-step-backward"></i> Back</a>''' % (URL)
    print "<br><br>"

## === Directory Buttons ======================================================
## Create button for each directory
print '''<h3><i class="fa fa-archive"></i> Directories</h3>'''
if len(dlist) > 0:
    print '''
    <div class="btn-group-vertical" style='margin-left:30px'>
    '''
    for d in dlist:
        DIR = d.split(' ')[-1]
        URL = 'https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_AWS_download.cgi?DATASET=%s&BUCKET=%s' % (dataset, bucket+DIR)
        print '''<a class='btn btn-success' href="%s">%s</a>''' % (URL, DIR)
    print '''</div>'''
else:
    print "<p>None"

print "<hr>"
## === File download buttons ==================================================
# If we are in the deepest directory, then make download buttons for each file.
print '''<h3><i class="fa fa-file"></i> Files</h3>'''
# 1) List files in the requested bucket
rclone_ls = subprocess.check_output(rclone + ls, shell=True)

# 2) Split the file names to a list
flist = rclone_ls.split('\n')

# 3) Remove empty elements. There is always one at the end.
flist.remove('')

# 4) Order the files
flist.sort() 

if len(flist) > 0:

    ## Create an HTML link for each file, put in a table with file size.
    print '''
    <table class='table table-striped table-hover sortable'>
        <tr>
            <th>File Object Name</th>
            <th>Size</th>
        </tr>
    '''
    for f in flist:
        # Build the URL for each file
        SIZE = float(f.split(' ')[-2])      # File Size is second to last item, in bytes
        FILE = f.split(' ')[-1]             # File Name is last item
        URL = baseURL + bucket + FILE       # Build download URL
        
        if SIZE > 1000000000:
            SIZE_UNITS = '%.1f GB' % (SIZE/10**9)
            print '''<tr>
                    <td><i class="fas fa-download"></i> <a href="%s">%s</a></td><td align="right" style="padding-left:30px"><b style="color:#2441ff;">%s</b></td>
                </tr>''' % (URL, FILE, SIZE_UNITS)
        elif SIZE > 1000000:
            SIZE_UNITS = '%.1f MB' % (SIZE/10**6)
            print '''<tr>
                    <td><i class="fas fa-download"></i> <a href="%s">%s</a></td><td align="right" style="padding-left:30px"><b style="color:#ff8119;">%s</b></td>
                </tr>''' % (URL, FILE, SIZE_UNITS)
        elif SIZE > 1000:
            SIZE_UNITS = '%.1f KB' % (SIZE/10**3)
            print '''<tr>
                    <td><i class="fas fa-download"></i> <a href="%s">%s</a></td><td align="right" style="padding-left:30px"><b style="color:#00ad1d;">%s</b></td>
                </tr>''' % (URL, FILE, SIZE_UNITS)
        else:
            SIZE_UNITS = '%.1f' % (SIZE)
            print '''<tr>
                    <td><i class="fas fa-download"></i> <a href="%s">%s</a></td><td align="right" style="padding-left:30px"><b style="color:grey;">%s</b></td>
                </tr>''' % (URL, FILE, SIZE_UNITS)

    print '''
    </table>
    '''
else:
    print "<p>None"

## === End of webpage =========================================================
print '''
<br>
<div align=right><a href="https://github.com/blaylockbk/Web-Homepage/blob/master/cgi-bin/generic_AWS_download.cgi"><i class="fab fa-github"></i> Page</a>
<script src="./js/site/siteclose.js"></script>
</div>
</body>
</html>
'''
