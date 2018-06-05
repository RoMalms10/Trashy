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
            alert("Something went wrong")
          }
        }
      })
    });
    function deleteMarker () {
      var tempMarker = this;
      var markerLoc = tempMarker.getLatLng();
      console.log("In function for delete");
      $.ajax({
        url: '/delete',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({'latitude': markerLoc.lat, 'longitude': markerLoc.lng}),
        success: function (data) {
          // Removes the marker from the map
          if (data) {
            mymap.removeLayer(tempMarker);
          } else {
            alert("Something went wrong")
          }
        }
      })
    }
    // $('#delete').click(function () {
      // var tempMarker = this;
      // var markerLoc = tempMarker.getLatLng();
      // console.log("In function for delete");
      // $.ajax({
      //   url: '/delete',
      //   type: 'POST',
      //   contentType: 'application/json',
      //   dataType: 'json',
      //   data: JSON.stringify({'latitude': markerLoc.lat, 'longitude': markerLoc.lng}),
      //   success: function (data) {
      //     // Removes the marker from the map
      //     if (data) {
      //       mymap.removeLayer(tempMarker);
      //     } else {
      //       alert("Something went wrong")
      //     }
      //   }
      // })
    // });
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
      var markerClusters = L.markerClusterGroup();
      for(var i = 0 ; i <= data.length-1; i++) {
        if (data[i].user_id) {
          var popupInfo = data[i].name + "<br/>";
          var marker = L.marker([data[i].latitude, data[i].longitude]);
          marker.setPopupContent(popupInfo);
          marker.bindPopup($('<div class="ui button" id="delete">Delete Trash Can</div>').click(deleteMarker));
          // var popupInfo = data[i].name + '<br/>' + '<div class="ui button" id="delete">Delete Trash Can</div>'
        } else {
          var popupInfo = data[i].name;
          var marker = L.marker([data[i].latitude, data[i].longitude]).bindPopup(popupInfo);
        }
        // var marker = L.marker([data[i].latitude, data[i].longitude]).setContent(popup).bindPopup($('#delete').click(delete));
        markerClusters.addLayer(marker);
      };
      mymap.addLayer(markerClusters); 
    }
  }
})();
