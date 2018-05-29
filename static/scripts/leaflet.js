(function() {
  $(document).ready(function() {
    $('.sidebar.big.icon').click(function() {
      $('.ui.inverted.secondary.pointing.menu').toggleClass('ui inverted vertical menu')
    });  
  });

  var mymap = L.map('mapid').setView([37.752, -122.447], 12);
  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoicm9tYWxtczEwIiwiYSI6ImNqaHF6c2NvbTA3dmkzMHBwaWwzZmhibWIifQ.RpiKEopngPIF8x2SnDR5-g'
  }).addTo(mymap);

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (pos) {

      //Center map around geolocation
      var geo = [pos.coords.latitude, pos.coords.longitude];
      mymap = mymap.setView(geo, 17);

      // Add circle around person
      var circle = L.circle(geo, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.2,
        radius: 300
      }).addTo(mymap);
    })
  }
    $.get("/api/bins", function(data) {
      // Populates markers on map
      if(data) {
        for(var i = 0 ; i <= data.length-1; i++) {
          var marker = L.marker([data[i].location.lat, data[i].location.lng]).addTo(mymap);
        };   
      };
    })
})();
