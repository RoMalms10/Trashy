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

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (pos) {

      //Center map around geolocation
      var geo = [pos.coords.latitude, pos.coords.longitude];
      mymap = mymap.setView(geo, 16);

      // Add circle around person
      var circle = L.circle(geo, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.2,
        radius: 150
      }).addTo(mymap);
    })
  }
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
