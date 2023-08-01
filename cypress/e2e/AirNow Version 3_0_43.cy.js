/// <reference types="cypress"/>
let baseUrl = Cypress.config().baseUrl; //accessing baseUrl

describe('AirNow Version 3.0.43 Tests', () => {
    // display baseUrl
    it('baseUrl: '+baseUrl, () => {
        // nothing
    })
    
    it('AIR-567 iPhone 13 Mini Landscape Display', () => {
        cy.viewport(812,375); // set to iPhone mini landscape size
        cy.visit(baseUrl + '/aqi');
        cy.get(':nth-child(1) > .card-link > .links-card-style > :nth-child(2) > a > .links-card-image')
            .should('have.css', 'max-width', '100%')
        cy.viewport(1200, 800); // set back to full browser size
    })

    it('AIR-603 Air Quality Guide for Ozone', () => {
        cy.visit(baseUrl + '/publications/activity-guides/air-quality-activity-guide-for-ozone/');
        cy.get('strong > a') // verify new link is present
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content out of the first element found
            .then(content => content.includes('Guide for Ozone')) // search for the link text that is present
            .should('be.true'); // assert that the statement is 'true', or we found the text

        // Verify the new link is present and that it is labeled as 'Guide for Ozone'. cw 2023-03-03
    })

    it('AIR-603 Air Quality Guide for PM', () => {
        cy.visit(baseUrl + '/publications/activity-guides/air-quality-activity-guide-for-particle-pollution/');
        cy.get('strong > a') // verify new link is present
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content out of the first element found
            .then(content => content.includes('Guide for Particle Pollution')) // search for the link text that is present
            .should('be.true'); // assert that the statement is 'true', or we found the text

        // Verify the new link is present and that it is labeled as 'Guide for Particle Pollution'. cw 2023-03-03
    })

    it('AIR-603 Air Quality Guide for PM', () => {
        cy.visit(baseUrl + '/publications/activity-guides/air-quality-activity-guide-for-particle-pollution/');
        cy.get('strong > a') // verify new link is present
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content out of the first element found
            .then(content => content.includes('Guide for Particle Pollution')) // search for the link text that is present
            .should('be.true'); // assert that the statement is 'true', or we found the text

        // Verify the new link is present and that it is labeled as 'Guide for Particle Pollution'. cw 2023-03-03
    })

    it('AIR-603 Air Quality Guide for PM -- Standard Link Test', () => {
        // "Standard Link Test". It requires 3 variables to be set. cw 2023-03-09
        cy.visit(baseUrl + '/publications/activity-guides/air-quality-guide-for-particle-pollution/'); // The link is on this page.
        let thisLink = '/sites/default/files/2023-03/air-quality-guide-for-particle-pollution_0.pdf'; // The Link to test.
        let thisLinkText = 'Guide for Particle Pollution'; // Linked text to test.

        // Standard "Link Test" below. No need to change below here. cw 2023-03-09
        cy.get('a[href$="'+thisLink+'"]') // using the variable thisLink to VERIFY the link... Part 1
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content out of the first element found
            .then(content => content.includes(thisLinkText)) // search for the link text that is present
            .should('be.true'); // assert that the statement is 'true', or we found the text
        cy.request(thisLink) // using the variable thisLink to FOLLOW the link... Part 2

        // Verify the new link is present on the given page AND follow the link to the PDF. cw 2023-03-09
    })

    it('AIR-605 Spanish F&S Map Questions & Answers PDF Update', () => {
        // "Standard Link Test". It requires 3 variables to be set. cw 2023-03-09
        cy.visit(baseUrl + '/es/fasm-info/'); // The link is on this page.
        let thisLink = 'https://document.airnow.gov/fire-and-smoke-map-questions-and-answers-en-espanol.pdf'; // The Link to test.
        let thisLinkText = 'Preguntas y respuestas'; // Linked text to test.

        // Standard "Link Test" below. No need to change below here. cw 2023-03-09
        cy.get('a[href$="'+thisLink+'"]') // using the variable thisLink to VERIFY the link... Part 1
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content out of the first element found
            .then(content => content.includes(thisLinkText)) // search for the link text that is present
            .should('be.true'); // assert that the statement is 'true', or we found the text
        cy.request(thisLink) // using the variable thisLink to FOLLOW the link... Part 2

        // Verify the new link is present on the given page AND follow the link to the PDF. cw 2023-03-09
    })


});





