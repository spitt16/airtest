/// <reference types="cypress"/>
const site = "https://air572.app.cloud.gov/";

describe.only('AIR-572 Popup for Non PM Reporting Area', () => {
    // Visit and get the page that changed
    it.only('Carlsbad, NM Test', () => {
        let baseUrl = Cypress.config().baseUrl; //accesing baseUrl
        cy.visit(baseUrl+'/?city=Carlsbad&state=NM&country=USA') // test with the builtin test area of Carlsbad, NM
        //cy.visit('https://www.airnow.gov/?city=Carlsbad&state=NM&country=USA')
        cy.wait(5000)
        cy.get('#missingPM25Popup').contains('Current PM2.5 data is not available, but there are indications of elevated PM2.5 nearby.')
    })
})

