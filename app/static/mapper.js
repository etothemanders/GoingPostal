var geocoder;
var map;


function initialize() {
	geocoder = new google.maps.Geocoder();
  //TODO: Center on the browser's location
	var latlng = new google.maps.LatLng(36.3955, -97.8783);
  var mapOptions = {
    center: latlng,
    zoom: 5
  };
  map = new google.maps.Map(document.getElementById("map-canvas"),
      					  mapOptions);

  getLatLongs();
  colorizePaths();

}

google.maps.event.addDomListener(window, 'load', initialize);


function getLatLongs() {
  $.ajax({
    url: "/get_latlongs",
    type: "GET"
  }).fail(function(resp){
    console.log("getLatLongs failed.");
  }).done(function(resp){
  var rows = resp['resp'];
  // If there weren't any new locations to add, plot the paths
  if (rows.length === 0) {
    console.log("No rows in response.");
    map.data.loadGeoJson('/load_GeoJson');
  }
  // If there were new locations to geocode, geocode them
	for (var i = 0; i < rows.length; i++) {
    var loc_id = rows[i]['id'];
    var location = rows[i]['placename'];
    getLatLong(loc_id, location);
	  }
  });
}

function getLatLong(loc_id, location) {
  geocoder.geocode({ 'address': location }, function(results, status) {
  	if (status == google.maps.GeocoderStatus.OK) {
		var result = results[0].geometry.location;
    var latitude = result.k;
    var longitude = result.B;
    console.log("latitude is " + latitude + "longitude is " + longitude);
    console.log(typeof(latitude));
		makeSaveLocRequest(loc_id, latitude, longitude);
	} else {
		alert("Geocode was not successful for the following reason: " + status);
	}
});
}

function makeSaveLocRequest(loc_id, latitude, longitude) {
	$.ajax({
		url : "/save_location",
		type: "POST",
		data: {
			id: loc_id,
      latitude: latitude.toString(),
      longitude: longitude.toString()
		}
  // If the save request failed.
	}).fail(function(resp){
		console.log("makeSaveLocRequest failed.");
  // If the save request was successful.
	}).done(function(resp){
		console.log(" makeSaveLocRequest succeeded.");
  //After the save location route, always do this
  }).always(function(resp) {
      console.log('hello');
      map.data.loadGeoJson('/load_GeoJson');
  });
}

function colorizePaths() {
  map.data.setStyle(function(feature) {
    var color = "gray";

    return ({
      strokeColor: color,
    });
  });

  map.data.addListener('mouseover', function(event) {
    console.log("You moused over something.");
    map.data.revertStyle();
    map.data.overrideStyle(event.feature, {
        strokeColor: event.feature.getProperty('strokeColor')
    });
  });

  map.data.addListener('mouseout', function(event) {
    console.log("You moused out.");
    map.data.revertStyle();
  });
}