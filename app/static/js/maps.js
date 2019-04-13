var directionsRenderer;
var directionsService;
var coords = [];
var mapElement;
var map;
var origin;
var destination;

function initMap() {
    var bounds  = new google.maps.LatLngBounds();
    directionsRenderer = new google.maps.DirectionsRenderer;
    directionsService = new google.maps.DirectionsService;
    mapElement = document.getElementById('map');
    origin = coords[0];
    destination = coords[1];

    map = new google.maps.Map(mapElement, {
      zoom: 7,
      center: origin
    });
    directionsRenderer.setMap(map);
    directionsService.route({
      origin: origin,
      destination: destination,
      travelMode: "DRIVING"
    }, function(response, status) { 
      if (status == 'OK') {
        directionsRenderer.setDirections(response);
        var tt = 0;
        var td = 0;
        response["routes"][0]["legs"].forEach(function(leg, i) {
          tt += leg["duration"]["value"];
          td += leg["distance"]["value"];
        })
        document.getElementById("time").innerHTML = "Total time : " + (tt / 3600).toFixed(2) + " hours"
        document.getElementById("distance").innerHTML = "Total distance : " + (td / 1609.34).toFixed(1) + " miles"

      } else if (status == 'ZERO_RESULTS'){ 
        // catch error
        console.log("There are no results for this route.")
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
}

function updateMap(lat=null, long=null) {
  if (lat == null && long == null) {
    // Reset button clicked
    wypts = []
  } else {
    wypts = [{
      location : {
        lat : lat,
        lng : long
      }, 
      stopover : true
    }]
  }
  var mapElement = document.getElementById('map');
  directionsService.route({
    origin: origin,
    destination: destination,
    waypoints: wypts,
    travelMode: "DRIVING"
  }, function(response, status) {
    if (status == 'OK') {
      var tt = 0;
        var td = 0;
        response["routes"][0]["legs"].forEach(function(leg, i) {
          tt += leg["duration"]["value"];
          td += leg["distance"]["value"];
        })
        document.getElementById("time").innerHTML = "Total time : " + (tt / 3600).toFixed(2) + " hours"
        document.getElementById("distance").innerHTML = "Total distance : " + (td / 1609.34).toFixed(1) + " miles"
      directionsRenderer.setDirections(response);
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  });
}