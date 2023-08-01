(function ($, Drupal) {
  Drupal.behaviors.topTenHelper = {
    attach: function (context, settings) {
      //let PubSub = Drupal.behaviors.PubSub;
      //  let AirNowGov = Drupal.behaviors.AirNowGov;
      //let ReportingArea = AirNowGov.ReportingArea;

      $(document).ready(function() {
        handleAqiLegend();
        $(".po-aqi-scale").toggleClass("noData");

        function handleAqiLegend() {
          $('.po-aqi-scale-btn').click(function() {
            $(this).addClass('po-aqi-scale-btn-hidden');
            $('.po-aqi-scale-display').removeClass('po-aqi-scale-display-hidden');
          });
          $('.po-aqi-scale-display .fa-times').click(function() {
            $('.po-aqi-scale-display').addClass('po-aqi-scale-display-hidden');
            $('.po-aqi-scale-btn').removeClass('po-aqi-scale-btn-hidden');
          });
        }

        populateTopTen();
      });

        function populateTopTen() {
          //alert("populateTopTen starting");

          // Retrieve the Top Ten aqi cw 2020-07-30
          // resetting because it could be set from previous calls
          topTenData = {};
          // use ajax to get the data cw 2020-07-30
          //console.log(AirNowGov.API_URL);
          $.ajax({
            type: "GET",
            url: AirNowGov.API_URL + "reportingarea/get_top",
            context: this,
            success: function (response) {
              //console.log("Hit!");
              // output it
              for (let i = 0; i < response.length; i++) {
                //console.log(response[i]);
                //console.log(response[i].reportingArea);
                //console.log(response[i].stateCode);
                //console.log(response[i].aqi);
                console.log(response[i].reportingArea + " category is " + response[i].category);
                console.log("ActionDay is " + response[i].isActionDay);

                // data insertion
                eval('cityCell'+i).innerHTML = response[i].reportingArea + ", " + response[i].stateCode;
                eval('cityCell'+i).href = "/?city=" + response[i].reportingArea + "&state=" + response[i].stateCode + "&country=USA";

                eval('aqiCell'+i).innerHTML = response[i].aqi;
                eval('aqiCell'+i).classList.add(categoryStyle(response[i].category));
                }
            },
            error: function (response) {
              // TODO: Handle errors
              // console.error(response);
              topTenData = false;
              console.log("Top Ten AQI Locations data not found. This is an AirNow API error.");
              }
          });
        }
    }

  }
  // Convert category to color for use in CSS references cw 2020-07-30
  function categoryStyle(category){
    let style = "green"; // good
    if (category === "Moderate") {
        style = "moderate"; // moderate
    } else if (category === "Unhealthy for Sensitive Groups") {
        style = "unhealthy-sensitive"; // semi unhealthy
    } else if (category === "Unhealthy") {
        style = "unhealthy"; // unhealthy
    } else if (category === "Very Unhealthy") {
        style = "very-unhealthy"; // very unhealthy
    } else if (category === "Hazardous") {
        style = "hazardous"; // hazardous
    }
    return style;
  }



})(jQuery, Drupal);
