$(document).ready(function(){
    $('.control').click(function(){
        $(this).toggleClass('closed');
        $(this).toggleClass('opened');
        $(this).siblings('ul').toggleClass('closed');
    });

});