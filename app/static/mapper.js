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

  map.data.setStyle(function(feature) {
    var color = "gray";
    var strokeWeight = 5;

    return ({
      strokeColor: color,
      strokeWeight: strokeWeight
    });
  });

  getLatLongs();
  colorizePaths();
  colorizeTable();

}

google.maps.event.addDomListener(window, 'load', initialize);


function getLatLongs() {
  if (GP.locations) {
    if (GP.locations.length === 1) {
      // TODO create a point feature
    } else {
      GP.packagePathCoordinates = [];

      for (var i=0; i < GP.locations.length; i++) {
        geocoder.geocode({ 'address': GP.locations[i] }, function(results, status) {
          if (status === google.maps.GeocoderStatus.OK) {
            var best_match = results[0].geometry.location;
            var latitude = best_match.lat();
            var longitude = best_match.lng();
            GP.packagePathCoordinates.push({'lat': latitude, 'lng': longitude});
            
            if (GP.locations.length === GP.packagePathCoordinates.length) {
              GP.packagePath = new google.maps.Polyline({
                path: GP.packagePathCoordinates,
                geodesic: true,
                strokeColor: "#FF6633",
                strokeWeight: 5
              });
              GP.packagePath.setMap(map);
            }
          }
        });
      }
    }
  } else {
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
}

function getLatLong(loc_id, location) {
  geocoder.geocode({ 'address': location }, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
    var result = results[0].geometry.location;
    var latitude = result.lat();
    var longitude = result.lng();
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
  map.data.addListener('mouseover', function(event) {
    //Highlight the corresponding table row
    var id = event.feature.getProperty('shipmentID');
    var row = $("tr#table_row_" + id);
    row.addClass("activeRow");
    //Highlight the package path
    map.data.revertStyle();
    map.data.overrideStyle(event.feature, {
        strokeColor: event.feature.getProperty('strokeColor'),
    });
  });
  map.data.addListener('mouseout', function(event) {
    // Un-highlight the corresponding table row
    var id = event.feature.getProperty('shipmentID');
    var row = $("tr#table_row_" + id);
    row.removeClass("activeRow");
    // Un-highlight the package path
    map.data.revertStyle();
  });
}

function colorizeTable() {
  $("tbody tr").mouseenter(function() {
    // Highlight the table row
    $(this).addClass("activeRow");
    // Highlight corresponding package path
    var table_row_id = $(this).attr('id');
    var id = table_row_id.substring(10);
    map.data.setStyle(function(feature) {
      if (feature.getProperty('shipmentID') == id) {
        map.data.revertStyle();
        map.data.overrideStyle(feature, {
          strokeColor: feature.getProperty('strokeColor'),
          strokeWeight: feature.getProperty('strokeWeight')
          });
        }
      // Otherwise, keep the other package path the same style
      else {
        return ({ strokeColor: "gray",
                  strokeWeight: 5 });
      }
    });
  }).mouseout(function() {
    // Un-highlight the table row
    $(this).removeClass("activeRow");
    // Un-highlight the corresponding package path
    map.data.revertStyle();
    map.data.setStyle(function(feature) {
      var color = "gray";
      var strokeWeight = 5;
      return ({ strokeColor: color,
               strokeWeight: strokeWeight
      });
    });
  });
}