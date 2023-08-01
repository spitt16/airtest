(function($, Drupal) {
  // Create Storage namespace
  let PubSub = window.PubSub;
  let AirNowGov = window.AirNowGov;
  let Storage = AirNowGov.Storage;
  let PageLoader = AirNowGov.PageLoader;
  let GeoLocation = AirNowGov.GeoLocation = {};
  let Geocoder = null;

  const STORAGE_KEY = "Location";
  const AUTOCOMPLETE_DELAY_MILLISECONDS = 500; // 1/2 a second
  const KEY_CODES = {
    "ENTER": 13,
    "LEFT": 37,
    "UP": 38,
    "RIGHT": 39,
    "DOWN": 40
  };

  const TOPIC_BASE = AirNowGov.APP_NAME + "." + STORAGE_KEY;
  const TOPICS = GeoLocation.TOPICS = {
    "new_location": TOPIC_BASE + ".new_location",
    "services_ready": TOPIC_BASE + ".services_ready",
  };

  const STATE_CODES = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
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

  // True if we pull a location from the url.  If true, we won't prompt for user's GPS location
  let urlLocation = false;
  let servicesReady = false;
  let user_selected_location = false;

  function getLocation() {
    let item = Storage.getItem(STORAGE_KEY);
	  if (!item) {
      item = saveLocation({
        "latitude": null,
        "longitude": null,
        "displayName": "N/A",
        "cityName": "N/A",
        "stateName": "N/A",
        "stateCode": "N/A",
        "countryCode": "N/A",
        "isStateSearch": false,
        "geolocation": false,
        "utcOffset": false
      });
    }
    return item.data;
  }

  function saveLocation(location, silent) {
    let item = Storage.storeItem(STORAGE_KEY, location);
    if (silent !== true) {
      PubSub.publish(TOPICS.new_location, true);
    }
    return item;
  }

  let getLocationDisplayName = GeoLocation.getLocationDisplayName = function() {
    let location = getLocation();
    if (!location.latitude && !location.longitude) {
      return false;
    }
    return location.displayName;
  };

  let getLocationStateName = GeoLocation.getLocationStateName = function() {
    let location = getLocation();
    if (!location.latitude && !location.longitude) {
      return false;
    }
    return location.stateName ;
  };

  let getLatLng = GeoLocation.getLatLng = function() {
    let location = getLocation();
    if (!location.latitude && !location.longitude) {
      return false;
    }
    return {lat: location.latitude, lng: location.longitude};
  };

  let getLatLngTimezone = GeoLocation.getLatLngTimezone = function(callback) {
    let location = getLocation();
    if (!location.latitude && !location.longitude) {
      callback(false);
    }

    callback(location.utcOffset);
  };

  let getStateCode = GeoLocation.getStateCode = function() {
    let location = getLocation();
    if (!location.latitude && !location.longitude) {
      return false;
    }
    return location.stateCode;
  };

  let isStateSearch = GeoLocation.isStateSearch = function() {
    let location = getLocation();
    if (!location.latitude && !location.longitude) {
      return false;
    }
    return location.isStateSearch;
  };

  let getCityName = GeoLocation.getCityName = function() {
    let location = getLocation();
    if (!location.latitude && !location.longitude) {
      return false;
    }
    return location.cityName;
  }

  let getCountryCode = GeoLocation.getCountryCode = function() {
      let location = getLocation();
      if (!location.latitude && !location.longitude) {
        return false;
      }
      return location.countryCode;
    };

  let getUserSelectedLocation = GeoLocation.getUserSelectedLocation = function() {
    return user_selected_location;
  };

  let resetUserSelectedLocation = GeoLocation.resetUserSelectedLocation = function() {
    user_selected_location = false;
  };

  function lookupLocation(response, type, latlng) {
    // IE11 fix - ES6 introduced defaulted function parameters, but sadly ES6 is not supported in IE11.
    latlng = typeof latlng !== "undefined" ? latlng : null;
    // These four variables are the set differently depending on what type of call is made
     //<!-- latlng = null; // AirNowDrupal #107 IE fix cw 2019-03-08 // This change Reversed on 2019-04-10 -->
	user_selected_location = (type === "SearchInput" || type === "UpdateUserLocation");
    let location, city, state, countryCode;
    if (type === "CityStateCountry") {
      location = {
        lat: response.candidates[0].location.y,
        lng: response.candidates[0].location.x
      };
      let attributes = response.candidates[0].attributes;
      city = attributes.City.length ? attributes.City : attributes.SubRegion; // ArcGIS findAddressCandidates provides "SubRegion" with an uppercase 'R'
      state = attributes.Region;
      countryCode = attributes.Country;
    } else if (type === "SearchInput") {
      location = {
        lat: response.result.feature.geometry.y,
        lng: response.result.feature.geometry.x
      };
      let attributes = response.result.feature.attributes;
      city = attributes.City.length ? attributes.City : "";
      state = attributes.Region;
      countryCode = attributes.Country;
    } else {
      location = latlng;
      let address = response.address;
      city = address.City.length ? address.City : address.Subregion; // ArcGIS reverseGeocode provides "Subregion" with a lowercase 'r'
      state = address.Region;
      countryCode = address.CountryCode;
    }

    // These are overrides for the two locations in Mexico due to differences in how ESRI provides the information
    // compared to how we want to present that information for the locations in Mexico.
    if ((state === "The Federal District" || state === "Mexico City") && countryCode === "MEX") {
      city = "Mexico City";
      state = "";
      countryCode = "MEX";
    } else if (state === "Baja California") {
      state = "";
      countryCode = "MEX";
    } else if (!state && countryCode) {
      if (countryCode !== "USA") {
        state = "";
      }
    }

    if (type === "LatLong" || type === "SearchInput") {
      if (!state && countryCode === "USA") {
        // TODO: Display a message to user
        return;
      }
      if (!city) {
        redirectToStatePage(state);
        return;
      }
    } else {
      if (!city && !state) {
        // TODO: Display a message to user
        return;
      }
    }

    state = typeof STATE_CODES[state] !== "undefined" ? state.trim() : "";
    let displayName = city;
    if (state.length) {
      displayName += ", " + STATE_CODES[state];
    } else if (countryCode.length && countryCode !== "USA") {
      displayName += ", " + countryCode;
    }
    if (type === "CityStateCountry" || type === "SearchInput") {
      let sessionLocation = getLocation();
      let newSessionLocation = {
        latitude: location.lat,
        longitude: location.lng,
        displayName: displayName,
        cityName: city,
        stateName: state,
        stateCode: state.length ? STATE_CODES[state] : "",
        countryCode: countryCode,
        isStateSearch: false,
        geolocation: (type ===  "CityStateCountry" ? true : sessionLocation.geolocation)
      };
      if (type === "SearchInput" && newSessionLocation.isStateSearch) {
        window.open("/state/?name=" + newSessionLocation.stateName.replace(/ /g, "-").toLowerCase(), "_self"); //AirNowDrupal #196 cw 2019-09-20
      }
      saveLocation(newSessionLocation);
    } else {
      state = typeof STATE_CODES[state] !== "undefined" ? state.trim() : "";
      let updatedSessionLocation = {
        latitude: location.lat,
        longitude: location.lng,
        displayName: displayName,
        cityName: city,
        stateName: state,
        stateCode: state.length ? STATE_CODES[state] : "",
        countryCode: countryCode,
        isStateSearch: false,
        geolocation: true
      };
      saveLocation(updatedSessionLocation);
    }
  }

  // TODO: Rename to "updateUserLocation"
  let requestUserLocation = GeoLocation.requestUserLocation = function() {
    //AIR 281 Geolocation feedback cw 2021-08-30
    console.log("navigator.geolocation has been clicked!");
    navigator.geolocation.getCurrentPosition(successCallback, errorCallback) // Attepmt to use Geolocation

    function successCallback() {
      console.log("Success!");
      let geoLocationElement = document.getElementById("tippy-10");  // close a possible open "geolocation" tippy
       if (!(geoLocationElement == null)) {
        geoLocationElement.style.visibility="hidden";
      }
    }

    function errorCallback(error) {
      //showGeolocationError(error)
    }

   // Error Handling for GeoLocation via Javascript Alert boxes. cw 2021-08-25
   function showGeolocationError(error) {
     switch(error.code) {
       case error.PERMISSION_DENIED:
         console.log("Browser denied the request for your location." );
         alert("Browser denied the request for your location.\n\nThis feature may be blocked by your system administrator." );
         break;
       case error.POSITION_UNAVAILABLE:
        console.log("Location information is unavailable." );
        alert("Location information is unavailable.\n\nThis feature may be blocked by your system administrator." );
         break;
       case error.TIMEOUT:
        console.log("The request to get location timed out." );
        alert("The request to get location timed out." );
         break;
       case error.UNKNOWN_ERROR:
         console.log("An unknown error occurred." );
         alert("An unknown error occurred." );
         break;
     }
   }

   navigator.geolocation.getCurrentPosition(function(position) {
      let latlng = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      $.ajax({
        type: "GET",
        url: "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?f=json&langCode=EN&featureTypes=PointAddress,Locality,Postal&location=" + latlng.lng + "," + latlng.lat,
        context: this,
        success: function (response) {
          lookupLocation(response, "UpdateUserLocation", latlng);
        },
        error: function (response) {
          // TODO: Handle errors
          console.error(response);
        }
      });
    });
  };

  function redirectToStatePage(stateName) {
    window.open("/state/?name=" + stateName.replace(/ /g, "-").toLowerCase(), "_self");  //AirNowDrupal #196 cw 2019-09-20
  }

  let lookupLocationByLatLng = GeoLocation.lookupLocationByLatLng = function(latlng, fromUrl) {
    urlLocation = fromUrl === true;

    $.ajax({
      type: "GET",
      url: "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?f=json&langCode=EN&featureTypes=PointAddress,Locality,Postal&location=" + latlng.lng + "," + latlng.lat,
      context: this,
      success: function (response) {
        lookupLocation(response, "LatLong", latlng);
      },
      error: function (response) {
        // TODO: Handle errors
        console.error(response);
      }
    });
  };

  // FIXME
  let lookupLocationByCityStateCountry = GeoLocation.lookupLocationByCityStateCountry = function(city, state, country, fromUrl) {
    urlLocation = fromUrl === true;

    let query = "";
    if (city && state && !country) {
      query = "city=" + city + "&region=" + state;
    } else if (city && !state && country) {
      query = "city=" + city + "&countryCode=" + country;
    } else if (city && state && country) {
      query = "city=" + city + "&region=" + state + "&countryCode=" + country;
    }

    if (query) {
      $.ajax({
        type: "GET",
        url: "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?f=json&langCode=EN&outFields=PlaceName,Type,City,Country,Addr_type,Region,SubRegion&" + query,
        context: this,
        success: function (response) {
            lookupLocation(response, "CityStateCountry");
        },
        error: function (response) {
          // TODO: Handle errors
          console.error(response);
        }
      });
    }
  };

  let enableGeolocationLookupField = GeoLocation.enableGeolocationLookupField = function(className) {
    let link_tag = document.createElement('link');
    link_tag.setAttribute("rel", "stylesheet");
    link_tag.setAttribute("href", "https://js.arcgis.com/3.26/esri/css/esri.css");
    (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(link_tag);

    let script_tag = document.createElement('script');
    script_tag.setAttribute("type", "text/javascript");
    script_tag.setAttribute("src", "https://js.arcgis.com/3.26/");
    if (script_tag.readyState) {
      script_tag.onreadystatechange = function () {
        // For old versions of IE
        if (this.readyState == 'complete' || this.readyState == 'loaded') {
          onArcgisLoadCallback();
        }
      };
    } else {
      // Other browsers
      script_tag.onload = onArcgisLoadCallback;
    }
    (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);

    function onArcgisLoadCallback() {
      PubSub.publish(TOPICS.services_ready, true);
      servicesReady = true;

      let inputs = document.getElementsByClassName(className);
      let sessionLocation = getLocation();

      for (let i = 0; i < inputs.length; i++) {
        let input = inputs[i];

        require([
          "esri/dijit/Search",
          "esri/tasks/locator"
        ], function (Search, Locator) {
          let search = new Search({
            allPlaceholder: "ZIP Code, City, or State",
            enableSourcesMenu: false,
            activeSourceIndex: "all",
            sources: [{
              locator: new Locator("//geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer"),
              categories: ["City", "Region", "Postal"],
              countryCode: "US",
              outFields: ["PlaceName", "Type", "City", "Region", "Country", "Addr_type"],
              maxSuggestions: 5,
              name: "USA",
              placeholder: "ZIP Code, City, or State",
              singleLineFieldName: "SingleLine"
            }]
            // AirNow Drupal #149 - Removing Mexico from suggestions to promote up the Reporting Area list
            //   locator: new Locator("//geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer"),
            //   categories: ["City", "Region", "Postal"],
            //   countryCode: "MX",
            //   outFields: ["PlaceName", "Type", "City", "Region", "Country", "Addr_type"],
            //   maxSuggestions: 3,
            //   name: "Mexico",
            //   placeholder: "ZIP Code, City, or State",
            //   singleLineFieldName: "SingleLine"
            // }]
          }, input.id);

          search.on("clear-search", function(event, a) {
            let searchWidget = this;
            let $this = $("#"+searchWidget.id);
            let suggestionsMenu = $this.find(".searchMenu.suggestionsMenu");
            suggestionsMenu.toggleClass("show", false);
          });

          search.on("suggest-results", function(event, a) {
            let searchWidget = this;
            let $this = $("#"+searchWidget.id);
            let suggestionsMenu = $this.find(".searchMenu.suggestionsMenu");

            // Manually add the header "USA" to the 1st set of suggestions
            let suggestionsMenuDiv = suggestionsMenu.children("div");
            if (suggestionsMenuDiv.length) {
              suggestionsMenuDiv
                .prepend($("<div></div>")
                  .addClass("menuHeader")
                  .text("USA"));
            }

            // Request Reporting Area suggestions, and add them to the suggestions dropdown UI
            $.ajax({
              type: "GET",
              url: AirNowGov.API_URL + "reportingarea/suggestions",
              data: {
                "term": event.value,
                "maxSuggestions": 5
              },
              context: this,
              success: function (response) {
                if (response && response.length > 0) {
                  let reportingAreaMenu = $("<ul></ul>").attr("role", "menu");
                  let hasValidSuggestion = false;
                  for (let i = 0; i < response.length; i++) {
                    hasValidSuggestion = true;
                    let suggestionHtml = "<strong>" + response[i].slice(0, event.value.length) + "</strong>" + response[i].slice(event.value.length, response[i].length);
                    let menuItem = $("<li></li>")
                      .attr("data-index", i)
                      .attr("role", "menuitem")
                      .attr("tabindex", 0)
                      .attr("data-suggestion", response[i])
                      .html(suggestionHtml);
                    reportingAreaMenu.append(menuItem);
                    menuItem.on("click", function (e) {
                      let suggestion = $(this).data("suggestion");
                      let reportingAreaName = suggestion;
                      let stateCode = "";
                      if (suggestion.charAt(reportingAreaName.length - 4) === ",") {
                        reportingAreaName = suggestion.slice(0, suggestion.length - 4);
                        stateCode = suggestion.slice(suggestion.length - 2, suggestion.length);
                      } else {
                        reportingAreaName = suggestion;
                        stateCode = "";
                      }
                      suggestionsMenu.toggleClass("show", false);
                      searchWidget.clear();
                      AirNowGov.ReportingArea.lookupLocationByReportingAreaStateCode(reportingAreaName, stateCode, function (response) {
                        if (response && response.latitude && response.longitude) {
                          $(".searchGroup.showSuggestions").removeClass("showSuggestions");
                          $(".searchInput").val("");
                          // Lookup location by lat/lon
                          lookupLocationByLatLng({
                            lat: Number(response.latitude),
                            lng: Number(response.longitude)
                          }, true);
                        }
                      });
                    });
                  }
                  if (!hasValidSuggestion) {
                    return;
                  }
                  if (!suggestionsMenuDiv.length) {
                    suggestionsMenuDiv = $("<div></div>");
                    suggestionsMenu.append(suggestionsMenuDiv).toggleClass("show", true);
                  }
                  suggestionsMenuDiv
                    .append($("<div></div>")
                      .addClass("menuHeader")
                      .text("Reporting Area"))
                    .append(reportingAreaMenu);
                }
              },
              error: function (response) {
                console.error(response);
              }
            });

          });

          search.on("select-result", function (event) {
            lookupLocation(event, "SearchInput");
            $(".searchInput").val("");
          });

          search.startup();
        });
      }

    }

    // // FIXME: Determine if custom locations should be a "source"
    // function buildCustomSuggestions(currentInput) {
    //   let text = $(currentInput).val();
    //
    //   let matching = [];
    //   for (let idx in data) {
    //     let d = data[idx];
    //
    //     if (d.reportingarea.substr(0, text.length).toUpperCase() === text.toUpperCase()) {
    //       matching.push(d);
    //     }
    //   }
    //
    //   $(".custom-pac-item").remove();
    //
    //   setTimeout(function() {
    //     $(".custom-pac-item").remove();
    //     for (let i = 0; i < 2 && matching[i]; i++) {
    //       let d = matching[i];
    //       $(".pac-container")
    //         .append($("<div>")
    //           .attr("id", "custom-pac-item-" + i)
    //           .addClass("pac-item")
    //           .addClass("custom-pac-item")
    //           .on("mousedown", function () {
    //             let inputs = document.getElementsByClassName(className);
    //             let latlng = {
    //               lat: d.latitude,
    //               lng: d.longitude
    //             };
    //
    //             for(let i = 0; i < inputs.length; i++) {
    //               $(inputs[i]).val("");
    //             }
    //
    //             // Lookup location by lat/lon
    //             lookupLocationByLatLng(latlng);
    //           })
    //           .append($("<span>")
    //             .addClass("pac-icon"))
    //           .append($("<span>")
    //             .addClass("pac-item-query")
    //             .html("<b>" + d.reportingarea.substr(0, text.length) + "</b>" + d.reportingarea.substr(text.length, d.reportingarea.length)))
    //           .append($("<span>")
    //             .text(d.state_code + ", USA")));
    //     }
    //   }, 250);
    // }
    //
  };

  let isReady = GeoLocation.isReady = function() {
    return servicesReady;
  }
})(jQuery, Drupal);
