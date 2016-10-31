$('#id_name').change(function () {

	var building = $('#id_name').val();
	$('#id_room_number option').hide();
	$('#id_room_number option.'+building.replace(/ /g, '.')).show();

});
$('#id_room_number option').each(function(index) {

    var building = $(this).text();
	$(this).addClass(building);
	$(this).text($(this).val());
	$(this).hide();
});

$('#id_building').change(function () {

	var building = $('#id_building').val();
	$('#id_suite_number option').hide();
	$('#id_suite_number option.'+building.replace(/ /g, '.')).show();

});

$('#id_suite_number option').each(function(index) {
    
	var building = $(this).text();
	$(this).addClass(building);
	$(this).text($(this).val());
	$(this).hide();
});
