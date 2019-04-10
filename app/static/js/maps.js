
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
    directionsRenderer.setOptions({ preserveViewport : false });
    directionsService.route({
      origin: origin,
      destination: destination,
      travelMode: "DRIVING"
    }, function(response, status) {
      if (status == 'OK') {
        directionsRenderer.setDirections(response);
      } else if (status == 'ZERO_RESULTS'){ 
        // catch error
        console.log("There are no results for this route.")
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
}

function updateMap(lat, long) {
  console.log(lat + " " + long);
  var mapElement = document.getElementById('map');
  directionsService.route({
    origin: origin,
    destination: destination,
    waypoints: [{
      location : {
        lat : lat,
        lng : long
      }, 
      stopover : true
    }],
    travelMode: "DRIVING"
  }, function(response, status) {
    if (status == 'OK') {
      directionsRenderer.setDirections(response);
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  });
}