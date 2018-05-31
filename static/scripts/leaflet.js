(function() {
  $(document).ready(function() {
    // Get the menu to show when it's small
    $('.sidebar.big.icon').click(function() {
      $('.ui.inverted.secondary.pointing.menu').toggleClass('ui inverted vertical menu')
    });  
  });

  var mymap = L.map('mapid').setView([37.752, -122.447], 16);
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(mymap);

  mymap.locate();

  mymap.on('locationfound', function (info) {
    var radius = info.accuracy / 7;
    mymap.setView([info.latitude, info.longitude], 16)
    L.circle(info.latlng, radius).addTo(mymap);
    $.ajax({
      url: '/api/bins/proximity',
      type: 'POST',
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify({'latitude': info.latitude, 'longitude': info.longitude}),
      success: putMarkers
    })
  });

  mymap.on('locationerror', function (info) {
    mymap.setView([37.752, -122.447], 16);
    let coords = mymap.getCenter()
    $.ajax({
      url: '/api/bins/proximity',
      type: 'POST',
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify({'latitude': coords.lat, 'longitude': coords.lng}),
      success: putMarkers
    })
  });

  function putMarkers (data) {
    if (data) {
      // Populates markers on map
      var markerClusters = L.markerClusterGroup();
      for(var i = 0 ; i <= data.length-1; i++) {
        var popup = data[i].name + '<br/>' + 'Confirm Button Here';
        var marker = L.marker([data[i].latitude, data[i].longitude]).bindPopup(popup);
        markerClusters.addLayer(marker);
      };
      mymap.addLayer(markerClusters); 
    }
  }

  // function allMarkers () {
  //   $.get("/api/bins", putMarkers {
  //   })
  // }

})();
