var coords = [];

function initMap() {
    var bounds  = new google.maps.LatLngBounds();
    var origin = coords[0];
    var destination = coords[1];
    var directionsRenderer = new google.maps.DirectionsRenderer;
    var directionsService = new google.maps.DirectionsService;
    var mapElement = document.getElementById('map');
    var map = new google.maps.Map(mapElement, {
      zoom: 12,
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
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
}