/*$(".room-type-filter").on("changed.bs.select", function(event, clickedIndex, newValue, oldValue) {
    var room_types = ["S", "D", "T", "Q", "B"]
    // It passes through event, clickedIndex, newValue, oldValue.
    console.log(clickedIndex);
    console.log(event);
    console.log(newValue);
    console.log(oldValue);
    
    if(newValue != ""){
        $(".room-list tr:not(." + newValue + ")").hide();
        $(".room-list tr." + newValue ).show();
        return;
    }
    
    $(".room-list tr").show();
});

$(".floor-filter").on("changed.bs.select", function(event, clickedIndex, newValue, oldValue) {
    var room_types = ["0", "1", "2", "3", "4"]
    // It passes through event, clickedIndex, newValue, oldValue.
    console.log(clickedIndex);
    console.log(event);
    console.log(newValue);
    console.log(oldValue);
    
    if(newValue != ""){
        $(".room-list tr:not(." + newValue + ")").hide();
        $(".room-list tr." + newValue ).show();
        return;
    }
    
    $(".room-list tr").show();
});*/

$(".room-filter").on("change", function () {
    var value1 = $("#floorFilter").val();
    var value2 = $("#roomTypeFilter").val();
    
    console.log(value1);
    console.log(value2);
    
    if ((typeof value1 !== "undefined") && (typeof value2 !== "undefined")) {
        console.log("both are defined");
        if (value1 != "all" && value2 != "all") {
            $(".room-list tr").hide()
            $("." + value1 + "." + value2).show();
            return;
        }
    }

    if (typeof value1 !== "undefined") {
        console.log("value1 is defined");
        if (value1 != "all") {
            $(".room-list tr").hide()
            $("." + value1).show();
            return;
        }
    }

    else if (typeof value2 !== "undefined") {
        console.log("value2 is defined");
        if (value2 != "all") {
            $(".room-list tr").hide()
            $("." + value2).show();
            return;
        }
    }
    
    $(".room-list tr").show();
});
