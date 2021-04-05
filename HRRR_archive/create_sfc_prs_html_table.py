# Brian Blaylock
# 14 March 2018                                                          Pi Day

"""
Create HTML Table of HRRR sfc and prs files

The input file was created using: `wgrib2 filename.grib2 -v`
"""

# Read in the file
with open('prsf00.txt', 'r') as f:
    lines = f.readlines()

# For each line, split it and store data of interest in lists
msg = []
shortName = []
fullName = []
units = []
level = []
fxxPeriod = []

for l in lines:
    a = l.split(':')
    msg.append(a[0])
    var_name_units = a[3].split(' ')
    shortName.append(var_name_units[0])
    fullName.append(' '.join(var_name_units[1:-1]))
    units.append(var_name_units[-1][1:-1])
    level.append(a[4])
    if a[-2]=='':
        fxxPeriod.append('(none)')        
    elif a[-2][0].isdigit() and int(a[-2][0]) > 0 and 'max' in a[-2]:
        fxxPeriod.append('Previous Hour Max')
    elif a[-2][0].isdigit() and int(a[-2][0]) == 0 and 'max' in a[-2]:
        fxxPeriod.append('Previous Hour Max')
    elif a[-2][0].isdigit() and int(a[-2][0]) > 0 and 'ave' in a[-2]:
        fxxPeriod.append('Previous Hour Average')
    elif a[-2][0].isdigit() and int(a[-2][0]) == 0 and 'ave' in a[-2]:
        fxxPeriod.append('Previous Hour Average')
    elif a[-2][0].isdigit() and int(a[-2][0]) > 0 and 'acc' in a[-2]:
        fxxPeriod.append('Previous Hour Accumulated')
    elif a[-2][0].isdigit() and int(a[-2][0]) == 0:
        fxxPeriod.append('Accumulated since f00')
    elif a[-2][0].isdigit() and int(a[-2][0]) == 0:
        fxxPeriod.append('Accumulated since f00')
    else:
        fxxPeriod.append('File fxx')


table_headers = ['Record Number', 'Short Name', 'Full Name', 'Level', 'Forecast Period', 'Units']

f = open('/uufs/chpc.utah.edu/common/home/u0553130/public_html/Brian_Blaylock/HRRR_archive/hrrr_prs_table_f00-f01.html', 'w')
f.write('''
<html>
<head>
<script src="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>HRRR GRIB2 Tables</title>
</head>

<body>
<script src="js/site/sitemenu.js"></script>


<div class="container">
      <h1 align="center">HRRR Grib2 Tables</h1>
<br>
<center>
<a class="btn btn-primary" href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/HRRR_archive/hrrr_sfc_table_f00-f01.html">sfc f00-f01</a>
<a class="btn btn-primary" href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/HRRR_archive/hrrr_sfc_table_f02-f18.html">sfc f02-f18</a>
<a class="btn btn-primary active" href="https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/HRRR_archive/hrrr_prs_table_f00-f01.html">prs f00-f01</a>
</center>
<br>
<table class='table table-hover sortable'>
<tr>''')
for header in table_headers:
      f.write('<th>'+header+'</th>')
f.write('''</tr>''')


f.write('''<tr>''')
      
for i in range(len(msg)):
    f.write('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' \
    % (msg[i], shortName[i], fullName[i], level[i], fxxPeriod[i], units[i]))

f.write('''
</table>

</div>
<script src="./js/site/siteclose.js"></script>
</body>
</html>
''')
f.close()
