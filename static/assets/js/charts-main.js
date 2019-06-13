type = ['','info','success','warning','danger'];


charts = {
//    initPickColor: function(){
//        $('.pick-class-label').click(function(){
//            var new_class = $(this).attr('new-class');
//            var old_class = $('#display-buttons').attr('data-class');
//            var display_div = $('#display-buttons');
//            if(display_div.length) {
//            var display_buttons = display_div.find('.btn');
//            display_buttons.removeClass(old_class);
//            display_buttons.addClass(new_class);
//            display_div.attr('data-class', new_class);
//            }
//        });
//    },

//    checkScrollForTransparentNavbar: debounce(function() {
//            $navbar = $('.navbar[color-on-scroll]');
//            scroll_distance = $navbar.attr('color-on-scroll') || 500;
//
//            if($(document).scrollTop() > scroll_distance ) {
//                if(transparent) {
//                    transparent = false;
//                    $('.navbar[color-on-scroll]').removeClass('navbar-transparent');
//                    $('.navbar[color-on-scroll]').addClass('navbar-default');
//                }
//            } else {
//                if( !transparent ) {
//                    transparent = true;
//                    $('.navbar[color-on-scroll]').addClass('navbar-transparent');
//                    $('.navbar[color-on-scroll]').removeClass('navbar-default');
//                }
//            }
//    }, 0),


    //PARAMETERS FOR FIRST GRAPH AT STATISTICS PAGE:

    initChartist: function(){
        const Http = new XMLHttpRequest();
        console.log("inside http request");
        const url_charts='http://localhost:5000/get_avg_capacity_and_days';

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
                series: [[70,70,70,70,70], [], avg_values]
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

        Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);
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