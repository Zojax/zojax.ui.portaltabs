$(document).ready(function(){
    console.log('JS')
//    $('.closed').click(function(){
//        $(this).addClass('opened');
//    });
//
//    $('.opened').click(function(){
//        $(this).addClass('closed');
//    });

    $('.control').click(function(){
        $(this).toggleClass('closed');
        $(this).toggleClass('opened');
        $(this).siblings('ul').toggleClass('closed');
    });

});