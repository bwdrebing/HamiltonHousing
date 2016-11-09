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

$('.preview').on('click', function(event) {
    
    event.preventDefault();

    //Call the function that will produce your confirmation text here...
    if(!($('form')[0].checkValidity())){
        var obj = $.alert({
            title: "Opps!",
            content: "Looks like you forgot a fill out part of the form!"
        });
    }
    else {
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