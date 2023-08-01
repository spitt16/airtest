/// <reference types="cypress"/>

// Testing basic function and database connectivity for the RBLC ColdFusion Application cw 2023-01-01


// Assign the baseURL to the ColdFusion servers
let baseUrl = "https://cfpub.epa.gov";

describe.only('RBLC Tests', () => {
    // display baseUrl
    it('baseUrl: '+baseUrl, () => {
        // nothing
    })
    // CFPUB
    //
    // get the basic search page
    it('RBLC Basic Search at: '+baseUrl, () => {
        cy.visit(baseUrl+'/rblc/index.cfm?action=Search.BasicSearch&lang=en')
        cy.get('H1').contains('RBLC Basic Search')
    })
    // get the basic login page, submit it and get "Bad user ID" message... thus the database is connection and working
    it('RBLC Login Page at: '+baseUrl, () => {
        cy.visit(baseUrl+'/rblc_admin/index.cfm?action=Login.Login')
        cy.get('#frmLogin').submit()
    })

    it('RBLC CFID & CFTOKEN are secure HTML cookies', () => {
        cy.request({
            url: baseUrl+'/rblc/index.cfm?action=Search.BasicSearch&lang=en',
            headers: {
                'Accept': 'text/html'
            }
        }).then((response) => {
            // cy.getCookie('CFID').then((cookie) => {
            //     const cfidValue = cookie.value;
            //     // Do something with the CFID value
            //     cy.log(`CFID value: ${cfidValue}`)
            //     cy.task('log', 'CFID value: '+cfidValue);
            // })
            cy.getCookie('CFID').then((cookie) => {
                //cy.task('log', 'CFID secureValue: '+cookie.secure)
                expect(cookie.secure).to.be.true // Use Chai BDD Assertion to get the "secure" attribute of the given cookie
            })
            cy.getCookie('CFTOKEN').then((cookie) => {
                //cy.task('log', 'CFTOKEN secureValue: '+cookie.secure)
                expect(cookie.secure).to.be.true // Use Chai BDD Assertion to get the "secure" attribute of the given cookie
            })

        })
        // get the basic search page and verify if the CFID & CFTOKEN cookies have the attribute of "secure". cw 2023-03-27
    })

    it('RBLC CFID & CFTOKEN are HTML only cookies', () => {
        cy.request({
            url: baseUrl+'/rblc/index.cfm?action=Search.BasicSearch&lang=en',
            headers: {
                'Accept': 'text/html'
            }
        }).then((response) => {
            cy.getCookie('CFID').then((cookie) => {
                expect(cookie.httpOnly).to.be.true // Use Chai BDD Assertion to get the "httpOnly" attribute of the given cookie
            })
            cy.getCookie('CFTOKEN').then((cookie) => {
                expect(cookie.httpOnly).to.be.true // Use Chai BDD Assertion to get the "httpOnly" attribute of the given cookie
            })

        })
        // get the basic search page and verify if the CFID & CFTOKEN cookies have the attribute of "httpOnly". cw 2023-03-27
    })

    /* ONLY while inside EPA Network... cw 2023-02-01

    // CFPSTAGE
    //
    // get the basic search page
    let baseUrl2 = "https://cfpstage.rtpnc.epa.gov";

    it('RBLC Basic Search at: '+baseUrl2, () => {
        cy.visit(baseUrl2+'/rblc/index.cfm?action=Search.BasicSearch&lang=en')
        cy.get('H1').contains('RBLC Basic Search')
    })
    // get the basic login page, submit it and get "Bad user ID" message... thus the database is connection and working
    it('RBLC Login Page at: '+baseUrl2, () => {
        cy.visit(baseUrl2+'/rblc_admin/index.cfm?action=Login.Login')
        cy.get('#frmLogin').submit()
    })

    // CFPSTAGE2021
    //
    // get the basic search page
    let baseUrl3 = "https://cfpstage2021.rtpnc.epa.gov";

    it('RBLC Basic Search at: '+baseUrl3, () => {
        cy.visit(baseUrl3+'/rblc/index.cfm?action=Search.BasicSearch&lang=en')
        cy.get('H1').contains('RBLC Basic Search')
    })
    // get the basic login page, submit it and get "Bad user ID" message... thus the database is connection and working
    it('RBLC Login Page at: '+baseUrl3, () => {
        cy.visit(baseUrl3+'/rblc_admin/index.cfm?action=Login.Login')
        cy.get('#frmLogin').submit()
    })

    // */
})

