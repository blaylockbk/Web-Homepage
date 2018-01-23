#!/uufs/chpc.utah.edu/sys/installdir/anaconda/4.2.0/bin/python

#if this doesn't work try /usr/local/bin/python

"""
Brian Blaylock
Decebmer 13, 2017

"""

import subprocess
import cgi, cgitb
cgitb.enable()

form = cgi.FieldStorage()


## Get Bucket name from the form, or set default
try:
    bucket = form['BUCKET'].value
except:
    # Demo, default bucket
    bucket = 'HRRR/oper/prs/20170101/'


## You must have a / at the end of the bucket name
if bucket[-1] != '/':
    bucket = bucket+'/'


## Pando URL
baseURL = 'https://pando-rgw01.chpc.utah.edu/'


## Begin the HTML document
print "Content-Type: text/html\n"

print'''<!DOCTYPE html>
<html>
<head>
<title>Horel Pando Allocation</title>
<script src="../js/site/siteopen.js"></script>
</head>

<body>
<div class='container'>
<h1>Horel Pando Allocation 
    <a class='btn btn-danger' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=HRRR">HRRR</a>
    <a class='btn btn-danger' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=GOES16">GOES16</a>
    <a class='btn btn-danger' href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=horel-archive">Horel Archive</a>
</h1>
<form>
<p style="font-size:20px"><b>Bucket URL: </b>%s<input type=text size=50 name=BUCKET value=%s>''' % (baseURL, bucket)

print '<hr>'


## === rclone directories =====================================================
## Create list of directories and files in the bucket with rclone
# 1) The location of the rclone command
#rclone = '/uufs/chpc.utah.edu/sys/installdir/rclone/1.29/bin/rclone'
rclone = '/uufs/chpc.utah.edu/common/home/horel-group/archive_s3/rclone-beta/rclone --config /uufs/chpc.utah.edu/common/home/u0553130/.rclone.conf'

# 2) The rclone comand to list files in this bucket
#    'horelS3' is the bucket named I configured rclone to access the Pando.
ls = ' ls --max-depth 1 horelS3:%s' % bucket
lsd = ' lsd horelS3:%s' % bucket

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
if len(dirs) > 2:
    back_bucket = '/'.join(bucket.split('/')[:-2])
    URL = 'http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=%s' % (back_bucket)
    print '''<a href="%s"><i class="fas fa-step-backward"></i> Back</a>''' % (URL)
    print "<br><br>"


## === Directory Buttons ======================================================
## Create button for each directory
print '''<h4><i class="fa fa-archive"></i> Directories</h4>'''
if len(dlist) > 0:
    print '''
    <div class="btn-group-vertical">
    '''
    for d in dlist:
        DIR = d.split(' ')[-1]
        URL = 'http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=%s' % (bucket+DIR)
        print '''<a class='btn btn-success' href="%s">%s</a>''' % (URL, DIR)
    print '''</div>'''
else:
    print "<p>None"

print "<hr>"
## === File download buttons ==================================================
# If we are in the deepest directory, then make download buttons for each file.
print '''<h4><i class="fa fa-file"></i> Files</h4>'''
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
    </form>
    '''
else:
    print "<p>None"

## === End of webpage =========================================================
print '''
<br>
<script src="./js/site/siteclose.js"></script>
</div>
</body>
</html>
'''