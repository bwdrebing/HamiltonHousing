/*
Any buttons with the class "preview" will now have a confirmation popup
before submitting.  The only this that is up to you, is the define a textFunction
in a different script that will return a string containing the html you wish to 
display in the confirmation popup. An example can be found in 
studentInfoConfirmText.js. Remember to include this textFunction in the template :)
 
 TL;DR: Add preview class to button, and define your own textFunction() to display
 text in the confimation popup
*/

$('.preview').on('click', function(event) {
    
    event.preventDefault();

    //Call the function that will produce your confirmation text here...
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
});