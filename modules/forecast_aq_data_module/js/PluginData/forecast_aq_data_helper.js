(function ($, Drupal) {
  Drupal.behaviors.forecastAQDataHelper = {
    attach: function (context, settings) {
      // console.log("Forecast AQ Data Helper (Original)");

      const DAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      let PubSub = Drupal.behaviors.PubSub;
      let AirNowGov = Drupal.behaviors.AirNowGov;
      let ReportingArea = AirNowGov.ReportingArea;
      let GeoLocation = AirNowGov.GeoLocation;

      let primaryPollutantCardExpanded = true; // AirNowDrupal #143 Forecast Primary Pollutant starts open cw 2019-05-31

      let dataProviderMapLoaded = false;
      let reportingAreaDataLoaded = false;
      let hasForecastProvider = false;

      function getDayName(dayOffset) {
        let today = new Date();
        let todayDayOfWeek = today.getDay(); // 0 - sunday, 6 - saturday
        let offsetDayOfWeek = (todayDayOfWeek + dayOffset) % 7;

        if (offsetDayOfWeek === todayDayOfWeek) {
          return "Today";
        } else if (offsetDayOfWeek === (todayDayOfWeek + 1)) {
          return "Tomorrow";
        }
        return DAY_NAMES[offsetDayOfWeek];
      }

      function toggleNoDataDisplay(noData) {
        $(".band-forecast-aq-row").closest(".band-style-general").toggleClass("noData", noData);
      }


      $(document).ready(function() {
        PubSub.subscribe(ReportingArea.TOPICS.new_data, function() {
          hasForecastProvider = false;
          reportingAreaDataLoaded = true;
          clearData();
          populateData();
          setForecastProvider();
        });
        PubSub.subscribe(ReportingArea.TOPICS.new_dataproviders, function() {
          setForecastProvider();
        });
        populateData();
        setForecastProvider();
      });

      function populateData() {
        let todayPrimaryData = ReportingArea.getMaxForecastReportingAreaData(0);
        let todayOtherData = ReportingArea.getOtherForecastReportingAreaData(0);
        let locationDisplayName = GeoLocation.getLocationDisplayName();

        let hasData = todayPrimaryData || todayOtherData || locationDisplayName,
            hasAvailableData = (todayPrimaryData && locationDisplayName.length > 0) || todayOtherData.length > 0;

        toggleNoDataDisplay(!hasData);

        if (hasData) {
          reportingAreaDataLoaded = true;
          let fullDiscussion = todayPrimaryData ? todayPrimaryData[ReportingArea.FIELDS.discussion] : "";
          let charTrimNum = 140; // number of characters shown
          let shortDiscussion = fullDiscussion.length > charTrimNum ? fullDiscussion.substring(0, charTrimNum).trim() + "..." : fullDiscussion;

          if(fullDiscussion.length > 0) {
            // if(!$(".forecast-aq-discussion").hasClass("has-discussion")) {
              $(".forecast-aq-discussion").toggleClass("no-discussion", false).toggleClass("has-discussion", true);
            // }

            // show short discussion by default
            let showFull = false;
            $('#forecastDiscussion').html("<span class='forecast-discussion-title'>Forecast Discussion:</span> " + shortDiscussion);

            // When Discussion link clicked, toggle discussion message between full and short
            $('#forecastDiscussionLink').text("Full Forecast Discussion").click(function () {
              showFull = !showFull;
              if (showFull) {
                $('#forecastDiscussion').html("<span class='forecast-discussion-title'>Forecast Discussion:</span> " + fullDiscussion);
                $('#forecastDiscussionLink').text("Minimize Forecast Discussion");
              } else {
                $('#forecastDiscussion').html("<span class='forecast-discussion-title'>Forecast Discussion:</span> " + shortDiscussion);
                $('#forecastDiscussionLink').text("Full Forecast Discussion");
              }
            });
          } else {
            $('#forecastDiscussion').html("");
            $('#forecastDiscussionLink').html("");
            if (!hasForecastProvider) {
              $(".forecast-aq-discussion").toggleClass("has-discussion", false).toggleClass("no-discussion", true);
            }
            // if($(".forecast-aq-discussion").hasClass("has-discussion") || !$(".forecast-aq-discussion").hasClass("no-discussion")) {
            //   $(".forecast-aq-discussion").removeClass("has-discussion").addClass("no-discussion");
            // }
          }


          // FIXME: These day boxes need a click event.  When clicked, it should populate the cards with the corresponding dayOffset (0 - 6)
          // EX: let selectedPrimaryData = ReportingArea.getMaxForecastReportingAreaData(selectedDayNumber);
          //     let selectedOtherData = ReportingArea.getOtherForecastReportingAreaData(selectedDayNumber);
          let startingTranslucent = 0.05;
          let lastDayWithData = -1;
          for (let i = 0; i < 6; i++) {
            (function(ReportingArea, i) {
              let dayPrimaryData = ReportingArea.getMaxForecastReportingAreaData(i);
              let aqi = "";
              let category = "Not Available";
              let parameter = "&nbsp;";
              let isActionDay = false;

              if (dayPrimaryData) {
                aqi = dayPrimaryData[ReportingArea.FIELDS.aqi];
                category = dayPrimaryData[ReportingArea.FIELDS.category];
                parameter = dayPrimaryData[ReportingArea.FIELDS.parameter];
                lastDayWithData = i;
                isActionDay = dayPrimaryData[ReportingArea.FIELDS.isActionDay];
        
        // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
				/*if (aqi > 500) {
			      category = "Beyond the AQI"; // cw 2019-10-08
                }*/
              } else {
                aqi = "";
                category = "Not Available";
                parameter = "&nbsp;";
              }
              let actionDayText = "";
              if (isActionDay) {
                actionDayText = "<br /><span class='action-day'>(!) Action Day</span>"
              }
              $('#day-' + i + ' .day-name').html(getDayName(i) + actionDayText);

              $('#day-' + i + ' .day-aqi-value').text(aqi !== undefined ? aqi : "");
              $('#day-' + i + ' .day-status').text(category);
              $('#day-' + i + ' .day-pollutant').html(parameter);
              $('#day-' + i + ' .day-status-image')
                .toggleClass("good", category === "Good")
                .toggleClass("moderate", category === "Moderate")
                .toggleClass("unhealthy-sensitive", category === "Unhealthy for Sensitive Groups")
                .toggleClass("unhealthy", category === "Unhealthy")
                .toggleClass("very-unhealthy", category === "Very Unhealthy")
                .toggleClass("hazardous", category === "Hazardous"          // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
                /*|| category === "Beyond the AQI"*/) // Added Beyond Index; Getting correct "toggle" for Primary Pollutant in Current Air Quality cw 2019-10-10
                .attr("title", "AQI " + (aqi !== undefined ? aqi : "") + " - " + (category !== undefined ? category : ""));

              let translucentAmt = 0,
                  currentDay = $('.day-shade-' + i);
              if (i < 1) {
                translucentAmt = (- 1) * startingTranslucent;
              } else if (i > 1) {
                translucentAmt = (i - 1) * startingTranslucent;
              }

              let dayShade = shadeDayColor(translucentAmt);
              currentDay.css('background-color', dayShade);
              currentDay.find('.mobile-day-caret-triangle').css('border-top-color', dayShade);

              $('#day-' + i).on("click.forecastDay", function (event) {
                $(".forecast-aq-band-row").find(".pollutant-card.primary-pollutant-card")
                  .toggleClass("good", false)
                  .toggleClass("moderate", false)
                  .toggleClass("unhealthy-sensitive", false)
                  .toggleClass("unhealthy", false)
                  .toggleClass("very-unhealthy", false)
                  .toggleClass("hazardous", false);
                changeDayCards(event, i, hasAvailableData);
              });
            })(ReportingArea, i);
          }

          // Hide trailing day cards that have no data.  Make sure to restore days with data
          for (let i = 0; i < 6; i++) {
            // $("#day-holder-" + i).toggle(i <= lastDayWithData);
            if (i > lastDayWithData && i >= 2) {
              $("#day-holder-" + i).find('.day').css("visibility", "hidden");
              $("#day-holder-" + i).addClass("na-holder");
              $("#day-holder-" + i).css("background-color", "");
            } else {
              $("#day-holder-" + i).find('.day').css("visibility", "visible");
              $("#day-holder-" + i).removeClass("na-holder");
            }
          }

          // if (todayPrimaryData) {
            createPollutantCard(
              $(".band-forecast-aq-row .primary-pollutant-card"),
              "forecast-aq-primary",
              "Primary Pollutant",
              "This pollutant currently has the highest forecasted AQI in the area.",
              [todayPrimaryData],
              true,
              hasAvailableData
            );
          // }

          if (todayOtherData) {
            createPollutantCard(
              $(".band-forecast-aq-row .other-pollutants-card"),
              "forecast-aq-other",
              "Other Pollutants",
              " ",
              todayOtherData,
              false,
              hasAvailableData
            );
          }
        }

        setForecastDaysDataMessage(hasAvailableData);

        setMobileDayHeights(".days .day", '(max-width: 767px)');
        $(window).off("resize.mobileDayHeights");
        $(window).on("resize.mobileDayHeights", function () {
          setMobileDayHeights(".days .day", '(max-width: 767px)');
        });
      }

      function shadeDayColor(percent) {
        let color = "#167fac";
        let hexCode = parseInt(color.slice(1), 16),
            shade = percent < 0 ? 0 : 255,
            percentAbs = percent < 0 ? percent*-1 : percent,
            R=hexCode>>16,
            G=hexCode>>8&0x00FF,
            B=hexCode&0x0000FF;
        return "#"+(0x1000000+(Math.round((shade-R)*percentAbs)+R)*0x10000+(Math.round((shade-G)*percentAbs)+G)*0x100+(Math.round((shade-B)*percentAbs)+B)).toString(16).slice(1);
      }

      function setForecastDaysDataMessage(hasAvailableData) {
        if(hasAvailableData) {
          // if($(".forecast-aq-days").hasClass("no-data") || !$(".forecast-aq-days").hasClass("has-data")) {
            $(".forecast-aq-days").removeClass("no-data").addClass("has-data");
          // }
        } else {
          // if($(".forecast-aq-days").hasClass("has-data") || !$(".forecast-aq-days").hasClass("no-data")) {
            $(".forecast-aq-days").removeClass("has-data").addClass("no-data");
          // }
        }
      }

      function clearData() {
        $(".band-forecast-aq-row .primary-pollutant-card").find(".pollutants-list").empty();
        $(".band-forecast-aq-row .other-pollutants-card").find(".pollutants-list").empty();
        $(".pollutant-card").removeClass("good moderate unhealthy-sensitive unhealthy very-unhealthy hazardous");
      }

      function changeDayCards(event, selectedDayNumber, hasAvailableData) {
        let selectedPrimaryData = ReportingArea.getMaxForecastReportingAreaData(selectedDayNumber),
            selectedOtherData = ReportingArea.getOtherForecastReportingAreaData(selectedDayNumber);
        $(".band-forecast-aq-row .pollutants-list").empty();

        createPollutantCard(
          $(".band-forecast-aq-row .primary-pollutant-card"),
          "forecast-aq-primary",
          "Primary Pollutant",
          "This pollutant currently has the highest forecasted AQI in the area.",
          [selectedPrimaryData],
          true,
          hasAvailableData
        );

        createPollutantCard(
          $(".band-forecast-aq-row .other-pollutants-card"),
          "forecast-aq-other",
          "Other Pollutants",
          " ",
          selectedOtherData,
          false,
          hasAvailableData
        );

        $(".day-holder").find(".show-day-caret").removeClass("show-day-caret");
        $("#day-holder-"+selectedDayNumber).find(".day-caret").addClass("show-day-caret");
      }

      function createPollutantCard(pollutantCard, uniqueId, title, subtext, reportingareaData, isPrimary, hasAvailableData) {
        pollutantCard.find(".pollutant-title-section .pollutant-card-title").text(title);

        if(subtext != null) {
          pollutantCard.find(".pollutant-title-section .pollutant-card-title-subtext").text(subtext);
        }

        if(typeof reportingareaData == "undefined" ||  reportingareaData.length == 0 || !hasAvailableData) {
          let noPollutantDiv = $('<div/>', {
              'class': 'no-pollutant-info'
            }).append($('<p/>', {
              'text': 'No ' + title + ' Available'
            })),
            pollutantList = pollutantCard.find(".pollutants-list");

          pollutantCard.addClass("show-none-text");
          // pollutantCard.parent().addClass("hidden-xs");
          pollutantList.append(noPollutantDiv);
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

      function appendPollutantInfo(pollutantCard, id, title, category, aqi, isPrimary) {
        let pollutantList = pollutantCard.find(".pollutants-list");
        if(typeof id != "undefined" &&
          typeof title != "undefined") {
          pollutantList.append(constructPollutantInfo(id, title, category, aqi, isPrimary));
        }

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
        
         // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
		  /*if (aqi < 501) {
		    aqiStatusClass = "hazardous"; // maroon, hazardous
            aqiCategoryMessageKey = "hazardous";
		  } else {
            aqiStatusClass = "hazardous";
            aqiCategoryMessageKey = "beyond_aqi"; // Added Beyond AQI cw 2019-10-10
			category = "Beyond the AQI"; // cw 2019-10-10
          }*/
		}

        if (isPrimary === true) {
          $(".forecast-aq-band-row").find(".pollutant-card.primary-pollutant-card")
            .toggleClass("good", category === "Good")
            .toggleClass("moderate", category === "Moderate")
            .toggleClass("unhealthy-sensitive", category === "Unhealthy for Sensitive Groups")
            .toggleClass("unhealthy", category === "Unhealthy")
            .toggleClass("very-unhealthy", category === "Very Unhealthy")
            .toggleClass("hazardous", category === "Hazardous"          // AirNowDrupal #538 eb 2023-06-15 Removed code that displayed Beyond the AQI
            /*|| category === "Beyond the AQI"*/);  // Added Beyond Index; Getting correct "toggle" for Primary Pollutant in Current Air Quality cw 2019-10-10
        }

        let extendedMessage;
        if (settings.planYourDayDescriptions.hasOwnProperty(parameter.toLowerCase())) {
          if (settings.planYourDayDescriptions[parameter.toLowerCase()].hasOwnProperty(aqiCategoryMessageKey)) {
            extendedMessage = settings.planYourDayDescriptions[parameter.toLowerCase()][aqiCategoryMessageKey].forecast;
          } else {
            extendedMessage = settings.planYourDayDescriptions.default[aqiCategoryMessageKey].forecast;
          }
        } else {
          extendedMessage = settings.planYourDayDescriptions.default[aqiCategoryMessageKey].forecast;
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
            'class': 'fa fa-caret-right',  // AirNowDrupal # 117 Do NOT hide forecast caret in mobile cw 2019-04-09
            'aria-hidden': 'true'
          }),
          headingStatusDiv = $('<div/>', {
            // 'style': 'color: ' + aqiTextColor + '; background-color: ' + aqiBackgroundColor + ';', //TODO: Replace with class
            'class': 'col-xs-2 pi-heading-status pollutant-status-circle text-center ' + aqiStatusClass, // TODO: call it "-aqibubble" (or something like that) instead of "-status"
            'text': aqi,
            'title': "AQI " + aqi + " - " + category
          }),
          headingMessageDiv = $('<div/>', {
            'class': 'pi-heading-message col-xs-5', // TODO: call it "-category" instead of "-message"
            'text': category
          }),
          //pollutantInfoSubDiv = $('<div/>', {
          //  'class': 'col-xs-12 pollutant-info-sub ' + hideClass
          //}).append("<h4><b>Plan Your Day</b></h4>" + extendedMessage);

		  // AirNowDrupal # 106 Line and Plan Your Day label removed cw 2019-02-26
		  pollutantInfoSubDiv = $('<div/>', {
            'class': 'col-xs-12 pollutant-info-sub ' + hideClass
          }).append(extendedMessage);

        if (isPrimary === true && primaryPollutantCardExpanded === true) {
          // Toggle arrow direction based on if Plan Your Day is collapsed or not
          headingTitleCaret
            .toggleClass("fa-caret-right", !primaryPollutantCardExpanded)
            .toggleClass("fa-caret-down", primaryPollutantCardExpanded);
        }

        if(isPrimary) {
          let headingPrimaryPollutantMobileLabel = $("<span/>", {
            'class': 'visible-xs pp-label-mobile',
            'text': 'Primary Pollutant'
          });

          pollutantInfoHeadingDiv.append(headingPrimaryPollutantMobileLabel);
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

      function setForecastProvider() {
        if (!reportingAreaDataLoaded) {
          return;
        }

        let forecastProviderContainer = $(".forecastProvider");
        forecastProviderContainer.empty(); // remove all children

        let radps = ReportingArea.getReportingAreaDataProviders();
        let forecastProvider = radps.forecastProvider; // Primary Agency
        let forecastProviderURL = radps.forecastProviderURL; // Primary Agency
        let reportingAreaID = radps.id;
        let twcCityCode = radps.twcCityCode;

        if (forecastProvider) {
          hasForecastProvider = true;
          forecastProviderContainer.append("<p class='forecastProviderLabel'><b>Forecast courtesy of</b></p>");
          if (forecastProviderURL) {
            forecastProviderContainer.append("<p class='forecastProviderAgency'><a href='" + forecastProviderURL + "' target='_blank'>" + forecastProvider + "</a></p>");
          } else {
            forecastProviderContainer.append("<p class='forecastProviderAgency'>" + forecastProvider + "</p>");
          }


          $(".forecast-aq-discussion").toggleClass("no-discussion", false).toggleClass("has-discussion", true);
        } else {
          hasForecastProvider = false;
        }
      }
    }
  };

  function setMobileDayHeights(dayClasses, mqValue) {
    if(mqValue == null) {
      mqValue = 'all';
    }

    $(dayClasses).css('height', "");

    let mq = window.matchMedia(mqValue);
    let minHeight = 0;

    $(dayClasses).each(function(k, v) {
      if($(v).height() > minHeight) {
        minHeight = $(v).height();
      }
    });

    if(mq.matches) {
      $(dayClasses).css('height', minHeight+'px');
    } else {
      $(dayClasses).css('height', "");
    }

	// AirNowDrupal # 141 Mobile i icon on Air Quality Forecast title cw 2019-09-12
	if (navigator.userAgent.match(/(iPod|iPhone|iPad|Android)/)) { // Only on Mobile
		let currentTitle = document.getElementById("forecast-aq-band").innerHTML; // Capture current label
		if (currentTitle.indexOf("button_info.png") <= 0) { // Only the first time
			document.getElementById("forecast-aq-band").innerHTML = currentTitle + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img alt='Air Quality Forecast Icon' class='forecast-aq-band-i-icon' src='/themes/anblue/images/icons/button_info.png' width='25' height='25'>"; // Add info icon
			let Tooltips = AirNowGov.Tooltips;
			Tooltips.createTip(".forecast-aq-band-i-icon", "airQualityForecast", "bottom"); // Create the Tooltips
		};
	};
  }
})(jQuery, Drupal);
