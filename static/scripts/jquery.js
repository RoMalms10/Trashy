(function() {
  $(document).ready(function() {
    $('.sidebar.big.icon').click(function() {
      $('.ui.inverted.secondary.pointing.menu').toggleClass('ui inverted vertical menu')
    });  
  });

  // Initialize and add the map
  var initMap = function initializeGoogleMap() {

    $.get("/api/bins", function(data) {

      var sf = {lat: 37.752, lng: -122.447};
      var map = new google.maps.Map(document.getElementById('map'), {zoom: 12, center: sf});

      if(data) {
        for(var i = 0 ; i <= data.length-1; i++) {
          var pin = new google.maps.Marker({position: new google.maps.LatLng(data[i].location.lat, data[i].location.lng), map: map, title: data[i].name });
          var infowindow = new google.maps.InfoWindow({
            content: "<div id=\"content\" style=\"color: black;\"><div id=\"bodyContent\">Location: "+ data[i].name+"</div></div>"
          });
//          pin.addListener('click', function() {
//            infowindow.open(map, pin);
          google.maps.event.addListener(pin, 'click', (function(pin, i) {
            return function() {
              infowindow.setContent(locations[i].lat);
              infowindow.open(map, pin);
            }
          })(pin, i));
        };
  //      map.setCenter(data[0].location)    
      };
    })
  }
  window.initMap = initMap;
})();

// iffe
