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
    var parent = $(this).parents('.tab-pane');
    
    //Show/Hide the form groups and then set the inputs to required or not.
    if(active){
        parent.find('.PullField').show();
        parent.find('.PullField').find('input').prop('required', true);
    } else {
        parent.find('.PullField').hide();
        parent.find('.PullField').find('input').prop('required', false);
    }   
});