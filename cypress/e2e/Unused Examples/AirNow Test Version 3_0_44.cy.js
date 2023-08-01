/// <reference types="cypress"/>
let baseUrl = Cypress.config().baseUrl; //accessing baseUrl

describe.only('AirNow Version 3.0.44 Tests', () => {
    // display baseUrl
    it('baseUrl: '+baseUrl, () => {
        // nothing
    })

    // it('AIR-599 Hide title for Zero Announcements', () => {
    //     cy.viewport(812,375); // set to iPhone mini landscape size
    //     cy.visit(baseUrl + '/aqi');
    //     cy.get(':nth-child(1) > .card-link > .links-card-style > :nth-child(2) > a > .links-card-image')
    //         .should('have.css', 'max-width', '100%')
    //     cy.viewport(1200, 800); // set back to full browser size
    // })

    it('Content 175 Coping with the Stress of Wildfire Smoke', () => {
        // "Standard Link Test". It requires 3 variables to be set. cw 2023-03-09
        cy.visit(baseUrl + '/publications/wildfire-guide-factsheets/coping-with-the-stress-of-wildfire-smoke'); // The link is on this page.
        let thisLink = '/sites/default/files/2023-03/coping-with-the-stress-of-wildfire-smoke.pdf'; // The Link to test.
        let thisLinkText = 'Coping with the Stress of Wildfire Smoke'; // Linked text to test.

        // Standard "Link Test" below. No need to change below here. cw 2023-03-09
        cy.get('a[href$="'+thisLink+'"]') // using the variable thisLink to VERIFY the link... Part 1
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content out of the first element found
            .then(content => content.includes(thisLinkText)) // search for the link text that is present
            .should('be.true'); // assert that the statement is 'true', or we found the text
        cy.request(thisLink) // using the variable thisLink to FOLLOW the link... Part 2

        // Verify the new link is present on the given page AND follow the link to the PDF. cw 2023-03-09
    })

    it('AIR-608 2023 AQAW Announcement', () => {
        cy.visit(baseUrl + '/?city=Durham&state=NC&country=USA'); // The link is on this page.
        cy.get('div.announcement-container > h2.title')
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML'
            .then(content => content.includes('Celebrate Air Quality Awareness Week')) // search for the link text that is present
            
        // Looks for the new annoucement for AQAW 2023 cw 2023-04-19
    })

    it('AIR-558 Spanish Metadata Update', () => {
        cy.visit(baseUrl + '/four-steps-in-spanish'); // The link is on this page.
        cy.get('html:root') // Get the HTML page
            .invoke('prop', 'outerHTML') // invoke a function 'prop' to get the 'outerHTML', or pull the HTML content
            .then(pageSource => pageSource.toString().includes('Cuatro pasos para iniciar un Programa de banderines sobre la calidad del aire')) // search for some text that is present 
            .should('be.true') // assert that the above is 'true', or we did not find the text
            
        // Looks for the some Spanish Metadata text on the given page cw 2023-04-19
    })

    //     cy.visit(baseUrl + '/?city=Durham&state=NC&country=USA'); // The link is on this page.
    //     cy.wait(3000);
    //     cy.get('body') // load all the HTML
    //         .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
    //         .then(content => content.includes('<!-- AIR-599')) // search for the link text that is present
    //         .should('be.true'); // assert that the statement is 'true', or we found the text

    //     // Verify that the new code is present by looking for the Jira Issue number in the HTML source. cw 2023-04-03
    // })

    // it.only('AIR-601 More Than 2 Data Providers', () => {
    //     cy.visit(baseUrl + '/?city=Washington&state=DC&country=USA'); // The link is on this page.
    //     cy.wait(2000)
    //     cy.get('.marquee-dataprovider-col > :nth-child(3) > a') //  <-- Is this correct ?? 
    //         .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML'
    //         .then(content => content.includes("EPA Office of Atmospheric Protection")) // search for the link text that is present

    //     // Looks for the THIRD Data provider. Mike will fix this. 
    // })

});





