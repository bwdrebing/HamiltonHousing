$('#thumbnail-gallery a').click(function() {
    $('#floorPlanName').html($('img', this).attr('alt'));
});
