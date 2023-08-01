(function ($, Drupal) {
			
  function addBandTabListeners() {
    console.log("addBandTabListeners");
    $(".btn-band-tab").on("click.bcTab", function() {
      let currentId = this.id,
          currentIdSplit = currentId.split("-"),
          currentBandContainerNid = parseInt(currentIdSplit[currentIdSplit.length-1]),
          currentBandIndex = parseInt(currentIdSplit[currentIdSplit.length-2]);


    })
  }

  function fixImageCaptions() {
    let imageWithCaptions = $("img[data-caption]");

    for(let i = 0; i < imageWithCaptions.length; i++) {
      let currentImageWithCaptions = $(imageWithCaptions[i]),
          parent = currentImageWithCaptions.parent(),
          divCaption = $('<div/>', {
            text: currentImageWithCaptions.attr("data-caption"),
            css: {
              "position": "absolute",
              "font-size": "12px",
              "width": currentImageWithCaptions.css("width"),
              "top": currentImageWithCaptions.css("height")
            }
          });

      parent.append(divCaption);
      currentImageWithCaptions.css("margin-bottom", divCaption.css("height"));
    }
  }

  Drupal.behaviors.bandsBehavior = {
    attach: function (context, settings) {
      $(document).ready(function () {
        //  Attach band container tab clicks
        // addBandTabListeners();

        // TODO: Replace this with a drupal way that works for CFEditor
        // fixImageCaptions();
      });
    }
  };
})(jQuery, Drupal);
