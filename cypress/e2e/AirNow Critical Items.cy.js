//
// Critical Items Cypress Test
// Version 1.0
// cw 2023-02-01
//
// / <reference types="cypress"/>
let baseUrl = Cypress.config().baseUrl; //accessing baseUrl

describe('AirNow Critical Items', () => {
    // display baseUrl
    it('baseUrl: '+baseUrl, () => {
        // nothing
    })
    // Check on the Logo on the about page

     it('AirNow Logo', () => {
        cy.visit(baseUrl+'/about-airnow/')
        cy.get('#navbarHeader > img')
    })
    it('Aggregated JS ON', () => {
        cy.visit(baseUrl+'/about-airnow/')
        cy.get('script[src*="/sites/default/files/js/js_"]'); // All the <script> elements that have a Drupal Aggregated-style src attribute cw 2023-01-26
    })
    it('Aggregated CSS ON', () => {
        cy.visit(baseUrl+'/about-airnow/')
        cy.get('link[href*="/sites/default/files/css/css_"]'); // All the <link> elements that have a Drupal Aggregated-style href attribute cw 2023-01-26
    })

    it('TWIG & Theme Debugging OFF', () => {
        cy.visit(baseUrl + '/about-airnow/')
        cy.get('html:root') // Get the HTML page
            .eq(0) // Errors, cannot be chained off 'cy', or stop here if the page is an error
            .invoke('prop', 'outerHTML') // invoke a function 'prop' to get the 'outerHTML', or pull the HTML content
            .then(pageSource => pageSource.toString().includes('<!-- THEME DEBUG -->')) // search for some text that is present only if Theme Debugging is "on"
            .should('be.false') // assert that the above is 'false', or we did not find the text
        // In this 'get' we pull out the HTML, search it for the "THEME DEBUG" text, and assert that it is missing. cw 2023-01-27

        // HINT to fix: Set in Drupal in "sites/default/local.services.yml" & "default.services.yml" at the parameter twig.config: and turn it if OFF set the following... debug: false & auto_reload: null & cache: true   cw 2023-01-26
    });

    it('Correct Path used by Dial Page icons', () => {
        cy.visit(baseUrl+'/?city=Durham&state=NC&country=USA') // Must go a Dial page to check for the icon at the bottom of the page.
        cy.get('.basic-image > img') // find the first Dial page footer icon graphic by using a "unique" CSS selector and filter down to it's image tag
            .invoke('attr', 'src') // find the src attribute
            .then(src => src.includes(Cypress.config().baseUrl)) // is baseURL inside the img src URL
        // Get the first image on the page and see if it is coming from the baseUrl cw 2023-01-27
    });

    it('Historic State JSON Data Available', () => {
        // What is "today"?
        var dayjs = require('dayjs') // load the dayjs library
        //cy.log('Testing: '+dayjs().format('DD/MM/YYYY'))  // Today's date
        var year =  parseInt(dayjs().format('YYYY')); //cy.log(year); // this month
        var month = parseInt(dayjs().format('M')); //cy.log(month); // this month with NO leading zeros
        var day = parseInt(dayjs().format('DD')); //cy.log(day); // this day
        // What is "yesterday"?
        var yesterday = day - 1; //cy.log(yesterday);
        if (yesterday == 0) { // ONLY if first day of month
            month = month - 1;
            yesterday = 28; // special date change to deal with February cw 2020-03-31
        }
        cy.log('Yesterday: '+year+'/'+month+'/'+yesterday) // yesterday's date
        cy.request('http://airnowgovapi.com/andata/States/West_Virginia/'+year+'/'+month+'/'+yesterday+'.json', ) // check yesterday's JSON data for West Virginia

        // What is "6 months ago"?
        //var sixMonthsAgo = day - 1; cy.log(yesterday);
        if (month > 7) { // if more than halfway through the year, so the year is the same
            month = month - 6;
        } else { // first half of the year, so look at the correct month at the end of last year... "cary over" one year as 12 months
            month = month - 6 + 12;
            year = year - 1;
        }
        cy.log('6mths ago: '+year+'/'+month+'/'+yesterday) // 6 months ago's date
        cy.request('http://airnowgovapi.com/andata/States/West_Virginia/'+year+'/'+month+'/'+yesterday+'.json', ) // check JSON data for 6 months ago for West Virginia

        // Get JSON data for "yesterday" and for "6 months ago" for "West Virginia" because WV has a small amount of data, but it should be there.  cw 2023-01-30
    });

    it('National Map Timestamp Current on National Maps page', () => {
        // What is "today"?

        // set up dayjs library
        var dayjs = require('dayjs'); // load the dayjs library
        var customParseFormat = require('dayjs/plugin/customParseFormat'); // load the customParseFormat Plugin
        dayjs.extend(customParseFormat); // get advanced formats for dates

        //cy.log('Testing: '+dayjs().format('DD/MM/YYYY'))  // Today's date
        var year =  dayjs().format('YYYY'); //cy.log(year); // this month as a string
        var monthName = dayjs().format('MMMM'); //cy.log(monthName); // this month name as a string in long form
        var day = dayjs().format('DD'); //cy.log(day); // this day as a string

        cy.visit(baseUrl+'/national-maps/') // Go to the National Maps page
        cy.wait(5000); // Five-second delay for gispub to fill out the timestamp
        // Find Updated
        cy.get('#currenttimestamp') // find the timestamp
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes('Updated ')) // search for some text that is present only if the timestamp is available
            assert.isOk('htmlSource', 'Current Map has an Updated value.') // assert that the above is 'ture', or we did find the text
        cy.get('#forecasttimestamp') // find the timestamp
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes('Updated ')) // search for some text that is present only if the timestamp is available
            assert.isOk('htmlSource', 'Forecast Map has an Updated value.'); // assert that the above is 'ture', or we did find the text
        // Find date
        cy.get('#forecasttimestamp') //find the timestamp
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes(monthName+' '+day+', '+year)) // search for the text that is present ONLY if the date is correct
            assert.isOk('htmlSource', 'Forecast Map has current date.'); // assert that the above is 'ture', or we did find today's date
        cy.get('#currenttimestamp') //find the timestamp
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => htmlSource.toString().includes(monthName+' '+day+', '+year)) // search for the text that is present ONLY if the date is correct
            assert.isOk('htmlSource', 'Current Map has current date.'); // assert that the above is 'ture', or we did find today's date

        // Get the timestamp from the National Maps page and check the date and time against "current" data and time.  cw 2023-01-30

        // How long ago was it updated?
        cy.visit(baseUrl+'/national-maps/') // Go to the National Maps page... again.
        cy.wait(5000); // Five-second delay for gispub to fill out the timestamp
        cy.get('#currenttimestamp') // find the timestamp for Current AQ Map
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => { // run a javscript function using the variable 'htmlSource'
                htmlSource.toString();
                var mapTime = htmlSource.substring(htmlSource.search('Updated ')+8, htmlSource.length -4); // everything after the "Updated" and the single space; this is the current date of the timestamp as a string
                mapTime = dayjs(mapTime, 'MMMM DD, YYYY hh:mm A'); cy.log('mapTime: '+mapTime);// convert the mapTime to a dayjs object
                var currentTime = dayjs(); cy.log('currentTime: '+currentTime); // currentTime as a dayjs object
                var timeDiff = currentTime - mapTime; // compute the difference
                timeDiff = timeDiff/1000/60; // convert the time difference to minutes
                assert(timeDiff < 120, "Current AQ Map is older than 120 minutes.")
            })
        cy.get('#forecasttimestamp') // find the timestamp for Forecast AQ Map
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => { // run a javscript function using the variable 'htmlSource'
                htmlSource.toString();
                var mapTime = htmlSource.substring(htmlSource.search('Updated ')+8, htmlSource.length -4); // everything after the "Updated" and the single space; this is the current date of the timestamp as a string
                mapTime = dayjs(mapTime, 'MMMM DD, YYYY hh:mm A'); cy.log('mapTime: '+mapTime);// convert the mapTime to a dayjs object
                var currentTime = dayjs(); cy.log('currentTime: '+currentTime); // currentTime as a dayjs object
                var timeDiff = currentTime - mapTime; // compute the difference
                timeDiff = timeDiff/1000/60; // convert the time difference to minutes
                assert(timeDiff < 120, "Forecast AQ Map is older than 120 minutes.")
            })
        // Get the timestamp from the National Maps and determine if they are within two hours old cw 2023-01-30
    });

    it('fire.airnow.gov is Available', () => {
        cy.visit('https://fire.airnow.gov') // get visit the main site URL.
        cy.get('[data-i18n="[html]site-version"]') // get the custom selector used on F&S Map via regular expression
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => { // run a javascript function using the variable 'htmlSource'
                cy.log("Version: "+htmlSource);
            })

        // Load the Fire & Smoke Map URL to make sure it there, then load and display the Version number cw 2023-02-06
    });

    it('DoSAir iframe content on the Embassies & Consulates Page', () => {
        cy.visit(baseUrl+'/international/us-embassies-and-consulates/') // Go to the National Maps page... again.
        cy.get('[data-reactid=".0.0.0.0.0.0.0.1"]') // get the custom selector used via a regular expression
            // The "reactid" values are inside the iFrame content; That content must be build with REACT.js cw 2023-02-06
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => { // run a javscript function using the variable 'htmlSource'
                htmlSource.toString()
                //cy.log(htmlSource)
                assert.isOk(htmlSource == 'AirNow Department of State', 'iFrame contains the text: AirNow Department of State.') // assert that the above is 'ture', or we did find the text
            })

        // Load the Embassies & Consulates pge to make sure it's there. cw 2023-02-06
    });

    it('ColdFusion Server Apache Domain Name Forward', () => {
        cy.visit('https://airnow.gov') // visit the redirected URL
        cy.get('#navbarHeader > img') // get the AirNow Logo on the Home page

        // Load Redirected URL. If redirected correctly, then the AirNow Logo should be present. cw 2023-02-06
    });

    it('Drupal Security Message NOT present', () => {
        cy.visit(baseUrl+'/about-airnow/') // visit the redirected URL
        cy.get('html:root') // Get the HTML page
            .eq(0) // Errors, cannot be chained off 'cy', or stop here if the page is an error
            .invoke('prop', 'outerHTML') // invoke a function 'prop' to get the 'outerHTML', or pull the HTML content
            .then(pageSource => pageSource.toString().includes('There is a security update available for your version of Drupal.')) // search for some text that is present only if the Security Massage is appearing
            .should('be.false') // assert that the above is 'false', or we did not find the text

        // the Drupal Security Update required messages should not be seen by the Public User. cw 2023-02-06
    });

    it('State Notifications List', () => {
        cy.request(baseUrl+'/stateNotifications.json').as('stateNotification')// REQUEST the State Notification JSON file from the current baseURL
        cy.get('@stateNotification').then((response) => { // JSON is automatically parsed
            expect(response.body[0]).to.have.property('state') // JSON has parsed correctly, and has at least one state property
            let i = 0; let states = '';
            while (i < response.body.length) {
                let thisState = response.body[i].state;
                if (thisState === 'TE' || thisState === 'TF' || thisState === 'TG') { // Skip over the Test States
                    // nothing
                } else { // Let add this one.
                    if (i == 0) {
                        states = response.body[i].state;// This is the first state. Start the list.
                    } else {
                        states = states + ', ' + response.body[i].state; // Add this state to the list
                    }
                }
                i++;
            }
            // Show the list of States
            cy.log(states);
            cy.task('log', '      State Notification list is: '+states); // Use task PlugIn to output to the terminal cw 2023-02-07
            // Here are six ^^ spaces to make this text line up in the terminal output cw 2023-02-07
        })
        // Read the State Notification JSON and find all the non Test states and display them... cw 2023-02-06
    });
})