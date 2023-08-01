/// <reference types="cypress"/>
let baseUrl = Cypress.config().baseUrl; //accessing baseUrl

describe('AirNow Version 3.0.45 Tests', () => {
    // display baseUrl
    it('baseUrl: '+baseUrl, () => {
        // nothing
    })

    it('AIR-612 Nav Bar menu item link to WebCMS AQAW Page', () => {
        cy.visit(baseUrl + '/about-airnow/'); // The link is on this page.

        cy.get('.navigation-holder') // Get the entire Drop Down menu... Part 1
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content out of the first element found
            .then(content => content.includes('https://www.epa.gov/air-quality/air-quality-awareness-week') )// search for the link text that is present
            .should('be.true'); // assert that the statement is 'true', or we found the text
        cy.request('https://www.epa.gov/air-quality/air-quality-awareness-week') // test the actual link... Part 2

        // Verify the new link is present on the given page AND follow the link. cw 2023-05-09
    })

    it('AIR-613 Coco está rojo video on Coco Red page', () => {
        cy.visit(baseUrl + '/education/why-is-coco-red/'); // The link is on this page.

        // Standard "Link Test" below. No need to change below here. cw 2023-03-09
        cy.get('body') // using the variable thisLink to VERIFY the link... Part 1
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content out of the first element found
            .then(content => content.includes('Ver en YouTube')) // search for the link text that is present
            .should('be.true'); // assert that the statement is 'true', or we found the text

        // Verify the new EMBEDDED VIDEO is present on the given page. cw 2023-05-09npx cypress open

    })

    it('AIR-617 Remove access to old PDF for EPA-456/F-23-001 and EPA-456/F-23-002', () => {
        cy.request({ url: baseUrl + '/sites/default/files/2023-03/air-quality-guide-for-particle-pollution.pdf', failOnStatusCode: false})
            .then((response) => {
                expect(response.status).to.eq(404);
            });
        // Verify the new old PDF returns a 404. cw 2023-05-24
    })

});

// Git push test.



