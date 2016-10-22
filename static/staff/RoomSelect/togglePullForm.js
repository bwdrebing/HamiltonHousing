$("#id_Show_Pull").change(function (){
	if($("#id_Show_Pull:checked").val()){
		$(".PullFields").show();	
		$(".PullFields :input").prop('required',true);
	} else {
		$(".PullFields :input").prop('required',false);
		$(".PullFields").hide();	
	}
})
