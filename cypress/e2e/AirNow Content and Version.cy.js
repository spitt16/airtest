/// <reference types="cypress"/>

// Now displaying the CURRENT values. cw 2023-05-24

//
describe('AirNow Version Checks', () => {
    // display baseUrl
    let baseUrl = Cypress.config('baseUrl'); //accessing baseUrl
    it('baseUrl: '+baseUrl, () => {
        // nothing
    })
    // Get the AirNow Version and Content number from the about page    
    it('Version Number', () => {
        cy.visit(baseUrl+'/about-airnow/')
        cy.get('#code_version')
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => {
                // run a javscript function using the variable 'htmlSource'
                htmlSource.toString();
                cy.log(htmlSource.toString() );
                cy.task('log', '      '+ htmlSource.toString() ); // Use task PlugIn to output to the terminal cw 2023-03-01
            })
    })
    it('Content Number ', () => {
        cy.visit(baseUrl+'/about-airnow/')
        cy.get('#content_version')
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(htmlSource => {
              // run a javscript function using the variable 'htmlSource'
              htmlSource.toString();
              cy.log(htmlSource.toString() );
              cy.task('log', '      '+ htmlSource.toString() ); // Use task PlugIn to output to the terminal cw 2023-03-01
            })
    })
})

