(function ($, Drupal) {

  function setSquareCard(cardClass, mqValue) {
    if(mqValue == null) {
      mqValue = 'all';
    }
    let mq = window.matchMedia(mqValue);
    if(mq.matches) {
      let percentAmt = .75;
      let cardWidth = $(cardClass).width() * percentAmt;
      $(cardClass).css('height', cardWidth+'px');
    } else {
      $(cardClass).css('height', "");
    }
  }

  Drupal.behaviors.cardsBehavior = {
    attach: function (context, settings) {
      let cardClass = '.band-style-nondesc .inner-card-style-basic';

        setSquareCard(cardClass, '(min-width: 768px) and (max-width: 818px)');
        $(window).resize(function() {
          setSquareCard(cardClass, '(min-width: 768px) and (max-width: 818px)');
        });
    }
  };
})(jQuery, Drupal);


