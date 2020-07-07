      // Display current date
    var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    var date = new Date();
    document.querySelector("#dateTime").innerHTML = date.toLocaleDateString("en-US", options);
  
    // Display weather details in .weather-details DOM 
    var city = document.querySelector(".weather-city");
    var temp = document.querySelector(".weather-temp");
    var description = document.querySelector(".weather-description");
    var icon = document.querySelector(".icon");
    var maxMinTemp = document.querySelector(".max-min-temp");
    var humidity = document.querySelector(".humidity");
    $.getJSON('https://geolocation-db.com/json/')
            .done (function(location) {
                var lat = (location.latitude);
                var lon = (location.longitude);         
                var tempCity = (location.city);
                $.ajax({
                  url: 'https://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lon+'&units=metric&'+
                        
                        // Place your API key
                        'appid=apikey',

                  dataType: "jsonp",
                  success: function (data) {
                    city.innerHTML = data.name + ', ' + data.sys.country;
                    temp.innerHTML = Math.round(data.main.temp) +'&deg;';
                    description.innerHTML = data.weather[0].description + ',';
                    icon.src = "static/weather-icons/"+data.weather[0].icon+"@2x.png";
                    humidity.innerHTML = data.main.humidity+'% Humidity';
                    maxMinTemp.innerHTML = Math.round(data.main.temp_max) + '&deg;' + '/' + Math.round(data.main.temp_min) + '&deg;';
                  }
                });
            });

            
    // Show hide description input field       
    $(document).ready(function() {
        $("#task-form").click(function() { 
                $('#story').show('slow');
        //return false;
        });
  
        $(document).mouseup(function(e){
        var container = $("#task-form");
  
        // If the target of the click isn't the container
        if(!container.is(e.target) && container.has(e.target).length === 0){
        $('#story').hide('slow');
      }
    });
  });//end