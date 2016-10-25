function buildingFilter(element) {
    var value = $(element).val().toLowerCase();
    
    $("#building-sidebar > li").each(function() {
        if ($(this).text().toLowerCase().search(value) > -1) {
            $(this).show();
        }
        else {
            $(this).hide();
        }
    });
}