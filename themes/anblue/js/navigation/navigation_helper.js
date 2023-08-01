(function ($, Drupal) {
  Drupal.behaviors.myModuleBehavior = {
    attach: function (context, settings) {
      let PubSub = Drupal.behaviors.PubSub;
      let AirNowGov = Drupal.behaviors.AirNowGov;
      let ReportingArea = AirNowGov.ReportingArea;
      let GeoLocation = AirNowGov.GeoLocation;
      let Tooltips = AirNowGov.Tooltips;

      let themeDirectory = settings.themeDirectory;
      let themeImgDirectory = themeDirectory + /images/;

      const MAX_ROTATION_DEGREES = 180;
      const MIN_ROTATION_DEGREES = 0;

      $(document).ready(function(){
        smoothScrollingAnchors();

        bindNavToolEvents();
        GeoLocation.enableGeolocationLookupField("location-input-style");

        $(".navbar .location-input-gps-btn").on("click", function() {
          // TODO: disable if blocked by user
          GeoLocation.requestUserLocation();
        });

        // Events to accomodate small screen sizes and the lack of status bar real estate.

        // Expand geo-search input, and hide alerts & announcements
        $("#nav-geosearch-tool .location-input").click(function() {
          let $this = $(this);
          if (!$this.hasClass("aqi-nav-scroll-hidden")) {
            $(".nav-left-side-toolbar").parent().toggleClass("mobile-inactive", true);
            setTimeout(function() {
              $this.toggleClass("active", true);
            }, 175);
          }
        });

        // Shrink geo-search input, and show alerts & announcements
        $(document).click(function(event) {
          $target = $(event.target);
          if(!$target.closest("#nav-geosearch-tool .location-input").length && $("#nav-geosearch-tool .location-input").is(":visible")) {
            $("#nav-geosearch-tool .location-input").removeClass('active');
            setTimeout(function() {
              $(".nav-left-side-toolbar").parent().toggleClass("mobile-inactive", false);
            }, 175);
          }
        });

        PubSub.subscribe(ReportingArea.TOPICS.new_data, function() {
          // This is fired at each reporting area change cw 2021-06-11
          populateData();
          populateDialData();
          checkNotifications();  // AIR-451 cw 2021-06-11
        });
        // This is fired at inital page load cw 2021-06-11
        populateData();
        populateDialData();
        checkNotifications();  // AIR-451 cw 2021-06-11

        dismissStatus();
      });

    function dismissStatus() {
		// AirNowDrupal # 112 Multiple Changes cw 2019-04-10
		$(".status-message-container .status-message-dismiss").on("click.dismissStatus", function() {
            $(".status-message-container").addClass("hidden");
			// AirnowDrupal # 132 Dismissed alert creates a non-presistant cookie Save cw 2019-05-29
			$(document).ready(function() {
				cookieValue = escape("1") + ";";
				document.cookie = "statusMessageDismiss=" + cookieValue;
				});
        });

        $(".bb-mobile-status-bar .status-message-dismiss").on("click.dismissStatus", function() {
          $(".bb-mobile-status-bar").removeClass("visible-xs").addClass("hidden");
		  // AirnowDrupal # 132 Dismissed alert creates a non-presistant cookie Save cw 2019-05-29
		  $(document).ready(function() {
		  		cookieValue = escape("1") + ";";
				document.cookie = "statusMessageDismiss=" + cookieValue;
				});
        });
      }

      function getDegree(aqi) {
        let deg;
        // AQI values 0 - 200 represent the first 4/6 of the dial
        if (aqi <= 200) {
          deg = (aqi / 200) * (MAX_ROTATION_DEGREES * (4/6));
        }
        // AQI values 201 - 300 represent the second to last 1/6 of the dial
        else if (aqi <= 300) {
          deg = (MAX_ROTATION_DEGREES * (4/6)) + ((((aqi-200) / (300-200))) * (MAX_ROTATION_DEGREES * (1/6)))
        }
        // AQI values 301 - 500 represent the last 1/6 of the dial
        else if (aqi <= 500) {
          deg = (MAX_ROTATION_DEGREES * (5/6)) + ((((aqi-300) / (500-300))) * (MAX_ROTATION_DEGREES * (1/6)))
        }
        // AQI values above 400 should just be treated as the maximum rotation
        else {
          deg = MAX_ROTATION_DEGREES;
        }
        return deg;
      }

      function toggleNoDataDisplay(noData) {
        $(".mobile-city").toggleClass("noData", noData);
        $(".bb-info-holder").toggleClass("noData", noData);
        if (noData) {
          $(".bb-info-holder .curr-cond-label a").html("Get Current and Forecast Air Quality for Your Area");
        } else {
          $(".bb-info-holder .curr-cond-label a").html("Current Conditions");
        }
        $(".bb-info-holder .aqi-container").toggleClass("hidden", false);
        $(".bb-info-holder #nav-aqi-tool").toggleClass("hidden", false);
      }

      // Rotates the arrow to the provided degrees.  Degree values capped at 0 and 180
      function rotateArrow(deg) {
        // Ensure we do not rotate too far in either direction
        deg = Math.max(MIN_ROTATION_DEGREES, Math.min(deg, MAX_ROTATION_DEGREES));
        // Apply the rotation
        let arrows = document.getElementsByClassName("aq-dial-arrow");
        for (let i = 0; i < arrows.length; i++) {
          let arrow = arrows[i];
          arrow.style.webkitTransform = "rotate("+deg+"deg)";
          arrow.style.mozTransform = "rotate("+deg+"deg)";
          arrow.style.msTransform = "rotate("+deg+"deg)";
          arrow.style.oTransform = "rotate("+deg+"deg)";
          arrow.style.transform = "rotate("+deg+"deg)";
        }
      }

      $('.band-back-to-top').on("click.backToTop", function(){
        $("html, body").animate({ scrollTop: 0 }, 500);
        return false;
      });


      // Search Button Click Events
      $(document).once("closeSearchBtnEnableDoc").on("click.searchBtnClose", function(){
        handleSearchDropDown(false);
      });

      $('.dropdown.dropdown-search').find('.dropdown-content').on('click', function(event){
        event.stopPropagation();
      });

      addDropdownButtonListener();
      addAQIDropdownButtonListener();
      // addAQINavScroll();

      // Mobile dropdown click event
      $(".mobile-dropdown").on("click", function(event) {
        if($("#master-navbar").hasClass("mobile-nav")) {
          $("#master-navbar").removeClass("mobile-nav");
        } else {
          $("#master-navbar").addClass("mobile-nav");
        }
      });

      function populateData() {
        let currentAQData = ReportingArea.getMaxCurrentReportingAreaData();
        // let forecastAQDataToday = ReportingArea.getMaxForecastReportingAreaData(0);
        // let forecastAQDataTomorrow = ReportingArea.getMaxForecastReportingAreaData(1);
        let locationDisplayName = GeoLocation.getLocationDisplayName();

        let hasData = currentAQData || locationDisplayName;

        toggleNoDataDisplay(!hasData);

        if (hasData) {
          let category = currentAQData[ReportingArea.FIELDS.category];
          let aqiStatusClass = "default";
          let allClasses = "default good moderate unhealthy-sensitive unhealthy very-unhealthy hazardous";

          if (category === "Good") {
            aqiStatusClass = "good"; // green, good
          } else if (category === "Moderate") {
            aqiStatusClass = "moderate"; // yellow, moderate
          } else if (category === "Unhealthy for Sensitive Groups") {
            aqiStatusClass = "unhealthy-sensitive"; // orange, semi unhealthy
          } else if (category === "Unhealthy") {
            aqiStatusClass = "unhealthy"; // red, unhealthy
          } else if (category === "Very Unhealthy") {
            aqiStatusClass = "very-unhealthy"; // purple, very unhealthy
          } else if (category === "Hazardous") {
            aqiStatusClass = "hazardous"; // maroon, hazardous
          }

          $(".curr-cond-label a").text(locationDisplayName);

          $(".btn.btn-aqi-nav").removeClass(allClasses).addClass(aqiStatusClass);
        }
      }

      function populateDialData() {
        if($('.marquee').length > 0) {
          return;
        }

        // $('.marquee').css(
        //   { 'background': 'url('+themeImgDirectory+'default_marquee_img.jpg)',
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
            categoryImageType = "hazardous"; // hazardous

         // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
            /*if (aqi < 501) {
              categoryImageType = "hazardous"; // hazardous
            } else {
              categoryImageType = "beyond_index"; // beyond aqi
              category = "Beyond the AQI"; // Must be set for the pop-up rollover. Not in JSON data cw 2019-10-07
            } EEEBBB  */
          }

          $(".aq-dial .aq-dial-status").attr("src", "/themes/anblue/images/dial2/dial_" + categoryImageType + ".svg");

          // FIXME: Needs integration into new dial
          // Tooltips.createTip(".marquee-dial-col-holder .marquee-dial-status-tooltip-hotspot", "categories", "right", category, currentAQData[ReportingArea.FIELDS.parameter], null, 0);
          // Tooltips.createTip(".marquee-dial-col-holder #pp-data", "pollutant", "top", null, currentAQData[ReportingArea.FIELDS.parameter]);

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
          if (Number(hour) < 12) { // 12:00 AM - 11:59 AM
            if (Number(hour) === 0) {
              time = "12:" + minute + " AM";
            } else {
              time = "" + Number(hour) + ":" + minute + " AM";
            }
          } else { // 12:00 PM - 11:59 PM
            if (Number(hour) === 12) {
              time = rawTime + " PM";
            } else {
              time = "" + Number(hour - 12) + ":" + minute + " PM";
            }
          }
          let tz = currentAQData[ReportingArea.FIELDS.timezone];
          $(".aq-dial .aq-updated-time").html(time + " " + tz);

          $(".aq-dial .aq-dial-arrow").show();

          $(".aq-dial .aqi").text("NowCast AQI " + aqi);
          $(".aq-dial .pollutant").text(currentAQData[ReportingArea.FIELDS.parameter]);
          // FIXME: Currently not supported in new dial
          // if (currentAQData[ReportingArea.FIELDS.parameter] === "PM2.5"
          //   || currentAQData[ReportingArea.FIELDS.parameter] === "PM10") {
          //   $(".pp-label-text p").text("Particle Pollution");
          // } else {
          //   $(".pp-label-text p").text("");
          // }

          $(".location-label").text(locationDisplayName);
          $(".mobile-location-label").text(locationDisplayName);
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
          $(".aq-dial .aqi").text("NowCast AQI N/A");
          $(".aq-dial .pollutant").text("N/A");
          $(".aq-dial .aq-dial-status").attr("src", "/themes/anblue/images/dial2/dial_not_available.svg");

          $(".location-label").text(locationDisplayName);
          $(".mobile-location-label").text(locationDisplayName);
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
        $(".current-aq-label h4").text("Current Air Quality");
        $(".aq-forecast-label").text("Air Quality Forecast");

        // setMarqueeForecastSections(forecastAQDataToday, ReportingArea, ".aq-day-current", "Today");
        // setMarqueeForecastSections(forecastAQDataTomorrow, ReportingArea, ".aq-day-next", "Tomorrow");

      }

    }
  };

  // function addAQINavScroll() {
  //   if($("#location-input").length > 0) {
  //     $(".aqi-nav-scroll").addClass("aqi-nav-scroll-hidden");
  //     $(document).on("scroll", function() {
  //         if($("#location-input").offset().top >= $("#bb-nav").offset().top) {
  //           $(".aqi-nav-scroll").addClass("aqi-nav-scroll-hidden");
  //           removeAQIDropdownButtonListener();
  //         } else {
  //           $(".aqi-nav-scroll").removeClass("aqi-nav-scroll-hidden");
  //           addAQIDropdownButtonListener();
  //         }
  //     });
  //   }
  // }

  function addAQIDropdownButtonListener() {
    $(".btn.btn-aqi-nav").once("aqiNavBtnEnable").on("click.aqiBtnOpen", function(event) {
      event.stopPropagation();
      handleAQIDropdownButton();
    });
  }
  //
  // function removeAQIDropdownButtonListener() {
  //   $(".btn.btn-aqi-nav").removeOnce("aqiNavBtnEnable").off("click.aqiBtnOpen");
  // }

  function handleAQIDropdownButton() {
    $(".aq-dial.status-bar").toggle();
    $(".btn-aqi-nav .aqi-nav-text").toggle();
    $(".btn-aqi-nav .fa.fa-times").toggle();
  }

  function addDropdownButtonListener() {
    $("#search-btn").once("searchBtnEnable").on("click.searchBtnOpen", function(event) {
      event.stopPropagation();
      handleSearchDropDown(true);
    });
  }

  function handleSearchDropDown(enabled) {
    let searchBtn = $("#search-btn");
    let dropdownSearch = $('.dropdown.dropdown-search').find('.dropdown-content');
    if(enabled) {
      dropdownSearch.css("display", "block");
      searchBtn.find(".fa-search").toggle(false);
      searchBtn.find(".fa-times").toggle(true);
      searchBtn.removeOnce("searchBtnEnable").off("click.searchBtnOpen");

      searchBtn.once("closeSearchBtnEnable").on("click.searchBtnClose", function(event){
        event.stopPropagation();
        handleSearchDropDown(false);
      });
    } else {
      dropdownSearch.css("display", "none");
      searchBtn.find(".fa-search").toggle(true);
      searchBtn.find(".fa-times").toggle(false);
      addDropdownButtonListener();
      searchBtn.removeOnce("closeSearchBtnEnable").off("click.searchBtnClose");
    }
  }

  // Set jQuery events for the navigation tools
  function bindNavToolEvents() {
    let navTools = $(".nav-left-side-toolbar .nav-tool");
    let navToolPopups = $(".nav-left-side-toolbar .nav-tool-popup");
    let navToolPopupArrows = navTools.find(".nav-tool-popup-arrow");
    let navToolPopupDismisses = navToolPopups.find(".popup-dismiss");

    // Toggle Tool Popups
    navTools.click(function() {
      let $this = $(this);
      // If we are on narrow screens, move to new
      if ($(document).width() <= 510) {
        window.location = $this.next().find(".view-all-link a").attr('href');
      }
      let thisNavToolPopup = $this.next();
      let thisNavToolPopupArrow = $this.find(".nav-tool-popup-arrow");
      navTools.not($this).removeClass('active');
      $this.toggleClass('active');
      navToolPopups.not(thisNavToolPopup).hide();
      navToolPopupArrows.not(thisNavToolPopupArrow).hide();
      thisNavToolPopupArrow.toggle();
      thisNavToolPopup.toggle();
    });

    // Dismiss Tool Popup
    navToolPopupDismisses.click(function() {
      let $this = $(this);
      let thisNavToolPopup = $this.parent();
      let thisNavTool = thisNavToolPopup.prev();
      let thisNavToolPopupArrow = thisNavTool.find(".nav-tool-popup-arrow");
      thisNavToolPopup.hide();
      thisNavToolPopupArrow.hide();
      thisNavTool.removeClass('active');
    });

    // Close Tool Popup
    $(document).click(function(event) {
      $target = $(event.target);
      if(!$target.closest(navTools).length && !$target.closest(navToolPopups).length && navTools.is(":visible")) {
        navToolPopups.hide();
        navToolPopupArrows.hide();
        navTools.removeClass('active');
      }
    });
  }

  // This has code regarding anchor clicks. When clicks are done, they will smoothly scroll to the anchor and
  // account for the height offset of the navigation bar
  function smoothScrollingAnchors() {

    let $htmlbody = $('html, body');
    let smoothScroll = function(event) {
      let hash;
      if(event) {
        event.preventDefault();
        hash = $.attr(this, 'href');
      } else {
        hash = location.hash;
      }

      let navOffset = $("#master-navbar").height() - 1;
      $htmlbody.animate({
        scrollTop: ($(hash).offset().top - navOffset)
      }, 500);
    };

    $(document).on('click.smoothAnchors', 'a[href^="#"]', smoothScroll);

    //  This is the smooth scroll to an anchor in the url (if that exists)
    // $('html, body').hide();
    if(location.hash) {
      setTimeout(function () {
        $('html, body').scrollTop(0).show();
        smoothScroll();
      }, 0);
    } else {
      // $('html, body').show();
    }
  }

  // AIR-451 Fire & Notice State-level Notifications cw 2021-06-11
  // Fire & Notice Notifications JavaScript cw 2021-06-10
  function checkNotifications() {
    // hide possible old State Notifications
    if (document.getElementById("nav-center-toolbar").style.display == "block") {
      document.getElementById("nav-center-toolbar").style.display = "none";
      document.getElementById("fire-smoke-map").style.display = "none";
      document.getElementById("mobile-fire-smoke-map").style.display = "none";
    }
    // set-up Current state value cw 2021-08-04
    let queryString = window.location.search;
    let urlParams = new URLSearchParams(queryString);
    //let currentState = AirNowGov.GeoLocation.getStateCode();alert(currentState);
    let currentState = urlParams.get('state');
    // Read /stateNotifications.json for the data
    var jqxhr = $.getJSON( "/stateNotifications.json", function(json) { //AIR-466 Always read the JSON from the top-level directory cw 2021-08-04
      })
      .fail(function() {
      console.log( "There has been an error reading the stateNotifications.json file." );
      })
      .done(function(json) {
        if (urlParams.has('state') || urlParams.has('test') ) {
          // AIR-451 Testing URLs cw 2021-06-17
          if (urlParams.has('test') & urlParams.get('test') == 'TestFireMode') { currentState = "TF"; };
          if (urlParams.has('test') & urlParams.get('test') == 'TestNoticeMode') { currentState = "TE"; };
          if (urlParams.has('test') & urlParams.get('test') == 'TestGeneralMode') { currentState = "TG"; };
      $.each( json, function( key, value ) {
          // IF the stateNotifications.json includes the current state then process it
          if ( value.state == currentState) {
            // default when there's any Notification
            document.getElementById("nav-right-side-toolbar").style.top = "0px";
            // Change the Notification button; Branch on Notification for words and background color
            if (value.notification.type == "Wildfires") {
              // Fire Notification
              document.getElementById("state-notification").style.background = "darkred";
              document.getElementById("state-notification").style.color = "white";
              // Lat & Long for Fire & Smoke Map button
              let userLatitude = AirNowGov.GeoLocation.getLatLng().lat;
              let userLongitude = AirNowGov.GeoLocation.getLatLng().lng;
              document.getElementById("nav-right-side-toolbar").style.position = "relative";
              if (screen.width < 770) { 	// mobile size
                // for ONLY a Mobile sized site we need to move the "nav-right-side-toolbar" UP
                if (screen.width > 320) { 	// mobile size
                  document.getElementById("nav-right-side-toolbar").style.top = "-30px";
                } else { // iPhone 5 size
                  document.getElementById("nav-right-side-toolbar").style.top = "-44px";
                }
                document.getElementById("state-notification").text = currentState+" "+value.notification.type;
                document.getElementById("mobile-fire-smoke-map").style.display = "inline";
                document.getElementById("mobile-fire-smoke-map").href = "https://fire.airnow.gov/?lat="+userLatitude+"&lng="+userLongitude+"&zoom=8";
              } else { 					// web size
                document.getElementById("nav-right-side-toolbar").style.top = "-30px";
                document.getElementById("state-notification").text = value.notification.type+" in "+currentState;
                document.getElementById("fire-smoke-map").style.display = "inline";
                document.getElementById("fire-smoke-map").href = "https://fire.airnow.gov/?lat="+userLatitude+"&lng="+userLongitude+"&zoom=8";
              }
            } else {
              // Notice Notification words and background color
              document.getElementById("state-notification").style.background = "darkred"; // blue = #167fac   orange = #ff7e00 cw 2022-12-05
              document.getElementById("state-notification").style.color = "white";
              document.getElementById("nav-right-side-toolbar").style.position = "relative";
              if (screen.width < 770) { 	// mobile size
                // for ONLY a Mobile sized site we need to move the "nav-right-side-toolbar" UP
                if (screen.width > 320) { 	// mobile size
                  document.getElementById("nav-right-side-toolbar").style.top = "-30px";
                } else { // iPhone 5 size
                  document.getElementById("nav-right-side-toolbar").style.top = "-44px";
                }
                document.getElementById("state-notification").text = currentState+" "+value.notification.type;
                document.getElementById("mobile-fire-smoke-map").style.display = "none"; // No Fire & Smoke Map button
              } else { 					// web size
                document.getElementById("nav-right-side-toolbar").style.top = "-30px";
                document.getElementById("state-notification").text = value.notification.type+" for "+currentState;
                document.getElementById("fire-smoke-map").style.display = "none"; // No Fire & Smoke Map button
              }
            }

            // Display the notification button
            //AirNowGov.Tooltips.createTip(".nav-center-toolbar", "stateNotification", "bottom");
            document.getElementById("nav-right-side-toolbar").style.display = "inline";
            if (screen.width < 770) { 	// mobile size
              //alert(screen.width);
              document.getElementById("nav-right-side-toolbar").style.display = "none"; //AIR-464 Hide nav input field on mobile cw 2021-08-03
            }
            document.getElementById("nav-center-toolbar").style.display = "block";
            document.getElementById("state-notification").style.position = "fixed";
            document.getElementById("state-notification").style.zIndex = "10";
            document.getElementById("nav-geosearch-tool").style.zIndex = "0"; //AIR-464 Behind the State Notification Button cw 2021-08-03
            document.getElementById("nav-geosearch-tool").disabled = "true"; //AIR-464 Behind the State Notification Button cw 2021-08-03
            document.getElementById("nav-geosearch-tool").style.display = "none"; //AIR-464 Behind the State Notification Button cw 2021-08-03

            // Link to the Alert box in stateNotifications.json
            thisAlertNode = value.notification.alertnode;
            if (thisAlertNode > 0 ) { // Non-zero alertnodes will open the Alert list
              $("#state-notification").on("click", function(e) {
                // Display the Alerts via ccs changes cw 2021-08-02
                if (screen.width < 770) { 	// mobile size
                  document.getElementById("nav-right-side-toolbar").style.display = "none"; //AIR-464 Hide it on mobile cw 2021-08-03
                  // for ONLY a Mobile sized site redirect to the "alerts" page
                  window.location.assign("/alerts/");


                } else { 					// web size
                    $("#nav-alerts-popup-arrow").addClass("active");
                    document.getElementById("nav-alerts-popup-arrow").style.display = "block";
                    $("#nav-alerts-popup").addClass("active");
                    document.getElementById("nav-alerts-popup").style.display = "block";
                    // Loop to find the alert for this State Notification
                    var i;
                    for (i = 0; i < document.getElementsByClassName("alert-container").length; i++) {
                      var thisAlert = document.getElementsByClassName("alert-container")[i].innerHTML;
                      // Clear any other previuos hightlighting
                      document.getElementsByClassName("alert-container")[i].style.background ="#fff";
                      if (thisAlert.indexOf(thisAlertNode) > 0) {
                        // Hightlight this element
                        document.getElementsByClassName("alert-container")[i].style.background = "#e3e3e3"; //"superlightgray"
                        }
                      }
                 }
                  // Stop processing the click event; navbar has an event to "hide" the Alerts
                  e.stopPropagation();
                  e.stopImmediatePropagation();
                  });
                }
              if (thisAlertNode == 0 ) { // Zero alertnodes will open an Alert dialog box
                $("#state-notification").on("click", function(e) {
                  thisAlertText = value.notification.alerttext;
                  // Alert box using Text in the alerttext field of stateNotifications.json
                  if (thisAlertText.length > 0 ) { // If there is alert text, then display it
                    alert(thisAlertText);
                    }
                    // Stop processing the click event; navbar has an event to "hide" the Alerts
                    e.stopPropagation();
                    e.stopImmediatePropagation();
                  });
                }
            };
        });
          };
      });
  };

})(jQuery, Drupal);
