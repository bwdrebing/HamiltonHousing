//Add the back-btn class to any button that you want to be a back button

$('.back-btn').on('click', function(event){
    event.preventDefault();
    parent.history.back();  
    
});