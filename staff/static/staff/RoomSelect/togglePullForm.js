$("#id_Show_Pull").change(function (){
    var parentId = $(this).parent().parent().parent().attr('id');
	if($("#id_Show_Pull:checked").val()){
		$(".PullField" + parentId).show();	
		$(".PullField" + parentId + " :input").prop('required',true);
	} else {
		$(".PullField" + parentId + " :input").prop('required',false);
		$(".PullField" + parentId).hide();	
	}
})

$('input').each(function(){
    $(this).addClass("form-control");   
});