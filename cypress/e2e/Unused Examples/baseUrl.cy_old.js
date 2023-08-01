//Accessing baseUrl value from cypress.json
describe('Example of BaseUrl', () => {
    it('Example of Baseurl', () => {
        let baseUrl = Cypress.config('baseUrl'); //accessing baseUrl
        cy.visit(baseUrl); //passing url value to cy.visit()
        //alert("Testing URL: "+baseUrl)
    });
});