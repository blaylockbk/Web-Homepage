# Brian Blaylock
# August 14, 2017


import numpy as np

table = np.genfromtxt('https://api.mesowest.utah.edu/archive/HRRR/GRIB2Table_hrrr_2d.txt',
                      delimiter=',',
                      skip_header=4,
                      names=True,
                      dtype=None)

all_headers = table.dtype.names

table_headers = ['RecordNumber', 'WGrib2Name', 'FieldType', 'VerticalLevels', 'Units']

f = open('hrrr_sfc_table.html', 'w')
f.write('''
<html>
<head>
<script src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/js/site/siteopen.js"></script>
<title>HRRR Download Page</title>
</head>

<body>
<script src="js/site/sitemenu.js"></script>


<div class="container">
      <h1 align="center">HRRR Table: SFC</h1>
<br>
<table class='table table-hover sortable'>
<tr>''')
for header in table_headers:
      f.write('<th>'+header+'</th>')
f.write('''</tr>''')

f.write('''<tr>''')
      
for row in range(len(table[header])):
    f.write('<tr>')
    for header in table_headers:            
        f.write('''
<td>'''+str(table[header][row])+'''</td>
''')
    f.write('</tr>')

f.write('''
</table>

</div>

</body>
</html>
''')
f.close()