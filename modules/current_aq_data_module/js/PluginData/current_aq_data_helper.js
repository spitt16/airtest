(function ($, Drupal) {
  Drupal.behaviors.currentAQDataHelper = {
    attach: function (context, settings) {
      // console.log("Current AQ Data Helper (Original)");

      let PubSub = Drupal.behaviors.PubSub;
      let AirNowGov = Drupal.behaviors.AirNowGov;
      let ReportingArea = AirNowGov.ReportingArea;
      let GeoLocation = AirNowGov.GeoLocation;
      let Tippy = Drupal.behaviors.Tippy = window.Tippy;

      // let ol = Drupal.behaviors.ol;

      let primaryPollutantCardExpanded = true;

      // FIXME: this should be set via CMS, or at least in base.js
      const S3_BUCKET_URL = AirNowGov.API_URL + "andata";

      const ESRI_FEATURE_STYLE = {
        1: {color: 'rgb(0, 228, 0)', weight:0, fillOpacity:0.75},
        2: {color: 'rgb(255, 255, 0)', weight:0, fillOpacity:0.75},
        3: {color: 'rgb(255, 126, 0)', weight:0, fillOpacity:0.75},
        4: {color: 'rgb(255, 0, 0)', weight:0, fillOpacity:0.75},
        5: {color: 'rgb(143, 63, 151)', weight:0, fillOpacity:0.75},
        6: {color: 'rgb(126, 0, 35)', weight:0, fillOpacity:0.75}
      };

      const TIMEZONE_ABBRS = {
        "ADT": -3,
        "AST": -4,
        "EDT": -4,
        "EST": -5,
        "CDT": -5,
        "CST": -6,
        "MDT": -6,
        "MST": -7,
        "PDT": -7,
        "PST": -8
      };

      //let chart = false; // Bad!  But here just to ease of getting something displayed for conference
      //let chartSeriesData = [];
      //let chartReportingAreaName = "";
      //let chartReportingAreaState = "";
      //let chartLocationName = "";
      //let chartMode = "day"; // "day", "week", "month".  FIXME: make enum for this
      //let chartTimezoneLabel = "";
      let map = false; // Bad!  But here just to ease of getting something displayed for conference
      let extentBBox = [];
      let overlayLayer = false;
      let aqiDataTime = new Date();

      function toggleNoDataDisplay(noData) {
        $(".band-current-aq-row").closest(".band-style-general").toggleClass("noData", noData);
      }

      $(document).ready(function() {
      //  $("#chatButtonHolder #chartBtnDay").click(function() {
      //    if (chartMode !== "day") {
      //      chartMode = "day";
      //      setChartData(chartReportingAreaName, chartLocationName, chartReportingAreaState);
      //      if (settings.hasOwnProperty("currentBandChartFilterDescriptions")) {
      //        $("#chartBtnInfo").attr("title", settings["currentBandChartFilterDescriptions"]["day_description"]);
      //      }
      //      $("#chatButtonHolder button").removeClass("activeChartButton");
      //      $(this).addClass("activeChartButton");
      //    }
      //  });

      //  $("#chatButtonHolder #chartBtnWeek").click(function() {
      //    if (chartMode !== "week") {
      //      chartMode = "week";
      //      setChartData(chartReportingAreaName, chartLocationName, chartReportingAreaState);
      //      if (settings.hasOwnProperty("currentBandChartFilterDescriptions")) {
      //        $("#chartBtnInfo").attr("title", settings["currentBandChartFilterDescriptions"]["month_description"]); // FIXME: ChartFilterDescriptions.php mixes month/week up, fix that then adjust this
      //      }
      //      $("#chatButtonHolder button").removeClass("activeChartButton");
      //      $(this).addClass("activeChartButton");
      //    }
      //  });

      //  $("#chatButtonHolder #chartBtnMonth").click(function() {
      //    if (chartMode !== "month") {
      //      chartMode = "month";
      //      setChartData(chartReportingAreaName, chartLocationName, chartReportingAreaState);
      //      if (settings.hasOwnProperty("currentBandChartFilterDescriptions")) {
      //        $("#chartBtnInfo").attr("title", settings["currentBandChartFilterDescriptions"]["week_description"]); // FIXME: ChartFilterDescriptions.php mixes month/week up, fix that then adjust this
      //      }
      //      $("#chatButtonHolder button").removeClass("activeChartButton");
      //      $(this).addClass("activeChartButton");
      //    }
      //  });

        PubSub.subscribe(ReportingArea.TOPICS.new_data, function() {
          removePollutantCards();
          populateData();
        });

        //PubSub.subscribe(GeoLocation.TOPICS.new_location, function() {
        //  let locationName = GeoLocation.getLocationDisplayName();
        //  if (locationName && chart) {
        //    let chartTitle = locationName;
        //    if (chartMode === "day") {
        //      chartTitle += " (Today)";
        //    } else if (chartMode === "week") {
        //      chartTitle += " (This Week)";
        //   } else {
        //      chartTitle += " ("+moment().format("MMMM")+")";
        //    }
        //    chart.setTitle({text: chartTitle});
        //  }
        //});

        populateData();
        addMapIconTooltips();
        //addChartInfoIconTooltips();
        });

      function populateData() {
        let primaryData = ReportingArea.getMaxCurrentReportingAreaData();
        let latLng = GeoLocation.getLatLng();
        let locationName = GeoLocation.getLocationDisplayName();

        let hasData = primaryData || latLng,
            hasAvailableData = primaryData;

        toggleNoDataDisplay(!hasData);

        if (hasData) {
          generateOLMap();
          // generateHighchartsPlot();
          //chartTimezoneLabel = primaryData[ReportingArea.FIELDS.timezone];
          //createChart();
          let allReportingAreas = ReportingArea.getAllReportingAreaData();
          if (allReportingAreas && allReportingAreas.length) {
            //setChartData(allReportingAreas[0][ReportingArea.FIELDS.reportingAreaName], locationName, allReportingAreas[0][ReportingArea.FIELDS.stateCode]);
            setMapOverlay(allReportingAreas[0], [latLng.lng, latLng.lat]);
          } else {
            setMapOverlay(false, [latLng.lng, latLng.lat]);
            //chart.setTitle({text: "AQI Data Unavailable"});
            //chart.series[0].setData([]);
            //chart.xAxis[0].update({
            //  title: {
            //    text: ""
            //}
            //});
            //chart.redraw();
            $(".btn-current-chart").addClass("hidden");
          }

          createPollutantCard(
            $(".band-current-aq-row .primary-pollutant-card"),
            "current-aq-primary",
            "Primary Pollutant",
            "This pollutant currently has the highest AQI in the area.",
            [primaryData],
            true,
            hasAvailableData
          );

          let otherData = ReportingArea.getOtherCurrentReportingAreaData();
          createPollutantCard(
            $(".band-current-aq-row .other-pollutants-card"),
            "current-aq-primary",
            "Other Pollutants",
            null,
            otherData,
            false,
            hasAvailableData
          );

          // AIR-572 If this Reporting Area has an aqi, but is missing PM25, then check for nearby "high" PM25 cw 2022-12-14
          // first work with max; trival change cw 2023-02-07
          let getMaxCurrentReportingAreaData = ReportingArea.getMaxCurrentReportingAreaData();

          if (getMaxCurrentReportingAreaData[ReportingArea.FIELDS.parameter] === "PM2.5") {
            sessionStorage.setItem("AirNowGov.missingPm25Flag", "false");
          }

          // now look at others
          let getOtherCurrentReportingAreaData = ReportingArea.getOtherCurrentReportingAreaData();

          let currentData = ReportingArea.getOtherCurrentReportingAreaData();
          // loop the others
          for (let i = 0; i < currentData.length; i++) {
            let c = currentData[i];
            if (c[ReportingArea.FIELDS.parameter] === "PM2.5") {
              sessionStorage.setItem("AirNowGov.missingPm25Flag", "false");
              }

            }

          // Check Contour or Interpolated values for possible "high" PM value cw 2022-12-14
          let missingPm25Flag = sessionStorage.getItem("AirNowGov.missingPm25Flag");

          if (missingPm25Flag == "true") { // No PM25 for this Reporting Area
            // pull current values
            currentMaxAQI = getMaxCurrentReportingAreaData[ReportingArea.FIELDS.aqi];
            currentMaxCategory = getMaxCurrentReportingAreaData[ReportingArea.FIELDS.category];

            // Pull Contour or Interpolated values
            let reportingArea = getMaxCurrentReportingAreaData[ReportingArea.FIELDS.reportingAreaName];
            let stateCode =  getMaxCurrentReportingAreaData[ReportingArea.FIELDS.stateCode];
            $.ajax({
              type: "POST",
              url: AirNowGov.API_URL + "reportingarea/getinterpolatedPM25",
              data: {
                "reportingArea": reportingArea,
                "stateCode": stateCode
              },
              context: this,
              success: function (response) {
                // use the interploated values
                let interpolatedAqi_PM25 = response.interpolatedAqi_PM25;
                let interpolatedAqiCategory_PM25 = response.interpolatedAqiCategory_PM25;

                // interpolated CAN return undefined
                if (typeof interpolatedAqi_PM25 !== 'undefined' || typeof interpolatedAqiCategory_PM25 !== 'undefined') {

                  // convert aqi to category numbers cw 2022-12-14
                  function convertaqiToCatNum(aqiValue) {
                    if (aqiValue < 51) {
                      categoryValue = 1; // green, good
                    } else if (aqiValue >= 51 && aqiValue < 101) {
                      categoryValue = 2; // yellow, moderate
                    } else if (aqiValue >= 101 && aqiValue < 151) {
                      categoryValue = 3; // orange, semi unhealthy
                    } else if (aqiValue >= 151 && aqiValue < 201) {
                      categoryValue = 4; // red, unhealthy
                    } else if (aqiValue >= 201 && aqiValue < 301) {
                      categoryValue = 5; // purple, very unhealthy
                    } else if (aqiValue >= 301) {
                      categoryValue = 6; // maroon, hazardous

                    // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
                   /* } else if (aqiValue >= 501) {
                      categoryValue = 7; // Beyond the AQI added cw 2019-10-08*/
                    }
                    return (categoryValue);
                  }

                  // get Number values for the categories
                  currentAqiCatNum = convertaqiToCatNum(currentMaxAQI);
                  interpolatedAqiCatNum = convertaqiToCatNum(interpolatedAqi_PM25);

                  // ... IF contour PM2.5 is 1 category higher AND greater than 50 AQI higher, then report out ...
                  if (interpolatedAqiCatNum - currentAqiCatNum > 1 && interpolatedAqi_PM25 - currentMaxAQI > 50) {
                    // report out... needs to cover/replace the top of the dial
                    // AIR-572 Pop up message with close "X" cw 2023-01-20
                    var missingPM25Popup = document.getElementById("missingPM25Popup");
                    htmlMessage = "<div style=\'text-align: left;'>X</div><div>Current PM2.5 data is not available, but there are indications of elevated PM2.5 nearby.<br><br>Please consult the <a href=\'https://fire.airnow.gov\?lat="+latLng.lat+"&lng="+latLng.lng+"&zoom=8\' target=\'_new\'>Fire and Smoke Map<\/a><br> for nearby PM2.5 values.<div></div>";
                    document.getElementById("missingPM25Popup").innerHTML = htmlMessage;
                    // 2 second delay cw 2023-01-23
                    function popupDelayFunction() {
                      // code to run after the timeout
                      missingPM25Popup.classList.toggle("show");
                    }
                    // stop for sometime if needed
                    setTimeout(popupDelayFunction, 2000);
                  }
                }
              },
              error: function (response) {
                // AIR-572 No interpolated API data returned, so hide the pop up via CSS changes, if it is visible cw 2023-01-12
                document.getElementById("missingPM25Popup").className = "popuptext";
                console.error("No data found for this Reporting Area.");
              }
            });
          } // END missing PM25 flag part of AIR-572 cw 2023-01-12
          else {
            // AIR-572 Not missing PM25 data, so hide the pop up via CSS changes, if it is visible cw 2023-01-12
            document.getElementById("missingPM25Popup").className = "popuptext";
          }
        } else {
          // AIR-572 No data at all, so hide the pop up via CSS changes, if it is visible cw 2023-01-12
          document.getElementById("missingPM25Popup").className = "popuptext";
        }
      }

      function addMapIconTooltips() {
        let tippyContainer = $("#tippy_container");
        $(".map-icon").each(function(idx) {
          let trigger = "click";
		  let interactive = "false"; // AirNowDrupal#192 Fixing Pop-ups cw 2019-09-19 Arrr!
          if ($(".map-icon-" + idx + " img").attr("alt") === 'Map Info Icon') { // Originally there were other icons cw 2019-09-19
			// AirNowDrupal#124 cw 2019-04-16
            trigger = "click"; // Map Info Icon always click to close cw 2019-04-16
			interactive = "true";
          }
          let mapIconTooltipHtmlContainer = $("#map-icon-tooltip-html-" + idx);
          if (mapIconTooltipHtmlContainer.length) {
            let mapIconTooltipHtml = mapIconTooltipHtmlContainer.text();
            tippyContainer.html(mapIconTooltipHtml);
			// debug cw 2019-04-17
		    //console.log("map-icon-tooltip-html-" + idx+": trigger="+trigger+" & interactve="+interactive );
            Tippy(this, {
              html: "#tippy_container",
              theme: 'currentmapicon',
              placement: 'bottom', // AirNowDrupal#124 cw 2019-04-16
              animation: "shift-toward", // shift toward; scale
              trigger: trigger,
              size: 'large',
              interactive: interactive,  // AirNowDrupal#124 cw 2019-04-16
              interactiveBorder: 15,
              delay: [300, 100]
            });
          }
        });
      }

      //function addChartInfoIconTooltips() {
      //  let tippyContainer = $("#tippy_container");
      //  let chartIconTooltip = $("#chartBtnInfo")[0];
      //  let chartIconTooltipHtmlContainer = $("#chart-icon-tooltip-html");
      //  if (chartIconTooltipHtmlContainer.length) {
      //    let chartIconTooltipHtml = chartIconTooltipHtmlContainer.text();
      //    tippyContainer.html(chartIconTooltipHtml);
      //    Tippy(chartIconTooltip, {
      //      html: "#tippy_container",
      //      theme: 'currentcharticon',
      //      placement: 'bottom',
      //      animation: "shift-toward", // shift toward; scale
      //      trigger: 'focus click',
      //      size: 'large',
      //      dynamicTitle: true,
      //      interactive: true,
      //      interactiveBorder: 15,
      //      delay: [300, 100],
      //      distance: -5
      //    });
      //  }
        // FIXME: Not sure why the above did not work on its own, but the below line got the tooltip to display.  Tip is passed through the settings, can refactor to remove usage in twig file
        //$("#chartBtnInfo").attr("title", settings["currentBandChartFilterDescriptions"]["day_description"]);
      //		}

      function removePollutantCards() {
        $(".band-current-aq-row .primary-pollutant-card").find(".pollutants-list").empty();
        $(".band-current-aq-row .other-pollutants-card").find(".pollutants-list").empty();
		//$(".pollutant-card").removeClass("good moderate unhealthy-sensitive unhealthy very-unhealthy hazardous");
      }

      function createPollutantCard(pollutantCard, uniqueId, title, subtext, reportingareaData, isPrimary, hasAvailableData) {
        pollutantCard.find(".pollutant-title-section .pollutant-card-title").text(title);

        if(subtext != null) {
          pollutantCard.find(".pollutant-title-section .pollutant-card-title-subtext").text(subtext);
        }

        if(typeof reportingareaData == "undefined" || reportingareaData.length == 0 || !hasAvailableData) {
          let noPollutantDiv = $('<div/>', {
              'class': 'no-pollutant-info'
            }).append($('<p/>', {
              'text': 'No ' + title + ' Available'
            })),
            pollutantList = pollutantCard.find(".pollutants-list");

          pollutantCard.addClass("show-none-text");
          // pollutantCard.parent().addClass("hidden-xs");
          pollutantList.append(noPollutantDiv);
          // pollutantCard.removeClass("good moderate unhealthy-sensitive unhealthy very-unhealthy hazardous")
        } else {
          pollutantCard.removeClass("show-none-text");
          // pollutantCard.parent().removeClass("hidden-xs");
          for(let i in reportingareaData) {
            let reportingarea = reportingareaData[i];
            appendPollutantInfo(
              pollutantCard,
              uniqueId + "-" + i.toString(),
              reportingarea[ReportingArea.FIELDS.parameter],
              reportingarea[ReportingArea.FIELDS.category],
              reportingarea[ReportingArea.FIELDS.aqi],
              isPrimary
            );
          }
        }
      }

      function appendPollutantInfo(pollutantCard, id, parameter, category, aqi, isPrimary) {
        let pollutantList = pollutantCard.find(".pollutants-list");
        pollutantList.append(constructPollutantInfo(id, parameter, category, aqi, isPrimary));

        let currentPollutant = pollutantList.find("#" + id);
        currentPollutant.find(".pollutant-info-heading").click(function(event) {
          let currentPollutantSub = currentPollutant.find(".pollutant-info-sub");

          if(currentPollutantSub.hasClass("pollutant-info-sub-hide")) {
            currentPollutant.find(".pollutant-info-sub").removeClass("pollutant-info-sub-hide");
            primaryPollutantCardExpanded = true;
          } else {
            currentPollutant.find(".pollutant-info-sub").addClass("pollutant-info-sub-hide");
            primaryPollutantCardExpanded = false;
          }
          // Toggle arrow direction based on if Plan Your Day is collapsed or not
          currentPollutant.find("i")
            .toggleClass("fa-caret-right", !primaryPollutantCardExpanded)
            .toggleClass("fa-caret-down", primaryPollutantCardExpanded);
        });
      }

      function constructPollutantInfo(id, parameter, category, aqi, isPrimary) {
        // FIXME: this is just a rough example, CSS should define classes for this that are based off the category names, and not the AQI values
        let aqiTextColor = "white";
        let aqiBackgroundColor = "#5E5E5E";
        let aqiCategoryMessageKey = "not_available";
        let aqiStatusClass = "default";
        let additionalPiClass = "";

        if (category === "Good") {
          aqiStatusClass = "good"; // green, good
          aqiCategoryMessageKey = "good";
        } else if (category === "Moderate") {
          aqiStatusClass = "moderate"; // yellow, moderate
          aqiCategoryMessageKey = "moderate";
        } else if (category === "Unhealthy for Sensitive Groups") {
          aqiStatusClass = "unhealthy-sensitive"; // orange, semi unhealthy
          aqiCategoryMessageKey = "sensitive_unhealthy";
          additionalPiClass = 'unhealthy-sensitive-adj';
        } else if (category === "Unhealthy") {
          aqiStatusClass = "unhealthy"; // red, unhealthy
          aqiCategoryMessageKey = "unhealthy";
        } else if (category === "Very Unhealthy") {
          aqiStatusClass = "very-unhealthy"; // purple, very unhealthy
          aqiCategoryMessageKey = "very_unhealthy";
        } else if (category === "Hazardous") {
          aqiStatusClass = "hazardous"; // maroon, hazardous
            aqiCategoryMessageKey = "hazardous";
        }
        
        // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
		  /*if (aqi < 501) {
		    aqiStatusClass = "hazardous"; // maroon, hazardous
            aqiCategoryMessageKey = "hazardous";
			//category = "Hazardous"; // cw 2019-10-10
		 /* } else {
            aqiStatusClass = "hazardous";
            aqiCategoryMessageKey = "beyond_aqi"; // Added Beyond AQI cw 2019-10-10
			category = "Beyond the AQI"; // cw 2019-10-10
          }*/
		

        if (isPrimary === true) {
          $(".current-aq-band-row").find(".pollutant-card.primary-pollutant-card")
            .toggleClass("good", category === "Good")
            .toggleClass("moderate", category === "Moderate")
            .toggleClass("unhealthy-sensitive", category === "Unhealthy for Sensitive Groups")
            .toggleClass("unhealthy", category === "Unhealthy")
            .toggleClass("very-unhealthy", category === "Very Unhealthy")
            .toggleClass("hazardous", category === "Hazardous"          // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
            /*|| category === "Beyond the AQI"*/);  // Added Beyond Index; Getting correct "toggle" for Primary Pollutant in Current Air Quality cw 2019-10-10
        }

        let extendedMessage;
        if (parameter && settings.planYourDayDescriptions.hasOwnProperty(parameter.toLowerCase())) {
          if (settings.planYourDayDescriptions[parameter.toLowerCase()].hasOwnProperty(aqiCategoryMessageKey)) {
            extendedMessage = settings.planYourDayDescriptions[parameter.toLowerCase()][aqiCategoryMessageKey].current;
          } else {
            extendedMessage = settings.planYourDayDescriptions.default[aqiCategoryMessageKey].current;
          }
        } else {
          extendedMessage = settings.planYourDayDescriptions.default[aqiCategoryMessageKey].current;
        }

        let hideClass = "pollutant-info-sub-hide";
        if (isPrimary === true && primaryPollutantCardExpanded === true) {
          hideClass = "";
        }

        let pollutantInfoDiv = $('<div/>', {
            'class': 'row pollutant-info ' + additionalPiClass,
            'id': id
          }),
          pollutantInfoHeadingDiv = $('<div/>', {
            'class': 'col-xs-12 pollutant-info-heading'
          }),
          headingTitleDiv = $('<div/>', {
            'class': 'pi-heading-title col-xs-5'
          }),
          headingTitleCaret = $('<i/>', {
            'class': 'fa fa-caret-right',
            'aria-hidden': 'true'
          }),
          headingStatusDiv = $('<div/>', {
            // 'style': 'color: ' + aqiTextColor + '; background-color: ' + aqiBackgroundColor + '; border-radius: 50px;',
            'class': 'pi-heading-status col-xs-2 pollutant-status-circle ' + aqiStatusClass, // TODO: call it "-aqibubble" (or something like that) instead of "-status"
            'text': aqi,
            'title': "AQI " + aqi + " - " + category
          }),
          headingMessageDiv = $('<div/>', {
            'class': 'pi-heading-message col-xs-5', // TODO: call it "-category" instead of "-message"
            'text': category
          }),
          // Line and Steps to take label
		  //pollutantInfoSubDiv = $('<div/>', {
          //  'class': 'col-xs-12 pollutant-info-sub ' + hideClass
          //}).append("<h4><b>Steps to Take</b></h4>" + extendedMessage);

		  // AirNowDrupal # 106 Line and Steps to Take label removed cw 2019-02-26
		  pollutantInfoSubDiv = $('<div/>', {
            'class': 'col-xs-12 pollutant-info-sub ' + hideClass
          }).append(extendedMessage);

        if (isPrimary === true && primaryPollutantCardExpanded === true) {
          // Toggle arrow direction based on if Plan Your Day is collapsed or not
          headingTitleCaret
            .toggleClass("fa-caret-right", !primaryPollutantCardExpanded)
            .toggleClass("fa-caret-down", primaryPollutantCardExpanded);
        }


        headingTitleDiv
          .append(headingTitleCaret)
          .append(parameter);

        pollutantInfoHeadingDiv
          .append(headingTitleDiv)
          .append(headingStatusDiv)
          .append(headingMessageDiv);

        pollutantInfoDiv
          .append(pollutantInfoHeadingDiv)
          .append(pollutantInfoSubDiv);

        return pollutantInfoDiv;
      }

      function generateOLMap() {
        if (map) {
          return;
        }
        let latLng = GeoLocation.getLatLng();
        map = L.map('map', {attributionControl: false, zoomControl: false}).setView([latLng.lat, latLng.lng], 6);
        L.esri.basemapLayer('Imagery').addTo(map);
        L.esri.basemapLayer('ImageryLabels').addTo(map);
        map.dragging.disable();
        map.touchZoom.disable();
        map.doubleClickZoom.disable();
        map.scrollWheelZoom.disable();
        map.boxZoom.disable();
        map.keyboard.disable();
        if (map.tap) map.tap.disable();
        document.getElementById('map').style.cursor='default';
        L.esri.featureLayer({
          url: 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/AirNowLatestContoursCombined/FeatureServer/0',
          simplifyFactor: 0.5,
          precision: 5,
          style: function (feature) {
            return ESRI_FEATURE_STYLE[feature.properties.gridcode];
          }
        }).addTo(map);
      }

      function findTimezoneAbbr(currentTZOffset) {
        let isDST = moment().isDST();
        for (let tzAbbr in TIMEZONE_ABBRS) {
          let tzOffset = TIMEZONE_ABBRS[tzAbbr];
          if (tzOffset === currentTZOffset) {
            if (isDST && tzAbbr[1] === "D" || !isDST && tzAbbr[1] === "S") {
              return tzAbbr;
            }
          }
        }
        return false;
      }


      function setMapOverlay(reportingAreaData, mapCenterLatLng) {
        if (!map) {
          return;
        }

        // Fixes a race condition issue with map.setView by only proceeding once moveend event has triggered.
        //   NOTE: this will cause issues if we ever let the user manually pan the map.
        map.once("moveend", function() {
          let tz = reportingAreaData ? reportingAreaData[ReportingArea.FIELDS.timezone] : false;
          let tzOffset = tz ? TIMEZONE_ABBRS[tz] : false;
          let mapDiv = $("#map");
          let mapOverlay = $("#map-overlay");
          //let extentBBox = map.getView().calculateExtent(map.getSize());

          // AirNowDrupal#375 Monitor Near Me "closer" cw 2020-11-18
          //map.setView(mapCenterLatLng, 9); // Zooms in Leaflet Map AND Monitors Near Me URL
          //console.log("map.getBounds().getSouthWest(): " +map.getBounds().getSouthWest());
          // Pads the map area bounds as a PERCENTAGE where 1 = 100%. To make it smaller you need to use a negative number that is between 0 and -0.5.
          // Padding by 0 would not change the size, padding by -0.5 would make it size 0.
          var newAreaBounds = map.getBounds().pad(-.45) // Zoom in a bunch
          // Now using "newAreaBounds" to apply the above padding
          //let bottomleft = L.Projection.SphericalMercator.project(map.getBounds().getSouthWest()); // old way
          //let topright = L.Projection.SphericalMercator.project(map.getBounds().getNorthEast()); // old way
          let bottomleft = L.Projection.SphericalMercator.project(newAreaBounds.getSouthWest());
          
          let topright = L.Projection.SphericalMercator.project(newAreaBounds.getNorthEast());
          extentBBox = [bottomleft.x, bottomleft.y, topright.x, topright.y];

          mapOverlay.hide();

          $(".air-quality-monitors-near-me").attr("href", AirNowGov.INTERACTIVE_MAP_URL + "?xmin=" + extentBBox[0] + "&ymin=" + extentBBox[1] + "&xmax=" + extentBBox[2] + "&ymax=" + extentBBox[3] + "&clayer=none&mlayer=ozonepm");

          // New button Event; new window for AirNowDrupal # 88 cw 2019-02-05
          $("#map").unbind("click");
          $("#map").on("click", function() {
            let win = window.open(AirNowGov.INTERACTIVE_MAP_URL + "?xmin=" + extentBBox[0] + "&ymin=" + extentBBox[1] + "&xmax=" + extentBBox[2] + "&ymax=" + extentBBox[3] + "&clayer=ozonepm&mlayer=none", "_blank");
            win.focus();
          });

          // Anchor tag changed to National Maps for AirNowDrupal #125 cw 2019-04-09
          $("#national-maps").off("click").on("click", function() {
            $(location).attr('href', "/national-maps");
          });

          let loadingHeader = $(".demo_text_overlay");
          loadingHeader.show();


          let featureServerInfoUrl = "https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/AirNow24HrCombined/FeatureServer/0/query?where=1%3D1&outFields=UNIXTIME,Timestamp&returnGeometry=false&orderByFields=Timestamp+DESC&resultRecordCount=1&f=json";

          $.ajax({
            url: featureServerInfoUrl,
            success: function(response) {
              // AIR-530 The Stringify method fixes bug that was breaking the timestamp on the Current Air Quality mini map. cw 2022-03-24
              var responseJSON = JSON.parse(JSON.stringify(response)); // AIR-530 Sucessful object built with updated JSON files ONLY cw 2022-03-24
              // AIR-530 Original Code: let responseJSON = JSON.parse(response);
              if (responseJSON["features"].length && responseJSON["features"][0]) {
                if (responseJSON["features"][0]["attributes"] && responseJSON["features"][0]["attributes"]["Timestamp"]) {
                  let timestamp = responseJSON["features"][0]["attributes"]["Timestamp"];
                  setMapTimestamp(timestamp, tz, tzOffset);
                }
              }
            }
          });

          function setMapTimestamp(timestamp, tz, tzOffset) {
            if (!tz && !tzOffset) {
              GeoLocation.getLatLngTimezone(function(responseTZOffset) {
                let responseTZAbbr = findTimezoneAbbr(responseTZOffset);
                if (!responseTZOffset || !responseTZAbbr) {
                  responseTZOffset = 0;
                  responseTZAbbr = "UTC";
                }
                let dateTime = moment(timestamp).utcOffset(responseTZOffset);
                $(".time_overlay").text("Updated " + dateTime.format("h:mm a ") + responseTZAbbr + ", " + dateTime.format("MMM D "));
              });
            } else {
              let dateTime = moment(timestamp).utcOffset(tzOffset);
              $(".time_overlay").text("Updated " + dateTime.format("h:mm a ") + tz + ", " + dateTime.format("MMM D "));
            }
          }
        });

        // map.getView().setCenter(ol.proj.transform(mapCenterLatLng, LAT_LNG_PROJECTION, ARCGIS_WORLD_TOPO_PROJECTION));
        map.setView(mapCenterLatLng.reverse(), 6);
      }

      function createChart() {
        if (chart) {
          return;
        }
        let chartId = "chart";

        chart = Highcharts.chart(chartId, {
          title: {
            text: "Loading...",
            margin: 50
          },
          xAxis: {
            type: 'datetime',
            title: {
              text: ""
            },
            align: "center",
            startOfWeek: 0,
            labels: {
              formatter: function () {
                let dateTime = moment(this.value);
                let format = dateTime.format("MMM Do");
                if (chartMode === "day") {
                  dateTime = dateTime.utcOffset(utcOffset);
                  format = dateTime.format("h A");
                }
                return format;
              }
            }
          },
          yAxis: {
            min: 0,
            softMax: 125,
            ceiling: 500,
            title: {
              text: "NowCast Air Quality Index (AQI)"
            },
            opposite: true,
            tickInterval: 50,
            minorTicks: true,
            minorTickInterval: 25
          },
          legend: {
            enabled: false
          },
          tooltip: {
            positioner: function () {
              return { x: 10, y: 80 };
            },
            formatter: function() {
              // const pointData = chartSeriesData.find(row => row.timestamp === this.point.x);

              let me = this;
              const pointData = chartSeriesData.find(function(row){
                 return row.timestamp === me.point.x;
                });

              let aqiValue = pointData.aqi;
              let categoryValue = "None";
              let pollutantValue = pointData.pollutant;
              let dateTime = moment(this.point.x);
              let dateTimeStr = dateTime.format("MMM Do, YYYY");
              if (chartMode === "day") {
                let utcOffset = pointData.utcOffset;
                dateTime = dateTime.utcOffset(utcOffset);
                dateTimeStr += " " + dateTime.format("hA");
              }

              if (pollutantValue === "O3") {
                pollutantValue = "Ozone";
              } else if (pollutantValue === "PM2.5 - Principal") {
                pollutantValue = "PM2.5";
              } else if (pollutantValue === "PM10 - Principal") {
                pollutantValue = "PM10";
              }

              if (aqiValue < 51) {
                categoryValue = "Good"; // green, good
              } else if (aqiValue >= 51 && aqiValue < 101) {
                categoryValue = "Moderate"; // yellow, moderate
              } else if (aqiValue >= 101 && aqiValue < 151) {
                categoryValue = "Unhealthy for Sensitive Groups"; // orange, semi unhealthy
              } else if (aqiValue >= 151 && aqiValue < 201) {
                categoryValue = "Unhealthy"; // red, unhealthy
              } else if (aqiValue >= 201 && aqiValue < 301) {
                categoryValue = "Very Unhealthy"; // purple, very unhealthy
              } else if (aqiValue >= 301 && aqiValue < 501) {
                categoryValue = "Hazardous"; // maroon, hazardous
              }
                       
              // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
              /*} else if (aqiValue >= 501) {
                categoryValue = "Beyond the AQI"; // Beyond the AQI added cw 2019-10-08
              }*/

              let dateTimeLine = "<h2>" + dateTimeStr + "</h2><br/><br/>";
              let aqiLine = (chartMode === "day") ? "<b>NowCast AQI: </b>" + aqiValue + "<br/>" : "<b>AQI: </b>" + aqiValue + "<br/>";
              let pollutantLine = "<b>Pollutant: </b><span class='highchart-tooltip-pollutant-text'>" + pollutantValue + "</span><br/>";
              let categoryLine = "<b>Category: </b><span class='highchart-tooltip-category-text'>" + categoryValue + "</span><br/>";

              return dateTimeLine + aqiLine + pollutantLine + categoryLine;
            }
          },
          series: [{
            name: "AQI",
            type: "column",
            data: [],
            borderColor: "#000000",
            borderWidth: 1,
            zones: [{
              value: 51,
              className: "zone-good",
              color: "#00E400"
            }, {
              value: 101,
              className: "zone-moderate",
              color: "#FFFF00"
            }, {
              value: 151,
              className: "zone-unhealthy-sensitive",
              color: "#FF7E00"
            }, {
              value: 201,
              className: "zone-unhealthy",
              color: "#FF0000"
            }, {
              value: 301,
              className: "zone-very-unhealthy",
              color: "#8F3E96"
            }, {
              className: "zone-hazardous",
              color: "#7E0023"
            }],
            pointIntervalUnit: 'hour'
          }],
          lang: {
            noData: 'No Data'
          },
          credits: {
            enabled: false
          },
          exporting: {
            csv: {
              columnHeaderFormatter: function (item, key) {
                if (!item || item instanceof Highcharts.Axis) {
                  return "UTC";
                }
                // Item is not axis, now we are working with series.
                // Key is the property on the series we show in this column.
                return item.name;
              }
            },
            buttons: {
              contextButton: {
                menuItems: [
                  "printChart",
                  "separator",
                  "downloadPNG",
                  "downloadJPEG",
                  "downloadPDF",
                  "downloadSVG",
                  "separator",
                  "downloadCSV"
                ]
              }
            }
          }
        });
      }

      function setChartData(reportingAreaName, location, stateCode) {
        if(typeof reportingAreaName != "undefined") {
          chartReportingAreaName = reportingAreaName;
          chartReportingAreaState = stateCode;
          chartLocationName = location;

          function createUrl(jsonFileName) {
            let url = S3_BUCKET_URL + "/ReportingAreas/" + jsonFileName.split(" ").join("_");
            if (chartMode === "week" || chartMode === "month") {
              url += "_MONTH";
            }
            url += ".json";
            return url;
          }

          let url = createUrl(typeof stateCode !== "undefined" ? reportingAreaName + "_" + stateCode : reportingAreaName + "_NA");
          let urlFallback1 = typeof stateCode !== "undefined" ? createUrl(reportingAreaName + "_NA") : false;
          let urlFallback2 = createUrl(reportingAreaName);

          function getJsonData(jsonUrl) {
            $.ajax({
              url: jsonUrl,
              success: function(response) {
                let s3_data = JSON.parse(response);
                //parseChartS3Data(s3_data, location);
                // chart.series[0].setData(chartSeriesData.map(row => [row.timestamp, row.aqi]));
                //chart.series[0].setData(chartSeriesData.map(function(row) {
                //  return [row.timestamp, row.aqi];
                //}));
                //chart.redraw();
                $(".btn-current-chart").removeClass("hidden");
              },
              error: function(response) {
                if (urlFallback1 && jsonUrl === url) {
                  getJsonData(urlFallback1);
                  return;
                } else if ((urlFallback1 && jsonUrl === urlFallback1) || (!urlFallback1 && jsonUrl === url)) {
                  getJsonData(urlFallback2);
                  return;
                }
                //chart.setTitle({text: "AQI Data Unavailable"});
                //chart.series[0].setData([]);
                //chart.redraw();
                //$(".btn-current-chart").addClass("hidden");
              }
            });
          }
          getJsonData(url);
        } else {
          //chart.setTitle({text: "AQI Data Unavailable"});
          //chart.series[0].setData([]);
          //chart.redraw();
          //$(".btn-current-chart").addClass("hidden");
        }

      }

      function parseChartS3Data(s3_data, location) {
        let aqiData = s3_data.aqi;
        let pollutantData = s3_data.param;
        let utcOffset = s3_data.utcOffset;
        let endTimeUTC = s3_data.endTimeUTC;

        let delta = chartMode === "day" ? "hours" : "days";
        let xAxisLabel = chartMode === "day" ? chartTimezoneLabel : "";
        let yAxisLabel = chartMode === "day" ? "NowCast Air Quality Index (AQI)" : "Air Quality Index (AQI)";
        let chartTitle = location;

        chartSeriesData = [];

        let dataTime = moment().minutes(0).seconds(0).milliseconds(0);
        if (chartMode !== "day") {
          dataTime = dataTime.subtract(1, "days");
        } else {
          dataTime = moment(endTimeUTC + " +0000", "YYYY-MM-DD HH:mm:SS ZZ").utcOffset(utcOffset).add(1, "hours").minutes(0).seconds(0).milliseconds(0);
        }

        let minDataTime;
        if (chartMode === "day") {
          minDataTime = dataTime.clone().startOf("day").subtract(1, "hours");
        } else if (chartMode === "week") {
          minDataTime = dataTime.clone().subtract(7, "days");
        } else {
          minDataTime = dataTime.clone().subtract(30, "days");
        }

        for (let i = aqiData.length - 1; i >= 0 && dataTime.isAfter(minDataTime); i--) {
          let aqi = aqiData[i];
          let pollutant = pollutantData[i];

          chartSeriesData.push({
            timestamp: dataTime.valueOf(),
            utcOffset: utcOffset,
            aqi: i >= 0 ? aqiData[i] : 0, // if we need more data than we have AQI values, set the missing ones to 0
            pollutant: i >= 0 ? pollutantData[i] : "N/A", // if we need more data than we have pollutant values, set the missing ones to "N/A"
          });

          dataTime = dataTime.subtract(1, delta);
        }

        chartSeriesData = chartSeriesData.reverse();

        chart.setTitle({text: chartTitle});
        chart.xAxis[0].update({
          title: {
            text: xAxisLabel
          },
          labels: {
            formatter: function () {
              let dateTime = moment(this.value);
              let format = dateTime.format("MMM Do");
              if (chartMode === "day") {
                dateTime = dateTime.utcOffset(utcOffset);
                format = dateTime.format("h A");
              }
              return format;
            }
          }
        });
        chart.yAxis[0].update({
          title: {
            text: yAxisLabel
          },
        });
      }
    }
  };

})(jQuery, Drupal);
