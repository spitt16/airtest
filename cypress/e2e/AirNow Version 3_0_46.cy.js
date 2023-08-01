/// <reference types="cypress"/>
let baseUrl = Cypress.config().baseUrl; //accessing baseUrl

describe('AirNow Version 3.0.46 Tests', () => {
    // display baseUrl
    it('baseUrl: '+baseUrl, () => {
        // nothing
    })

    it('Site Improve \"Text not included in an ARIA landmark\" on National Maps Page Top Ten AQI', () => {
        cy.visit(baseUrl + '/national-maps'); // The link is on this page.
        cy.wait(2000);
        cy.get('#cityCell0') // Finds the first AQI Top Ten's alt parameter value cw 2023-06-01
            .invoke('prop', 'outerHTML') // invoke a function 'prop' to get the 'outerHTML'
            .then(content => content.includes("City 1")) // search for the link text that is present
            .should('be.true'); // assert that the statement is 'true', or we found the text

         // Looks for the NEW alt tag parameter in the first AQI Top Ten city cw 2023-06-01
    });

    it('AIR-601 More Than 2 Data Providers on Dial Page', () => {
        cy.visit(baseUrl + '/?city=Washington&state=DC&country=USA'); // The link is on this page.
        cy.wait(2000)
        cy.get('a[href$=\"http://www.mde.maryland.gov/PROGRAMS/AIR/Pages/index.aspx\"') // Finds the current Air Now Tech third data provider link cw 2023-05-09
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML'
            .then(content => content.includes("Maryland Department of the Environment")) // search for the link text that is present

         // Looks for the THIRD Data provider... Washington, DC has 4 of them.
    });

});

// Git push test

