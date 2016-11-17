// -------------------------------------------
//  initialize floor plan zoom plugin
// -------------------------------------------
$("#fullFloorPlan").elevateZoom({
    zoomType: 'inner',
    cursor: 'crosshair',
    gallery:'thumbnail-gallery',  
    galleryActiveClass: 'active', 
    imageCrossfade: true,
}); 

// -------------------------------------------
//  switch floor plan header with thumbnail 
//  name
// -------------------------------------------
$('#thumbnail-gallery a').click(function() {
    $('#floorPlanName').html($('img', this).attr('alt'));
});
