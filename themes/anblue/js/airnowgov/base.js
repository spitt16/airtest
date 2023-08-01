(function ($, Drupal) {
  // Create AirNowGov namespace
  let AirNowGov = Drupal.behaviors.AirNowGov = window.AirNowGov = {};
  Drupal.behaviors.PubSub = window.PubSub;

  //TODO: Replace this with a openlayers module that only loads when a module/block needs it to, instead of when the theme loads
  // Drupal.behaviors.ol = window.ol;
  //Drupal.behaviors.Highcharts = window.Highcharts;
  let Tippy = Drupal.behaviors.Tippy = window.Tippy;

  AirNowGov.APP_NAME = "AirNowGov";
  // TODO: have this configurable elsewhere
  AirNowGov.API_URL = "//airnowgovapi.com/"; // Production
  //AirNowGov.API_URL = "https://web-stage.airnowgovapi.com/"; // Staging
  AirNowGov.INTERACTIVE_MAP_URL = "https://gispub.epa.gov/airnow/";

  let GLOBALS = AirNowGov.GLOBALS = {};
  GLOBALS.getUrlVar = function (key) {
    if (GLOBALS.urlVars.hasOwnProperty(key)) {
      return decodeURIComponent(GLOBALS.urlVars[key]);
    }
    return false;
  };
  GLOBALS.urlVars = {};
  let urlVarsPairsStr = window.location.search.slice(1).split("&");
  for (let idx in urlVarsPairsStr) {
    if (urlVarsPairsStr.hasOwnProperty(idx)) {
      let urlVarPairStr = urlVarsPairsStr[idx];
      let urlVarPair = urlVarPairStr.split("=");
      GLOBALS.urlVars[urlVarPair[0]] = urlVarPair[1];
    }
  }
		
  // Temporary until we know how to properly integrate external libraries
  // AirNowDrupal#224 Third layer deep if..else structures added cw 2019-12-02
  AirNowGov.Tooltips = {
    createTip: function (selector, tip_id, placement, aqi_category, parameter, customTitle, distance) {
      distance = typeof distance !== "undefined" ? distance : 0;
      let tip = false;
      if (tip_id === "categories") {
        if (aqi_category === "Good") {
          if (parameter === "OZONE") {
            tip = AirNowGov.Tooltips.tips.categories.good.ozone;
          } else {
            tip = AirNowGov.Tooltips.tips.categories.good.default;
          }
        } else if (aqi_category === "Moderate") {
          if (parameter === "OZONE") {
            tip = AirNowGov.Tooltips.tips.categories.moderate.ozone;
          } else {
            tip = AirNowGov.Tooltips.tips.categories.moderate.default;
          }
        } else if (aqi_category === "Unhealthy for Sensitive Groups") {
          if (parameter === "OZONE") {
            tip = AirNowGov.Tooltips.tips.categories.unhealthySensitive.ozone;
          } else {
            tip = AirNowGov.Tooltips.tips.categories.unhealthySensitive.default;
          }
        } else if (aqi_category === "Unhealthy") {
          if (parameter === "OZONE") {
            tip = AirNowGov.Tooltips.tips.categories.unhealthy.ozone;
          } else {
            tip = AirNowGov.Tooltips.tips.categories.unhealthy.default;
          }
        } else if (aqi_category === "Very Unhealthy") {
          if (parameter === "OZONE") {
            tip = AirNowGov.Tooltips.tips.categories.veryUnhealthy.ozone;
          } else {
            tip = AirNowGov.Tooltips.tips.categories.veryUnhealthy.default;
          }
        } else if (aqi_category === "Hazardous") {
          if (parameter === "OZONE") {
            tip = AirNowGov.Tooltips.tips.categories.hazardous.ozone;
          } else {
            tip = AirNowGov.Tooltips.tips.categories.hazardous.default;
          }
          
         // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
       /* } else if (aqi_category === "Beyond the AQI") {
          if (parameter === "OZONE") {
            tip = AirNowGov.Tooltips.tips.categories.beyondAQI.ozone;
          } else {
            tip = AirNowGov.Tooltips.tips.categories.beyondAQI.default;
          }*/
        }
      } else if (tip_id === "pollutant") {
        if (parameter === "PM2.5") {
          tip = AirNowGov.Tooltips.tips.pollutant.pm25;
        } else if (parameter === "PM10") {
          tip = AirNowGov.Tooltips.tips.pollutant.pm10;
        } else if (parameter === "OZONE") {
          tip = AirNowGov.Tooltips.tips.pollutant.ozone;
        }
      } else {
        tip = AirNowGov.Tooltips.tips[tip_id];
      }

      if (tip) {
        let title = tip.title;
        let message = tip.message;
        title = customTitle ? customTitle : title;
        // AirNowDrupal#124 Make Close button cw 2019-04-16
        // AirNowDrupal#192 Fix Links in pop-ups on Mobile; Click close-box will hide the entire Tippy cw 2019-09-19 Arrr!
        // On clicking on the "close-box" we will hide the tippy... debug: alert(document.activeElement.style.visibility);

        let tipHtml = "<div class='tippy-close-holder'><div onMouseDown='document.activeElement.style.visibility=\"hidden\";'><div id='close-box' class='fa fa-times' style='position: absolute; left: 5px; top: 5px; z-index: -1;'></div></div></div><div align='center'><h4>" + title + "</h4><p>" + message + "</p></div>";
        $("#tippy_container").html(tipHtml);

        $(selector).attr("title", null);
        let elem = document.querySelector(selector);
        if (elem.hasOwnProperty("_tippy")) {
          elem._tippy.destroy();
        }
        // AirNowDrupal #124 Mobile click to close cw 2019-04-16
        let trigger = "mouseenter";
        let interactive = "true";
        if (window.innerWidth <= 767) {
          placement = "bottom";
          // AirNowDrupal#124 cw 2019-04-16
          let trigger = "mouseenter click"; // Tippys are click to close in Mobile cw 2019-04-16
          let interactive = "true";
        }
        // AirNowDrupal #124 moving the placement of currentAirQuality tooltip on smaller screen sizes to avoid UNDERlap with the Menu bar cw 2019-06-20
        if ((tip_id === "currentAirQuality") && window.innerWidth <= 767) {
          placement = "bottom";
        }
        // AirNowDrupal #123 moving the placement of AirQulityForecastDetails tooltip on smaller screen sizes to avoid being on top of leaflet map cw 2019-06-24
        if ((tip_id === "airQualityForecast") && window.innerWidth <= 767) {
          placement = "top";
        }
        return Tippy(selector, {
          html: "#tippy_container",
          placement: placement,
          theme: "marquee",
          animation: "shift-toward", // shift toward; scale
          delay: [300, 100],
          // distance: distance, // Disabling to fix tooltip overlapping issue with certain popups
          interactive: interactive, // AirNowDrupal #124 cw 2019-04-16
          trigger: trigger, // AirNowDrupal #124 cw 2019-04-16
          interactiveBorder: 5
        });
      }
    },

    tips: {
      categories: {
        good: {
          default: {
            title: "Good",
            message: "Enjoy your outdoor activities."
          },
          ozone: {
            title: "Good",
            message: "Enjoy your outdoor activities."
          }
        },
        moderate: {
          default: {
            title: "Moderate",
            message: "If you are <b>unusually sensitive</b> to particle pollution, consider reducing your activity level or shorten the amount of time you are active outdoors."
          },
          ozone: {
            title: "Moderate",
            message: "If you are <b>unusually sensitive</b> to ozone, consider reducing your activity level or shorten the amount of time you are active outdoors."
          }
        },
        unhealthySensitive: {
          default: {
            title: "Unhealthy for Sensitive Groups",
            message: "<b>People with heart or lung disease, older adults, children and teens:</b><br /><ul><li>Choose less strenuous activities.</li><li>Shorten the amount of time you are active outdoors.</li><li>Be active outdoors when air quality is better.</li></ul>"
          },
          ozone: {
            title: "Unhealthy for Sensitive Groups",
            message: "<b>People with lung disease such as asthma, children and teens, older adults, and people who are routinely active outdoors for six or more hours a day:</b><br /><ul><li>Choose less strenuous activities.</li><li>Shorten the amount of time you are active outdoors.</li><li>Be active outdoors when air quality is better.</li></ul>"
          }
        },
        unhealthy: {
          default: {
            title: "Unhealthy",
            message: "<b>People with heart or lung disease, older adults, children and teens:</b><br /><ul><li>Avoid strenuous outdoor activities.</li><li>Keep outdoor activities short.</li><li>Consider moving physical activities indoors or rescheduling.</li></ul><br /><b>Everyone else:</b> Choose less strenuous activities, shorten the amount of time you are active outdoors, or be active outdoors when air quality is better."
          },
          ozone: {
            title: "Unhealthy",
            message: "<b>People with lung disease such as asthma, children and teens, older adults, and people who are routinely active outdoors for six or more hours a day:</b><br /><ul><li>Avoid strenuous outdoor activities.</li><li>Keep outdoor activities short.</li><li>Consider moving physical activities indoors or rescheduling.</li></ul><br /><b>Everyone else:</b> Choose less strenuous activities, shorten the amount of time you are active outdoors, or be active outdoors when air quality is better."
          }
        },
        veryUnhealthy: {
          default: {
            title: "Very Unhealthy",
            message: "<b>People with heart or lung disease, older adults, children and teens:</b><br />Avoid physical activities outdoors.<br /><b>Everyone else:</b> Avoid strenuous outdoor activities, keep outdoor activities short, and consider moving physical activities indoors or rescheduling."
          },
          ozone: {
            title: "Very Unhealthy",
            message: "<b>People with lung disease such as asthma, children and teens, older adults, and people who are routinely active outdoors for six or more hours a day:</b><br />Avoid physical activities outdoors.<br /><b>Everyone else:</b> Avoid strenuous outdoor activities, keep outdoor activities short, and consider moving physical activities indoors or rescheduling."
          }
        },
        hazardous: {
          default: {
            title: "Hazardous",
            message: "<b>Everyone</b> should stay indoors and reduce activity levels."
          },
          ozone: {
            title: "Hazardous",
            message: "<b>Everyone</b> should stay indoors."
          }
        },
        // Air-538 eb 2023-06-15 Removed code that displayed Beyond the AQI and the message for values above 500
        /*beyondAQI: {
          default: {
            title: "Beyond the AQI",
            message: "Values above 500 are considered <a href='/aqi/aqi-basics/extremely-high-levels-of-pm25'>Beyond the Air Quality Index</a>.<br /><strong>Everyone</strong> should stay indoors and reduce activity levels.<br />"
          },
          ozone: {
            title: "Beyond the AQI",
            message: "Values above 500 are considered <a href='/aqi/aqi-basics/extremely-high-levels-of-pm25'>Beyond the Air Quality Index</a>.<br /><strong>Everyone</strong> should stay indoors.<br />"
          }
        },*/
      },
      pollutant: {
        pm25: {
          title: "PM2.5 - Particle Pollution",
          message: "Extremely small particles that can harm the heart and lungs. <br /><br /><a target='_blank' href='https://www.epa.gov/pm-pollution/particulate-matter-pm-basics#PM'>More about particle pollution</a>."
        },
        pm10: {
          title: "PM10 Particle Pollution",
          message: "Small particles that can harm the heart and lungs. <br /><br /><a target='_blank' href='https://www.epa.gov/pm-pollution/particulate-matter-pm-basics#PM'>More about particle pollution</a>."
        },
        ozone: {
          title: "Ozone",
          message: "Ozone, which forms in the air mostly on hot sunny days, can trigger harmful respiratory effects. <br /><br /><a target='_blank' href='https://www.epa.gov/ozone-pollution/basic-information-about-ozone#what%20where%20how'>More about ozone</a>."
        }
      },
      aqi: {
        title: "Air Quality Index",
        message: "The U.S. Air Quality Index (AQI) is a color-coded scale from 0 to 500 used to communicate air quality. <a target='_blank' href='/aqi/aqi-basics'>More about the AQI</a>.<br /><br />\"NowCast\" is an estimate of the AQI to show the current air quality. Check your current air quality to see if now is a good time for outdoor activities. <a target='_blank' href='/aqi/aqi-basics/using-air-quality-index#nowcast'>More about the NowCast</a>."
      },
      airQualityForecast: {
        title: "Air Quality Forecast",
        message: "The Air Quality Forecast is a prediction of the day’s AQI in your area. Use it to plan your day. <br /><br /><a target='_blank' href='/aqi/aqi-basics/using-air-quality-index#forecasts'>More about the air quality forecast</a><br /><br /><a target='_blank' href='/aqi/action-days'>More about Action Days</a>."
      },
      currentAirQuality: {
        title: "Current Air Quality",
        message: "Current Air Quality is the most recent air quality in your area. It’s updated hourly. Check your current air quality to see if now is a good time for outdoor activities. <a target='_blank' href='/aqi/aqi-basics/using-air-quality-index#nowcast'>More about Current Air Quality</a>.<br /><br />Planning the whole day? Check the air quality forecast."
      },
      gpsButton: {
        title: "GeoLocation",
        message: "This button allows AirNow to find the Air Quality at your current location.<br /><br />To use this feature you must allow AirNow to access your location in your device settings."
      }
    }
  };
})(jQuery, Drupal);
