// Grab current obs from MesoWest API (version 2)
// Brian Blaylock
// September 17, 2015

var r_time = 300000; // Refresh time 5 min
var api_token = '2562b729557f45f5958516081f06c9eb';
var stid = 'ukbkb,wbb,kcho,epmu1,klgu,kpvu,klax,kmwh,CMP21';
setTimeout(poll, 500); // every 2 seconds

function CtoF(tempC){
	
	tempF = Math.round(tempC*9/5 + 32)
	
	return tempF
	
}

function short_name(data,stnidx){
  // Gets the name of the station and creates a short name
        try{
        if (data.STATION[stnidx].NAME=='EPHRAIM'){        
            s = 'Ephraim'
        }
        else if (data.STATION[stnidx].NAME=='EW2355 Spanish Fork'){
            s = 'Spanish Fork' 
        }
        else if (data.STATION[stnidx].NAME=='Charlottesville-Albemarle Airport'){
            s = 'Charlottesville' 
        }
        else if (data.STATION[stnidx].NAME=='Grant County Airport'){
            s = 'Moses Lake' 
        }
        else if (data.STATION[stnidx].NAME=='U of U William Browning Building'){
            s = 'WBB' 
        }
        else if (data.STATION[stnidx].NAME=='Provo, Provo Municipal Airport'){
            s = 'Provo' 
        }
        else if (data.STATION[stnidx].NAME=='St. George'){
            s = 'St. George' 
        }
        else if (data.STATION[stnidx].NAME=='Los Angeles, Los Angeles International Airport'){
            s = 'LAX' 
        }
        else if (data.STATION[stnidx].NAME=='Logan-Cache Airport'){
            s = 'Logan' 
        }  
        else {
            s='error/unknown'}
            }
         catch(err){s='error/unknown'}
    return s
}

function poll(){
var api_path = 'http://api.mesowest.net/v2/stations/nearesttime?stid='+stid+'&within=30&vars=air_temp&obtimezone=local&token='+api_token;
//alert(api_path);
$.getJSON('http://api.mesowest.net/v2/stations/nearesttime?callback=?',
  {
  // specify the request parameters here
  stid:stid,
  within:120, //Grabs the latest obs in the last two hours. If there isn't one for a station then code breaks
  token:api_token,
  },
  function (data)
  {
            
	  //alert(Object.keys(data.STATION)); //Use this to view what options are available
	  //alert(data.STATION[0].NAME); //Used to find out which Station is in which index
	  
      try{	
       airTemp_0 = short_name(data,0)+": " +CtoF(data.STATION[0].OBSERVATIONS.air_temp_value_1.value);}
	   catch(err){
	   airTemp_0 =short_name(data,0)+': '+'-na-';}
	  
      try{
       airTemp_1    = short_name(data,1)+": " +CtoF(data.STATION[1].OBSERVATIONS.air_temp_value_1.value);}
	   catch(err){
		airTemp_1 = short_name(data,1)+": " +'-na-';}
	   
       try{
	    airTemp_2   = short_name(data,2)+": " +CtoF(data.STATION[2].OBSERVATIONS.air_temp_value_1.value);}
        catch(err){
		airTemp_2 = short_name(data,2)+": " +'-na-';}
	   
       try{
	    airTemp_3   = short_name(data,3)+": " +CtoF(data.STATION[3].OBSERVATIONS.air_temp_value_1.value);}
	    catch(err){
		airTemp_3 = short_name(data,3)+": "  +'-na-';}
	   
       try{
	    airTemp_4   = short_name(data,4)+": " +CtoF(data.STATION[4].OBSERVATIONS.air_temp_value_1.value);}
	    catch(err){
		airTemp_4 = short_name(data,4)+": "  +'-na-';}
	   
       try{
	    airTemp_5   = short_name(data,5)+": " +CtoF(data.STATION[5].OBSERVATIONS.air_temp_value_1.value);}
	    catch(err){
		airTemp_5 = short_name(data,5)+": "  +'-na-';}
	   
       try{
	    airTemp_6   = short_name(data,6)+": " +CtoF(data.STATION[6].OBSERVATIONS.air_temp_value_1.value);}
	    catch(err){
		airTemp_6 = short_name(data,6)+": "  +'-na-';}
	   
       try{
	    airTemp_7   =short_name(data,7)+": " +CtoF(data.STATION[7].OBSERVATIONS.air_temp_value_1.value);}
	    catch(err){
		airTemp_7 = short_name(data,7)+": "  +'-na-';}
       
       try{
	    airTemp_8   = short_name(data,8)+": " +CtoF(data.STATION[8].OBSERVATIONS.air_temp_value_1.value);}
	    catch(err){
		airTemp_8 = short_name(data,8)+": "  +'-na-';}
	
	
	  
//set up variable it will return to the HTML 
  
  $('#ret-tempSF').html("<a target='new' style='color:white;text-decoration:none;' href='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=ukbkb&unit=0&timetype=LOCAL'>"+airTemp_8 + "&deg</a>");
  $('#ret-tempWBB').html("<a target='new' style='color:white;text-decoration:none;' href='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=wbb&unit=0&timetype=LOCAL'>"+airTemp_0 + "&deg</a>");
  $('#ret-tempKCHO').html("<a target='new' style='color:white;text-decoration:none;' href='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=kpvu&unit=0&timetype=LOCAL'>"+airTemp_1 + "&deg</a>");
  $('#ret-tempEPMU1').html("<a target='new' style='color:white;text-decoration:none;' href='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=klgu&unit=0&timetype=LOCAL'>"+airTemp_7 + "&deg</a>");
  $('#ret-tempKLGU').html("<a target='new' style='color:white;text-decoration:none;' href='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=cmp21&unit=0&timetype=LOCAL'>"+airTemp_2 + "&deg</a>");
  $('#ret-tempKPVU').html("<a target='new' style='color:white;text-decoration:none;' href='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=epmu1&unit=0&timetype=LOCAL'>"+airTemp_5 + "&deg</a>");
  $('#ret-tempKLAX').html("<a target='new' style='color:white;text-decoration:none;' href='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=kmwh&unit=0&timetype=LOCAL'>"+airTemp_6 + "&deg</a>");  
  $('#ret-tempKMWH').html("<a target='new' style='color:white;text-decoration:none;' href='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=klax&unit=0&timetype=LOCAL'>"+airTemp_3 + "&deg</a>");
  $('#ret-tempSTG').html("<a target='new' style='color:white;text-decoration:none;' href='http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=kcho&unit=0&timetype=LOCAL'>"+airTemp_4 + "&deg</a>");
                                                                                                                                    
}); 
  setTimeout(poll, r_time); 

}  

// NOTHING FOLLOWS //