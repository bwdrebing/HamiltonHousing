$(document).ready(function () {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });
    
  $('#main').click(function() {
    
    $('.row-offcanvas').removeClass('active');
  });
});