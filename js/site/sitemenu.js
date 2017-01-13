/* Array of image URLs to randomly set as the page top photo*/
var pics = [
"./images/Panorama/fremont_pan.png",
"./images/Panorama/utahcounty_pan.png",
"./images/Panorama/utahcounty2_pan.png",
"./images/Panorama/sundance_pan.png",
"./images/Panorama/snowcanyon_pan.png",
/*"./images/Panorama/copter_pan.png",*/
/*"./images/Panorama/spring_pan.png",*/
"./images/Panorama/lights_pan.png",
"./images/Panorama/maple_pan.png",
"./images/Panorama/payette_pan.png",
"./images/Panorama/timp_pan.png",
"./images/Panorama/cu_pan.png",
"./images/Panorama/granite_pan.png",
"./images/Panorama/badger_pan.png",
"./images/Panorama/library_pan.png",
"./images/Panorama/buffalo_pan.png",
"./images/Panorama/gsl_pan.png",
"./images/Panorama/moab_pan.png",
"./images/Panorama/uofu_snow_pan.png",
"./images/Panorama/hobble_pan.png",
"./images/Panorama/cross_pan.png",
"./images/Panorama/soldier_pan.png",
"./images/Panorama/riverbottoms_pan.png",
/*"./images/Panorama/lmr_pan.png",*/
"./images/Panorama/slc_pan.png",
"./images/Panorama/bflat_pan.png",
"./images/Panorama/utahlake_pan.png",
];


function getRandomInt (min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

var idx =  getRandomInt(0,pics.length-1)

function change_title_pic(){
    var idx =  getRandomInt(0,pics.length-1)
    document.getElementById("title_pic").src=pics[idx];
}



document.write('\
<script src="js/site/CurrentTemp.js"></script>\
<div class="">\
	<img title="click me" id="title_pic" src="'+pics[idx]+'" onclick="change_title_pic();" width="100%">\
</div>\
<div id="page">\
		<a href="http://kbkb-wx.blogspot.com/" target="_blank">\
		<img style="width:50px;height:50px;vertical-align:middle" src="images/WeatherBalloon.gif" align="left">\
		</a>\
	<ul class="HeadMenu">\
		<li><a href="home.html" class="dropdown">Home</a></li>\
	</ul>\
	<ul class="HeadMenu">\
		<li><a href="home.html" class="dropdown">Research</a></li>\
		<li class="sublinks">\
            <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_ver.html">HRRR Verification</a>\
            <a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/MS.html">MS</a>\
			<a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/PhD.html">PhD</a>\
            <a href="http://meso2.chpc.utah.edu/gslso3s/" target="_blank">GSLSOS 2015</a>\
			<a href="http://esrl.noaa.gov/csd/projects/songnex/" target="_blank">SONGNEX 2015</a>\
            <a href="http://www.inscc.utah.edu/~u0198116/uintahbasin.html" target="_blank">UBOS 2013-15</a>\
            <a href="http://www.nserc.und.edu/sarp/sarp-2009-2013/2013/sarp-2013-student-presentation-videos/la-air-quality-group/meteorological-influences-on-surface-ozone-in-the-los-angeles-basin" target="_blank">SARP 2013</a>\
			<a href="http://home.chpc.utah.edu/~hoch/MATERHORN_experiment.html" target="_blank">MATERHORN 2013</a>\
            <a href="http://mesowest.utah.edu/" target="_blank">MesoWest</a>\
		</li>\
	</ul>\
	<ul class="HeadMenu">\
		<li><a href="home.html" class="dropdown">Web Tools</a></li>\
		<li class="sublinks">\
			<a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html">HRRR Archive</a>\
            <a href="./cgi-bin/ts_multistations.cgi">Multi-Station Time Series</a>\
			<a href="./satellite_image_viewer.php">Satellite Images</a>\
			<a href="./hrrr_sounding_viewer.php">HRRR Soundings</a>\
            <a href="./ksl_ozone_viewer.php">KSL Ozone Plots</a>\
			<a href="../Camera_Display/">Camera Display</a>\
			<a href="http://meso1.chpc.utah.edu/NAA/">NAA School</a>\
			<a href="./cgi-bin/ozone_rose.cgi">Wind/Ozone Rose</a>\
			<a href="./map.html">Station Map</a>\
			<a href="./HRRR_Winds/">HRRR Winds</a>\
			<a href="./HRRR_Wake_Finder/">Wake Finder</a>\
		</li>\
	</ul>\
	<ul class="HeadMenu">\
		<li><a href="./wrf.html" class="dropdown">WRF</a></li>\
		<li class="sublinks">\
			<a href="./wrf.html">WRF</a>\
            <a href="./hrrr.html">HRRR</a>\
			<a href="./tracer.html">Tracers</a>\
			<a href="./lake_surgery.html">Lake Surgery</a>\
            <a href="./results.html">Results</a>\
			<a href="./wrf_post.html">Post Processing</a>\
		</li>\
	</ul>\
	<ul class="HeadMenu">\
		<li><a href="./presentations.html" class="dropdown">Presented/Published</a></li>\
        <li class="sublinks">\
			<a href="./presentations.html">Presentations</a>\
            <a href="./publications.html">Publications</a>\
            <a href="./mapsonthehill.html">Maps on the Hill</a>\
		</li>\
	</ul>\
	<ul class="HeadMenu">\
		<li><a href="home.html" class="dropdown">Blogs</a></li>\
		<li class="sublinks">\
			<a href="http://kbkb-wx.blogspot.com/" target="_blank">WX @ KBKB</a>\
			<a href="http://kbkb-wx-python.blogspot.com/" target="_blank">KBKB - Python</a>\
			<a href="http://wasatchweatherweenies.blogspot.com/" target="_blank">Wasatch W.W.</a>\
			<a href="http://cliffmass.blogspot.com/" target="_blank">Cliff Mass</a>\
		</li>\
	</ul>\
	<ul class="HeadMenu">\
		<li><a href="home.html" class="dropdown">Education</a></li>\
		<li class="sublinks">\
			<a href="./wxMeritBadge.html">Weather Merit Badge</a>\
			<a href="./schoolvisits.html">School Visits</a>\
            <a href="./wxstation.html">WX Station</a>\
		</li>\
	</ul>\
</div>\
\
\
<!-- message banner below -->\
\
<!--\
<div style="background-color:yellow"><p style="padding:5px" align=center><big>If you find this website useful, consider making a donation to my old elemenarty school:</big>\
<big>\<a href="https://www.donorschoose.org/project/believe-in-books/2183632/" target="_blank"><b> Books for Larsen 6th Graders</b></a></big>\
-->\
</div>\
');
