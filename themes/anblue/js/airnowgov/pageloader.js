(function($, Drupal) {
  let PubSub = window.PubSub;
  let AirNowGov = window.AirNowGov;
  let ReportingArea = AirNowGov.ReportingArea;
  let GeoLocation = AirNowGov.GeoLocation;
  let PageLoader = AirNowGov.PageLoader = {};


  const TOPIC_BASE = AirNowGov.APP_NAME + ".PageLoader";
  const TOPICS = PageLoader.TOPICS = {
    "services_ready": TOPIC_BASE + ".services_ready"
  };

  let performingUrlSearch = false;
  let readyStatus = {
    geoLocation: false,
    reportingArea: false
  };

  function isReady() {
    return readyStatus.geoLocation === true
      && readyStatus.reportingArea === true;
  }

  function loadReportingAreaFromLatLng(latitude, longitude) {
    if (latitude && longitude) {
      // Don't search if geolocation city/state/country matches and session hasn't expired
      let userLatitude = GeoLocation.getLatLng().lat;
      let userLongitude = GeoLocation.getLatLng().lng;
      if (userLatitude === latitude && userLongitude === longitude) {
        if (!ReportingArea.isSessionExpired()) {
          return;
        }
      }

      // Lookup location by lat/lon
      performingUrlSearch = true;
      GeoLocation.lookupLocationByLatLng({
        lat: Number(latitude),
        lng: Number(longitude)
      }, true);
    }
  }

  function loadReportingAreaFromCityStateCountry(city, state, country) {
    if (city && (state || country)) {
      // Don't search if geolocation city/state/country matches and session hasn't expired
      let userCity = GeoLocation.getCityName();
      let userStateCode = GeoLocation.getStateCode();
      let userCountryCode = GeoLocation.getCountryCode();
      if (city === userCity && state === userStateCode && country === userCountryCode) {
        if (!ReportingArea.isSessionExpired()) {
          return;
        }
      }

      performingUrlSearch = true;
      GeoLocation.lookupLocationByCityStateCountry(city, state, country, true);
    }
  }

  function loadReportingAreaFromReportingAreaState(reportingArea, stateCode) {
    if (reportingArea && stateCode) {
      // Don't search if reporting area name/state matches and session hasn't expired
      let raData = ReportingArea.getAllReportingAreaData();
      let userReportingArea = raData.length ? raData[0].reportingArea : false;
      let userStateCode = raData.length ? raData[0].stateCode : false;
      if (userReportingArea === reportingArea && userStateCode === stateCode) {
        if (!ReportingArea.isSessionExpired()) {
          return;
        }
      }

      performingUrlSearch = true;
      ReportingArea.lookupLocationByReportingAreaStateCode(reportingArea, stateCode, function (response) {
        if (response && response.latitude && response.longitude) {
          // Lookup location by lat/lon
          GeoLocation.lookupLocationByLatLng({
            lat: Number(response.latitude),
            lng: Number(response.longitude)
          }, true);
        }
      }, this);
    }
  }

  let updateURLParameters = PageLoader.updateURLParameters = function() {
    if (!GeoLocation.getUserSelectedLocation()
        && ((location.search.indexOf("reportingArea") !== -1 && location.search.indexOf("stateCode") !== -1)
            || (location.pathname.indexOf("reportingArea") !== -1 && location.pathname.indexOf("stateCode") !== -1))) {
      // We want to create/update a ReportingArea URL
      let reportingAreaData = ReportingArea.getAllCurrentReportingAreaData()[0];
      if (!reportingAreaData || reportingAreaData !== AirNowGov.GLOBALS.getUrlVar("reportingArea")) {
        return;
      }
      let reportingArea = reportingAreaData.reportingArea;
      let stateCode = reportingAreaData.stateCode;
      if (!reportingArea || !stateCode) {
        return;
      }
      let shareableURL = "/?";
      shareableURL += "reportingArea=" + reportingArea.replace(" ", "%20");
      shareableURL += "&stateCode=" + stateCode;
      if (shareableURL !== (location.pathname + location.search)) {
        let stateObj = {newURL: shareableURL};
        history.replaceState(stateObj, "", shareableURL);
      }
    } else if (!GeoLocation.getUserSelectedLocation()
               && ((location.search.indexOf("latitude") !== -1 && location.search.indexOf("longitude") !== -1)
                   || (location.pathname.indexOf("latitude") !== -1 && location.pathname.indexOf("longitude") !== -1))) {
      // We want to create/update a LatLng URL
      // This shouldn't be hit, as its been replaced by reportingArea
      return;
    } else if ((location.search.indexOf("city") !== -1 && location.search.indexOf("state") !== -1 && location.search.indexOf("country") !== -1)
               || (location.pathname.indexOf("city") !== -1 && location.pathname.indexOf("state") !== -1 && location.pathname.indexOf("country") !== -1)
               || location.pathname === "/" || location.pathname.indexOf("which-flag-do-i-fly") !== -1) { // AirNowDrupal#313 cw 2020-07-07
      // We want to create/update the CityStateCountry URL, or we're on the base URL
      let city = GeoLocation.getCityName();
      let state = GeoLocation.getStateCode();
      let countryCode = GeoLocation.getCountryCode();
      let shareableURL = "";
      // AirNowDrupal#313 If needed add "lang" to Which Flag Do I Fly URLs cw 2020-07-07
      if (location.pathname.indexOf("which-flag-do-i-fly") === 1) {
        lang = RegExp('[\?&]lang=([^&#]*)').exec(window.location.href);
        shareableURL += "/which-flag-do-i-fly/?lang="+lang[1]+"&";
      } else {
        shareableURL += "/?";
      }
      shareableURL += "city=" + city.replace(" ", "%20");
      if (state.length && state !== "MX") {
        shareableURL += "&state=" + state;
      }
      shareableURL += "&country=" + countryCode;
      if (shareableURL !== (location.pathname + location.search) ) {
        let stateObj = {newURL: shareableURL};
        history.replaceState(stateObj, "", shareableURL);
      }
      GeoLocation.resetUserSelectedLocation();
    }
  };

  function init() {
    if (!isReady()) {
      return;
    }
    PubSub.subscribe(GeoLocation.TOPICS.new_location, function() {
      updateURLParameters();
    });
    let getUrlVarFn = AirNowGov.GLOBALS.getUrlVar;
    let urlVars = AirNowGov.GLOBALS.urlVars;
    if (urlVars.hasOwnProperty("latitude") && urlVars.hasOwnProperty("longitude")) {
      loadReportingAreaFromLatLng(getUrlVarFn("latitude"), getUrlVarFn("longitude"));
    } else if (urlVars.hasOwnProperty("city") && (urlVars.hasOwnProperty("state") || urlVars.hasOwnProperty("country"))) {
      loadReportingAreaFromCityStateCountry(getUrlVarFn("city"), getUrlVarFn("state"), getUrlVarFn("country"));
    } else if (urlVars.hasOwnProperty("reportingArea") && urlVars.hasOwnProperty("stateCode")) {
      loadReportingAreaFromReportingAreaState(getUrlVarFn("reportingArea"), getUrlVarFn("stateCode"));
    } else {
      updateURLParameters();
    }

    PubSub.publish(TOPICS.services_ready, true);
  }

  let isPerformingURLSearch = PageLoader.isPerformingURLSearch = function() {
    return performingUrlSearch === true;
  };

  // Wait for GeoLocation utility to be ready
  if (GeoLocation.isReady()) {
      readyStatus.geoLocation = true;
      init();
  } else {
    PubSub.subscribe(GeoLocation.TOPICS.services_ready, function () {
      readyStatus.geoLocation = true;
      init();
    });
  }

  // Wait for ReportingArea utility to be ready
  if (ReportingArea.isReady()) {
    readyStatus.reportingArea = true;
    init();
  } else {
    PubSub.subscribe(ReportingArea.TOPICS.services_ready, function() {
      readyStatus.reportingArea = true;
      init();
    });
  }
})(jQuery, Drupal);
