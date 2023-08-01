(function ($, Drupal) {
  Drupal.behaviors.statePageHelper = {
    attach: function (context, settings) {

      let PubSub = Drupal.behaviors.PubSub;
      let AirNowGov = Drupal.behaviors.AirNowGov;
      let ReportingArea = AirNowGov.ReportingArea;
      let GeoLocation = AirNowGov.GeoLocation;
      let Tooltips = AirNowGov.Tooltips;
      // let ol = Drupal.behaviors.ol;

      let datePicker = false;
      let stateName = AirNowGov.GLOBALS.getUrlVar("name");
      let states = [
        'Alabama',
        'Alaska',
        'Arizona',
        'Arkansas',
        'California',
        'Colorado',
        'Connecticut',
        'Delaware',
        'District Of Columbia',
        'Florida',
        'Georgia',
        'Hawaii',
        'Idaho',
        'Illinois',
        'Indiana',
        'Iowa',
        'Kansas',
        'Kentucky',
        'Louisiana',
        'Maine',
        'Maryland',
        'Massachusetts',
        'Mexico',
        'Michigan',
        'Minnesota',
        'Mississippi',
        'Missouri',
        'Montana',
        'Nebraska',
        'Nevada',
        'New Hampshire',
        'New Jersey',
        'New Mexico',
        'New York',
        'North Carolina',
        'North Dakota',
        'Ohio',
        'Oklahoma',
        'Oregon',
        'Pennsylvania',
        'Puerto Rico',
        'Rhode Island',
        'South Carolina',
        'South Dakota',
        'Tennessee',
        'Texas',
        'Utah',
        'Vermont',
        'Virginia',
        'Washington',
        'West Virginia',
        'Wisconsin',
        'Wyoming'];
      let stateCodes = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District Of Columbia': 'DC',
        'Federated States Of Micronesia': 'FM',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Marshall Islands': 'MH',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Mexico': 'MX',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Palau': 'PW',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
      };
      let stateMap = false;
      let overlayLayer = false;
      let regionLookup = false;
      let californiaRegionized = {}; // will have form {regionName: {city: cityRowHTML, city2: city2RowHTML}}

      let defaultPickerDate = new Date().fp_incr(-1);

      const DEFAULT_STATE_NAME = states[0];

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

      $(document).ready(function() {
        let setToDefaultState = false;
        if (stateName) {
			// AirNowDrupal #191 cw 2019-09-20
          stateName = toTitleCase(stateName.replace(/\+/g, " ").replace(/%20/g, " ").replace(/-/g, " "));
          if (states.indexOf(stateName) < 0) {
            setToDefaultState = true;
          }
        } else {
          setToDefaultState = true;
        }

        if (setToDefaultState) {
          stateName = DEFAULT_STATE_NAME;
          let updatedUrl = "?";
          updatedUrl += "name=" + stateName.toLowerCase();
          let stateObj = {newURL: updatedUrl};
          history.replaceState(stateObj, "", updatedUrl);
        }

        $(".stateTitle").text(stateName);
        $("div.metaTagStatePage").html( "<meta title='"+stateName+" Sate Page'><meta description='AirNow.gov state page for "+stateName+". This page list all the Air Quality Index (AQI) reporting area within the state of "+stateName+".'>" );

        // <meta name="description" content="{{ state_name }} Air Quality Index (AQI) Reporting Areas list with Current AQI, Today's AQI and Tomorrow's AQI">
        // SUBSCRIBING TO STATE CURRENT STATE DATA EVENT
        PubSub.subscribe(ReportingArea.TOPICS.state_data, function () {
          let cities = ReportingArea.getStateCities();
          // perhaps call internal function to iterate over each returned city and call ReportingArea.getStateCityData to build each row. pass in blah[0] for example
          populateCurrentAqi(cities);
        });

        // SUBSCRIBING TO STATE HISTORICAL STATE DATA EVENT
        PubSub.subscribe(ReportingArea.TOPICS.state_historical_data, function () {
          toggleHistoricalLoading(false);

          let cities = ReportingArea.getStateCities();

          populateHistoricalAqi(cities);
        });

        ReportingArea.lookupStateReportingAreaData(stateCodes[stateName]);

        setElements();    // bindings and setting element data

        // constructStateMap(settings.state_extent);
        // setTimeout(function(){
        //     $('#currentLoading th').text("Unable to load data, please try again");
        //   },
        //   5000);

        // FIXME: this only goes to the national extent... We need the map to determine the state bounds
        $("#air-quality-monitors-in-state").off("click").on("click", function() {
          let win = window.open(AirNowGov.INTERACTIVE_MAP_URL, "_blank");
          win.focus();
        });
      });

      function populateCurrentAqi(cities) {
        $('#currentLoading').hide();
        let currentTableBody = $("#currentAQITableBody");

        if (stateName === "California") { // using region lookup for master region city dictionary
          let shortenedCities = cities;
          shortenedCities = shortenedCities.map(function(city) {
            city = city.replace(/ /g, "");
            return city;
          });

          // TODO: only do this if california in the url
          regionLookup = settings.california_regions;
          for (let region in regionLookup) {
            if (regionLookup.hasOwnProperty(region)) {
              californiaRegionized[region] = {};
              let regionCities = regionLookup[region];
              for (let cityIndex = 0; cityIndex < regionCities.length; cityIndex++) {
                let city = regionCities[cityIndex];
                if (shortenedCities.indexOf(city.replace(/ /g, "")) > -1) {
                  californiaRegionized[region][city] = "";
                }
              }
            }
          }
        }

        let tzAbbrCounts = {};
        $("#noCurrentDataAvailable").toggle(cities.length === 0);
        for (var i = 0; i < cities.length; i++) {
          let cityData = ReportingArea.getStateCityData(cities[i]);

          let current = cityData["current"];
          let todayForecast = cityData["forecast_today"];
          let tomorrowForecast = cityData["forecast_tomorrow"];

          let time = current[ReportingArea.FIELDS.time] === undefined ? "": formatTime(current);
          let timeZone = false;
          if (typeof current[ReportingArea.FIELDS.timezone] !== "undefined") {
            timeZone = current[ReportingArea.FIELDS.timezone];
          } else if (typeof todayForecast[ReportingArea.FIELDS.timezone] !== "undefined") {
            timeZone = todayForecast[ReportingArea.FIELDS.timezone];
          } else if (typeof tomorrowForecast[ReportingArea.FIELDS.timezone] !== "undefined") {
            timeZone = tomorrowForecast[ReportingArea.FIELDS.timezone];
          }

          // Tally up all timezone abbreviation occurrances.  This will be used to tell the map which timezone to display
          if (timeZone && tzAbbrCounts.hasOwnProperty(timeZone)) {
            tzAbbrCounts[timeZone] = tzAbbrCounts[timeZone] + 1;
          } else {
            tzAbbrCounts[timeZone] = 1;
          }

          // FIXME: This is a quick fix so we don't show timezones when we don't have the time.  Needs proper integration into status of the Current AQI gray category
          if (time === "") {
            timeZone = "";
          }

          let newRow = $("<tr></tr>");

          //let dataCourtesyOf = current[ReportingArea.FIELDS.reportingAgency];
          let dataCourtesyText = "";

          let hasReportingAreaData = current[ReportingArea.FIELDS.reportingAreaName]
            || todayForecast[ReportingArea.FIELDS.reportingAreaName]
            || tomorrowForecast[ReportingArea.FIELDS.reportingAreaName];

          let cityLink;
          if (hasReportingAreaData) {
            // AirNowDrupal # 108 State Page Links and Bookmarks Fix cw 2019-03-20
            // Reverted to pre-#108 fix - amc 2019-04-11
            cityLink = "<a class='state-city-cell-link' href='\\?reportingArea=" + cities[i] + "&stateCode=" + stateCodes[stateName] + "'><b>" + cities[i] + "</b></a>";
          } else {
            cityLink = "<b>" + cities[i] + "</b>";
          }

          let cityName = $("<td>" + cityLink + dataCourtesyText + "</td>");
          cityName.append($("<br>"))
            .append($("<span>")
              .addClass("city-time-cell")
              .html(time + " " + timeZone));

          let currentAQI = $("<td>")
            .addClass("currentAirQualityColumn")
            .addClass("state-table-cell-border")
            .addClass("text-align-center")
            .append(constructStyledAqi(current, true));

          let todayForecastAQI = $("<td>")
            .addClass("state-table-cell-border")
            .append(constructStyledAqi(todayForecast));

          let tomorrowForecastAQI = $("<td>")
            .addClass("center-cell")
            .append(constructStyledAqi(tomorrowForecast));

          newRow.append(cityName);
          newRow.append(currentAQI);
          newRow.append(todayForecastAQI);
          newRow.append(tomorrowForecastAQI);

          if (regionLookup) {
            for (let region in regionLookup) {
              if (regionLookup.hasOwnProperty(region)) {
                if (regionLookup[region].indexOf(cities[i]) > -1) {
                  californiaRegionized[region][cities[i]] = newRow;
                } else {
                  if (regionLookup[region].indexOf(cities[i].replace(/ /g, "")) > -1) {
                    californiaRegionized[region][cities[i].replace(/ /g, "")] = newRow;
                  }
                }
              }
            }
          } else {
            currentTableBody.append(newRow);
          }
        }
        if (regionLookup) {
          for (let region in californiaRegionized) {
            if (californiaRegionized.hasOwnProperty(region)) {
              let regionId = region.replace(/ /g, "");
              currentTableBody.append("\n" +
                "        <tr" + " id=" + regionId + " class=\"region-name\">\n" +
                "          <td colspan=\"4\">\n" +
                "            <b>" + region + "</b>\n" +
                "          </td>\n" +
                "        </tr>\n");

              for (let city in californiaRegionized[region]) {
                if (californiaRegionized[region].hasOwnProperty(city)) {
                  let row = californiaRegionized[region][city];

                  // let cityData = ReportingArea.getStateCityData(city);
                  // let current = cityData["current"];

                  // No Data row
                  if (row === "") {
                    row = $("<tr></tr>");

                    // TODO: How to get lat and long if we have no current data?
                    // let cityLink = "\\?latitude=" + current['latitude'] + "&longitude=" + current['longitude'];
                    // let cityName = $("<td><a class='state-city-cell-link' href='"+cityLink+"'><b>" + city + "</b></a>" + "</td>");
                    let cityName = $("<td><b>" + city + "</b>" + "</td>");

                    let currentAQI = $("<td>")
                      .addClass("currentAirQualityColumn")
                      .addClass("state-table-cell-border")
                      .addClass("text-align-center")
                      .append(constructStyledAqi([], true));

                    let todayForecastAQI = $("<td>")
                      .addClass("state-table-cell-border")
                      .append(constructStyledAqi([]));

                    let tomorrowForecastAQI = $("<td>")
                      .addClass("center-cell")
                      .append(constructStyledAqi([]));

                    row.append(cityName);
                    row.append(currentAQI);
                    row.append(todayForecastAQI);
                    row.append(tomorrowForecastAQI);

                    currentTableBody.append(row);
                  } else {
                    currentTableBody.append(row);
                  }
                }
              }
            }
          }
        }

        // Determine most used timezone abbreviation, which will be used to set the map's data timestamp.
        // Default to user's local timezone if no timezone abbreviations found.
        let tz = "Local";
        let tzOffset = Number(moment().format("Z").split(":")[0]);
        if (tzAbbrCounts) {
          let maxTz = false;
          let maxCount = -999;
          for (let tzAbbr in tzAbbrCounts) {
            let count = tzAbbrCounts[tzAbbr];
            if (count > maxCount) {
              maxCount = count;
              maxTz = tzAbbr;
            }
          }
          if (maxTz) {
            tz = maxTz;
            tzOffset = TIMEZONE_ABBRS[tz];
          }
        }

        // loadCurrentMapData(tz, tzOffset);
      }

      function toggleHistoricalLoading(show) {

        if(show) {
          let historicalTableBody = $("#historicalAQITableBody");

          //Empty out table before appending cities
          historicalTableBody.find(".state-table-historicaldata-row").remove();
          historicalTableBody.find(".region-name").remove();

          $('#historicalLoading th').text("Loading...");
          $('#historicalLoading').show();
        } else {
          $('#historicalLoading').hide();
        }
      }

      function populateHistoricalAqi(cities) {
        $('#historicalLoading').hide();

        let historicalData = ReportingArea.getStateHistoricalData();
        let historicalTableBody = $("#historicalAQITableBody");

        //Empty out table before appending cities
        // historicalTableBody.find(".state-table-historicaldata-row").remove();
        // historicalTableBody.find(".region-name").remove();

		    // Added check for 403 errors, will say unable to load
        if(historicalData === false) {
          $('#historicalLoading th').text("Unable to load data, please try again");
          $('#historicalLoading').show();
          return;
        }
        if (stateName === "California") { // using region lookup for master region city dictionary
          let shortenedCities = cities;
          shortenedCities = shortenedCities.map(function(city) {
            city = city.replace(/ /g, "");
            return city;
          });

          regionLookup = settings.california_regions;
          for (let region in regionLookup) {
            if (regionLookup.hasOwnProperty(region)) {
              californiaRegionized[region] = {};
              let regionCities = regionLookup[region];
              for (let cityIndex = 0; cityIndex < regionCities.length; cityIndex++) {
                let city = regionCities[cityIndex];
                if (shortenedCities.indexOf(city.replace(/ /g, "")) > -1) {
                  californiaRegionized[region][city] = "";
                }
              }
            }
          }
        }


        $("#noHistoricalDataAvailable").toggle(cities.length === 0);
        for (var i = 0; i < cities.length; i++) {
          let cityData = {};
          let stateCityData = ReportingArea.getStateCityData(cities[i]);
          let currentStateCityData = stateCityData["current"];

          // SOME CITIES IN THE 'MASTER CITY LIST' ARE NOT IN THE LIST WE GET BACK FROM API
          if (historicalData.hasOwnProperty(cities[i])) {
            cityData = historicalData[cities[i]];
          } else {
            continue;
          }
          let ozone = cityData["ozone"];
          let pm25 = cityData["pm25"];
          let pm10 = cityData["pm10"];

          let newRow = $("<tr class='state-table-historicaldata-row'></tr>");

          let dataCourtesyText = "";

          // let cityLink = "\\?latitude=" + currentStateCityData['latitude'] + "&longitude=" + currentStateCityData['longitude'];
          // let cityName = $("<td><b><a href='"+cityLink+"'>" + cities[i] + "</a></b>" + dataCourtesyText + "</td>");
          // Requested to not show links on Historic table
          let cityName = $("<td><b>" + cities[i] + "</b>" + dataCourtesyText + "</td>");

          let ozoneAQI = $("<td>")
            .addClass("state-table-cell-border")
            .addClass("text-align-center")
            .append(constructStyledAqiHistorical(ozone));

          let pm25AQI = $("<td>")
            .addClass("state-table-cell-border")
            .append(constructStyledAqiHistorical(pm25));

          let pm10AQI = $("<td>")
            .addClass("center-cell")
            .append(constructStyledAqiHistorical(pm10));

          newRow.append(cityName);
          newRow.append(ozoneAQI);
          newRow.append(pm25AQI);
          newRow.append(pm10AQI);

          if (regionLookup) {
            // for california regions
            for (let region in regionLookup) {
              if (regionLookup.hasOwnProperty(region)) {
                if (regionLookup[region].indexOf(cities[i]) > -1) {
                  californiaRegionized[region][cities[i]] = newRow;
                } else {
                  if (regionLookup[region].indexOf(cities[i].replace(/ /g, "")) > -1) {
                    californiaRegionized[region][cities[i].replace(/ /g, "")] = newRow;
                  }
                }
              }
            }
          } else {
            // for non california states
            historicalTableBody.append(newRow);
          }
        }
        // for california regions
        if (regionLookup) {
          for (let region in californiaRegionized) {
            if (californiaRegionized.hasOwnProperty(region)) {
              let regionId = region.replace(/ /g, "");
              historicalTableBody.append("\n" +
                "        <tr" + " id=" + regionId + " class=\"region-name\">\n" +
                "          <td colspan=\"4\">\n" +
                "            <b>" + region + "</b>\n" +
                "          </td>\n" +
                "        </tr>\n");

              for (let city in californiaRegionized[region]) {
                if (californiaRegionized[region].hasOwnProperty(city)) {
                  let row = californiaRegionized[region][city];

                  let stateCityData = ReportingArea.getStateCityData(city);
                  let currentStateCityData = stateCityData["current"];
                  let todayStateCityData = stateCityData["forecast_today"];
                  let tomorrowStateCityData = stateCityData["forecast_tomorrow"];

                  // No data row
                  if (row === "") {
                    row = $("<tr class='state-table-historicaldata-row'></tr>");
                    // let dataCourtesyOf = current[ReportingArea.FIELDS.reportingAgency];
                    let dataCourtesyText = "";

                    let latitude = false;
                    let longitude = false;
                    if (currentStateCityData.hasOwnProperty("latitude") && currentStateCityData.hasOwnProperty("latitude")) {
                      latitude = currentStateCityData["latitude"];
                      longitude = currentStateCityData["longitude"];
                    } else if (todayStateCityData.hasOwnProperty("latitude") && todayStateCityData.hasOwnProperty("latitude")) {
                      latitude = todayStateCityData["latitude"];
                      longitude = todayStateCityData["longitude"];
                    } else if (tomorrowStateCityData.hasOwnProperty("latitude") && tomorrowStateCityData.hasOwnProperty("latitude")) {
                      latitude = tomorrowStateCityData["latitude"];
                      longitude = tomorrowStateCityData["longitude"];
                    }

                    let cityLink = "<b>" + city + "</b>";

                    let cityName = $("<td>" + cityLink + dataCourtesyText + "</td>");

                    // let cityLink = "\\?latitude=" + currentStateCityData['latitude'] + "&longitude=" + currentStateCityData['longitude'];
                    // let cityName = $("<td><a href='" + cityLink + "'><b>" + city + "</a></b>" + dataCourtesyText + "</td>");
                    // let cityName = $("<td class='city-no-historical-data'><b>" + city + "</b>" + dataCourtesyText + "</td>");

                    let ozoneAQI = $("<td>")
                      .addClass("state-table-cell-border")
                      .addClass("text-align-center")
                      .append(constructStyledAqiHistorical(-999));

                    let pm25AQI = $("<td>")
                      .addClass("state-table-cell-border")
                      .append(constructStyledAqiHistorical(-999));

                    let pm10AQI = $("<td>")
                      .addClass("center-cell")
                      .append(constructStyledAqiHistorical(-999));

                    row.append(cityName);
                    row.append(ozoneAQI);
                    row.append(pm25AQI);
                    row.append(pm10AQI);

                    historicalTableBody.append(row);
                  } else {
                    historicalTableBody.append(row);
                  }
                }
              }
            }
          }
        }
      }

      function constructStyledAqi(reportingArea, floatLeft) {
        let pollutant = reportingArea[ReportingArea.FIELDS.parameter];
        let aqi = reportingArea[ReportingArea.FIELDS.aqi];
        let category = reportingArea[ReportingArea.FIELDS.category];
        let aqiColor = "pollutant-status-circle default";


        if (category === undefined) {
          category = "";
        }

        if (((aqi >= 0) && (aqi < 51)) || (!aqi && category.toLowerCase() === "good")) {
          aqiColor = "pollutant-status-circle good";
        } else if (aqi < 101 || (!aqi && category.toLowerCase() === "moderate")){
          aqiColor = "pollutant-status-circle moderate";
        } else if (aqi < 151 || (!aqi && category.toLowerCase() === "unhealthy for sensitive groups")){
          aqiColor = "pollutant-status-circle unhealthy-sensitive";
        } else if (aqi < 201 || (!aqi && category.toLowerCase() === "unhealthy")){
          aqiColor = "pollutant-status-circle unhealthy";
        } else if (aqi < 301 || (!aqi && category.toLowerCase() === "very unhealthy")){
          aqiColor = "pollutant-status-circle very-unhealthy";
        } else if (aqi < 501 || (!aqi && category.toLowerCase() === "hazardous")){
          aqiColor = "pollutant-status-circle hazardous";
        } else if (aqi >= 501) {
          aqiColor = "pollutant-status-circle hazardous";
          category = "Beyond the AQI"; // Add Beyond Index cw 2019-10-08
        }

        if (aqi === undefined) {
          aqi = "";
        }

        let titleText = pollutant + ": AQI " + aqi + " - " + category;
        if (aqi === "" && category === "") {
          titleText = "Not Available";
          pollutant = "N/A";
          category = "";
        }

        if (category.toLowerCase() === "unhealthy for sensitive groups") {
          category = "USG";
        }

        let container = $("<div>")
          .addClass("state-aqi-container")
          .append($("<span>")
            .addClass("state-aqi-style")
            .addClass(aqiColor)
            .attr("title", titleText)
            .html(aqi))
          .append("<br>")
          .append($("<span>")
            .addClass("state-aqi-polutant")
            .html(pollutant))
          .append("<br>")
          .append($("<span>")
              .addClass("state-aqi-category")
              .html(category));
        return container;
      }

      function constructStyledAqiHistorical(aqi) {
        // let category = reportingArea[ReportingArea.FIELDS.category];
        let aqiColor = "pollutant-status-circle default",
            category = "default";

        if (((aqi >= 0) && (aqi < 51))) {
          aqiColor = "pollutant-status-circle good";
          category = "Good";
        } else if (aqi < 101){
          aqiColor = "pollutant-status-circle moderate";
          category = "Moderate";
        } else if (aqi < 151){
          aqiColor = "pollutant-status-circle unhealthy-sensitive";
          category = "USG";
        } else if (aqi < 201){
          aqiColor = "pollutant-status-circle unhealthy";
          category = "Unhealthy";
        } else if (aqi < 301){
          aqiColor = "pollutant-status-circle very-unhealthy";
          category = "Very Unhealthy";
        } else if (aqi < 501){
          aqiColor = "pollutant-status-circle hazardous";
          category = "Hazardous";
        } else if (aqi >= 501) {  // Add Beyond Index cw 2019-10-08
          aqiColor = "pollutant-status-circle hazardous";
          category = "Beyond the AQI";
        }

        if (aqi < 0) {
          aqiColor = "pollutant-status-circle default";
          aqi = "";
        }

        let titleText = "AQI " + aqi + " - " + category;
        if (aqi === "") {
          titleText = "Not Available";
          category = "";
        }

        let container = $("<div>")
          .addClass("state-aqi-container")
          .append($("<span>")
            .addClass("state-aqi-style")
            .addClass(aqiColor)
            .attr("title", titleText)
            .html(aqi))
          .append("<br>")
          .append($("<span>")
            .addClass("state-aqi-category")
            .html(category));
        return container;
      }

      function setElements() {
        $("#todayForecastDate").append(moment().format("dddd MMMM D"));
        $("#todayForecastDateAbbr").append(moment().format("MMM D"));
        $("#tomorrowForecastDate").append(moment().add(1, "days").format("dddd MMMM D"));
        $("#tomorrowForecastDateAbbr").append(moment().add(1, "days").format("MMM D"));

        let stateSelect = $("#stateSelect");
        // populating state select
        $.each(states, function() {
          stateSelect.append($("<option />").val(this.toLowerCase()).text(this));
        });

        // preventing weird scrolling behavior on click
        $('.state-tabs li a').click(function(e){
          e.preventDefault();
          e.stopImmediatePropagation();
          $(this).tab('show');

          // checking to see if we need to load the default dates historical data - first load
          if (this.id === "historicalAQITab") {
            let historicalTable = $('#historicalAQITableBody');
            if (historicalTable.length > 0 && historicalTable[0].childElementCount <= 3) {

              // first time opening tab, load historical data for yesterday
              ReportingArea.lookupStateHistoricalData(stateName.split(' ').join('_'), defaultPickerDate);
            }
          }

        });

        stateSelect.val(stateName.toLowerCase());
        stateSelect.on('change', function() {
          let newStateName = this.value.replace(/ /g, "-").toLowerCase();
          window.open("/state?name=" + newStateName, "_self");
        });

        // datepicker inst
        datePicker = flatpickr("#historicalDatePicker",
          {
            dateFormat: "Y/m/d",
            minDate: new Date().fp_incr(-365),
            maxDate: new Date().fp_incr(-1),
            disableMobile: true,
            defaultDate: defaultPickerDate,
            onChange: function(selectedDates, dateStr, instance) {
              if (selectedDates !== []) {
                toggleHistoricalLoading(true);
                ReportingArea.lookupStateHistoricalData(stateName.split(' ').join('_'), selectedDates[0]);
              }
            }
          }
          );

        // this is to fix a bug where datepicker would fill in this input with the default date...
        // ...for some unknown reason when using back button on browser to return to state page
        if ($('#location-input-nav')[0].value !== "") {
          $('#location-input-nav')[0].value = "";
        }

      }

      function formatTime(currentAQData) {
        // Convert reporting area's 24-hour update time to 12-hour
        let time;
        let rawTime = currentAQData[ReportingArea.FIELDS.time];
        if(rawTime) {
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
              time = "" + Number(hour-12) + ":" + minute + " PM";
            }
          }
          // let tz = currentAQData[ReportingArea.FIELDS.timezone];
          // let date = currentAQData[ReportingArea.FIELDS.issueDate].split("/");
          // aqiDataTime = new Date("20" + Number(date[2]), Number(date[0]), Number(date[1]), Number(hour), Number(minute), 0, 0);
          return time;
        }
      }

      function constructStateMap(extent) {
        if (stateMap) {
          return;
        }
        let latLng = GeoLocation.getLatLng();

        stateMap = L.map('stateMap', {attributionControl: false, zoomControl: false}).setView([latLng.lat, latLng.lng], 6);
        L.esri.basemapLayer('Imagery').addTo(stateMap);
        L.esri.basemapLayer('ImageryLabels').addTo(stateMap);
        stateMap.dragging.disable();
        stateMap.touchZoom.disable();
        stateMap.doubleClickZoom.disable();
        stateMap.scrollWheelZoom.disable();
        stateMap.boxZoom.disable();
        stateMap.keyboard.disable();
        if (stateMap.tap) stateMap.tap.disable();

        stateMap.fitBounds([extent[1],extent[0]],[extent[3],extent[2]]);
        let zoom = stateMap.getZoom();
        if (zoom > 6) {
          stateMap.setZoom(6);
        }
        L.esri.featureLayer({
          url: 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/AirNowLatestContours/FeatureServer/2',
          simplifyFactor: 0.5,
          precision: 5,
          style: function (feature) {
            return ESRI_FEATURE_STYLE[feature.properties.gridcode];
          }
        }).addTo(stateMap);

        //FIXME: Because we disabled the map, this no longer will be called.  Even if it was, we would not have an extent to zoom to.  A copy of this has been placed on the page load that will take user to national extent
        // $("#air-quality-monitors-in-state").off("click").on("click", function() {
        //   let extentBBox = stateMap.getView().calculateExtent(stateMap.getSize());
        //   let win = window.open(AirNowGov.INTERACTIVE_MAP_URL + "?xmin=" + extentBBox[0] + "&ymin=" + extentBBox[1] + "&xmax=" + extentBBox[2] + "&ymax=" + extentBBox[3], "_blank");
        //   win.focus();
        // });
      }

      function createMapImageOverlay(extent, tz, tzOffset) {
        if (overlayLayer) {
          stateMap.removeLayer(overlayLayer);
        }

        let loadingHeader = $(".map_loading_overlay");
        loadingHeader.show();

        let featureServerInfoUrl = "https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/AirNowLatestContours/FeatureServer/2?f=json";
        $.ajax({
          url: featureServerInfoUrl,
          success: function(response) {
            let responseJSON = JSON.parse(response);
            let timeExtent = responseJSON['timeInfo']['timeExtent'];
            let latestEndTime = timeExtent[1];
            setMapTimestamp(latestEndTime, tz, tzOffset);
            setFeatureLayer();
          }
        });

        function setMapTimestamp(timestamp, tz, tzOffset) {
          let dateTime = moment(timestamp).utcOffset(tzOffset);
          $(".time_overlay").text(dateTime.format("h:mm a, MMMM Do ") + "(" + tz + ")");
        }

      }

      function loadCurrentMapData(tz, tzOffset) {
        if (!stateMap) {
          return;
        }
        let mapDiv = $("#stateMap");
        let mapOverlay = $("#state-map-overlay");
        let bottomleft = L.Projection.SphericalMercator.project(stateMap.getBounds().getSouthWest());
        let topright = L.Projection.SphericalMercator.project(stateMap.getBounds().getNorthEast());
        extentBBox = [bottomleft.x, bottomleft.y, topright.x, topright.y];

        mapOverlay.hide();

        // createMapImageOverlay(transformedExtent, tz, tzOffset);
      }

      function toTitleCase(str) {
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
      }


    }
  };

})(jQuery, Drupal);
