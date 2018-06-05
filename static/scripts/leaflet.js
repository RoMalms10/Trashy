(function() {
  // $(document).ready(function() {
    $('#submit').click(function() {
      center = mymap.getCenter();
      $.ajax({
        url: '/add',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({'latitude': center.lat, 'longitude': center.lng}),
        success: function (data) {
          // Adds the new marker to the map with the Delete button
          if (data) {
            var popup = data.name + '<br/>' + '<div class="ui button" id="delete">Delete Trash Can</div>';
            var marker = L.marker([data.latitude, data.longitude]).bindPopup(popup).addTo(mymap);
          } else {
            alert("Invalid Parameters")
          }
        }
      })
    });
  // });

  var mymap = L.map('mapid').setView([37.752, -122.447], 16);
  L.tileLayer('https://a.tile.openstreetmap.org/{z}/{x}/{y}.png', {
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
      // var markerClusters = L.markerClusterGroup();
      for(var i = 0 ; i <= data.length-1; i++) {
        if (data[i].user_id) {
          var popupInfo = data[i].name + '<br/>' + '<div class="ui button" id="delete">Delete Trash Can</div>';
        } else {
          var popupInfo = data[i].name;
        }
        var marker = L.marker([data[i].latitude, data[i].longitude]).bindPopup(popupInfo);
        // markerClusters.addLayer(marker);
        mymap.addLayer(marker);
      };
      // mymap.addLayer(markerClusters); 
    } else {
      alert("Invalid parameters!")
    }
  }

  mymap.on('popupopen', function (info) {
    $('#delete').click(function () {
      $.ajax({
        url: '/delete',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({'latitude': info.popup._source._latlng.lat, 'longitude': info.popup._source._latlng.lng}),
        success: function (data) {
          // Removes the marker from the map
          if (data.status === "ok") {
            mymap.removeLayer(info.popup._source);
          } else {
            alert("Unable to delete marker")
          }
        }
      })
    });
  })
})();
