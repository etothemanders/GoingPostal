var GP = GP || {};

var Validator = (function() {
  var $trackButton = $('#cover-button');

  function addTrackButtonClickListener() {
    $trackButton.click(handleTrackBtnClick);
  }

  function handleTrackBtnClick(event) {
    event.preventDefault();
    validateFormInput();
  }

  function validateFormInput() {
    var $formInput = $('#cover-input').val().trim();
    var emptyError = 'Please enter a tracking number.';
    var invalidTrackingNumber = 'Please enter a valid UPS tracking number. Ex: 1ZY8Y608YW02920325';
    var errorMessage = false;
    
    $('#error-message').empty();

    if ($formInput === '') {
      errorMessage = emptyError;
    } else if (!/1Z[A-Z0-9]{16}/.test($formInput)) {
      errorMessage = invalidTrackingNumber;
    }

    if (errorMessage) {
      $('#tagline').css('margin-bottom', '10px');
      $('#error-message').html(errorMessage).removeClass('hidden');
    } else {
      $('#tagline').css('margin-bottom', '70px');
      $('#error-message').addClass('hidden');
      alert('no errors!');
    }
  }

  function init() {
    addTrackButtonClickListener();
  }

  return {
    init: init
  };
})();

$(document).ready(function () {
  GP.validator = Validator.init();
});
