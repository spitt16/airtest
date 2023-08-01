// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')

// This skips over the "World Imagery" error  cw 2023-01-23
Cypress.on('uncaught:exception', (err, runnable) => {
    // we expect a 3rd party library error with message 'list not defined'
    // and don't want to fail the test so we return false
    if (err.message.includes('city.replace')) { // When Cypress encounters the "city.replace error" from a Dial page with a City value in Session Storage
        console.log(err.message)
        return false
    }
    if (err.message.includes('Script error.')) { // When Cypress encounters the "unexpected token ':' " error from static.arcgis.com
        console.log(err.message)
        return false
    }
    // we still want to ensure there are no other unexpected
    // errors, so we let them fail the test
})
