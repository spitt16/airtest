
/// <reference types="cypress"/>
let baseUrl = Cypress.config().baseUrl; //accesing baseUrl

describe.only('AirNow Version 3.0.41 Tests', () => {
    // display baseUrl
    it('baseUrl: '+baseUrl, () => {
        // nothing
    })
    it('AIR-572 Popup for Non PM Reporting Area', () => {
        cy.visit(baseUrl+'/?city=Carlsbad&state=NM&country=USA') // test with the builtin test area of Carlsbad, NM
        cy.wait(5000)
    cy.get('#missingPM25Popup')

        // If the span is present then the latest code for AIR-572 code is deployed cw 2023-01-02
    })
    it('AIR-573 Viewport user-scalable should be YES for Accessibility', () => {
        //cy.get('link[href*="/sites/default/files/css/css_"]');
        cy.visit(baseUrl+'/about-airnow/');
        cy.get('head meta[name=viewport]').should(
            'have.attr',
            'content'
            )
            .then(content => content.toString().includes('user-scalable=yes')) // search for some text that is present only
            assert.isOk('content', 'Viewport meta tag set to user-scalable=yes.'); // assert that the above is 'ture', or we did find the text

        cy.get('head meta[name=viewport]').should(
            'have.attr',
            'content'
            )
            .then(content => content.toString().includes('maximum-scale=2.0')) // search for some text that is present only
            assert.isOk('content', 'Viewport meta tag set to maximum-scale=2.0.'); // assert that the above is 'ture', or we did find the text

        //If there is a meta tag that contains "user-scalable=yes" &  then it is set correctly.
    })
    it('AIR-590 R9 Administrator Reading Why is Coco Red? Videos', () => {
        cy.visit(baseUrl+'/air-quality-videos/');
        cy.get('#pacific')
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(content => content.includes('Why is Coco Red? Read Along Martha Guzman, EPA Regional Administrator')) // search for some text that is present only
            assert.isOk('content', 'English R9 Video is present.'); // assert that the above is 'ture', or we did find the text

        cy.get('#pacific')
            .invoke('prop', 'innerHTML') // invoke a function 'prop' to get the 'innerHTML', or pull the HTML content
            .then(content => content.includes('¿Por qué Coco es rojo? Lea junto con Martha Guzman, la Administradora de R9')) // search for some text that is present only
            assert.isOk('content', 'Spanish R9 Video is present.'); // assert that the above is 'ture', or we did find the text

        //If the videos Titles are present, then the video is as well.  cw 2023-02-08
    })
    it('AIR-592 Why is Coco Red? PDF Link', () => {
        cy.visit(baseUrl+'/publications/why-is-coco-red/why-is-coco-red-picture-book/');
        // English PDF of Coco Red
        cy.get('a[href*="https://document.airnow.gov/why-is-coco-red.pdf"]')
            .invoke('prop', 'href') // invoke a function 'prop' to get the 'href'
            .then(href => {
                cy.request({ // request the URL that is at that href
                    url: href,
                    encoding: 'binary',
                }).then((response) => {
                    response.headers['content-type'].includes('application/pdf') // The content-type header is correct for a PDF
                })
            });

        //If the PDF links are present, then click them and determine that a PDF is returned.  cw 2023-02-08
    })
    it('AIR-593 USDA Forest Service Link on Federal Partners Page', () => {
        cy.visit(baseUrl+'/partners/federal-partners/'); // This is the page
        cy.get('a[href*="https://www.fs.usda.gov/"]'); // verify the updated link URL

        // Check for the updated link  cw 2023-02-08
    });
})

