(function ($, Drupal) {
  Drupal.behaviors.statePageHelper = {
    attach: function (context, settings) {

      let PubSub = Drupal.behaviors.PubSub;
      let AirNowGov = Drupal.behaviors.AirNowGov;
      let ReportingArea = AirNowGov.ReportingArea;
      let GeoLocation = AirNowGov.GeoLocation;

      $(document).ready(function() {
        // Check for Language Code in URL; Using ISO 639-1 codes; Default to English. cw 2020-06-30
        lang = "en";
        if ( window.location.href.includes("lang=") ) {
         lang = urlParam("lang").substr(0,2);
        }

        if ( window.location.href.includes("city=") ) {
          // use City, State, country
          let city = urlParam("city");
          //console.log(city);
          let state = urlParam("state");
          let country = urlParam("country");

          if (city !== "" || state !== "" || country !== "") {
            GeoLocation.lookupLocationByCityStateCountry(city, state, country, false);
          }
        } else {
          // If no GeoLocation provide user feedback cw 2020-07-02
          //     When user enters a geolocation the subscribe above will kick-off PopulateData()
          if ( GeoLocation.getCityName() === false) {
            if (lang === "es") {
              alert("Ingrese un código postal o el nombre de una ciudad en la barra negra y seleccione una ubicación de la lista.");
            } else {
              alert("Please enter a Zip Code or a city name in the Black Bar and select a location from the list.");
            }
          }
        }

        // Move Geosearch box onto the page cw 2020-07-09
        var geoSearchBox = document.getElementsByClassName("location-input aqi-nav-scroll");
        if( $(geoSearchBox).parent().attr("id") == "nav-geosearch-tool") {
          $(geoSearchBox).detach().appendTo('#floatingGeoSearchBox');
          //var searchGroup = document.getElementsByClassName("location-input aqi-nav-scroll");
          $(geoSearchBox).css( "width", "185px");
          $(geoSearchBox).css( "background", "#333");
        }

        PubSub.subscribe(GeoLocation.TOPICS.new_location, function() {
            PubSub.publish(ReportingArea.TOPICS.new_data, true);
        });

        PubSub.subscribe(ReportingArea.TOPICS.new_data, function() {
            populateData();
        });

      });

        function populateData() {
            let locationDisplayName = GeoLocation.getLocationDisplayName();
            //let aqData = ReportingArea.getMaxCurrentReportingAreaData();
            let currentData = ReportingArea.getAllCurrentReportingAreaData();
            let fcstTodayData = ReportingArea.getMaxForecastReportingAreaData(0);
            let fcstTodayDataOther = ReportingArea.getOtherForecastReportingAreaData(0);
            let fcstTomorrowData = ReportingArea.getMaxForecastReportingAreaData(1);
            let fcstTomorrowDataOther = ReportingArea.getOtherForecastReportingAreaData(1);

            // Spanish for "Pollutant Details" and "MiddleText" cw 2020-07-01
            if (lang === "es") {
              today_details_button_div.innerHTML = "Datos de contaminantes";
              tomorrow_details_button_div.innerHTML = "Datos de contaminantes";
              document.getElementById('today-middle-text').innerHTML = "<strong>Pronóstico de calidad<br /><br /></strong>";
              document.getElementById('tomorrow-middle-text').innerHTML = "<strong>Pronóstico de calidad<br />del aire de mañana<br /></strong>";
              // Tranlate other English elements on the page cw 2020-07-01
              document.getElementById('whichFlagTitle').innerHTML = "<strong>¿Qué banderín ondeo?</strong>"
              document.getElementById('learnMore').innerHTML = "Más información sobre los <a href=\"/aqi/aqibasics\">colores del índice de la calidad del aire</a>.<p>Vea las <a href=\"/activity-guides-publications\">edidas que debe tomare</a> para cada color.";
            }

            // By default, show the Pollutant Details cw 2020-07-09
            document.getElementById("today_div").style.display = "table-row";
            document.getElementById("tomorrow_div").style.display = "table-row";

            if (fcstTodayData) {
                    let category = fcstTodayData[ReportingArea.FIELDS.category];
                    // Converted to Flag Progam Widget style cw 2020-06-11
                    // Custom Name label cw 2020-06-12
                    var name = document.getElementById('today-location-name');
                    name.innerHTML = "<strong>"+ fcstTodayData[ReportingArea.FIELDS.reportingAreaName] +", "+ fcstTodayData[ReportingArea.FIELDS.stateCode]+"</strong>";
                    // Target the flag graphic cw 2020-06-11
                    var image = document.getElementById('today-flag');
                    let flagColor = categoryColor(fcstTodayData[ReportingArea.FIELDS.category]);
                    //console.log("/themes/anblue/images/which-flag/"+flagColor+"-flag-sm-what.gif");
                    //console.log(image.src);
                    if (lang === "es") {
                      image.src = "/themes/anblue/images/which-flag/"+flagColor+"s-flag-sm-what.gif";
                    } else {
                      image.src = "/themes/anblue/images/which-flag/"+flagColor+"-flag-sm-what.gif";
                    }
                    image.alt = fcstTodayData[ReportingArea.FIELDS.category]
                    // Target the Middle Text Section cw 2020-06-12
                    // old format: <b>Today\'s Air Quality <br>Forecast<br> 6/8/2020  <br></b>
                    var middleText = document.getElementById('today-middle-text');
                    let date = fcstTodayData[ReportingArea.FIELDS.validDate];
                    if (lang === "es") {
                      middleText.innerHTML = "<strong>Pronóstico de calidad<br /><br /><br />"+ date +"</strong>";
                    } else {
                      middleText.innerHTML = "<strong>Today's Air Quality<br />Forecast<br /><br />"+ date +"</strong>";
                    }
                    if (document.getElementById("today_div").style.display === "table-row") { // if the Polutant Details are visable
                      // Target the Pollutant Section cw 2020-06-16
                      // First / Highest Pollutant
                      var poll_name = document.getElementById('today-poll-name');
                      //console.log(fcstTodayData);
                      //console.log(fcstTodayData[ReportingArea.FIELDS.parameter]);
                      //console.log(fcstTodayData[ReportingArea.FIELDS.aqi]);
                      //console.log(fcstTodayData[ReportingArea.FIELDS.category]);
                      poll_name.innerHTML = fcstTodayData[ReportingArea.FIELDS.parameter];
                      var image = document.getElementById('today-poll-dot');
                      let dotColor = categoryColor(fcstTodayData[ReportingArea.FIELDS.category]);
                      image.src = "/themes/anblue/images/which-flag/aqi_"+dotColor+".gif";
                      image.alt = fcstTodayData[ReportingArea.FIELDS.category];
                      var poll_cat = document.getElementById('today-poll-cat');
                      poll_cat.innerHTML = fcstTodayData[ReportingArea.FIELDS.category];
                      if (lang === "es") {
                        //console.log(fcstTodayData[ReportingArea.FIELDS.parameter]);
                        poll_name.innerHTML = parameterES(fcstTodayData[ReportingArea.FIELDS.parameter]);
                        image.alt = categoryES(fcstTodayData[ReportingArea.FIELDS.category]);
                        poll_cat.innerHTML = categoryES(fcstTodayData[ReportingArea.FIELDS.category]);
                      }
                      document.getElementById('today_row').style = "display: table-row;";
                      // Other Pollutants
                      //console.log(fcstTodayDataOther);
                      //console.log("fcstTodayDataOther.length");
                      //console.log(fcstTodayDataOther.length);
                      let dotColorOther = "white";
                      let otherPolls = "";
                        for (let i = 0; i < fcstTodayDataOther.length; i++) {
                          // console.log(fcstTodayDataOther[i]);
                          // console.log(fcstTodayDataOther[i][ReportingArea.FIELDS.parameter]);
                          // console.log(fcstTodayDataOther[i][ReportingArea.FIELDS.aqi]);
                          // console.log(fcstTodayDataOther[i][ReportingArea.FIELDS.category]);
                          let dotColorOther = categoryColor(fcstTodayDataOther[i][ReportingArea.FIELDS.category]);
                          // build the entire <TR> each time through the loop; branching for lang
                          if (lang === "es") {
                            eval("today_row"+i).innerHTML =
                            '<td width="55" style="padding:5px;" align="center">'+parameterES(fcstTodayDataOther[i][ReportingArea.FIELDS.parameter])+'</td>'+
          									'<td align="center" style="padding:5px;" align="center"><img alt="'+dotColorOther+'" src="/themes/anblue/images/which-flag/aqi_'+dotColorOther+'.gif" title=""></td>'+
          									'<td align="center" height="50" width="35" style="padding:5px;"  align="center">'+categoryES(fcstTodayDataOther[i][ReportingArea.FIELDS.category])+'</td>';
                            // display the row
                            eval("today_row"+i).style = "display: table_row;";
                          } else {
                            eval("today_row"+i).innerHTML =
                            '<td width="55" style="padding:5px;" align="center">'+fcstTodayDataOther[i][ReportingArea.FIELDS.parameter]+'</td>'+
          									'<td align="center" style="padding:5px;" align="center"><img alt="'+dotColorOther+'" src="/themes/anblue/images/which-flag/aqi_'+dotColorOther+'.gif" title=""></td>'+
          									'<td align="center" height="50" width="35" style="padding:5px;"  align="center">'+fcstTodayDataOther[i][ReportingArea.FIELDS.category]+'</td>';
                            // display the row
                            eval("today_row"+i).style = "display: table_row;";
                            } // end lang if
                        } // end for
                        // hide the rows that are not needed
                        for (let i = fcstTodayDataOther.length; i < 4; i++) {
                          eval("today_row"+i).style = "display: none;";
                        }
                      }
                    } else {
                      // There is no today forecast cw 2020-06-25
                      var name = document.getElementById('today-location-name');
                      name.innerHTML = "<strong>&nbsp;</strong>";
                      var image = document.getElementById('today-flag');
                      image.src = "/themes/anblue/images/which-flag/todayBW.gif";
                      image.alt = "No Data";
                      document.getElementById('today_row').style = "display: none;";
                      //document.getElementById('today_row').innerHTML = " ";
                      // hide the rows that are not needed
                      for (let i = fcstTodayDataOther.length; i < 4; i++) {
                        eval("today_row"+i).style = "display: none;";
                        eval("today_row"+i).innerHTML = " ";
                      }
                }

                if (fcstTomorrowData) {
                  let category = fcstTomorrowData[ReportingArea.FIELDS.category];
                  // Converted to Flag Progam Widget style cw 2020-06-11

                  // Custom Name label cw 2020-06-12
                  var name = document.getElementById('tomorrow-location-name');
                  name.innerHTML = "<strong>"+ fcstTomorrowData[ReportingArea.FIELDS.reportingAreaName] +", "+ fcstTomorrowData[ReportingArea.FIELDS.stateCode]+"</strong>";
                  // Target the flag graphic cw 2020-06-11
                  var image = document.getElementById('tomorrow-flag');
                  let flagColor = categoryColor(fcstTomorrowData[ReportingArea.FIELDS.category]);
                  //console.log("/themes/anblue/images/which-flag/"+flagColor+"-flag-sm-what.gif");
                  if (lang === "es") {
                    image.src = "/themes/anblue/images/which-flag/"+flagColor+"s-flag-sm-what.gif";
                  } else {
                    image.src = "/themes/anblue/images/which-flag/"+flagColor+"-flag-sm-what.gif";
                  }
                  image.alt = fcstTomorrowData[ReportingArea.FIELDS.category]
                  // Target the Middle Text Section cw 2020-06-12
                  var middleText = document.getElementById('tomorrow-middle-text');
                  let date = fcstTomorrowData[ReportingArea.FIELDS.validDate];
                  if (lang === "es") {
                    middleText.innerHTML = "<strong>Pronóstico de calidad<br />del aire de mañana<br /><br />"+ date +"</strong>";
                  } else {
                    middleText.innerHTML = "<strong>Tomorrow's Air Quality<br />Forecast<br /><br />"+ date +"</strong>";
                  }
                  if (document.getElementById("tomorrow_div").style.display === "table-row") { // if the Polutant Details are visable
                    // Target the Pollutant Section cw 2020-06-16
                    // First / Highest Pollutant
                    var tomorrow_poll_name = document.getElementById('tomorrow-poll-name');
                    //console.log(fcstTomorrowData);
                    //console.log(fcstTomorrowData[ReportingArea.FIELDS.parameter]);
                    //console.log(fcstTomorrowData[ReportingArea.FIELDS.aqi]);
                    //console.log(fcstTomorrowData[ReportingArea.FIELDS.category]);
                    tomorrow_poll_name.innerHTML = fcstTomorrowData[ReportingArea.FIELDS.parameter];
                    var image = document.getElementById('tomorrow-poll-dot');
                    let dotColor = categoryColor(fcstTomorrowData[ReportingArea.FIELDS.category]);
                    image.src = "/themes/anblue/images/which-flag/aqi_"+dotColor+".gif";
                    image.alt = fcstTomorrowData[ReportingArea.FIELDS.category]
                    var poll_cat = document.getElementById('tomorrow-poll-cat');
                    poll_cat.innerHTML = fcstTomorrowData[ReportingArea.FIELDS.category];
                    if (lang === "es") {
                      //console.log(fcstTomorrowData[ReportingArea.FIELDS.parameter]);
                      tomorrow_poll_name.innerHTML = parameterES(fcstTomorrowData[ReportingArea.FIELDS.parameter]);
                      image.alt = categoryES(fcstTomorrowData[ReportingArea.FIELDS.category]);
                      poll_cat.innerHTML = categoryES(fcstTomorrowData[ReportingArea.FIELDS.category]);
                    }
                    document.getElementById('tomorrow_row').style = "display: table-row;";
                    // Other Pollutants
                    //console.log(fcstTomorrowDataOther);
                    //console.log("fcstTomorrowDataOther.length");
                    //console.log(fcstTomorrowDataOther.length);
                    let dotColorOther = "white";
                    let otherPolls = "";
                      for (let i = 0; i < fcstTomorrowDataOther.length; i++) {
                        //console.log(fcstTomorrowDataOther[i]);
                        //console.log(fcstTomorrowDataOther[i][ReportingArea.FIELDS.parameter]);
                        //console.log(fcstTomorrowDataOther[i][ReportingArea.FIELDS.aqi]);
                        //console.log(fcstTomorrowDataOther[i][ReportingArea.FIELDS.category]);
                        let dotColorOther = categoryColor(fcstTomorrowDataOther[i][ReportingArea.FIELDS.category]);
                        // build the entire <TR> each time through the loop; branching for lang
                        if (lang === "es") {
                            eval("tomorrow_row"+i).innerHTML =
                            '<td width="55" style="padding:5px;" align="center">'+parameterES(fcstTomorrowDataOther[i][ReportingArea.FIELDS.parameter])+'</td>'+
          									'<td align="center" style="padding:5px;" align="center"><img alt="'+dotColorOther+'" src="/themes/anblue/images/which-flag/aqi_'+dotColorOther+'.gif" title=""></td>'+
          									'<td align="center" height="50" width="35" style="padding:5px;"  align="center">'+categoryES(fcstTomorrowDataOther[i][ReportingArea.FIELDS.category])+'</td>';
                            // display the row
                            eval("tomorrow_row"+i).style = "display: table_row;";
                          } else {
                            eval("tomorrow_row"+i).innerHTML =
                            '<td width="55" style="padding:5px;" align="center">'+fcstTomorrowDataOther[i][ReportingArea.FIELDS.parameter]+'</td>'+
          									'<td align="center" style="padding:5px;" align="center"><img alt="'+dotColorOther+'" src="/themes/anblue/images/which-flag/aqi_'+dotColorOther+'.gif" title=""></td>'+
          									'<td align="center" height="50" width="35" style="padding:5px;"  align="center">'+fcstTomorrowDataOther[i][ReportingArea.FIELDS.category]+'</td>';
                            // display the row
                            eval("tomorrow_row"+i).style = "display: table-row;";
                          } // enf lang if
                      } // end for
                      // hide the rows that are not needed
                      for (let i = fcstTomorrowDataOther.length; i < 4; i++) {
                        eval("tomorrow_row"+i).style = "display: none;";
                      }
                    }

                    // Add event for Tomorrow Pollutant Details rollup
                    $( "#tomorrow_details_button_div" ).click(function() {
                      //alert( "Handler for .click() called." );
                      //$(this).siblings('tomorrow_div').toggle();
                      var x = document.getElementById("tomorrow_div");
                      if (x.style.display === "none") {
                        x.style.display = "block";
                      } else {
                        x.style.display = "none";
                      }
                    });

                  } else {
                    // There is no tomorrow forecast cw 2020-06-25
                    var name = document.getElementById('tomorrow-location-name');
                    name.innerHTML = "<strong>&nbsp;</strong>";
                    var image = document.getElementById('tomorrow-flag');
                    image.src = "/themes/anblue/images/which-flag/todayBW.gif";
                    image.alt = "No Data";
                    document.getElementById('tomorrow_row').style = "display: none;";
                    //document.getElementById('tomorrow_row').innerHTML = " ";
                    // hide the rows that are not needed
                    for (let i = fcstTomorrowDataOther.length; i < 4; i++) {
                      eval("tomorrow_row"+i).style = "display: none;";
                      eval("tomorrow_row"+i).innerHTML = " ";
                    }
                  }

                // Add this to bottom of Page
                //console.log(fcstTodayData[ReportingArea.FIELDS.discussion]);
                if (fcstTodayData[ReportingArea.FIELDS.discussion]) {
                  //console.log("Discussion is: " + fcstTodayData[ReportingArea.FIELDS.discussion]);
                  // Build the forecast_disscusion
                  var forecast_disscusion = document.getElementById('forecast_disscusion');
                  forecast_disscusion.innerHTML = '<strong>Forecast Discussion:</strong> '+ fcstTodayData[ReportingArea.FIELDS.discussion];
                  forecast_disscusion.style = "display: table_row;"
                } else {
                  document.getElementById('forecast_disscusion').style = "display: none;"
                }

            }

        // Use values from the URL cw 2020-06-08
        // https://www.sitepoint.com/url-parameters-jquery/
        function urlParam(name){
          var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
          return results[1] || 0;
        }

        // Convert category to color for use in graphic files cw 2020-06-17
        function categoryColor(category){
          let color = "green"; // good
          if (category === "Moderate") {
              color = "yellow"; // moderate
          } else if (category === "Unhealthy for Sensitive Groups") {
              color = "orange"; // semi unhealthy
          } else if (category === "Unhealthy") {
              color = "red"; // unhealthy
          } else if (category === "Very Unhealthy") {
              color = "purple"; // very unhealthy
          } else if (category === "Hazardous") {
              color = "purple"; // hazardous
          }
          return color;
        }

        // Translate category to Spainsh cw 2020-07-01
        function categoryES(category){
          if (lang === "es") {
            let category_es = "Bueno"; // good
            if (category === "Moderate") {
                category_es = "Moderado"; // moderate
            } else if (category === "Unhealthy for Sensitive Groups") {
                category_es = "Saludable para grupos sensibles "; // semi unhealthy
            } else if (category === "Unhealthy") {
                category_es = "Insalubre"; // unhealthy
            } else if (category === "Very Unhealthy") {
                category_es = "Muy poco saludables"; // very unhealthy
            } else if (category === "Hazardous") {
                category_es = "Peligroso"; // hazardous
            }
            return category_es;
          }
        }

        // Translate Polutant parameter to Spainsh cw 2020-07-01
        function parameterES(parameter){
          if (lang === "es") {
            if (parameter === "PM2.5") {
                parameter_es = "PM2.5";
            } else if (parameter === "PM10") {
                parameter_es = "PM10";
            } else if (parameter === "OZONE") {
                parameter_es = "Ozono";
            } else if (parameter === "CO") {
                parameter_es = "Monóxido de carbono";
            } else if (parameter === "NO2") {
                  parameter_es = "Dióxido de azufre";
            } else if (parameter === "SO2") {
                parameter_es = "SO2";
            }
            return parameter_es;
          }
        }

        // Polutant parameter in Long Form cw 2020-07-01
        function parameterLong(parameter){
          if (parameter === "PM2.5") {
              parameter_long = "Particles (PM2.5)";
          } else if (parameter === "PM10") {
              parameter_long = "Particles (PM10)";
          } else if (parameter === "OZONE") {
              parameter_long = "Ozone";
          } else if (parameter === "CO") {
              parameter_long = "Carbon Monoxide";
          } else if (parameter === "NO2") {
                parameter_long = "Nitrogen Dioxide";
          } else if (parameter === "SO2") {
              parameter_long = "Sulfur Dioxide";
          }
          return parameter_long;
        }

    }
  }
})(jQuery, Drupal);
