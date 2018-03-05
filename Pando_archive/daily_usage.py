# Brian Blaylock
# January 5, 2018                            Oh boy, do I need a nap right now.

"""
Get the current size of our Pando archive.

Answers these thought provoking questions...
How much space is there remaining on the S3 archive?
How many days left until the S3 archive is filled?
  Uses space used between yesterday and today as an estimate of daily usage

Daily usage for each bucket is stored in the Pando_Space.csv file
"""

import matplotlib as mpl
mpl.use('Agg') #required for the CRON job. Says "do not open plot in a window"??
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy
import subprocess
from datetime import date, datetime, timedelta
import numpy as np

import matplotlib as mpl
mpl.rcParams['figure.figsize'] = [8, 5]
mpl.rcParams['figure.titlesize'] = 15
mpl.rcParams['figure.titleweight'] = 'bold'
mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10
mpl.rcParams['axes.labelsize'] = 10
mpl.rcParams['axes.titlesize'] = 12
mpl.rcParams['lines.linewidth'] = 1.8
mpl.rcParams['grid.linewidth'] = .1
mpl.rcParams['figure.subplot.wspace'] = 0.05
mpl.rcParams['figure.subplot.hspace'] = 0.01
mpl.rcParams['legend.fontsize'] = 8
mpl.rcParams['legend.framealpha'] = .75
mpl.rcParams['legend.loc'] = 'best'
mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['savefig.dpi'] = 100

#------------------------------------------------------------------------------
# Allocation (in GB)
allocation = 60 * 1e3

# Today's Date
DATE = date.today()
#------------------------------------------------------------------------------

rclone = '/uufs/chpc.utah.edu/common/home/horel-group7/Pando_Scripts/rclone-v1.39-linux-386/rclone'

## --- Get size of each bucket (in GB) ----------------------------------------
sizes = {}
buckets = ['GOES16', 'hrrr', 'hrrrX', 'hrrrak']
names = ['GOES16', 'hrrr', 'hrrrX', 'hrrrAK']
for b in buckets:
    outSize = subprocess.check_output(rclone+' size horelS3:%s/' % b, shell=True)
    print outSize
    sSIZE = outSize.index('(')+1
    eSIZE = outSize.index(' Bytes)')
    Bytes = outSize[sSIZE:eSIZE]
    GB = int(Bytes) * 1e-9
    print b, GB
    sizes[b]=GB

# Create a new line for the Pando_Space.csv file
new_line = '%s,%.2f,%.2f,%.2f,%.2f\n' % (DATE.strftime('%Y-%m-%d'),
                                                   sizes['GOES16'],
                                                   sizes['hrrr'],
                                                   sizes['hrrrX'],
                                                   sizes['hrrrak'])

# Append to file
with open("Pando_Space.csv", "a") as myfile:
    myfile.write(new_line)


## --- Create a plot ---
data = np.genfromtxt('Pando_Space.csv',
                      delimiter=',',
                      skip_header=6,
                      names=True,
                      dtype=None)

DATES = map(lambda x: datetime.strptime(x,'%Y-%m-%d'), data['DATE'])
y = np.row_stack([data['GOES16'], data['hrrr'], data['hrrrX'], data['hrrrAK']])

plt.stackplot(DATES,y, labels=names, colors=['#da4f4a', '#016ecd', '#5cb85c', '#faa632'],
              linewidths=0)
plt.ylim([0,allocation])
plt.legend()
plt.ylabel('Size in GB')
plt.title('Pando Usage and Allocation', loc='left')
plt.title('Updated: %s' % datetime.now().strftime('%d %b %Y %H:%M'), loc='right')
plt.grid()

formatter = DateFormatter('%b-%d\n%Y')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.savefig('remaining_space_plot.png')

## --- How much space was used yesterday? -------------------------------------
total_today   = data['GOES16'][-1] + data['hrrr'][-1] + data['hrrrX'][-1] + data['hrrrAK'][-1]
total_yesterday = data['GOES16'][-2] + data['hrrr'][-2] + data['hrrrX'][-2] + data['hrrrAK'][-2]

one_day_usage = total_today-total_yesterday
days_till_full = int(allocation/one_day_usage)

date_full = DATE+timedelta(days=days_till_full)

## --- Yesterday's Breakdown --------------------------------------------------
models = ['hrrr', 'hrrrak', 'hrrrX']
fields = ['sfc', 'prs', 'nat']
day_sizes = {}
for m in models:
  day_sizes[m] = {}
  for f in fields:
      outSize = subprocess.check_output(rclone+' size horelS3:%s/%s/%s/' % (m, f, DATE.strftime('%Y%m%d')), shell=True)
      sSIZE = outSize.index('(')+1
      eSIZE = outSize.index(' Bytes)')
      size = outSize[sSIZE:eSIZE]
      day_sizes[m][f] = int(size) * 1e-9

## --- Create HTML Page -------------------------------------------------------
html = '''
<!DOCTYPE html>
<html>

<head>
<title>Pando Allocation</title>
<link rel="stylesheet" href="../css/brian_style.css" />
<script src="../js/site/siteopen.js"></script>
</head>


<body>

<a name="TOP"></a>
<script src="./js/site/sitemenu.js"></script>	

<h1 align="center"><i class="fa fa-database"></i> Horel Group Pando Allocation</h1>

<div class='container'>
<div class="row" id="content">
            <div class=" col-md-3">
                    <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_download_register.html" class="btn btn-danger btn-block">
                    <i class="fa fa-user-plus"></i> Have you Registered?</a>        
            </div>
            <div class="col-md-3">
                    <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_practices.html" class="btn btn-warning btn-block">
                    <i class="far fa-handshake"></i> Best Practices</a>
            </div>
            <div class="col-md-3">
                    <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html" class="btn btn-success btn-block">
                    <i class="fa fa-info-circle"></i> HRRR FAQ</a>
            </div>
            <div class="col-md-3">
                    <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/hrrr_download.cgi" class="btn btn-primary btn-block">
                    <i class="fa fa-cloud-download-alt"></i> Web Download Page</a>
            </div>
        </div>
  <br>
  <script src='./js/pando_status.js'></script>
    <center><font size=12> %.1f TB out of 60 TB</font>
    <div class="progress" style="max-width:700px;height:35px">
            <div class="progress-bar progress-bar-danger" role="progressbar" style="width:%.f%%">
              <font size=4></font>
            </div>
            <div class="progress-bar progress-bar-primary" role="progressbar" style="width:%.f%%">
              <font size=4></font>
            </div>
            <div class="progress-bar progress-bar-success" role="progressbar" style="width:%.f%%">
              <font size=4></font>
            </div>
            <div class="progress-bar progress-bar-warning" role="progressbar" style="width:%.f%%">
              <font size=4></font>
            </div>
          </div>
    
    <img style='width:100%%;max-width:750px'src="./Pando_archive/remaining_space_plot.png">
    <br>
    <hr>
    <h4>Yesterday's Breakdown</h4>
    <table class="table table-bordered" style='text-align:center;max-width:700px'>
      <tr>
        <th style='text-align:center'>Space Used Yesterday</th>
        <th style='text-align:center'>Estimated Days Until Full</th>
        <th style='text-align:center'>Estimated Full Date</th>
      </tr>
      <tr>
        <td>%.2f GB</td>
        <td>%s</td>
        <td>%s</td>
      </tr>
    </table>''' % (total_today/1000,
              data['GOES16'][-1]/allocation*100,
              data['hrrr'][-1]/allocation*100,
              data['hrrrX'][-1]/allocation*100,
              data['hrrrAK'][-1]/allocation*100,
              one_day_usage,
              days_till_full,
              date_full.strftime('%d %B %Y'))
html += '''
    <table class="table table-bordered" style='text-align:center;max-width:700px'>
      <tr>
        <th style='text-align:center'></th>
        <th style='text-align:center' class="danger">GOES16</th>
        <th style='text-align:center' class="info">HRRR</th>
        <th style='text-align:center' class="success">HRRR-X</th>
        <th style='text-align:center' class="warning">HRRR-Alaska</th>
      </tr>
      <tr>
        <th>sfc</th>
        <td>--</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
      </tr>
      <tr>
        <th>prs</th>
        <td>--</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
      </tr>
      <tr>
        <th>nat</th>
        <td>--</td>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
      </tr>
      <tr>
        <th>Total</th>
        <th>%.1f GB</th>
        <th>%.2f GB</th>
        <th>%.2f GB</th>
        <th>%.2f GB</th>
      </tr>
    </table>

  </center>
  <hr>
  <div align=right>
    <a href="https://github.com/blaylockbk/Web-Homepage/blob/master/Pando_archive/index.html"><i class="fab fa-github"></i> Page</a>
    <a href="https://github.com/blaylockbk/Web-Homepage/blob/master/Pando_archive/daily_usage.py"><i class="fab fa-github"></i> Plot</a>
  </div>
</div>
<script src="./js/site/siteclose.js"></script>
</body>
</html>''' % (day_sizes['hrrr']['sfc'], day_sizes['hrrrX']['sfc'], day_sizes['hrrrak']['sfc'],
              day_sizes['hrrr']['prs'], day_sizes['hrrrX']['prs'], day_sizes['hrrrak']['prs'],
              day_sizes['hrrr']['nat'], day_sizes['hrrrX']['nat'], day_sizes['hrrrak']['nat'],
              data['GOES16'][-1]-data['GOES16'][-2],
              day_sizes['hrrr']['sfc']+day_sizes['hrrr']['prs']+day_sizes['hrrr']['nat'],
              day_sizes['hrrrX']['sfc']+day_sizes['hrrrX']['prs']+day_sizes['hrrrX']['nat'],
              day_sizes['hrrrak']['sfc']+day_sizes['hrrrak']['prs']+day_sizes['hrrrak']['nat']
              )

with open('index.html', 'w') as f:
    f.write(html)
