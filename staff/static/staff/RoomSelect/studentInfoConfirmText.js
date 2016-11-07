// Loads all inputted student information into a table

var textFunction = function() {

    var text = '<table class="table table-bordered">';
    text += "<tr><th>Room</th><th>Lottery #</th><th>Year</th><th>Gender</th><tr>";
    
    $('#room-nav a').each(function(index){
        var room = $(this).text();
        var ref = $(this).attr('href');
        
        
        
        $(ref + ' .Student').each(function(index){
            text += "<tr><td>" + room + "</td>";            

            $(this).find('.form-group').each(function(index){    
                var inputVal = '';
                
                if($(this).find('input').length == 0) {
                    inputVal = $(this).find('select').val();
                }
                else {
                    inputVal = $(this).find('input').val();
                }
               text += '<td>' + inputVal + '</td>';
            });
        });
        
        text = text + '</tr>';
        });
    
    text += "</table>";
    return text;
}
