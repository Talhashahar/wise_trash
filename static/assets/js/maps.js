function geticon(capacity){

    var full ={
        url: "http://localhost:5000/static/assets/img/full.png",
        scaledSize: new google.maps.Size(20, 27),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
    };
	var empty ={
        url: "http://localhost:5000/static/assets/img/empty.png",
        scaledSize: new google.maps.Size(20, 27),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
    };
	var middle ={
        url: "http://localhost:5000/static/assets/img/middle.png",
        scaledSize: new google.maps.Size(20, 27),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
    };
	var offline ={
        url: "http://localhost:5000/static/assets/img/offline.png",
        scaledSize: new google.maps.Size(20, 27),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
    };

    return capacity <= 50 ? empty : capacity <= 70 ? middle : full;
}

function initMap() {
var locations = window.locations;
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 17,
      center: new google.maps.LatLng(32.089206, 34.804282),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });


	//setMarkers(map)
    var infowindow = new google.maps.InfoWindow();

    var marker, i;

        for (i = 0; i < locations.length; i++) {
           var icon = geticon(locations[i][4]);
          marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i][1], locations[i][2]),
            map: map,
            icon: icon

          });

          google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                var info = 'ID: ' + locations[i][5] + '<br/> address: ' + locations[i][0] + '<br/> capacity: '+ locations[i][4] + '%';
              infowindow.setContent(info);
              infowindow.open(map, marker);
            }
          })(marker, i));
        }
}

