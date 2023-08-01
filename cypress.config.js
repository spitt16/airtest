const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
      on('task', {
        log(message) {
          console.log(message)
          return null
        },
      }),
      on('task', {
        getPdfContent (pdfName) {
          return parsePdf(pdfName)
        }
       })
    },
    baseUrl: 'https://www.airnow.gov',
    pageLoadTimeout: 120000, // 120 seconds
    projectId: "9shjxq", // Project ID fpr cloud.cypress.io cw 2023-01-31
  },
});
