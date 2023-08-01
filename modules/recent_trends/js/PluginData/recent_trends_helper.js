(function ($, Drupal) {
  Drupal.behaviors.recentTrendsHelper = {
    attach: function (context, settings) {
      let PubSub = Drupal.behaviors.PubSub;
      let AirNowGov = Drupal.behaviors.AirNowGov;
      let ReportingArea = AirNowGov.ReportingArea;
      let GeoLocation = AirNowGov.GeoLocation;
      let Tooltips = AirNowGov.Tooltips;

      const S3_BUCKET_URL = AirNowGov.API_URL + "andata";
      const DAY_IDX = 0;
      const WEEK_IDX = 1;
      const MONTH_IDX = 2;

      let chart = [false, false, false];
      let chartId = ["chart", "chart-week", "chart-month"];
      let chartSeriesData = [[], [], []];
      let chartReportingAreaName = ["", "", ""];
      let chartReportingAreaState = ["", "", ""];
      let chartTimezoneLabel = ["", "", ""];


      $(document).ready(function() {
        PubSub.subscribe(ReportingArea.TOPICS.new_data, function() {
          populateData();
        });

        handleAqiLegend();
        populateData();
      });


      function populateData() {
        let primaryData = ReportingArea.getMaxCurrentReportingAreaData();
        let latLng = GeoLocation.getLatLng();

        let hasData = primaryData || latLng;

          let allReportingAreas = ReportingArea.getAllReportingAreaData();
          for (let i = 0; i < chart.length; i++) {
            let chartMode = i === DAY_IDX ? "day" : i === WEEK_IDX ? "week" : "month";
            chartTimezoneLabel[i] = primaryData[ReportingArea.FIELDS.timezone];
            createChart(chartMode);
            if (allReportingAreas && allReportingAreas.length) {
              setChartData(chartMode, allReportingAreas[0][ReportingArea.FIELDS.reportingAreaName], allReportingAreas[0][ReportingArea.FIELDS.stateCode]);
            } else {
              chart[i].setTitle({text: "AQI Data Unavailable"});
              chart[i].series[0].setData([]);
              chart[i].xAxis[0].update({
                title: {
                  text: ""
                }
              });
              chart[i].redraw();
            }
          }

      }

      function createChart(chartMode) {
        let chartIdx = chartMode === "day" ? DAY_IDX : chartMode === "week" ? WEEK_IDX : MONTH_IDX;
        if (chart[chartIdx]) {
          return;
        }

        // Fixes an issue where Week/Month chart bars are not properly aligned to x-axis tick marks
        Highcharts.setOptions({
          global: {
            useUTC: false,
          }
        });

        chart[chartIdx] = Highcharts.chart(chartId[chartIdx], {
          title: {
            text: "Loading...",
            useHTML: true
          },
          xAxis: {
            type: 'datetime',
            title: {
              text: ""
            },
            startOfWeek: 0
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
            minorTickInterval: 25,
          },
          legend: {
            enabled: false
          },
          caption: {
            useHTML: true
          },
		  plotOptions: {
				series: {
					minPointLength: 2
				}
		  },
          tooltip: {
            // Disabling to let tooltip better track with the hovered row.  There might have been a reason to have this enabled that I don't recall - AMC, july 8 2019
            // positioner: function () {
            //   return { x: 10, y: 80 };
            // },
            formatter: function() {
              let me = this;
              const pointData = chartSeriesData[chartIdx].filter(function(row){
                return row.timestamp === me.point.x;
              })[0];

              let aqiValue = pointData.aqi;
              let categoryValue = "None";
              let pollutantValue = pointData.pollutant;

			  // AIRN-105 UTC Offset is only present in a "Day" JSON cw 2021-01-27
			  let dateTime = moment(this.point.x);
			  // Week & Month Charts have no need for utcOffset
			  let dateTimeStr = dateTime.format("MMM Do, YYYY");
			  // Day Charts NEED a utcOffset
			  if (chartMode === "day") {
			  // pointData.utcOffset is ONLY defined in a "Day" JSON
			  let utcOffset = pointData.utcOffset
				// Now we can do a utcOffset and reassign it to dateTime
				dateTime = moment(this.point.x).utcOffset(utcOffset);
				// then format dateTimeStr to include an AM/PM
				dateTimeStr = dateTime.format("MMM Do, YYYY hA");
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
              } else if (aqiValue >= 301&& aqiValue < 501) {
                categoryValue = "Hazardous"; // maroon, hazardous
              } else if (aqiValue >= 501) {
                categoryValue = "Beyond the AQI"; // Beyond the AQI cw 2019-10-07
              }

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
            borderWidth: 0,
            pointPadding: 0.05,
            groupPadding: 0.05,
            crisp: false,
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
            enabled: true,
            href: "https://urldefense.com/v3/__https://airnow.gov__;!!F1XoHSs!RDmiEd-Xzd0Ja9zJ9xcB6VRYMtLAnWl521kRBboCUmnwZvR3GySPgQXAlN8$ ",
            text: "AirNow.gov"
          },
          exporting: {
            chartOptions: {
              chart: {
                styledMode: true,
                events: {
                  load: function() {
                    this.container.classList.add('export');
                  }
                }
              }
            },
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


      function setChartData(chartMode, reportingAreaName, stateCode) {
        let chartIdx = chartMode === "day" ? DAY_IDX : chartMode === "week" ? WEEK_IDX : MONTH_IDX;

        if(typeof reportingAreaName !== "undefined") {
          chart[chartIdx].update({
            exporting: {
              filename: (chartIdx === DAY_IDX ? "today" : chartMode) + "__" + reportingAreaName.toLowerCase().replace(/ /g,"_") + "_reporting_area"
            }
          });

          chartReportingAreaName[chartIdx] = reportingAreaName;
          chartReportingAreaState[chartIdx] = stateCode;

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
                // AIR-530 The updated format needs to be "stringified" first cw 2022-03-24
                var s3_data = JSON.parse(JSON.stringify(response)); // AIR-530 Sucessful object built with updated JSON files ONLY cw 2022-03-24
                if (typeof s3_data === "string") { // AIR-530 IF it's a "string" then it's the old JSON format, so use the old method cw 2022-03-24
                  console.log('AIR-530: Using original JSON format.'); // AIR-530 User feedback cw 2022-03-24
                  var s3_data = JSON.parse(response); // AIR-530 This is the original code cw 2022-03-24
                }
                parseChartS3Data(chartMode, s3_data);
                chart[chartIdx].series[0].setData(chartSeriesData[chartIdx].map(function(row) {
                  return [row.timestamp, row.aqi];
                }));
                chart[chartIdx].redraw();
              },
              error: function(response) {
                if (urlFallback1 && jsonUrl === url) {
                  getJsonData(urlFallback1);
                  return;
                } else if ((urlFallback1 && jsonUrl === urlFallback1) || (!urlFallback1 && jsonUrl === url)) {
                  getJsonData(urlFallback2);
                  return;
                }
                chart[chartIdx].setTitle({text: "AQI Data Unavailable"});
                chart[chartIdx].series[0].setData([]);
                chart[chartIdx].redraw();
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


      function parseChartS3Data(chartMode, s3_data) {
        let chartIdx = chartMode === "day" ? DAY_IDX : chartMode === "week" ? WEEK_IDX : MONTH_IDX;

        let aqiData = s3_data.aqi;
        let pollutantData = s3_data.param;
        let utcOffset = s3_data.utcOffset;
        let startTimeUTC = s3_data.startTimeUTC;
        let endTimeUTC = s3_data.endTimeUTC;

        let delta = chartMode === "day" ? "hours" : "days";
        let xAxisLabel = chartMode === "day" ? chartTimezoneLabel[chartIdx] : "";
        let yAxisLabel = chartMode === "day" ? "NowCast Air Quality Index (AQI)" : "Air Quality Index (AQI)";


        let chartTitle = "";
        let chartSubtitle = chartReportingAreaName[chartIdx] + " Reporting Area";
        let chartCaption = "";
        if (chartMode === "day") {
          chartTitle = "<div class='chartHeader'>Today</div>";
          // chartCaption = "NowCast AQI for the last 24 hours";
          chartCaption = "<span class='chart-info-caption'>This chart shows the NowCast AQI in your area for the previous 24 hours. Mouse over or tap a bar to see which pollutant (ozone or PM) was highest that hour.</span>";
        } else if (chartMode === "week") {
          chartTitle = "<div class='chartHeader'>Week</div>";
          // chartCaption = "AQI for the last 7 days";
          chartCaption = "<span class='chart-info-caption'>This chart shows the daily AQI in your area for each of the last 7 days. Mouse over or tap a bar to see which pollutant (ozone or PM) was highest that day.</span>";
        } else { // chartMode === "month"
          chartTitle = "<div class='chartHeader'>Month</div>";
          // chartCaption = "AQI for the last 30 days";
          chartCaption = "<span class='chart-info-caption'>This chart shows the daily AQI in your area for each of the last 30 days. Mouse over or tap a bar to see which pollutant (ozone or PM) was highest that day.</span>";
        }

        chartSeriesData[chartIdx] = [];

        let startDateTime = moment.utc(startTimeUTC, "YYYY-MM-DD HH:mm:SS");
        let endDateTime = moment.utc(endTimeUTC, "YYYY-MM-DD HH:mm:SS");

        let dataDateTime;
        let diff;
        if (chartMode === "day") {
          endDateTime = endDateTime.utcOffset(utcOffset).add(1, "hours");
          // startDateTime = endDateTime.clone().startOf("day"); // midnight morning of the current day
          startDateTime = endDateTime.clone().subtract(24-1, "hours"); // 24 hours prior to now
          dataDateTime = endDateTime.clone();
          diff = endDateTime.diff(startDateTime, "hours");
        } else if (chartMode === "week") {
          endDateTime = moment().year(endDateTime.year()).month(endDateTime.month()).date(endDateTime.date()).startOf("day");
          startDateTime = endDateTime.clone().subtract(7-1, "days");
          dataDateTime = endDateTime.clone();
          diff = endDateTime.diff(startDateTime, "days");
        } else {
          endDateTime = moment().year(endDateTime.year()).month(endDateTime.month()).date(endDateTime.date()).startOf("day");
          startDateTime = endDateTime.clone().subtract(30-1, "days");
          dataDateTime = endDateTime.clone();
          diff = endDateTime.diff(startDateTime, "days");
        }

        for (let i = aqiData.length - 1; i >= 0 && dataDateTime.isSameOrAfter(startDateTime); i--) {
          let aqi = aqiData[i];
          let pollutant = pollutantData[i];

          chartSeriesData[chartIdx].push({
            timestamp: dataDateTime.valueOf(),
            utcOffset: utcOffset,
            aqi: i >= 0 ? aqiData[i] : 0, // if we need more data than we have AQI values, set the missing ones to 0
            pollutant: i >= 0 ? pollutantData[i] : "N/A", // if we need more data than we have pollutant values, set the missing ones to "N/A"
          });

          dataDateTime = dataDateTime.subtract(1, delta);
        }

        chartSeriesData[chartIdx] = chartSeriesData[chartIdx].reverse();

        chart[chartIdx].setTitle({text: chartTitle});
        chart[chartIdx].setSubtitle({text: chartSubtitle});
        chart[chartIdx].update({
          caption: {
            text: chartCaption
          }
        });
        chart[chartIdx].xAxis[0].update({
          title: {
            text: xAxisLabel
          },
          labels: {
            formatter: function () {
              let dateTime = moment(this.value);
              let format = dateTime.format("MMM Do");
              dateTime = dateTime.utcOffset(utcOffset);
              if (chartMode === "day") {
                format = dateTime.format("h A");
              }
              return format;
            }
          }
        });
        chart[chartIdx].yAxis[0].update({
          title: {
            text: yAxisLabel
          },
        });
      }

      function handleAqiLegend() {
        $('.po-aqi-scale-btn').click(function() {
          $(this).addClass('po-aqi-scale-btn-hidden');
          $('.po-aqi-scale-display').removeClass('po-aqi-scale-display-hidden');
        });

        $('.po-aqi-scale-display .fa-times').click(function() {
          $('.po-aqi-scale-display').addClass('po-aqi-scale-display-hidden');
          $('.po-aqi-scale-btn').removeClass('po-aqi-scale-btn-hidden');

        });
      }

    }
  };

})(jQuery, Drupal);
