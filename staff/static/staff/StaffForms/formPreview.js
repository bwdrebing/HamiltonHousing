/*
Any buttons with the class "preview" will now have a confirmation popup
before submitting.  The only this that is up to you, is the define a textFunction
in a different script that will return a string containing the html you wish to
display in the confirmation popup. An example can be found in
studentInfoConfirmText.js. Remember to include this textFunction in the template :)

 TL;DR: Add preview class to button, and define your own textFunction() to display
 text in the confimation popup

 Example:

 var textFunction = function(){
    var text = "<h1>Are you sure you wanna submit that??</h1>";
    return text;
 };
*/
function activateTab(tab){
    $('.nav-pills a[href="#' + tab + '"]').tab('show');
};


var locateInvalidInputs = function() {
  var formGroups = $('.form-group');
  var alertText = "<ul>";
  var invalid = false;
  formGroups.each(function(index){

    //Get any inputs within this form group
    var input = $("select, input", this);
    if(input.size() > 0){
      if(input.prop('required') && !(input[0].validity.valid)){
        invalid = true;
        var parentTab = $(this).parents(".tab-pane");
        activateTab(parentTab.attr('id'));

        alertText += "<li><strong>"
                      + $('#room-nav .active a').html() + " "
                      + $("label", this).html() +
                      "</strong></li>";
      }
    }
  });
  if(invalid){
    alertText += "</ul>";
    $.alert({
      title : "You need to fill out:",
      content : alertText,
      backgroundDismiss: true,
    });
  }
  return invalid;
};


$('.preview').on('click', function(event) {

    event.preventDefault();

    //Call the function that will produce your confirmation text here...
    if(!locateInvalidInputs()){
        var confirmationText = textFunction();

        var obj = $.confirm({
            title: 'Please confirm the information below...',
            content: confirmationText,
            confirm: function() { $('form').submit();},
            confirmButton: 'Confirm',
            cancelButton: 'Cancel',
            confirmButtonClass: 'btn-info',
            cancelButtonClass: 'btn-danger',
            theme: 'material',
        });
    }
});
