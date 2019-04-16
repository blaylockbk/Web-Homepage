## Brian Blaylock
## January 5, 2018                          Oh boy, do I need a nap right now.
## March 28, 2019                           Updated for Python 3 and GOES17.

"""
Get the current size of our Pando archive and store daily usage values for each
bucket in the `Pando_Space.csv` file.

Answers these thought provoking questions...
    How much space is there remaining on the S3 archive?
    How many days left until the S3 archive is filled?
    How much space did each file type take yesterday?
"""

import matplotlib as mpl
mpl.use('Agg') #required for the CRON job. Says, "Do not open plot in a window."
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import subprocess
from datetime import date, datetime, timedelta
import numpy as np
import matplotlib.font_manager as font_manager

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
mpl.rcParams['legend.loc'] = 'upper left'
mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['savefig.dpi'] = 100

##=============================================================================
# Allocation (in GB)
allocation = (60+70) * 1e3

# Today's Date
DATE = datetime.utcnow()
##=============================================================================

# Path to rclone software we use to check the size of the S3 buckets
rclone = '/uufs/chpc.utah.edu/common/home/horel-group7/Pando_Scripts/rclone-v1.39-linux-386/rclone'

## --- Get size of each bucket (in GB) ----------------------------------------
## ----------------------------------------------------------------------------
sizes = {}
buckets = ['GOES16', 'GOES17', 'hrrr', 'hrrrX', 'hrrrak']
for b in buckets:
    outSize = subprocess.check_output(rclone+' size horelS3:%s/' % b,
                                      shell=True, encoding='UTF-8')
    print('-------')
    print(b)
    print(outSize)
    sSIZE = outSize.index('(')+1
    eSIZE = outSize.index(' Bytes)')
    Bytes = outSize[sSIZE:eSIZE]
    GB = int(Bytes) * 1e-9
    print('%s: %s GB' % (b, GB))
    print('-------')
    sizes[b]=GB

## Create a new line for the Pando_Space.csv file
new_line = '%s,%.2f,%.2f,%.2f,%.2f\n' % (DATE.strftime('%m/%d/%Y'),
                                         sizes['GOES16']+sizes['GOES17'],
                                         sizes['hrrr'],
                                         sizes['hrrrX'],
                                         sizes['hrrrak'])

## Append line to file
with open("./Pando_Space.csv", "a") as myfile:
    myfile.write(new_line)


## --- Create a plot showing the usage of each data type over time ------------
## ----------------------------------------------------------------------------
data = np.genfromtxt('Pando_Space.csv',
                      delimiter=',',
                      skip_header=6,
                      names=True,
                      dtype=None,
                      encoding='UTF-8')

# Column headers (not DATE) that are used for plotting legend
names = data.dtype.names[1:]
labels = ['{:>6} {:>4.1f} TB'.format(n.upper(), data[n][-1]/1000) for n in names]

DATES = list(map(lambda x: datetime.strptime(x,'%m/%d/%Y'), data['DATE']))
y = np.row_stack([data['GOES'], data['hrrr'], data['hrrrX'], data['hrrrAK']])

plt.stackplot(DATES,y, labels=labels, colors=['#da4f4a', '#016ecd', '#5cb85c', '#faa632'],
              linewidths=0)
plt.ylim([0,allocation])
plt.xlim([DATES[0], DATES[-1]])

font = font_manager.FontProperties(family='monospace')
plt.legend(prop=font)
plt.ylabel('Size in GB')
plt.title('Pando Usage and Allocation', loc='left')
plt.title('Updated: %s' % datetime.utcnow().strftime('%d %b %Y %H:%M UTC'), loc='right', fontsize=10)
plt.grid()

formatter = DateFormatter('%b-%d\n%Y')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.savefig('remaining_space_plot.png')


## --- Yesterday's Usage Breakdown --------------------------------------------
## ----------------------------------------------------------------------------
day_sizes = {}
yesterday_str = (DATE-timedelta(days=1)).strftime('%Y%m%d')

buckets = ['hrrr', 'hrrrak', 'hrrrX', 'GOES16', 'GOES17']

for m in buckets:
    day_sizes[m] = {}
    #
    if m[:4] == 'GOES':
        fields = ['ABI-L2-MCMIPC', 'GLM-L2-LCFA']
    else:
        fields = ['sfc', 'prs', 'nat']
    #
    for f in fields:
        Bytes = 0
        GB = 0
        print('\n------')
        print(m, f)
        outSize = subprocess.check_output(rclone+' size horelS3:%s/%s/%s/' % (m, f, yesterday_str),
                                        shell=True, encoding='UTF-8')
        sSIZE = outSize.index(' (')+2
        eSIZE = outSize.index(' Bytes)')
        Bytes = outSize[sSIZE:eSIZE]
        GB = int(Bytes) * 1e-9
        day_sizes[m][f] = GB
        print(outSize)
        print('Bytes', Bytes)
        print('GB', GB)
        print('------')


## --- How much space was used yesterday? -------------------------------------
## ----------------------------------------------------------------------------
GOES16_total = day_sizes['GOES16']['ABI-L2-MCMIPC'] + day_sizes['GOES16']['GLM-L2-LCFA']
GOES17_total = day_sizes['GOES17']['ABI-L2-MCMIPC'] + day_sizes['GOES17']['GLM-L2-LCFA']
HRRR_total = day_sizes['hrrr']['sfc'] + day_sizes['hrrr']['prs'] + day_sizes['hrrr']['nat']
HRRRX_total = day_sizes['hrrrX']['sfc'] + day_sizes['hrrrX']['prs'] + day_sizes['hrrrX']['nat']
HRRRAK_total = day_sizes['hrrrak']['sfc'] + day_sizes['hrrrak']['prs'] + day_sizes['hrrrak']['nat']

yesterday_total = GOES16_total \
                + GOES17_total \
                + HRRR_total   \
                + HRRRX_total  \
                + HRRRAK_total \

# The total amount used so far...
total_used = data['GOES'][-1] + data['hrrr'][-1] + data['hrrrX'][-1] + data['hrrrAK'][-1]

# Estimate number of days until allocation will be filled based on yesterday's usage.
days_till_full = int((allocation-total_used)/yesterday_total)
date_full = DATE+timedelta(days=days_till_full)


## --- Create HTML Page -------------------------------------------------------
## ----------------------------------------------------------------------------
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

<br>
<div class="row" id="content">
    <div class="col-md-offset-3 col-md-3">
        <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html" class="btn btn-success btn-block">
        <i class="fa fa-info-circle"></i> HRRR Archive FAQ</a>
    </div>
    <div class=" col-md-3">
        <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/generic_pando_download.cgi?BUCKET=GOES16" class="btn btn-primary btn-block">
        <i class="fa fa-cloud-download-alt"></i> Pando Web Download</a>
    </div>
</div>

<h1 align="center"><i class="fa fa-database"></i> Horel Group Pando Allocation</h1>

<!--
<div class='container'>
<div class="row" id="content">
    <div class=" col-md-3">
    </div>
    <div class="col-md-3">
            
    </div>
    <div class="col-md-3">
            
    </div>
    <div class="col-md-3">
    </div>
</div>
-->

<br>
  <script src='./js/pando_status.js'></script>
    <center><font size=12> %.1f TB out of 130 TB</font>
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
    </table>''' % (total_used/1000,
                   data['GOES'][-1]/allocation*100,
                   data['hrrr'][-1]/allocation*100,
                   data['hrrrX'][-1]/allocation*100,
                   data['hrrrAK'][-1]/allocation*100,
                   yesterday_total,
                   days_till_full,
                   date_full.strftime('%d %B %Y'))

# HTML for GOES yesterday's usage table
html += '''
    <table class="table table-bordered" style='text-align:center;max-width:700px'>
      <tr>
        <th style='text-align:center'></th>
        <th style='text-align:center' class="danger">GOES-16 (East)</th>
        <th style='text-align:center' class="danger">GOES-17 (West)</th>
      </tr>
      <tr>
        <th style='text-align:right'>ABI-L2-MCMIPC</th>
        <td>%.2f</td>
        <td>%.2f</td>
      </tr>
      <tr>
        <th style='text-align:right'>GLM-L2-LCFA</th>
        <td>%.2f</td>
        <td>%.2f</td>
      </tr>
      <tr>
        <th style='text-align:right'>Total</th>
        <th style='text-align:center'>%.2f GB</th>
        <th style='text-align:center'>%.2f GB</th>
      </tr>
    </table>

''' % (day_sizes['GOES16']['ABI-L2-MCMIPC'], day_sizes['GOES17']['ABI-L2-MCMIPC'],
       day_sizes['GOES16']['GLM-L2-LCFA'], day_sizes['GOES17']['GLM-L2-LCFA'],
       GOES16_total, GOES17_total
       )

# HTML table for HRRR yesterday's usage
html += '''
    <table class="table table-bordered" style='text-align:center;max-width:700px'>
      <tr>
        <th style='text-align:center'></th>
        <th style='text-align:center' class="info">HRRR</th>
        <th style='text-align:center' class="success">HRRR-X</th>
        <th style='text-align:center' class="warning">HRRR-Alaska</th>
      </tr>
      <tr>
        <th style='text-align:right'>sfc</th>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
      </tr>
      <tr>
        <th style='text-align:right'>prs</th>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
      </tr>
      <tr>
        <th style='text-align:right'>nat</th>
        <td>%.2f</td>
        <td>%.2f</td>
        <td>%.2f</td>
      </tr>
      <tr>
        <th style='text-align:right'>Total</th>
        <th style='text-align:center'>%.2f GB</th>
        <th style='text-align:center'>%.2f GB</th>
        <th style='text-align:center'>%.2f GB</th>
      </tr>
    </table>

  </center>
  
  <hr>
  <div align=right class='container'>
    <a href="https://github.com/blaylockbk/Web-Homepage/blob/master/Pando_archive/index.html"><i class="fab fa-github"></i> Page</a>
    <a href="https://github.com/blaylockbk/Web-Homepage/blob/master/Pando_archive/daily_usage.py"><i class="fab fa-github"></i> Plot</a>
    <br>
    Last Updated: %s
  </div>

</div>
<script src="./js/site/siteclose.js"></script>
</body>
</html>''' % (day_sizes['hrrr']['sfc'], day_sizes['hrrrX']['sfc'], day_sizes['hrrrak']['sfc'],
              day_sizes['hrrr']['prs'], day_sizes['hrrrX']['prs'], day_sizes['hrrrak']['prs'],
              day_sizes['hrrr']['nat'], day_sizes['hrrrX']['nat'], day_sizes['hrrrak']['nat'],
              HRRR_total, HRRRX_total, HRRRAK_total,
              datetime.utcnow().strftime('%d %b %Y %H:%M UTC'))

with open('index.html', 'w') as f:
    f.write(html)
