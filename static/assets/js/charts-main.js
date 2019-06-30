type = ['','info','success','warning','danger'];


charts = {

    //PARAMETERS FOR FIRST GRAPH AT STATISTICS PAGE:
    initChartist: function(){
        const Http = new XMLHttpRequest();
        console.log("inside http request");
        //const url_charts='http://localhost:5000/get_charts_data';
        const url_charts='http://34.253.231.214:5000/get_charts_data';

        Http.open("GET", url_charts);
        Http.send();

        Http.onreadystatechange = (e) => {
        let avg_dates = []
        let avg_values = []

        let sum_dates = []
        let sum_values = []
        if (Http.readyState == 4 && Http.status ==200)
        {
            let result = JSON.parse(Http.response)
            result['avg_array'].forEach(res =>{
                avg_dates.push(res['day']);
                avg_values.push(res['avg']);
            })
            result['sum_array'].forEach(res =>{
                sum_dates.push(res['day']);
                sum_values.push(res['sum']);
            })
            let dataSales = {
                labels: avg_dates,
                series: [avg_values, [], []]
            }

            let dataSales_months = {
                labels: ['06-2018','07-2018','08-2018','09-2018','10-2018','11-2018','12-2018','01-2019','02-2019','03-2019','04-2019','05-2019'],
                series: [[], ['50','56','51','44','78','45','37','26','44','48','49','50'], []]
            }

            let dataSales_years = {
                labels: ['2016','2017','2018','2019'],
                series: [[], [], ['50','56','51','44']]
            }

          console.log(sum_values);
          let data = {
            labels: sum_dates,
            series: [
              [sum_values[0], sum_values[1], sum_values[2], sum_values[3], sum_values[4]],
              []
            ]


        }
        var optionsSales = {
          lineSmooth: false,
          low: 0,
          high: 100,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: false,
          showPoint: false,
          plugins: [
              Chartist.plugins.ctThreshold({
                  threshold: result['threshold']
              })
          ]
        };

        var responsiveSales = [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        Chartist.Line('#chartDays', dataSales, optionsSales, responsiveSales);
        Chartist.Line('#chartMonths', dataSales_months, optionsSales, responsiveSales);
        Chartist.Line('#chartYears', dataSales_years, optionsSales, responsiveSales);
        Chartist.Pie('#chartPreferences_1', { labels: [],series: []});
        Chartist.Pie('#chartPreferences', { labels: [`${result['online']}%`,`${result['offline']}%`],series: [result['online'], result['offline']]});


        var options = {
            seriesBarDistance: 10,
            axisX: {
                showGrid: false
            },
            height: "245px"
        };

        var responsiveOptions = [
          ['screen and (max-width: 640px)', {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        Chartist.Bar('#chartActivity', data, options, responsiveOptions);

        }

        }



    },

    initGoogleMaps: function(){
        var myLatlng = new google.maps.LatLng(40.748817, -73.985428);
        var mapOptions = {
          zoom: 13,
          center: myLatlng,
          scrollwheel: false, //we disable de scroll over the map
          styles: [{"featureType":"water","stylers":[{"saturation":43},{"lightness":-11},{"hue":"#0088ff"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"hue":"#ff0000"},{"saturation":-100},{"lightness":99}]},{"featureType":"road","elementType":"geometry.stroke","stylers":[{"color":"#808080"},{"lightness":54}]},{"featureType":"landscape.man_made","elementType":"geometry.fill","stylers":[{"color":"#ece2d9"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#ccdca1"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#767676"}]},{"featureType":"road","elementType":"labels.text.stroke","stylers":[{"color":"#ffffff"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#b8cb93"}]},{"featureType":"poi.park","stylers":[{"visibility":"on"}]},{"featureType":"poi.sports_complex","stylers":[{"visibility":"on"}]},{"featureType":"poi.medical","stylers":[{"visibility":"on"}]},{"featureType":"poi.business","stylers":[{"visibility":"simplified"}]}]

        }
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);

        var marker = new google.maps.Marker({
            position: myLatlng,
            title:"Hello World!"
        });

        // To add the marker to the map, call setMap();
        marker.setMap(map);
    },

	showNotification: function(from, align){
    	color = Math.floor((Math.random() * 4) + 1);

    	$.notify({
        	icon: "pe-7s-gift",
        	message: "Welcome to <b>WiseTrash Dashboard</b> - a beautiful project for Shenkar."

        },{
            type: type[color],
            timer: 4000,
            placement: {
                from: from,
                align: align
            }
        });
	}


}
