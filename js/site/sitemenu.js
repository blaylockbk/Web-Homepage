/* Array of image URLs to randomly set as the page top photo*/
var pics = [
    "./images/Panorama/fremont_pan.png",
    "./images/Panorama/utahcounty_pan.png",
    "./images/Panorama/utahcounty2_pan.png",
    "./images/Panorama/sundance_pan.png",
    "./images/Panorama/sundance2_pan.png",
    "./images/Panorama/snowcanyon_pan.png",
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
    "./images/Panorama/slc_pan.png",
    "./images/Panorama/bflat_pan.png",
    "./images/Panorama/utahlake_pan.png",
    "./images/Panorama/goes16_pan.png",
    "./images/Panorama/SF_pan.png",
    "./images/Panorama/brianhead_pan.png",
    "./images/Panorama/eclipse_pan.png",
];


function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

var idx = getRandomInt(0, pics.length - 1)

function change_title_pic() {
    var idx = getRandomInt(0, pics.length - 1)
    document.getElementById("title_pic").src = pics[idx];
}

document.write('<script src="js/site/CurrentTemp.js"></script>')

/*Get the URL. We don't want to display the top picture on image viewers*/
var url = window.location.pathname;
var filename = url.substring(url.lastIndexOf('/')+1);

if (window.location.href != 'http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/home.html' && filename != 'photo_viewer_v3.php' && filename != 'photo_viewer_v2.php' && filename != 'photo_viewer_v1.php' && filename != 'photo_viewer.php' && filename != 'photo_viewer2.php' && filename != 'photo_viewer_fire.php') {
    document.write('<div class=""><img title="click me" id="title_pic" src="' + pics[idx] + '" onclick="change_title_pic();" width="100%"></div>');
}


/* Someday, use the bootstrap mega-menus if that makes more sense to use*/

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
                            <li><a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/hrrr_FAQ.html "><i class="fa fa-info-circle fa-fw" aria-hidden="true"></i>  HRRR Archive</a></li>\
                            <li><a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/PhD.html "><i class="fa fa-graduation-cap fa-fw" aria-hidden="true"></i> PhD</a></li>\
                            <li><a href="http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/MS.html "><i class="fa fa-graduation-cap fa-fw" aria-hidden="true"></i> MS</a></li>\
                            <li class="dropdown-header">External Links</li>\
                            <li><a href="http://www.firescience.gov/" target="research "><i class="fa fa-free-code-camp fa-fw" aria-hidden="true"></i> JFSP</a></li>\
                            <li><a href="http://meso2.chpc.utah.edu/aq/ " target="research "><i class="fa fa-cloud fa-fw" aria-hidden="true"></i> Air Quality</a></li>\
                            <li><a href="http://meso2.chpc.utah.edu/aq/cgi-bin/gslso3s_home.cgi" target="research "><i class="fa fa-cloud fa-fw" aria-hidden="true"></i> GSLSO<sub>3</sub>S</a></li>\
                            <li><a href="http://esrl.noaa.gov/csd/projects/songnex/ " target="research "><i class="fa fa-cloud fa-fw" aria-hidden="true"></i> SONGNEX</a></li>\
                            <li><a href="http://www.inscc.utah.edu/~u0198116/uintahbasin.html " target="research "><i class="fa fa-cloud fa-fw" aria-hidden="true"></i> UBOS</a></li>\
                            <li><a href="http://www.nserc.und.edu/sarp/sarp-2009-2013/2013/sarp-2013-student-presentation-videos/la-air-quality-group/meteorological-influences-on-surface-ozone-in-the-los-angeles-basin " target="research "><i class="fa fa-plane fa-fw" aria-hidden="true"></i> SARP </a></li>\
                            <li><a href="http://home.chpc.utah.edu/~hoch/MATERHORN_experiment.html " target="research "><i class="fa fa-cloud fa-fw" aria-hidden="true"></i> MATERHORN</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Web Tools <span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="./cgi-bin/hrrr_download.cgi"><i class="fa fa-database fa-fw" aria-hidden="true"></i>  HRRR Archive Download</a></li>\
                            <li><a href="./cgi-bin/goes16_download.cgi"><i class="fa fa-database fa-fw" aria-hidden="true"></i>  GOES-16 on Amazon</a></li>\
                            <li><a href="./cgi-bin/goes16_pando.cgi"><i class="fa fa-database fa-fw" aria-hidden="true"></i>  GOES-16 on Pando</a></li>\
                            <li><a href="../Camera_Display "><i class="fa fa-video-camera fa-fw" aria-hidden="true"></i>  Camera Display</a></li>\
                            <li><a href="./cgi-bin/ts_multistations.cgi "><i class="fa fa-line-chart fa-fw" aria-hidden="true"></i> Multi-station Time Series</a></li>\
                            <li><a href="./cgi-bin/roses.cgi "><i class="fa fa-pie-chart fa-fw" aria-hidden="true"></i> Rose Plots</a></li>\
                            <li><a href="./cgi-bin/stn_climo.cgi "><i class="fa fa-sun-o fa-fw" aria-hidden="true"></i> Station Climatology</a></li>\
                            <li><a href="./hrrr_custom.html "><i class="fa fa-map-o fa-fw" aria-hidden="true"></i> HRRR Custom Maps</a></li>\
                            <li><a href="./cgi-bin/hrrrX-hrrr.cgi "><i class="fa fa-map fa-fw" aria-hidden="true"></i> HRRR Compare Maps</a></li>\
                            <li><a href="./hrrr_golf.html "><i class="fa fa-map-marker fa-fw" aria-hidden="true"></i> HRRR Point Forecast</a></li>\
                            <li><a href="./hrrr_fires.html "><i class="fa fa-free-code-camp fa-fw" aria-hidden="true"></i> HRRR Fires Forecast</a></li>\
                            <li><a href="./hrrr_sounding_viewer.php "><i class="fa fa-line-chart fa-fw" aria-hidden="true"></i> HRRR Soundings</a></li>\
                                                        <li><a href="./ksl_ozone_viewer.php "><i class="fa fa-cloud fa-fw" aria-hidden="true"></i> KSL Flights</a></li>\
                            <li><a href="./map.html "><i class="fa fa-map fa-fw" aria-hidden="true"></i>  Station Bing Map</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">WRF<span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="./wrf.html ">WRF Resources</a></li>\
                            <li><a href="./hrrr.html ">Initalize with HRRR</a></li>\
                            <li><a href="./tracer.html ">Tracer Plumes</a></li>\
                            <li><a href="./lake_surgery.html ">Lake Surgery</a></li>\
                            <li><a href="./wrf_post.html ">Data Post Processing</a></li>\
                            <li><a href="http://home.chpc.utah.edu/~u0553130/Ute_WRF/"><i class="fa fa-users fa-fw" aria-hidden="true"></i> Utah WRF Users Group</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Code<span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li class="dropdown-header"><i class="fa fa-github fa-fw" aria-hidden="true"></i> PyBKB_v2</li>\
                            <li><a href="https://github.com/blaylockbk/pyBKB_v2/tree/master/BB_MesoWest">BB_MesoWest</a></li>\
                            <li><a href="https://github.com/blaylockbk/pyBKB_v2/tree/master/BB_WRF">BB_WRF</a></li>\
                            <li><a href="https://github.com/blaylockbk/pyBKB_v2">all others</a></li>\
                            <li class="dropdown-header"><i class="fa fa-code fa-fw" aria-hidden="true"></i> Other</li>\
                            <li><a href="https://github.com/blaylockbk/CHPC-Settings">CHPC Settings</a></li>\
                            <li><a href="https://github.com/blaylockbk/Web-Homepage/tree/master/image_viewers">Image Viewer</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Published<span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="./publications.html "><i class="fa fa-file-text fa-fw" aria-hidden="true"></i> Publications</a></li>\
                            <li><a href="./presentations.html "><i class="fa fa-slideshare fa-fw" aria-hidden="true"></i> Presentations</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Blogs<span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="http://kbkb-wx.blogspot.com "><i class="fa fa-sun-o fa-fw" aria-hidden="true"></i> KBKB WX</a></li>\
                            <li><a href="http://kbkb-wx-python.blogspot.com "><i class="fa fa-code fa-fw" aria-hidden="true"></i> KBKB Python</a></li>\
                            <li><a href="http://wasatchweatherweenies.blogspot.com "><i class="fa fa-snowflake-o fa-fw" aria-hidden="true"></i> Wasatch W. W.</a></li>\
                            <li><a href="http://cliffmass.blogspot.com"><i class="fa fa-tint fa-fw" aria-hidden="true"></i> Cliff Mass</a></li>\
                            <li class="dropdown-header">Podcasts</li>\
                            <li><a href="https://talkpython.fm"><i class="fa fa-microphone fa-fw" aria-hidden="true"></i> Talk Python to Me</a></li>\
                            <li><a href="http://www.stuffyoushouldknow.com"><i class="fa fa-microphone fa-fw" aria-hidden="true"></i> Stuff You Should Know</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">Outreach<span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="./wxMeritBadge.html ">WX Merit Badge</a></li>\
                            <li><a href="./schoolvisits.html ">School Visits</a></li>\
                            <li><a href="http://wrnscoutevent.wixsite.com/wrnscoutevent">WRN Scout Event</a></li>\
                            <li><a href="http://science.utah.edu/events/science-day.php ">UofU Science Day</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                        <a class="dropdown-toggle" data-toggle="dropdown" href="#">UUNET<span class="caret"></span></a>\
                        <ul class="dropdown-menu">\
                            <li><a href="https://home.chpc.utah.edu/~u0790486/wxinfo/cgi-bin/wxmap.cgi?net=153">Current Map</a></li>\
                            <li><a href="https://home.chpc.utah.edu/~u0790486/wxinfo/cgi-bin/wxmap_24h_precip_api.cgi?net=153">24hr Precip Map</a></li>\
                            <li><a href="http://home.chpc.utah.edu/~u0790486/wxinfo/cgi-bin/uunet_charts.cgi">Battery Voltage</a></li>\
                            <li><a href="http://home.chpc.utah.edu/~u0790486/wxinfo/cgi-bin/current_home.cgi">Nearby Weather</a></li>\
                            <li><a href="https://home.chpc.utah.edu/~u0790486/wxinfo/uusodar2_time_series.html">Sodar Viewer</a></li>\
                            <li><a href="http://mesowest.utah.edu/cgi-bin/droman/uunet_stn_monitor.cgi">UUNET Quick Look Table</a></li>\
                            <li><a href="http://meso2.chpc.utah.edu/aq/">TRAX/KSL/Mobile Air Quality</a></li>\
                            <li><a href="https://asn.synopticdata.com/">Above Surface Network</a></li>\
                            <li><a href="http://meso1.chpc.utah.edu/mesowest_overview/#">MesoWest Group Overview</a></li>\
                        </ul>\
                    </li>\
\
                    <li class="dropdown">\
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#">External Links<span class="caret"></span></a>\
                    <ul class="dropdown-menu">\
                        <li><a href="http://mesowest.utah.edu/ " target="tools"><img src="./images/mesowest_icon.svg" height="14px"> MesoWest</a></li>\
                        <li><a href="http://weather.utah.edu/ " target="tools"><i class="fa fa-globe fa-fw" aria-hidden="true"></i> weather.utah.edu</a></li>\
                        <li><a href="http://rammb-slider.cira.colostate.edu/ " target="tools"><i class="fa fa-globe fa-fw" aria-hidden="true"></i> GOES-16 Viewer</a></li>\
                        <li><a href="https://worldview.earthdata.nasa.gov/ " target="tools" ><i class="fa fa-globe fa-fw" aria-hidden="true"></i> NASA World View</a></li>\
                        <li><a href="https://www.xcskies.com/map " target="tools" ><img src="./images/hawk.png" height="14px"> XC Skies Forecasts</a></li>\
                        <li><a href="http://cocorahs.org/ " target="tools"><i class="fa fa-tint fa-fw" aria-hidden="true"></i>  CoCoRaHS</a></li>\
                        <li><a href="https://www.meted.ucar.edu/ " target="tools"><i class="fa fa-superpowers fa-fw" aria-hidden="true"></i>  Comet MetEd</a></li>\
                        <li><a href="http://meso1.chpc.utah.edu/NAA " target="tools"><i class="fa fa-television fa-fw" aria-hidden="true"></i>  NAA School</a></li>\
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