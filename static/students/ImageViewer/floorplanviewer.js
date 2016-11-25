
var viewer = ImageViewer('.pannable-image',{});
$('.iv-zoom-slider').remove()


//If the window is being resized, redraw the image just in case
//the viewer was hidden and then shown again...
$(window).on('resize', function(e){
    var activeImage = $('.active.thumbnail');
    viewer.load(activeImage.attr('data-image'),
                activeImage.attr('data-zoom-image'));
});

var heightFromTopOfMain = function(elem){
  return elem.offset().top - $('#main').offset().top;

};

var oldButtonHeight = $('.sticky').offset().top;

// $('#main').scroll(function(){
//
//     var main_top = $('#main').scrollTop();
//     var bottomOfNav = $('.navbar-fixed-top').height();
//     var div_top = $('.sticky-anchor').offset().top;
//
//     //If we have scrolled past the button, stick it!
//     if(bottomOfNav > div_top){
//         $('.sticky').addClass('stick');
//         $('.sticky_anchor').height($('sticky').outerHeight());
//         $('.stick').offset({top: bottomOfNav,
//                             left: $('.stick').offset().left});
//     } else {
//         $('.sticky').removeClass('stick');
//         $('.sticky_anchor').height(0);
//     }
//
// });
//
// $(".navbar-toggle").on('mouseup', function(e){
//     if($('.stick').length){
//         var stickyOffset = $('.stick').offset();
//         var sidebarOffset = $('#sidebar').offset();
//         //TODO: This needs to happen after default!
//        $('.stick').offset({top: stickyOffset.top,
//                           left: sidebarOffset.left + $('#sidebar').width()});
//     }
// });
