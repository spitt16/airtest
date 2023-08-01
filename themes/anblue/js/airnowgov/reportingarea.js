(function($, Drupal) {
  // Create ReportingArea namespace
  let AirNowGov = window.AirNowGov;
  let PubSub = window.PubSub;
  let GeoLocation = AirNowGov.GeoLocation;
  let ReportingArea = AirNowGov.ReportingArea = {};
  let Storage = AirNowGov.Storage;

  const STORAGE_KEY = "ReportingArea";
  const STORAGE_KEY_WEATHER = "Weather";
  const STORAGE_KEY_RADPS = "RADPS"; // ReportingArea Data Providers
  const FIELDS = ReportingArea.FIELDS = {
    "issueDate": "issueDate",
    "validDate": "validDate",
    "recordSequence": "recordSequence",
    "timezone": "timezone",
    "time": "time",
    "dataType": "dataType",
    "isPrimary": "isPrimary",
    "reportingAreaName": "reportingArea",
    "stateCode": "stateCode",
    "latitude": "latitude",
    "longitude": "longitude",
    "parameter": "parameter",
    "aqi": "aqi",
    "category": "category",
    "isActionDay": "isActionDay",
    "discussion": "discussion",
    "reportingAgency": "reportingAgency"
  };

  let loadingData = false;
  let loadingCurrentData = false;
  let loadingHistoricalData = false;
  let servicesReady = false;

  const TOPIC_BASE = AirNowGov.APP_NAME + "." + STORAGE_KEY;
  const TOPICS = ReportingArea.TOPICS = {
    "new_data": TOPIC_BASE + ".new_data",
    "new_weather_data": TOPIC_BASE + ".new_weather_data",
    "state_data": TOPIC_BASE + ".state_data",
    "state_historical_data": TOPIC_BASE + ".state_historical_data",
    "new_dataproviders": TOPIC_BASE + ".new_dataproviders",
    "services_ready": TOPIC_BASE + ".services_ready"
  };


  let stateReportingAreaData = false;
  let cachedHistoricalData = {}; // look up by date
  let historicalData = {}; // look up by date

  function getReportingArea() {
    let item = Storage.getItem(STORAGE_KEY);
    if (!item) {
      item = saveReportingArea({
        "current": [],
        "forecast": [],
        "init": false
      });
    }
    let locationCoord = GeoLocation.getLatLng();
    let locationStateCode = GeoLocation.getStateCode();
    if (Storage.isItemExpired(STORAGE_KEY) && locationCoord) {
      lookupLocationReportingAreaData(locationCoord.lat, locationCoord.lng, locationStateCode);
    }
    if (!locationCoord && !item.data.current.length && !item.data.forecast.length) {
      return false;
    }
    return item.data;
  }

  let isSessionExpired = ReportingArea.isSessionExpired = function() {
    let item = Storage.getItem(STORAGE_KEY);
    if (!item) {
      return true;
    }
    return Storage.isItemExpired(STORAGE_KEY);
  };

  function getWeather() {
    let item = Storage.getItem(STORAGE_KEY_WEATHER);
    if (!item) {
      item = saveWeather({
        "category": "",
        "description": "",
        "degree": false
      });
    }
    let locationCoord = GeoLocation.getLatLng();
    if (Storage.isItemExpired(STORAGE_KEY_WEATHER) && locationCoord) {
      lookupLocationWeatherData(locationCoord.lat, locationCoord.lng, 50);
    }
    if (!locationCoord && !item.data.category.length && !item.data.degree) {
      return false;
    }
    return item.data;
  }

  function getRADPS() {
    let item = Storage.getItem(STORAGE_KEY_RADPS);
    if (!item) {
      item = saveRADPS({
        name: false,
        id: false,
        twcCityCode: false,
        state: false,
        stateCode: false,
        dataProviders: false,
        dataProviderURLs: false,
        forecastProviders: false, //AIR-620 add to storage values cw 2023-05-30
        forecastProviderURLs: false, //AIR-620 add to storage values cw 2023-05-30
        forecastProvider: false,
        forecastProviderURL: false
      });
    }
    return item.data;
  }

  function saveRADPS(new_radps) {
    let item = Storage.storeItem(STORAGE_KEY_RADPS, new_radps);
    return item;
  }

  function saveReportingArea(reportingarea) {
    let item = Storage.storeItem(STORAGE_KEY, reportingarea);
    PubSub.publish(TOPICS.new_data, true);
    return item;
  }

  function saveWeather(weather) {
    let item = Storage.storeItem(STORAGE_KEY_WEATHER, weather);
    PubSub.publish(TOPICS.new_weather_data, item.data);
    return item;
  }

  function saveReportingAreaDataProviders(reportingAreaDataProviders) {
    let item = saveRADPS(reportingAreaDataProviders);
    PubSub.publish(TOPICS.new_dataproviders, true);
    return item;
  }

  // let getStateCities = ReportingArea.getStateCities = function() {
  //   return []; // ["Alexandria", "Altoona", ...]
  // };

  // let getStateCityData = ReportingArea.getStateCityData = function(reportingAreaName) {
  //   return {
  //     current: {}, // reportingarea record with max aqi
  //     forecast_today: {},  // reportingarea record with max aqi
  //     forecast_tomorrow: {} // reportingarea record with max aqi
  //   }
  // };
  //
  // let lookupStateReportingAreaData = ReportingArea.lookupStateReportingAreaData = function(state_code) {
  //   // ajax call
  //   PubSub.publish(TOPICS.state_data, true);
  // };

  // returns all parameters for all days (sequence numbers)
  let getAllReportingAreaData = ReportingArea.getAllReportingAreaData = function() {
    let reportingarea = getReportingArea();
    if (!reportingarea) {
      return false;
    }
    return reportingarea.current.concat(reportingarea.forecast);
  };

  // returns true if any parameters found from reporting area data
  let hasReportingAreaData = ReportingArea.hasReportingAreaData = function() {
    let data = getAllReportingAreaData();
    return data.length > 0;
  };

  let isDataInit = ReportingArea.isDataInit = function() {
      let data = getReportingArea();
      return data.init !== false;
  };

  // returns array of all parameters for the given dayOffset (sequence number)
  let getAllCurrentReportingAreaData = ReportingArea.getAllCurrentReportingAreaData = function() {
    let reportingarea = getReportingArea();
    if (!reportingarea) {
      return false;
    }
    return reportingarea.current;
  };

  // returns primary parameter (max AQI) for the given dayOffset (sequence number)
  let getMaxCurrentReportingAreaData = ReportingArea.getMaxCurrentReportingAreaData = function() {
    let reportingarea = getReportingArea();
    if (!reportingarea) {
      return false;
    }
    let currentData = reportingarea.current;
    let current = false;
    for (let i = 0; i < currentData.length; i++) {
      let c = currentData[i];
      if (!current) {
        current = c;
      } else {
        if (c[FIELDS.aqi] > current[FIELDS.aqi]) {
          current = c;
        }
      }
    }

    return current;
  };

  // returns non-primary parameter (max AQI) for the given dayOffset (sequence number)
  let getOtherCurrentReportingAreaData = ReportingArea.getOtherCurrentReportingAreaData = function() {
    let allCurrent = getAllCurrentReportingAreaData();
    if (!allCurrent) {
      return false;
    }
    let otherCurrent = [];
    let maxAQI = -999;
    let maxIdx = -1;
    for (let i in allCurrent) {
      let c = allCurrent[i];
      otherCurrent.push(c);
      if (maxAQI < 0 || c[FIELDS.aqi] > maxAQI) {
        maxAQI = c[FIELDS.aqi];
        maxIdx = otherCurrent.length - 1;
      }
    }
    otherCurrent.splice(maxIdx, 1);
    otherCurrent.sort(function compare(a, b) {
      if (a.aqi > b.aqi)
        return -1;
      if (a.aqi < b.aqi)
        return 1;
      return 0;
    });
    return otherCurrent;
  };

  // returns array of all parameters for the given dayOffset (sequence number)
  let getAllForecastReportingAreaData = ReportingArea.getAllForecastReportingAreaData = function(dayOffset) {
    let today = moment().hours(0).minutes(0).seconds(0).milliseconds(0);
    dayOffset = dayOffset !== undefined ? dayOffset : 0;
    let reportingarea = getReportingArea();
    if (!reportingarea) {
      return false;
    }
    let forecastData = reportingarea.forecast;
    let forecasts = [];
    for (let i = 0; i < forecastData.length; i++) {
      let f = forecastData[i];
      let validDate = moment(f[FIELDS.validDate], "MM/DD/YY").hours(0).minutes(0).seconds(0).milliseconds(0);
      if (moment.duration(validDate.diff(today)).days() !== dayOffset) {
        continue;
      }
      forecasts.push(f);
    }
    return forecasts;
  };

  // returns primary parameter (max AQI) for the given dayOffset (sequence number)
  let getMaxForecastReportingAreaData = ReportingArea.getMaxForecastReportingAreaData = function(dayOffset) {
    dayOffset = dayOffset !== undefined ? dayOffset : 0;
    let reportingarea = getReportingArea();
    if (!reportingarea) {
      return false;
    }
    let forecastData = reportingarea.forecast;
    let forecast = false;
    for (let i = 0; i < forecastData.length; i++) {
      let today = moment().hours(0).minutes(0).seconds(0).milliseconds(0);
      let f = forecastData[i];
      let validDate = moment(f[FIELDS.validDate], "MM/DD/YY").hours(0).minutes(0).seconds(0).milliseconds(0);
      if (moment.duration(validDate.diff(today)).days() !== dayOffset) {
        continue;
      }
      if (!forecast) {
        forecast = f;
      } else {
        if (f[FIELDS.aqi] > forecast[FIELDS.aqi]) {
          forecast = f;
        }
      }
    }
    return forecast;
  };

  // returns non-primary parameter (max AQI) for the given dayOffset (sequence number)
  let getOtherForecastReportingAreaData = ReportingArea.getOtherForecastReportingAreaData = function(dayOffset) {
    let allForecast = getAllForecastReportingAreaData(dayOffset);
    if (!allForecast) {
      return false;
    }
    let otherForecast = [];
    let maxAQI = -999;
    let maxIdx = -1;

    for (let i in allForecast) {
      let f = allForecast[i];
      otherForecast.push(f);
      if (maxAQI < 0 || f[FIELDS.aqi] > maxAQI) {
        maxAQI = f[FIELDS.aqi];
        maxIdx = otherForecast.length - 1;
      }
    }
    otherForecast.splice(maxIdx, 1);
    otherForecast.sort(function compare(a, b) {
      if (a.aqi > b.aqi)
        return -1;
      if (a.aqi < b.aqi)
        return 1;
      return 0;
    });
    return otherForecast;
  };

  let getReportingAreaDataProviders = ReportingArea.getReportingAreaDataProviders = function () {
    let radps = getRADPS();

    // If no explicit forecastProviderURL, check if agency has a url in DataProviderURLs and use that
    if (radps && radps.length
        && radps.forecastProvider
        && !radps.forecastProviderURL
        && radps.dataProviders.indexOf(radps.forecastProvider) > -1) {
      radps.forecastProviderURL = radps.dataProviderURLs[radps.dataProviders.indexOf(radps.forecastProvider)];
    }

    return radps;
  };

  PubSub.subscribe(GeoLocation.TOPICS.new_location, function() {
    let locationCoord = GeoLocation.getLatLng();
    let locationStateCode = GeoLocation.getStateCode();
    if (locationCoord) {
      lookupLocationReportingAreaData(locationCoord.lat, locationCoord.lng, locationStateCode);
    }
  });

  let getStateCities = ReportingArea.getStateCities = function() {
    return Object.keys(stateReportingAreaData).sort();
  };

  // TBD: What should be selected when multiple parameters given for a current or forecast day but none have AQI values?
  let getStateCityData = ReportingArea.getStateCityData = function(reportingAreaName) {
    let today = moment().hours(0).minutes(0).seconds(0).milliseconds(0);
    let cityData = stateReportingAreaData[reportingAreaName];

    // Get the current observed record with the highest value pollutant
    let maxCurrentData = false;
    if(typeof cityData != "undefined" && cityData.hasOwnProperty("current")) {
      for (let i = 0; i < cityData.current.length; i++) {
        let current = cityData.current[i];
        if (!maxCurrentData || maxCurrentData[FIELDS.aqi] < current[FIELDS.aqi]) {
          maxCurrentData = current;
        }
      }
    }

    // Get the today and tomorrow forecast record with the highest value pollutant
    let maxForecastToday = false;
    let maxForecastTomorrow = false;

    if(typeof cityData != "undefined" && cityData.hasOwnProperty("forecast")) {
      for (let i = 0; i < cityData.forecast.length; i++) {
        let forecast = cityData.forecast[i];
        let validDate = moment(forecast[FIELDS.validDate], "MM/DD/YY").hours(0).minutes(0).seconds(0).milliseconds(0);
        if (moment.duration(validDate.diff(today)).days() === 0 && (!maxForecastToday || maxForecastToday[FIELDS.aqi] < forecast[FIELDS.aqi])) {
          maxForecastToday = forecast;
        } else if (moment.duration(validDate.diff(today)).days() === 1 && (!maxForecastTomorrow || maxForecastTomorrow[FIELDS.aqi] < forecast[FIELDS.aqi])) {
          maxForecastTomorrow = forecast;
        }
      }
    }

    return {
      current: maxCurrentData,
      forecast_today: maxForecastToday,
      forecast_tomorrow: maxForecastTomorrow
    }
  };

  let getStateHistoricalData = ReportingArea.getStateHistoricalData = function() {
    return historicalData;
  };

  let lookupStateReportingAreaData = ReportingArea.lookupStateReportingAreaData = function(state_code) {
    if (!loadingCurrentData) {
      loadingCurrentData = true;
      $.ajax({
        type: "POST",
        url: AirNowGov.API_URL + "reportingarea/get_state",
        data: {
          "state_code": state_code,
        },
        context: this,
        success: function (response) {
          stateReportingAreaData = {};
          let today = moment().hours(0).minutes(0).seconds(0).milliseconds(0);

          for (let i = 0; i < response.length; i++) {
            let record = response[i];
            let reportingAreaName = record[FIELDS.reportingAreaName];
            let dataType = record[FIELDS.dataType];
            let validDate = moment(record[FIELDS.validDate], "MM/DD/YY").hours(0).minutes(0).seconds(0).milliseconds(0);
            if (moment.duration(validDate.diff(today)).days() >= 0) {
              if (reportingAreaName && !stateReportingAreaData.hasOwnProperty(reportingAreaName)) {
                stateReportingAreaData[reportingAreaName] = {
                  current: [],
                  forecast: []
                }
              }

              if (record[FIELDS.dataType] === "O") {
                stateReportingAreaData[reportingAreaName].current.push(record);
              } else if (record[FIELDS.dataType] === "F") {
                stateReportingAreaData[reportingAreaName].forecast.push(record);
              }
            }
          }
          PubSub.publish(TOPICS.state_data, true);
          loadingCurrentData = false;
        },
        error: function (response) {
          // TODO: Handle errors
          console.error(response);
          loadingCurrentData = false;
        }
      });
    }
  };

  let lookupStateHistoricalData = ReportingArea.lookupStateHistoricalData = function(state_name, dateInstance) {
    if (!loadingHistoricalData) {
      let formattedDate = dateInstance.getFullYear() + "/" + (dateInstance.getMonth() + 1) + "/" + (dateInstance.getDate());

      loadingHistoricalData = true;
      // if (cachedHistoricalData.hasOwnProperty(formattedDate)) {
      //   return
      // }
      $.ajax({
        type: "GET",
        url: AirNowGov.API_URL + "andata/States/" + state_name + "/" + formattedDate + ".json",
        context: this,
        success: function (response) {
          // resetting because it could be set from previous calls
          historicalData = {};

          // AIR-530 The updated format needs to be "stringified" first cw 2022-03-24
          var data = JSON.parse(JSON.stringify(response)).reportingAreas; // AIR-530 Sucessful object built with updated JSON files ONLY cw 2022-03-24
          if (typeof data === "undefined") { // AIR-530 IF it's "undefined" then it's the old JSON format, so use the old method cw 2022-03-24
            console.log('AIR-530: Using original JSON format.'); // AIR-530 User feedback cw 2022-03-24
            var data = JSON.parse(response).reportingAreas; // AIR-530 This is the original code cw 2022-03-24
          }

          // reformatting city list so city names are keys
          for (let i = 0; i < data.length; i++) {
            let cityData = data[i];
            let cityName = Object.keys(cityData)[0];
            historicalData[cityName] = cityData[cityName];
          }

          PubSub.publish(TOPICS.state_historical_data, true);
          loadingHistoricalData = false;
        },
        error: function (response) {
          // TODO: Handle errors
          // console.error(response);
          historicalData = false;
          PubSub.publish(TOPICS.state_historical_data, false);
          loadingHistoricalData = false;
        }
      });
    }
  };

  PubSub.subscribe(TOPICS.new_data, function() {
    let allReportingArea = getAllReportingAreaData();
    if (!allReportingArea) {
      return;
    }
    let radps = getReportingAreaDataProviders();
    let stateCode = allReportingArea[0][FIELDS.stateCode];
    let reportingAreaName = allReportingArea[0][FIELDS.reportingAreaName];
    if (radps.name !== reportingAreaName || radps.stateCode !== stateCode) {
      $.ajax({
        type: "GET",
        url: AirNowGov.API_URL + "andata/dataproviders",
        data: {
          "reportingArea": reportingAreaName,
          "stateCode": stateCode
        },
        context: this,
        success: function (response) {
          if (response && response.hasOwnProperty("dataProviders")) {
            saveReportingAreaDataProviders(response);
          }
        }
      });
    }
  });

  let lookupLocationReportingAreaData = ReportingArea.lookupLocationReportingAreaData = function(latitude, longitude, stateCode) {
    if (!loadingData) {
      let apiData = {
        "latitude": latitude,
        "longitude": longitude
      };
      if (stateCode) {
        apiData["stateCode"] = stateCode;
      }
      if (AirNowGov.GLOBALS.getUrlVar("maxDistance")) {
        let maxDistance = AirNowGov.GLOBALS.getUrlVar("maxDistance");
        if (maxDistance >= 0) {
          apiData["maxDistance"] = maxDistance; // miles
        } // else don't supply this parameter
      } else {
        // Default maxDistance
        apiData["maxDistance"] = 50; // miles
      }

      // AIR-572 set-up; assuming this is an "missing PM25" reporting area until we can prove otherwise cw 2022-12-13
      sessionStorage.setItem("AirNowGov.missingPm25Flag", "true");

      loadingData = true;
      $.ajax({
        type: "POST",
        url: AirNowGov.API_URL + "reportingarea/get",
        data: apiData,
        context: this,
        success: function (response) {
          let today = moment().hours(0).minutes(0).seconds(0).milliseconds(0);

          let currentData = [];
          let forecastData = [];

          let reportingareaData = response;
          if (reportingareaData.length) {
            for (let i = 0; i < reportingareaData.length; i++) {
              let record = reportingareaData[i];
              let validDate = moment(record[FIELDS.validDate], "MM/DD/YY").hours(0).minutes(0).seconds(0).milliseconds(0);
              if (moment.duration(validDate.diff(today)).days() >= 0) {
                if (record[FIELDS.dataType] === "O") {
                  currentData.push(record);
                } else if (record[FIELDS.dataType] === "F") {
                  forecastData.push(record);
                }
              } else if (moment.duration(validDate.diff(today)).days() === -1
                    && moment.duration(today.clone().startOf('day').diff(today)).hours() === 0
                    && record[FIELDS.time] === "23:00") {
                if (record[FIELDS.dataType] === "O") {
                  currentData.push(record);
                }
              }
            }
          }

          let reportingarea = {
            current: currentData,
            forecast: forecastData
          };
          saveReportingArea(reportingarea);
          loadingData = false;

          if(currentData.length > 0) {
            lookupLocationWeatherData(currentData[0][FIELDS.latitude], currentData[0][FIELDS.longitude], 50);
          } else if (forecastData.length > 0) {
            lookupLocationWeatherData(forecastData[0][FIELDS.latitude], forecastData[0][FIELDS.longitude], 50);
          }

          // location.reload();
        },
        error: function (response) {
          // TODO: Handle errors
          console.error(response);
        }
      });
    }
  };

  let lookupLocationByReportingAreaStateCode = ReportingArea.lookupLocationByReportingAreaStateCode = function (reportingArea, stateCode, callback, scope) {
    // AIR-572 set-up; assuming this is an "missing PM25" reporting area until we can prove otherwise cw 2022-12-13
    sessionStorage.setItem("AirNowGov.missingPm25Flag", "true");

    $.ajax({
      type: "POST",
      url: AirNowGov.API_URL + "reportingarea/get_location",
      data: {
        "reportingArea": reportingArea,
        "stateCode": stateCode
      },
      context: this,
      success: function (response) {
        callback.call(scope, response);
      },
      error: function (response) {
        callback.call(scope, []);
      }
    });
  };

  let weatherIcon = $(".weather-icon");
  let weatherDegreesValueWrapper = $(".weather-degrees-value-wrapper");
  let weatherValue = $(".weather-value");
  let weatherDegree = $(".weather-degrees");

  let lookupLocationWeatherData = ReportingArea.lookupLocationWeatherData = function (latitude, longitude, maxDistance) {
    $(".weather-loading").show();
    weatherDegreesValueWrapper.hide();
    weatherIcon.hide();
    AirNowGov.Tooltips.createTip(".nav-weather-tool", "weather", "bottom", null, null, null, -15);

    $.ajax({
      type: "POST",
      url: AirNowGov.API_URL + "weather/get",
      data: {
        "latitude": latitude,
        "longitude": longitude,
        "maxDistance": maxDistance // miles
      },
      context: this,
      success: function (response) {
        saveWeather({
          "category": response.category,
          "degrees": response.temperature,
          "description": response.description
        });
      },
      error: function (response) {
        setTimeout(function () {
          saveWeather({"category": "N/A", "degrees": -999});
        }, 3000);
      }
    });
  };

  PubSub.subscribe(TOPICS.new_weather_data, function(topic, weather) {
    handleWeatherDisplay(weather);
  });

  function handleWeatherDisplay(weather) {
    let degrees = weather.degrees;

    function toTitleCase(str) {
      return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      });
    }

    $(".weather-loading").hide();
    if (degrees === Number(-999) || isNaN(degrees)) {
      weatherDegreesValueWrapper.hide();
      weatherIcon.hide();

      degrees = "N/A";
      AirNowGov.Tooltips.createTip(".nav-weather-tool", "weather", "bottom", null, null, null, -15);
    } else {
      degrees = Math.round(degrees);
      let imgPath = lookupWeatherCategoryImage(weather.category);
      if (imgPath) {
        weatherIcon.css("display", "block").find("img").attr("src", imgPath);
      } else {
        weatherIcon.hide();
      }
      let description = weather.description ? weather.description : "Not Currently Available";

      weatherValue.show().text(degrees);
      weatherDegree.show();
      weatherDegreesValueWrapper.show();
    }
  }

  function lookupWeatherCategoryImage(category) {
    let imagesBase = "/themes/anblue/images/weather";
    let imageExt = ".svg";
    if (["dust", "fair_day", "fog", "funnel_cloud", "haze", "hurricane", "light_rain", "overcast_day", "partly_cloudy",
        "partly_cloudy_day", "rain", "rain_snow", "showers_in_vicinity", "smoke", "snow", "thunderstorm",
        "thunderstorm_in_vicinity", "windy"].indexOf(category) >= 1) {
      return imagesBase + "/weather_icon_" + category + imageExt;
    }
    return false;
  }

  // load cached weather
  handleWeatherDisplay(getWeather());

  PubSub.publish(TOPICS.services_ready, true);
  servicesReady = true;
  let isReady = ReportingArea.isReady = function () {
    return servicesReady;
  }
})(jQuery, Drupal);
