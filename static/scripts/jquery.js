// Initialize and add the map
function initMap() {
  // The location of San Francisco
  var sf = {lat: 37.752, lng: -122.447};
  // The map, centered at San Francisco
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 12, center: sf});
  // The marker, positioned at San Francisco
  var marker = new google.maps.Marker({position: sf, map: map});
}
