(function($, Drupal) {
  // Create Storage namespace
  let AirNowGov = window.AirNowGov;
  let Storage = AirNowGov.Storage = {};

  const EXPIRATION_LENGTH_MILLIS  = 1000 * 60 * 5; // 5 minutes
  const KEY_BASE = AirNowGov.APP_NAME + ".";

  let storeItem = Storage.storeItem = function(key, data) {
    let item = {
      "updated": new Date().getTime(),
      "data": data
    };
    sessionStorage.setItem(KEY_BASE + key, JSON.stringify(item));
    return item;
  };

  let getItem = Storage.getItem = function(key) {
    return JSON.parse(sessionStorage.getItem(KEY_BASE + key));
  };

  let isItemExpired = Storage.isItemExpired = function(key) {
    let item = getItem(key);
    return (new Date().getTime() - Number(item.updated) >= EXPIRATION_LENGTH_MILLIS)
  };

  let clearItem = Storage.clearItem = function(key) {
    sessionStorage.removeItem(KEY_BASE + key);
  }
})(jQuery, Drupal);
