
/// <r.onlyeference types="cypress"/>
let baseUrl = Cypress.config().baseUrl; //accessing baseUrl

describe('AirNow Version 3.0.42 Tests', () => {
    // display baseUrl
    it('baseUrl: '+baseUrl, () => {
        // nothing
    })


    it('AIR-594 Add Jefferson County to Alabama Sate & Local Partners', () => {
        cy.visit(baseUrl + '/partners/state-and-local-partners/');
        cy.get('a[href*="https://www.jcdh.org/SitePages/Programs-Services/EnvironmentalHealth/Air-RadiationProtectionDivision/AirRadProDiv.aspx"]') // verify new link is present
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content out of the first element found
            .then(content => content.includes('Jefferson County Department of Health')) // search for thw link text that is present
            .should('be.true'); // assert that the statement is 'true', or we found the text

        // Verify the new link is present and that it is labeled as 'Jefferson County Department of Health'. cw 2023-02-09
    })


});





