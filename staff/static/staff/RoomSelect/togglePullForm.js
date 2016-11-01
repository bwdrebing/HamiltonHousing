$('.toggle').toggles({
    drag: false,
    click: true,
    text: {
        on: "Yes",
        off: "No"
    },
    on: true,
});

$('.toggle').on('toggle',function(e,active){
    //Find the parent tab of the toggle...   
    var parent = $(this).parent().parent().parent();
    
    //Show/Hide the form groups and then set the inputs to required or not.
    if(active){
        parent.children('.PullField').show();
        parent.children('.PullField').find('input').prop('required', true);
    } else {
        parent.children('.PullField').hide();
        parent.children('.PullField').find('input').prop('required', false);
    }   
});