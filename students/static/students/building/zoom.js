//initiate the zoom plugin and pass the id of the div containing gallery images
$("#fullFloorPlan").elevateZoom({
    zoomType: 'inner',
    cursor: 'crosshair',
    gallery:'thumbnail-gallery',  
    galleryActiveClass: 'active', 
    imageCrossfade: true,
}); 

// pass the images to Fancybox
/*
$("#fullFloorPlan").bind("click", function(e) {  
    var ez = $('#fullFloorPlan').data('elevateZoom');	
	$.fancybox(ez.getGalleryList());
    return false;
});
*/