/*$('.table-hoverable').click(function () {
    $(this).nextUntil('.table-dropdown').slideToggle('normal');
    $(this).find("span").toggleClass("glyphicon-menu-up");
    $(this).find("span").toggleClass("glyphicon-menu-down");
});*/

$('.table-hoverable').hover(
    function () {
        $(this).addClass('active');
    }, 
    
    function () {
        $(this).removeClass('active');
    }
);