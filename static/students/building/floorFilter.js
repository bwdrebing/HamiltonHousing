$("#floorSelect").on("change", function(){
  var value = $(this).val();
  console.log(value);
  if(value != "all"){
    $(".room-list tr:not(." + value + ")").hide();
    $(".room-list tr." + value ).show();
    return;
  }
  $(".room-list tr").show();
});