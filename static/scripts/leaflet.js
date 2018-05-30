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
  });

  mymap.on('locationerror', function (info) {
    mymap.setView([37.752, -122.447], 16);
  });

  $.get("/api/bins", function(data) {
    // Populates markers on map
    if(data) {
      var markerClusters = L.markerClusterGroup();
      for(var i = 0 ; i <= data.length-1; i++) {
        var popup = data[i].name + '<br/>' + 'Confirm Button Here';
        var marker = L.marker([data[i].latitude, data[i].longitude]).bindPopup(popup);
        markerClusters.addLayer(marker);
      };
      mymap.addLayer(markerClusters);  
    };
  })
})();
