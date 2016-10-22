
$('#id_name').change(function () {
	var building = $('#id_name').val();
	alert('as');
	$('#id_room_number option').hide();
	$('#id_room_number option.'+building.replace(/ /g, '.')).show();

});
$('#id_room_number option').each(function() {
	var building = $(this).val();
	alert('as');
	$(this).class(builing);
	$(this).val($(this).text());
});


