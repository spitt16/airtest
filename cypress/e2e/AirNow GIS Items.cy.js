//
// GIS Items Cypress Test
// Version 1.0
// cw 2023-02-15
//
// / <reference types="cypress"/>
let baseUrl = "https://gispub.epa.gov/airnow" // override "config" & passed in baseUrl values cw 2023-02-14

describe('AirNow GIS Items', () => {
    // display baseUrl
    it('baseUrl: '+baseUrl, () => {
        // nothing
    })
    // Check on the Logo on the about page

     it('AirNow Logo on gispub', () => {
         cy.visit(baseUrl); // Go to the GIS Pub AirNow Interactive Map cw 2023-02-09
         cy.get('img[alt="Air Now Logo"]')
         cy.get('img[src="images/AirNow_Logo_White.svg"]');

         // get the AirNow Logo using a custom selector via regular expressions
    })
    it('National Map Timestamp Current on AirNow', () => {
        // What is "today"?
        var dayjs = require('dayjs'); // load the dayjs library
        var customParseFormat = require('dayjs/plugin/customParseFormat'); // load the customParseFormat Plugin
        dayjs.extend(customParseFormat); // get advanced formats for dates
        //cy.log('Testing: '+dayjs().format('DD/MM/YYYY'))  // Today's date
        var year = dayjs().format('YYYY'); //cy.log(year); // this month as a string
        var monthName = dayjs().format('MMMM'); //cy.log(monthName); // this month name as a string in long form
        var day = dayjs().format('DD'); //cy.log(day); // this day as a string

        cy.visit("https://www.airnow.gov" + '/national-maps/'); // Go to the National Maps page... on Production cw 2023-02-09
        cy.wait(5000); // Five-second delay for gispub to fill out the timestamp

        // Find Updated
        cy.get('#currenttimestamp') // find the timestamp
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes('Updated ')); // search for some text that is present only if the timestamp is available
        assert.isOk('htmlSource', 'Current Map has an Updated value.'); // assert that the above is 'ture', or we did find the text
        cy.get('#forecasttimestamp') // find the timestamp
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes('Updated ')); // search for some text that is present only if the timestamp is available
        assert.isOk('htmlSource', 'Forecast Map has an Updated value.'); // assert that the above is 'ture', or we did find the text

        // Find date
        cy.get('#forecasttimestamp') //find the timestamp
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes(monthName + ' ' + day + ', ' + year)); // search for the text that is present ONLY if the date is correct
        assert.isOk('htmlSource', 'Forecast Map has current date.'); // assert that the above is 'ture', or we did find today's date
        cy.get('#currenttimestamp') //find the timestamp
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes(monthName + ' ' + day + ', ' + year)); // search for the text that is present ONLY if the date is correct
        assert.isOk('htmlSource', 'Current Map has current date.'); // assert that the above is 'ture', or we did find today's date
        // Get the timestamp from the National Maps page and check the date and time against "current" data and time.  cw 2023-01-30

        // How long ago was the National Maps image updated?
        //cy.visit("https://www.airnow.gov"+'/national-maps/') // Go to the National Maps page... on Production cw 2023-02-09
        //cy.wait(5000); // Five-second delay for gispub to fill out the timestamp
        cy.get('#currenttimestamp') // find the timestamp for Current AQ Map
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => {
                // run a javscript function using the variable 'htmlSource'
                htmlSource.toString();
                var mapTime = htmlSource.substring(htmlSource.search('Updated ') + 8, htmlSource.length - 4); // everything after the "Updated" and the single space; this is the current date of the timestamp as a string
                mapTime = dayjs(mapTime, 'MMMM DD, YYYY hh:mm A');
                cy.log('mapTime: ' + mapTime); // convert the mapTime to a dayjs object
                var currentTime = dayjs();
                cy.log('currentTime: ' + currentTime); // currentTime as a dayjs object
                var timeDiff = currentTime - mapTime; // compute the difference
                timeDiff = timeDiff / 1000 / 60; // convert the time difference to minutes
                assert(timeDiff < 120, "Current AQ Map is older than 120 minutes.");
            });
    })

    it('Interactive Map (gispub) Timestamp Current', () => {
        // What is "today"?
        var dayjs = require('dayjs'); // load the dayjs library
        var customParseFormat = require('dayjs/plugin/customParseFormat'); // load the customParseFormat Plugin
        dayjs.extend(customParseFormat); // get advanced formats for dates
        //cy.log('Testing: '+dayjs().format('DD/MM/YYYY'))  // Today's date
        var year = dayjs().format('YYYY'); //cy.log(year); // this month as a string
        var monthName = dayjs().format('MMMM'); //cy.log(monthName); // this month name as a string in long form
        var day = dayjs().format('DD'); //cy.log(day); // this day as a string

        cy.visit(baseUrl); // Go to the GIS Pub AirNow Interactive Map cw 2023-02-09
        cy.wait(10000); // TEN-second delay for gispub to fill out the timestamp

        // Find Updated
        cy.get('#warning') // find the timestamp
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes('Data Updated ')); // search for some text that is present only if the timestamp is available
        assert.isOk('htmlSource', 'Interactive Map (gispub) has an "Data Updated" value.'); // assert that the above is 'ture', or we did find the text

        // Find date
        cy.get('#warning') //find the timestamp
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes(monthName + ' ' + day + ', ' + year)); // search for the text that is present ONLY if the date is correct
        assert.isOk('htmlSource', 'Interactive Map (gispub) has current date.'); // assert that the above is 'ture', or we did find today's date
        // Get the timestamp from the Interactive Map (gispub) page and check the date and time against "current" data and time.  cw 2023-02-09
        // How long ago was the Interactive Map data updated?
        //cy.visit(baseUrl) // Go to the GIS Pub AirNow Interactive Map cw 2023-02-09
        //cy.wait(5000); // Five-second delay for gispub to fill out the timestamp
        cy.get('div span#warndate') // find the timestamp for the Interactive Map
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => {
                // run a javscript function using the variable 'htmlSource'
                htmlSource.toString();
                var mapTime = htmlSource.substring(4, htmlSource.length - 4); // everything after the "Updated" and the single space; this is the current date of the timestamp as a string
                mapTime = dayjs(mapTime, 'MMMM DD, YYYY at hh:mm A');
                cy.log('mapTime: ' + mapTime); // convert the mapTime to a dayjs object
                var currentTime = dayjs();
                cy.log('currentTime: ' + currentTime); // currentTime as a dayjs object
                var timeDiff = currentTime - mapTime; // compute the difference
                timeDiff = timeDiff / 1000 / 60; // convert the time difference to minutes
                assert(timeDiff < 120, "Interactive Map (gispub) is older than 120 minutes.");
            });
    })

    it('ArcGIS Login NOT Required', () => {
        cy.visit(baseUrl); // Go to the GIS Pub AirNow Interactive Map cw 2023-02-09
        cy.get('html:root') // Get the HTML page
            .eq(0) // Errors, cannot be chained off 'cy', or stop here if the page is an error
            .invoke('prop', 'outerHTML') // invoke a function 'prop' to get the 'outerHTML', or pull the HTML content
            .then(pageSource => pageSource.toString().includes('Please sign in to access the item on ArcGIS Online')) // search for some text that is present only if Theme Debugging is "on"
            .should('be.false'); // assert that the above is 'false', or we did not find the text
        // In this 'get' we pull out the HTML, search it for the "Please sign in to access the item on ArcGIS Online" text, and assert that it is missing. cw 2023-02-09
    });

    it('Monitors Available', () => {
        cy.visit(baseUrl + '?xmin=-9532003.17527462&ymin=3818182.4369011233&xmax=-8044844.352958232&ymax=4759886.625374498&mlayer=ozonepm'); // Go to the GIS Pub AirNow Interactive Map WITH the monitor layers ON cw 2023-02-09
        cy.wait(10000); // wait for the GIS page to load... 10 seconds
        cy.get('#labels_layer > text') // There is a "text" element inside the "labels_layer" for EACH Monitor
            .then(numMonitors => numMonitors.length) // the number of monitors found
            .should('be.gt', 1); // We found some Monitors !

        // We will get the GIS site with the Monitors Layer turned ON then count the number of returned Monitors. cw 2023-02-09
    });

    it('AirNowLatestContoursCombined ESRI Service Available', () => {
        cy.visit('https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/AirNowLatestContoursCombined/FeatureServer'); // Go to the ESRI Server URL cw 2023-02-09
        cy.get('li a').invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes('AirNowLatest_Combined')) // search for some text that is present
            .debug().should('equal', true); // assert that the above is 'ture', or we did find the text

        // We will get the ESRI Services site that we use and verify that the layer is available. cw 2023-02-10
    });

    // A measure of Contours complexity... at 7209 showing contours on contours..
    // https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/AirNowLatestContoursCombined/FeatureServer/0/getEstimates?f=pjson
    // look for "count"
    it('AirNowLatestContoursCombined Esri Service "Count" value ', () => {
        cy.visit('https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/AirNowLatestContoursCombined/FeatureServer/0/getEstimates'); // Go to the ESRI Server getEstimates page cw 2023-03-01
        cy.get('.restBody')
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => {
                // run a javscript function using the variable 'htmlSource'
                htmlSource.toString();
                var countStart = htmlSource.indexOf("Count:")+7;
                var countEnd = htmlSource.indexOf("<br>",countStart);
                var count = htmlSource.substring(countStart, countEnd);
                //console.log(count);
                var countNum = parseInt(count);
                // Show the list of States
                cy.log(countNum);
                cy.task('log', '      Number of layers: '+countNum); // Use task PlugIn to output to the terminal cw 2023-03-01
                assert(countNum < 2000, "There may be too many contours layers!.")
                assert(countNum !== 0, "There are NO contour layers!.")
            })

        // We will get the ESRI Services "count" values which is the number of contour polygons; It may be "too high". cw 2023-02-10
    });
})