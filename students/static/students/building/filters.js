$(".room-filter").change(function () {
    var value1 = $("#floorFilter").val();
    var value2 = $("#roomTypeFilter").val();
    
    if (value1 != "all" && value2 != "all") {
        $(".room-list tr:not(." + value1 + "." + value2 + ")").hide();
        $("." + value1 + "." + value2).show();
        return;
    }
    
    if (value1 == "all") {
        $(".room-list tr:not(." + value1 + ")").hide();
        $("." + value2).show();
        return;
    }
    
    if (value2 == "all") {
        $(".room-list tr:not(." + value2 + ")").hide();
        $("." + value1).show();
        return;
    }
    
    $(".room-list tr").show();
});

var building_values = [];
var room_type_values = [];
var building_selected = [];
var room_type_selected = [];

/* create global variables based on what values the building filter is initialized with */
$(".building-filter").on("loaded.bs.select", function (e) {
    var sel = document.getElementById('buildingFilter');
    
    /* get all the values from the initialized select so that we can index later */
    for (var i = 0, n = sel.options.length; i < n; i++) {
        
      /* get select options, remove spaces, and 'bldg' to front and push to global array */
      if (sel.options[i].value) 
          building_values.push(sel.options[i].value.replace(/\s+/g, ''));
    }
});

/* create global variables based on what values the building filter is initialized with */
$(".room-type-filter").on("loaded.bs.select", function (e) {
    var sel = document.getElementById('roomTypeFilter');
    
    /* get all the values from the initialized select so that we can index later */
    for (var i = 0, n = sel.options.length; i < n; i++) {
        
      /* get select options, remove spaces, and 'bldg' to front and push to global array */
      if (sel.options[i].value) 
          room_type_values.push(sel.options[i].value.replace(/\s+/g, ''));
    }
});

/* when the building-filter is changed, the rows in the table will be hidden or shown */
$(".building-filter").on("changed.bs.select", function(e, clickedIndex, newValue, oldValue) {
    if (building_selected.length == 0) {
        building_selected.push(building_values[clickedIndex]);
        console.log("hiding anything without class ", building_values[clickedIndex]);
        $(".room-list tr:not(." + building_values[clickedIndex] + ")").hide();
        return;
    }
    
    /* this is a new value to filter by */
    if (newValue) {
        building_selected.push(building_values[clickedIndex]);
        building_selected.forEach(function (value) {
            $(".room-list tr." + value).show();
        });
        return;
    }
    
    /* this is an old value that is being removed */
    if (oldValue) {
        building_selected.splice(building_values[clickedIndex], 1);
        
        /* now nothing is building_selected */
        if (building_selected.length == 0) {
            $(".room-list tr:not(.apt-room)").show();
            return;
        }
        
        $(".room-list tr." + building_values[clickedIndex]).hide();
        return;
    }
});

/* when the building-filter is changed, the rows in the table will be hidden or shown */
$(".room-type-filter").on("changed.bs.select", function(e, clickedIndex, newValue, oldValue) {
    console.log("newValue ", newValue);
    console.log("oldValue ", oldValue);
    
    /* the first value to filter by */
    if (room_type_selected.length == 0) {
        room_type_selected.push(room_type_values[clickedIndex]);
        console.log("hiding anything without class ", room_type_values[clickedIndex]);
        $(".room-list tr:not(." + room_type_values[clickedIndex] + ")").hide();
        return;
    }
    
    /* this is a new value to filter by */
    if (newValue) {
        room_type_selected.push(room_type_values[clickedIndex]);
        room_type_selected.forEach(function (value) {
            if (building_selected.length > 0) {
                building_selected.forEach(function (value2) {
                    $(".room-list tr." + value + "." + value2).show();
                });
                return;
            }
            
            $(".room-list tr." + value).show();
        });
        return;
    }
    
    /* this is an old value that is being removed */
    if (oldValue) {
        room_type_selected.splice(room_type_values[clickedIndex], 1);
        
        /* now nothing is room_type_selected */
        if (room_type_selected.length == 0) {
            if (building_selected.length > 0) {
                building_selected.forEach(function (value) {
                    $(".room-list tr." + value).show();
                });
                return;
            }
            
            $(".room-list tr:not(.apt-room)").show();
            return;
        }
        
        $(".room-list tr." + room_type_values[clickedIndex]).hide();
        return;
    }
});
