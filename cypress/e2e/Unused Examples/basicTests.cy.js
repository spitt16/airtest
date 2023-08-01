/// <reference types="cypress"/>
// This is my basic test file

describe('My First Test', () => {
  // display baseUrl
  let baseUrl = 'https://preview:Welcome1@dev-airnowgov.pantheonsite.io/'; //accessing baseUrl

  it('AIR=### Quick Chris Test ', () => {
    cy.visit(baseUrl + '/about-airnow/')
    cy.get('.band-title-holder > #about-airnow')
      .contains('About AirNow')
  })

  it('AIR=### Quick Contact Us Test ', () => {
    cy.visit(baseUrl + '/contact-us/')
    cy.get(':nth-child(1) > .strip-margin')
      .contains('Contact Us')
  })

  it('AIR=### Quick Be Smoke Ready Image Test', () => {
    cy.visit(baseUrl + '/wildfires/be-smoke-ready/')
    cy.get('.banner-image')
      .invoke('prop', 'src') // invoke a function 'prop' to get the 'src'
      .then(src => src.includes('/sites/default/files/2022-09/be-smoke-ready-hero_0.png')) // search for some text that is present only if the URL is correct
      .should('be.true'); // assert that the statement is 'true', or we found the text
  })


})













