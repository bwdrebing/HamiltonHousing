$('#thumbnails img').click(function(){
    $('#fullFloorPlan').attr('src', $(this).attr('src'));
    $('#fullFloorPlan').attr('data-zoom-image', $(this).attr('src'));
    $('#floorPlanName').html($(this).attr('alt'));
});


$('#thumbnails a').click(function(){
    $("#thumbnails a").removeClass('active');
    $(this).addClass('active');
    
    $('#fullFloorPlan').attr('src', $('img', this).attr('src'));
    $('#fullFloorPlan').attr('data-zoom-image', $('img', this).attr('src'));
    $('#floorPlanName').html($('img', this).attr('alt'));
});