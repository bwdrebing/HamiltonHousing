$('#thumbnail-gallery a').click(function() {
//    $('#floorPlanName').html($('img', this).attr('alt'));
    viewer.load($(this).attr('data-image'),
                $(this).attr('data-zoom-image'));
    $('.active.thumbnail').removeClass('active');
    $(this).addClass('active');

    //Update floorplan title
    $('#floor-name').text($(this).find(".thumbnail-label").attr("title"));

});
