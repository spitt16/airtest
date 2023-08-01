(function ($, Drupal) {
  //console.log(Drupal);
  Drupal.behaviors.marqueeDataHelper = {
    attach: function (context, settings) {
      // console.log("Marquee Data Helper (Original)");

      handleAqiLegend();

      let PubSub = Drupal.behaviors.PubSub;
      let AirNowGov = Drupal.behaviors.AirNowGov;
      let ReportingArea = AirNowGov.ReportingArea;
      let GeoLocation = AirNowGov.GeoLocation;
      let PageLoader = AirNowGov.PageLoader;
      let Tooltips = AirNowGov.Tooltips;

      let themeDirectory = settings.themeDirectory;
      let sampleImages = settings.sampleMarqueeImages;
      let themeImgDirectory = themeDirectory + /images/;

      let dataProviderMapLoaded = false;
      let reportingAreaDataLoaded = false;

      const MAX_ROTATION_DEGREES = 180;
      const MIN_ROTATION_DEGREES = 0;

      function getDegree(aqi) {
        let deg;
        // AQI values 0 - 200 represent the first 4/6 of the dial
        if (aqi <= 200) {
          deg = (aqi / 200) * (MAX_ROTATION_DEGREES * (4 / 6));
        }
        // AQI values 201 - 300 represent the second to last 1/6 of the dial
        else if (aqi <= 300) {
          deg = (MAX_ROTATION_DEGREES * (4 / 6)) + ((((aqi - 200) / (300 - 200))) * (MAX_ROTATION_DEGREES * (1 / 6)))
        }
        // AQI values 301 - 500 represent the last 1/6 of the dial
        else if (aqi <= 500) {
          deg = (MAX_ROTATION_DEGREES * (5 / 6)) + ((((aqi - 300) / (500 - 300))) * (MAX_ROTATION_DEGREES * (1 / 6)))
        }
        // AQI values above 400 should just be treated as the maximum rotation
        else {
          deg = MAX_ROTATION_DEGREES;
        }
        return deg;
      }

      // Rotates the arrow to the provided degrees.  Degree values capped at 0 and 180
      function rotateArrow(deg) {
        // Ensure we do not rotate too far in either direction
        deg = Math.max(MIN_ROTATION_DEGREES, Math.min(deg, MAX_ROTATION_DEGREES));
        // Apply the rotation
        let arrows = document.getElementsByClassName("aq-dial-arrow");
        for (let i = 0; i < arrows.length; i++) {
          let arrow = arrows[i];
          arrow.style.webkitTransform = "rotate(" + deg + "deg)";
          arrow.style.mozTransform = "rotate(" + deg + "deg)";
          arrow.style.msTransform = "rotate(" + deg + "deg)";
          arrow.style.oTransform = "rotate(" + deg + "deg)";
          arrow.style.transform = "rotate(" + deg + "deg)";
        }
      }

      function toggleNoDataDisplay(noData) {
        $(".aq-dial:not(.status-bar)").toggle(!noData);
        $(".marquee-forecast-col").toggleClass("noData", noData);
        $(".marquee-location-col").toggleClass("noData", noData);
        $(".aq-dial-container").toggleClass("noData", noData);
        $(".po-aqi-scale").toggleClass("noData", noData);

        $(".location-holder").toggleClass("splash-screen", noData);

        // if (noData) {
        //   $(".marquee-location-col .location-label.standard-location-label").html("Get Current and Forecast<br />Air Quality for Your Area");
        // }
      }


      $(document).ready(function () {
        // GeoLocation.enableGeolocationLookupField("location-input-style");


        if (navigator.userAgent.match(/(iPod|iPhone|iPad|Android)/)) {
          $(document).on("keypress", "#location--inputmobile_input,.suggestionsMenu li", function (e) {
            if (e.keyCode === 13) {
              document.activeElement.blur();
              $("#location--inputmobile_input").blur();
              e.target.blur();
              $("html, body").animate({ scrollTop: "0" });
            }
          });
          $(document).on("click", ".suggestionsMenu li", function (e) {
            document.activeElement.blur();
            e.target.blur();
            $("#location--inputmobile_input").blur();
            $("html, body").animate({ scrollTop: "0" });
          });
          $(document).on("focus", "#location--inputmobile_input", function () {
            $("html, body").animate({ scrollTop: $("#location--inputmobile_input").offset().top - $("#master-navbar").height() - 25 });
          });
        }

        // Grabs the user's location, only if on the landing dial, there's no location set, and there's no URL parameters
        if ($("#location-input:empty, #location--inputmobile:empty") // AirNowDrupal # 107 Changed to a vaild jQuery selector cw-2019-03-08
          && !GeoLocation.getLocationDisplayName() && window.location.search.split(/\?|\&/).length === 1) {
          GeoLocation.requestUserLocation();
        }

        Tooltips.createTip(".aq-dial .bottom-half .current-aq-container .aqi", "aqi", "top");
        Tooltips.createTip(".aq-dial .bottom-half .current-aq-container .header", "currentAirQuality", "top");
        Tooltips.createTip(".aq-dial .bottom-half .forecast-aq-container .header", "airQualityForecast", "right");

        // AIR-281 Add Tippy ONLY if disabled cw 2021-09-02
        Tooltips.createTip("div.location-input-gps-btn", "gpsButton", "top");

        $(".aq-dial .forecast-aq-container .misc div").on("click", function () {
          $('html, body').animate({
            scrollTop: $("#forecast-aq-band").offset().top - $("#master-navbar").height()
          }, 1500);
        });
        $(".aq-dial .forecast-aq-container .today-aq-data").on("click", function () {
          $('html, body').animate({
            scrollTop: $("#forecast-aq-band").offset().top - $("#master-navbar").height()
          }, 1500);
          $("#day-0").click();
        });
        $(".aq-dial .forecast-aq-container .tomorrow-aq-data").on("click", function () {
          $('html, body').animate({
            scrollTop: $("#forecast-aq-band").offset().top - $("#master-navbar").height()
          }, 1500);
          $("#day-1").click();
        });

        $(".marquee-location-col .location-input-gps-btn").on("click", function () {
          // TODO: disable if blocked by user
          GeoLocation.requestUserLocation();
        });

        // FIXME: Delete once we delete the 2-day forecast widget
        $(".forecast-container").hide();

        // AirnowDrupal # 110 Do NOT use the multiple image feature  cw 2019-04-09
        //PubSub.subscribe(GeoLocation.TOPICS.new_location, function() {
        //  var randomImage = sampleImages["samples"][Math.floor(Math.random() * Math.floor(sampleImages["samples"].length))];

        //  var marqueeImage = new Image();
        //  marqueeImage.onload = function() {
        //    $('.marquee-background').css(
        //      { 'background': 'url('+randomImage+')',
        //        'background-attachment': 'fixed',
        //        'background-position': 'center',
        //        'background-repeat': 'no-repeat',
        //        'background-size': 'cover'
        //      }
        //    );

        // Fade in allowed
        //    $('.marquee-background').removeClass("marquee-background-hide");
        //    $(".day-holder").find(".show-day-caret").removeClass("show-day-caret");
        //    $("#day-holder-0").find(".day-caret").addClass("show-day-caret");
        //  };

        //  marqueeImage.src = randomImage;
        //  if (marqueeImage.complete){
        //    marqueeImage.onload();
        //  }

        // let mq = window.matchMedia('(max-width: 767px)');
        //
        // if(mq.matches) {
        //   $("html, body").animate({ scrollTop: 0 }, 500);
        // }
        //});
        $("#popup-announcement-container, #popup-announcement-container .popup-announcement-title-dismiss").on("click", function () {
          $("#popup-announcement-container").hide();
        });

        PubSub.subscribe(ReportingArea.TOPICS.new_data, function () {
          let hasData = ReportingArea.hasReportingAreaData();
          let hasLocation = GeoLocation.getLocationDisplayName();
          if (!hasData && hasLocation) {
            let locationStateName = GeoLocation.getLocationStateName();
            $("#popup-announcement-container").show();
            if (locationStateName) {
              let statePageUrl = "/state/?name=" + locationStateName.replace(/ /g, "-").toLowerCase();
              $("#popup-announcement-state-page-link").html(locationStateName + " state page");
              $("#popup-announcement-state-page-link").attr("href", statePageUrl);
              $("#popup-announcement-container .statePageLink").toggle(true);
              $("#popup-announcement-container .otherCountryText").toggle(false);
            } else {
              $("#popup-announcement-container .statePageLink").toggle(false);
              $("#popup-announcement-container .otherCountryText").toggle(true);
            }
          }
          populateData(false);
          reportingAreaDataLoaded = true;
          setDataProviders();
        });
        PubSub.subscribe(ReportingArea.TOPICS.new_dataproviders, function () {
          dataProviderMapLoaded = true;
          setDataProviders();
        });
        PubSub.subscribe(GeoLocation.TOPICS.new_location, function () {
          let locationDisplayName = GeoLocation.getLocationDisplayName();
          let locationStateName = GeoLocation.getLocationStateName();
          if (locationDisplayName) {
            //AIR-521 Dial Translation prep; no translate of Place Names cw 2022-04-07
            $(".location-label").html("<span class='notranslate'>"+locationDisplayName+"</span>");
            $(".mobile-location-label").html("<span class='notranslate'>"+locationDisplayName+"</span>");
            // AirNowDrupal # 118 Remove More Cities button cw 2019-04-01
            //$(".state-air-quality").text("More Cities in " + handleLongStateName(locationStateName));
            //$(".state-air-quality").off("click").on("click", function() {
            //  let win = window.open("/state/" + locationStateName.replace(/ /g, "-").toLowerCase(), "_self");
            //  win.focus();
            //});
            PageLoader.updateURLParameters();
          }
        });
        PubSub.subscribe(PageLoader.TOPICS.services_ready, function () {
          populateData(true);
          /* Data courtesy for FireFox Browsers  cw 2018-10-26 */
          dataProviderMapLoaded = true;
          setDataProviders();
        });
      });

      // addAQIDropdownButtonListener();
      addAQINavScroll();

      // $("#location-input-mobile").on("focusout.locationScrollUp", function(){
      //   let mq = window.matchMedia('(max-width: 767px)');
      //
      //   if(mq.matches) {
      //     $("html, body").animate({ scrollTop: 0 }, 500);
      //   }
      //   return false;
      // });


      function addAQINavScroll() {
        //location-input-style location-input-field
        if ($("#location-input:visible, #location--inputmobile:visible").length > 0) {
          $(".aqi-nav-scroll").addClass("aqi-nav-scroll-hidden");
          $(document).on("scroll", function () {
            let navLeftSideToolbarVisible = $(".nav-left-side-toolbar").is(":visible");
            if ($("#location-input:visible, #location--inputmobile:visible").first().offset().top >= $("#bb-nav").offset().top) {
              $(".aqi-nav-scroll").addClass("aqi-nav-scroll-hidden");
              if (screen.width < 770) { 	// mobile size
                document.getElementById("nav-right-side-toolbar").style.display = "none"; //AIR-464 Hide nav input field on mobile cw 2021-08-03
              }
              // AIR-451 Adding Notification Banner cw 2021-06-14
              document.getElementById("nav-center-toolbar").style.transition = "1s";
              document.getElementById("nav-center-toolbar").style.opacity = "1";
              removeAQIDropdownButtonListener();
            } else {
              $(".aqi-nav-scroll").removeClass("aqi-nav-scroll-hidden");
              // AIR-441 Adding Notification Banner cw 2021-06-14
              document.getElementById("nav-center-toolbar").style.transition = "1s";
              document.getElementById("nav-center-toolbar").style.opacity = "0";
              if (screen.width < 770) { 	// mobile size
                document.getElementById("nav-right-side-toolbar").style.display = "inline"; //AIR-464 Show nav input field on mobile cw 2021-08-03
              }
              addAQIDropdownButtonListener();
            }
          });
        }
      }

      function addAQIDropdownButtonListener() {
        $(".btn.btn-aqi-nav").once("aqiNavBtnEnable").on("click.aqiBtnOpen", function (event) {
          event.stopPropagation();
          handleAQIDropdownButton();
        });
      }

      function removeAQIDropdownButtonListener() {
        $(".btn.btn-aqi-nav").removeOnce("aqiNavBtnEnable").off("click.aqiBtnOpen");
      }

      function handleAQIDropdownButton() {
        $(".aq-dial.status-bar").toggle();
        $(".btn-aqi-nav .aqi-nav-text").toggle();
        $(".btn-aqi-nav .fa.fa-times").toggle();
      }

      function populateData(isInit) {

        // var randomImage = sampleImages["samples"][Math.floor(Math.random() * Math.floor(sampleImages["samples"].length))];
        //
        // $('.marquee-background').css(
        //   { 'background': 'url('+randomImage+')',
        //     'background-attachment': 'fixed',
        //     'background-position': 'center',
        //     'background-repeat': 'no-repeat',
        //     'background-size': 'cover'
        //   }
        // );

        let currentAQData = ReportingArea.getMaxCurrentReportingAreaData();
        let forecastAQDataToday = ReportingArea.getMaxForecastReportingAreaData(0);
        let forecastAQDataTomorrow = ReportingArea.getMaxForecastReportingAreaData(1);
        let locationDisplayName = GeoLocation.getLocationDisplayName();
        let locationStateName = GeoLocation.getLocationStateName();

        let hasData = currentAQData || forecastAQDataToday || forecastAQDataTomorrow || locationDisplayName;

        toggleNoDataDisplay(!hasData);

        if (hasData) {
          // FIXME: Handle if no current or forecast data
          reportingAreaDataLoaded = true;

          if (location.search.indexOf("reportingArea") !== -1) {
            // We're using a reportingArea URL, and we need to verify that the URL displayed matches the data
            PageLoader.updateURLParameters();
          }

          let hasData = ReportingArea.hasReportingAreaData();
          if (!hasData) {
            let locationStateName = GeoLocation.getLocationStateName();
            if (isInit && !PageLoader.isPerformingURLSearch() && ReportingArea.isDataInit()) {
              $("#popup-announcement-container").show();
              if (locationStateName) {
                let statePageUrl = "/state/?name=" + locationStateName.replace(/ /g, "-").toLowerCase();
                $("#popup-announcement-state-page-link").html(locationStateName + " state page");
                $("#popup-announcement-state-page-link").attr("href", statePageUrl);
                $("#popup-announcement-container .statePageLink").toggle(true);
                $("#popup-announcement-container .otherCountryText").toggle(false);
              } else {
                $("#popup-announcement-container .statePageLink").toggle(false);
                $("#popup-announcement-container .otherCountryText").toggle(true);
              }
            }
          }

          // AIR-521 no data for the dial; set category as HTML to the dial to facilitate translation. cw 2022-04-20
          if (!currentAQData) {
              $(".aq-dial .top-half").html("Not Available");
              $(".aq-dial .top-half").attr("style", "font-size: 1.5em;"); // Not Available -- smaller to fit
              }

          if (currentAQData) {
            let categoryImageType = "not_available";
            let aqi = currentAQData[ReportingArea.FIELDS.aqi];
            let category = currentAQData[ReportingArea.FIELDS.category];
            if (category === "Good") {
              categoryImageType = "good"; // good
            } else if (category === "Moderate") {
              categoryImageType = "moderate"; // moderate
            } else if (category === "Unhealthy for Sensitive Groups") {
              categoryImageType = "usg"; // semi unhealthy
            } else if (category === "Unhealthy") {
              categoryImageType = "unhealthy"; // unhealthy
            } else if (category === "Very Unhealthy") {
              categoryImageType = "very_unhealthy"; // very unhealthy
            } else if (category === "Hazardous") {
                       // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI  //if (aqi < 501) {
                categoryImageType = "hazardous"; // hazardous

              // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
             // } else {
                //categoryImageType = "beyond_index"; // beyond aqi
                //category = "Beyond the AQI"; // Must be set for the pop-up rollover. Not in JSON data cw 2019-10-07
             // }
            }

            // AIR-521 Need to define the toolTips first cw 2022-04-07
            Tooltips.createTip(".aq-dial .top-half", "categories", "right", category, currentAQData[ReportingArea.FIELDS.parameter], null, 0);
            Tooltips.createTip(".aq-dial .bottom-half .current-aq-container .pollutant", "pollutant", "top", null, currentAQData[ReportingArea.FIELDS.parameter]);

            $(".aq-dial .aq-dial-status").attr("src", "/themes/anblue/images/dial3/dial_" + categoryImageType + ".svg");
            // AIR-521 Category as HTML to the dial to facilitate translation. "dial3" images have no text. cw 2022-04-07
            $(".aq-dial .top-half").html(category);

            // AIR-521 Addjustments for different category values depending on aqi value
            $(".aq-dial .top-half").attr("style", "color: white; font-size: 1.75em; position: relative; box-sizing: border-box; height: 60%; width: 48%; top: 34%; left: 25%; right: 25%;"); // Good; Unhealty; Hazardous-- Defauts
            if (aqi > 50 && aqi < 101) {
              $(".aq-dial .top-half").attr("style", "color: black;"); // Moderate -- black text
            } else if (aqi > 100 && aqi < 151) {
              $(".aq-dial .top-half").attr("style", "font-size: 1.3em; top: 32%;"); //  USG -- two wide lines
            } else if (aqi > 200 /*&& aqi < 301 || aqi > 500*/) { // Very Unhealthy; Beyond the AQI -- one wide line           // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI

              $(".aq-dial .top-half").attr("style", "font-size: 1.3 em; top: 37%;");
              }

            // Note that setTimeout needed to allow initial animation to play
            setTimeout(function () {
              let deg = getDegree(aqi);
              rotateArrow(deg);
            }, 0);

            // Convert reporting area's 24-hour update time to 12-hour
            let time;
            let rawTime = currentAQData[ReportingArea.FIELDS.time];
            let hour = rawTime.split(":")[0];
            let minute = rawTime.split(":")[1];
            // [AirNowDrupal-325] Time should no longer include minutes.
            if (Number(hour) < 12) { // 12 AM - 11 AM
              if (Number(hour) === 0) {
                time = "12 AM";
              } else {
                time = "" + Number(hour) + " AM";
              }
            } else { // 12 PM - 11 PM
              if (Number(hour) === 12) {
                time = "12 PM";
              } else {
                time = "" + Number(hour - 12) + " PM";
              }
            }
            let tz = currentAQData[ReportingArea.FIELDS.timezone];
            let validDate = moment(currentAQData[ReportingArea.FIELDS.validDate], "MM/DD/YY");
            $(".aq-dial .aq-updated-time").html("<b>" + time + "</b> " + tz + " " + validDate.format("MMM D")); // [AirNowDrupal-325] Time should be bold.
            $(".aq-dial .aq-updated-time").show(); // AirNowDrupal#380 cw 2020-12-02
            $(".aq-dial .aq-dial-arrow").show();

            $(".aq-dial .aqi").html("<b>" + aqi + "</b> <span class='notranslate'>NowCast AQI</span>"); // [AirNowDrupal-325] AQI should be bold. // AIR-521 Save AQI from Translation cw 2022-04-07
            $(".aq-dial .pollutant").html("<b>" + currentAQData[ReportingArea.FIELDS.parameter] + "</b>"); // [AirNowDrupal-325] Pollutant should be bold.
            // FIXME: Currently not supported in new dial
            // if (currentAQData[ReportingArea.FIELDS.parameter] === "PM2.5"
            //   || currentAQData[ReportingArea.FIELDS.parameter] === "PM10") {
            //   $(".pp-label-text p").text("Particle Pollution");
            // } else {
            //   $(".pp-label-text p").text("");
            // }

            //AIR-521 Dial Translation prep; no translate of Place Names cw 2022-04-07
            $(".location-label").html("<span class='notranslate'>"+locationDisplayName+"</span>");
            $(".mobile-location-label").html("<span class='notranslate'>"+locationDisplayName+"</span>");
            $(".splash-sub-message").text("");
            // AirNowDrupal # 118 Remove More Cities button cw 2019-04-01
            //$(".state-air-quality").text("More Cities in " + handleLongStateName(locationStateName));
            //$(".state-air-quality").off("click").on("click", function() {
            //  let win = window.open("/state/" + locationStateName.replace(/ /g, "-").toLowerCase(), "_self");
            //  win.focus();
            //});
          } else {
            $(".aq-dial .aq-updated-time").text("").hide();
            $(".aq-dial .aq-dial-arrow").hide();
            $(".aq-dial .aqi").html("<span class='notranslate'>NowCast AQI</span> N/A");
            $(".aq-dial .pollutant").text("N/A");
            $(".aq-dial .aq-dial-status").attr("src", "/themes/anblue/images/dial3/dial_not_available.svg");

            //AIR-521 Dial Translation prep; no translate of Place Names cw 2022-04-07
            $(".location-label").html("<span class='notranslate'>"+locationDisplayName+"</span>");
            $(".mobile-location-label").html("<span class='notranslate'>"+locationDisplayName+"</span>");

            // AirNowDrupal # 118 Remove More Cities button cw 2019-04-01
            //$(".state-air-quality").text("More Cities in " + handleLongStateName(locationStateName));
            //$(".state-air-quality").off("click").on("click", function() {
            //  let win = window.open("/state/" + locationStateName.replace(/ /g, "-").toLowerCase(), "_self");
            //  win.focus();
            //});

            }

          // FIXME: Delete this code block once corner forecast widget is removed
          $(".aq-forecast-label").text("Air Quality Forecast");
          let hasActionDay = false;
          let todayHasActionDay = false;
          let tomorrowHasActionDay = false;
          if (forecastAQDataToday) {
            hasActionDay = hasActionDay || forecastAQDataToday[ReportingArea.FIELDS.isActionDay];
            todayHasActionDay = false || forecastAQDataToday[ReportingArea.FIELDS.isActionDay];
          }
          if (forecastAQDataTomorrow) {
            hasActionDay = hasActionDay || forecastAQDataTomorrow[ReportingArea.FIELDS.isActionDay];
            tomorrowHasActionDay = false || forecastAQDataTomorrow[ReportingArea.FIELDS.isActionDay];
          }
          $(".aq-dial .forecast-aq-container .today-aq-data .action-day").toggle(todayHasActionDay);
          $(".aq-dial .forecast-aq-container .tomorrow-aq-data .action-day").toggle(tomorrowHasActionDay);
          setMarqueeForecastSections(forecastAQDataToday, ReportingArea, ".aq-day-current", "Today", hasActionDay);
          setMarqueeForecastSections(forecastAQDataTomorrow, ReportingArea, ".aq-day-next", "Tomorrow", hasActionDay);


          if (forecastAQDataToday) {
            let category = forecastAQDataToday[ReportingArea.FIELDS.category];
            let fcstCategory = "no-data";
            let smallFont = false;
            if (category === "Good") {
              fcstCategory = "good"; // good
            } else if (category === "Moderate") {
              fcstCategory = "moderate"; // moderate
            } else if (category === "Unhealthy for Sensitive Groups") {
              fcstCategory = "unhealthy-sensitive"; // semi unhealthy
              smallFont = true;
            } else if (category === "Unhealthy") {
              fcstCategory = "unhealthy"; // unhealthy
            } else if (category === "Very Unhealthy") {
              fcstCategory = "very-unhealthy"; // very unhealthy
            } else if (category === "Hazardous") {
              fcstCategory = "hazardous"; // hazardous
            }
            let circle = $(".aq-dial .forecast-aq-container .today-aq-data .circle");
            $(circle)
              .toggleClass("good", category === "Good")
              .toggleClass("moderate", category === "Moderate")
              .toggleClass("unhealthy-sensitive", category === "Unhealthy for Sensitive Groups")
              .toggleClass("unhealthy", category === "Unhealthy")
              .toggleClass("very-unhealthy", category === "Very Unhealthy")
              .toggleClass("hazardous", category === "Hazardous")
              .toggleClass("no-data-fcst", false);
            let categoryText = $(".aq-dial .forecast-aq-container .today-aq-data .category");
            $(categoryText).text(category, true);
            $(categoryText).toggleClass("smallfont", smallFont);
          } else {
            let circle = $(".aq-dial .forecast-aq-container .today-aq-data .circle");
            $(circle).toggleClass("no-data-fcst", true);
            let categoryText = $(".aq-dial .forecast-aq-container .today-aq-data .category");
            $(categoryText).text("Not Available", true);
          }
          if (forecastAQDataTomorrow) {
            let category = forecastAQDataTomorrow[ReportingArea.FIELDS.category];
            let fcstCategory = "no-data";
            let smallFont = false;
            if (category === "Good") {
              fcstCategory = "good"; // good
            } else if (category === "Moderate") {
              fcstCategory = "moderate"; // moderate
            } else if (category === "Unhealthy for Sensitive Groups") {
              fcstCategory = "unhealthy-sensitive "; // semi unhealthy
              smallFont = true;
            } else if (category === "Unhealthy") {
              fcstCategory = "unhealthy"; // unhealthy
            } else if (category === "Very Unhealthy") {
              fcstCategory = "very-unhealthy"; // very unhealthy
            } else if (category === "Hazardous") {
              fcstCategory = "hazardous"; // hazardous
            }
            let circle = $(".aq-dial .forecast-aq-container .tomorrow-aq-data .circle");
            $(circle)
              .toggleClass("good", category === "Good")
              .toggleClass("moderate", category === "Moderate")
              .toggleClass("unhealthy-sensitive", category === "Unhealthy for Sensitive Groups")
              .toggleClass("unhealthy", category === "Unhealthy")
              .toggleClass("very-unhealthy", category === "Very Unhealthy")
              .toggleClass("hazardous", category === "Hazardous")
              .toggleClass("no-data-fcst", false);
            let categoryText = $(".aq-dial .forecast-aq-container .tomorrow-aq-data .category");
            $(categoryText).text(category, true);
            $(categoryText).toggleClass("smallfont", smallFont);
          } else {
            let circle = $(".aq-dial .forecast-aq-container .tomorrow-aq-data .circle");
            $(circle).toggleClass("no-data-fcst", true);
            let categoryText = $(".aq-dial .forecast-aq-container .tomorrow-aq-data .category");
            $(categoryText).text("Not Available", true);
          }
        }

      }

      function setDataProviders() {
        if (!dataProviderMapLoaded || !reportingAreaDataLoaded) {
          return;
        }

        let dataProviderContainer = $(".marquee-dataprovider-col");
        let dataProviderContainerMobile = $(".mobile-marquee-dataprovider-col");
        let dataProviderPopupMobile = $("#popup-data-provider-container");
        dataProviderContainer.empty(); // remove all children
        dataProviderContainerMobile.empty(); // remove all children
        dataProviderPopupMobile.find(".popup-data-provider-message").empty(); // remove all children
        let reportingAreaContainer = $(".reporting-location");
        reportingAreaContainer.empty();
        let mobileReportingAreaContainer = $(".mobile-reporting-location");
        mobileReportingAreaContainer.empty();

        let radps = ReportingArea.getReportingAreaDataProviders();
        let dataProviders = radps.dataProviders;
        let dataProviderURLs = radps.dataProviderURLs;
        let forecastProvider = radps.forecastProvider; // Primary Agency
        let forecastProviderURL = radps.forecastProviderURL; // Primary Agency
        let reportingAreaID = radps.id;
        let twcCityCode = radps.twcCityCode;
        if (dataProviders.length) {

          // dataProviderContainer.append("<p class='dataProviderLabel'><b><a href='/data-providers?code=" + twcCityCode + "'>Data courtesy of </a></b></p>");
          dataProviderContainer.append("<p class='dataProviderLabel'><b>Data courtesy of </b></p>");
          dataProviderContainerMobile.append("<p><b>Data Providers</b></p>");
          //if (forecastProvider && dataProviders.indexOf(forecastProvider) > -1) {//
          // AIR-508 The data provider section now displays the data pprovider link and not the forecast provider link.
          if (dataProviderURLs) {
            dataProviderContainer.append("<p class='dataProviderAgency'><a href='" + dataProviderURLs[0] + "' target='_blank'>" + dataProviders[0] + "</a></p>");
            dataProviderPopupMobile.find(".popup-data-provider-message").append("<p><a href='" + dataProviderURLs[0] + "' target='_blank'>" + dataProviders[0] + "</a></p>");
          } else {
            dataProviderContainer.append("<p class='dataProviderAgency'>" + dataProviders[0] + "</p>");
            dataProviderPopupMobile.find(".popup-data-provider-message").append("<p>" + dataProviders[0] + "</p>");
          }
          // }//
          if (dataProviders[1]) {

            if (dataProviderURLs) {
              dataProviderContainer.append("<p class='dataProviderAgency'><a href='" + dataProviderURLs[1] + "' target='_blank'>" + dataProviders[1] + "</a></p>");
              dataProviderPopupMobile.find(".popup-data-provider-message").append("<p><a href='" + dataProviderURLs[1] + "' target='_blank'>" + dataProviders[1] + "</a></p>");
            } else {
              dataProviderContainer.append("<p class='dataProviderAgency'>" + dataProviders[1] + "</p>");
              dataProviderPopupMobile.find(".popup-data-provider-message").append("<p>" + dataProviders[1] + "</p>");
            }

          }

          // }//
          /*let i = 0;
          for (let i in dataProviders) {
            let a = dataProviders[i];
            if (a !== forecastProvider) {
              if (dataProviderURLs[i]) {
                dataProviderContainer.append("<p class='dataProviderAgency'><a href='" + dataProviderURLs[i] + "' target='_blank'>" + a + "</a></p>");
                dataProviderPopupMobile.find(".popup-data-provider-message").append("<p><a href='" + dataProviderURLs[i] + "' target='_blank'>" + a + "</a></p>");
              } else {
                dataProviderContainer.append("<p class='dataProviderAgency'>" + a + "</p>");
                dataProviderPopupMobile.find(".popup-data-provider-message").append("<p>" + a + "</p>");
              }
            }
            i++;
          }*/
        }

        dataProviderPopupMobile.click(function (event) {
          $target = $(event.target);
          if (!$target.closest("#popup-data-provider").length) {
            dataProviderPopupMobile.hide();
          }
        });
        dataProviderPopupMobile.find(".popup-data-provider-title-dismiss").click(function () {
          dataProviderPopupMobile.hide();
        });

        dataProviderContainerMobile.click(function () {
          dataProviderPopupMobile.show();
        });

        let ra = ReportingArea.getAllReportingAreaData();
        if (ra.length) {
          reportingAreaContainer.append("<span class='reporting-location-name'>" + ra[0].reportingArea + " Reporting Area" + "</span>");
          mobileReportingAreaContainer.append("<span class='mobile-reporting-location-name'>" + ra[0].reportingArea + " Reporting Area" + "</span>");
        }
      }
    }
  };

  function setMarqueeForecastSections(forecastAQData, ReportingArea, forecastClass, forecastText, hasActionDay) {
    $(forecastClass + " .aq-day-label").text(forecastText);
    if (forecastAQData) {
      let category = forecastAQData[ReportingArea.FIELDS.category];
      let displayCategory = category;
      //displayCategory = ReportingArea.FIELDS.aqi;
      $(forecastClass + " .aq-day-category")
        .toggleClass("good", category === "Good")
        .toggleClass("moderate", category === "Moderate")
        .toggleClass("unhealthy-sensitive", category === "Unhealthy for Sensitive Groups")
        .toggleClass("unhealthy", category === "Unhealthy")
        .toggleClass("very-unhealthy", category === "Very Unhealthy")
        .toggleClass("hazardous", category === "Hazardous")

      if (displayCategory === "Unhealthy for Sensitive Groups") {
        displayCategory = "USG";
      }

      // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
      /*if (category === "Hazardous" && forecastAQData[ReportingArea.FIELDS.aqi] >= 500) {
        displayCategory = "Hazardous"; // Adding Beyond AQI cw 2019-10-08
      }*/
      if (forecastAQData[ReportingArea.FIELDS.isActionDay]) {
        $(forecastClass + " .aq-day-action").text("(!) Action Day").toggleClass("action-day", true).toggle(hasActionDay); // TODO: Icon to the left of text
      } else {
        $(forecastClass + " .aq-day-action").html("&nbsp;").toggleClass("action-day", false).toggle(hasActionDay);
      }
      $(forecastClass + " .aq-day-status-label").text(displayCategory);
    } else {
      $(forecastClass + " .aq-day-action").html("&nbsp;").toggleClass("action-day", false).toggle(hasActionDay);
      $(forecastClass + " .aq-day-status-label").text("N/A");
      $(forecastClass + " .aq-day-category")
        .removeClass("good")
        .removeClass("moderate")
        .removeClass("unhealthy-sensitive")
        .removeClass("unhealthy")
        .removeClass("very-unhealthy")
        .removeClass("hazardous");
    }
    $(forecastClass).closest(".forecast-container").toggleClass("narrowView", hasActionDay);
  }

  function handleAqiLegend() {
    $('.po-aqi-scale-btn').click(function () {
      $(this).addClass('po-aqi-scale-btn-hidden');
      $('.po-aqi-scale-display').removeClass('po-aqi-scale-display-hidden');
    });

    $('.po-aqi-scale-display .fa-times').click(function () {
      $('.po-aqi-scale-display').addClass('po-aqi-scale-display-hidden');
      $('.po-aqi-scale-btn').removeClass('po-aqi-scale-btn-hidden');

    });
  }

  function handleLongStateName(stateName) {
    stateName = stateName.replace("District of Columbia", "Dist. of Columbia");
    return stateName;
  }

})(jQuery, Drupal);
