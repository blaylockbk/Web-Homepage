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

document.write('<script src="js/site/CurrentTemp.js"></script>')

if (window.location.href != 'http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/home.html') {
	document.write('<div class=""><img title="click me" id="title_pic" src="'+pics[idx]+'" onclick="change_title_pic();" width="100%"></div>');	
}


document.write('\
<nav class="navbar navbar-inverse" style="border-radius:0;margin:0;">\
        <div class="container-fluid">\
            <div class="navbar-header">\
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">\
        <span class="icon-bar"></span>\
        <span class="icon-bar"></span>\
        <span class="icon-bar"></span>\
      </button>\
\
                <!--KBKB Logo-->\
                <a href="./home.html">\
\
                    <img style="width:50px;height:50px;vertical-align:middle" src="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/images/WeatherBalloon.gif" align="left">\
\
                </a>\
\
            </div>\
            <div class="collapse navbar-collapse" id="myNavbar">\
                <ul class="nav navbar-nav">\
                    <li><a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/home.html">Home</a></li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Research <span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_ver.html ">HRRR Verification</a></li>\
                            <li><a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/MS.html ">MS</a></li>\
                            <li><a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/PhD.html ">PhD</a></li>\
                            <li><a href="http://meso2.chpc.utah.edu/gslso3s/ " target="research ">GSLSO3S 2015</a></li>\
                            <li><a href="http://esrl.noaa.gov/csd/projects/songnex/ " target="research ">SONGNEX 2015</a></li>\
                            <li><a href="http://www.inscc.utah.edu/~u0198116/uintahbasin.html " target="research ">UBOS 2013-15</a></li>\
                            <li><a href="http://www.nserc.und.edu/sarp/sarp-2009-2013/2013/sarp-2013-student-presentation-videos/la-air-quality-group/meteorological-influences-on-surface-ozone-in-the-los-angeles-basin " target="research ">SARP 2013</a></li>\
                            <li><a href="http://home.chpc.utah.edu/~hoch/MATERHORN_experiment.html " target="research ">MATERHORN 2013</a></li>\
                            <li><a href="http://mesowest.utah.edu/ " target="research ">MesoWest</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Web Tools <span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html "><i class="fa fa-info-circle fa-fw" aria-hidden="true"></i>  HRRR Archive</a></li>\
                            <li><a href="./cgi-bin/ts_multistations.cgi "><i class="fa fa-line-chart fa-fw" aria-hidden="true"></i> Multi-station Time Series</a></li>\
                            <li><a href="./cgi-bin/roses.cgi "><i class="fa fa-pie-chart fa-fw" aria-hidden="true"></i> Rose Plots</a></li>\
                            <li><a href="./satellite_image_viewer.php "><i class="fa fa-picture-o fa-fw" aria-hidden="true"></i>  Satellite Images</a></li>\
                            <li><a href="./hrrr_sounding_viewer.php "><i class="fa fa-line-chart fa-fw" aria-hidden="true"></i> HRRR Soundings</a></li>\
                            <li><a href="./ksl_ozone_viewer.php "><i class="fa fa-line-chart fa-fw" aria-hidden="true"></i> KSL Ozone Plots</a></li>\
                            <li><a href="../Camera_Display "><i class="fa fa-video-camera fa-fw" aria-hidden="true"></i>  Camera Display</a></li>\
                            <li><a href="http://meso1.chpc.utah.edu/NAA "><i class="fa fa-television fa-fw" aria-hidden="true"></i>  NAA School</a></li>\
                            <li><a href="./map.html "><i class="fa fa-map fa-fw" aria-hidden="true"></i>  Station Bing Map</a></li>\
                            <li><a href="./HRRR_Winds "><i class="fa fa-map-o fa-fw" aria-hidden="true"></i> HRRR Winds</a></li>\
                            <li><a href="./HRRR_Wake_Finder "><i class="fa fa-map-o fa-fw" aria-hidden="true"></i> Wake Finder</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">WRF<span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="./wrf.html ">WRF</a></li>\
                            <li><a href="./hrrr.html ">HRRR</a></li>\
                            <li><a href="./tracer.html ">Tracers</a></li>\
                            <li><a href="./lake_surgery.html ">Lake Surgery</a></li>\
                            <li><a href="./results.html ">Results</a></li>\
                            <li><a href="./wrf_post.html ">Post Processing</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Published<span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="./publications.html ">Publications</a></li>\
                            <li><a href="./presentations.html ">Presentations</a></li>\
                            <li><a href="./mapsonthehill.html ">Maps on the Hill</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Blogs<span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="http://kbkb-wx.blogspot.com "><i class="fa fa-sun-o fa-fw" aria-hidden="true"></i> KBKB WX</a></li>\
                            <li><a href="http://kbkb-wx-python.blogspot.com "><i class="fa fa-code fa-fw" aria-hidden="true"></i> KBKB Python</a></li>\
                            <li><a href="http://wasatchweatherweenies.blogspot.com "><i class="fa fa-snowflake-o fa-fw" aria-hidden="true"></i> Wasatch W. W.</a></li>\
                            <li><a href="http://cliffmass.blogspot.com "><i class="fa fa-tint fa-fw" aria-hidden="true"></i> Cliff Mass</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Education<span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="./wxMeritBadge.html ">WX Merit Badge</a></li>\
                            <li><a href="./schoovisits.html ">School Visits</a></li>\
                        </ul>\
                    </li>\
\
                    <!--\
        <li><a href="#">Page 2</a></li>\
        <li><a href="#">Page 3</a></li>\
        -->\
                </ul>\
\
            </div>\
        </div>\
    </nav>\
');
