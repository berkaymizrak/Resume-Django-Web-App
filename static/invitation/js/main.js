(function ($) {
    "use strict";


    $(document).ready(function () {

        // wow js
        new WOW().init();

        // counter
        $('.counter').counterUp({
            delay: 10,
            time: 10000
        });

        // scrollIt for smoth scroll
        $.scrollIt({
            upKey: 38,             // key code to navigate to the next section
            downKey: 40,           // key code to navigate to the previous section
            easing: 'linear',      // the easing function for animation
            scrollTime: 600,       // how long (in ms) the animation takes
            activeClass: 'active', // class given to the active nav element
            onPageChange: null,    // function(pageIndex) that is called when page is changed
            topOffset: 0           // offste (in px) for fixed top navigation
        });

        // scrollup bottom to top
        $.scrollUp({
            scrollName: 'scrollUp', // Element ID
            topDistance: '4500', // Distance from top before showing element (px)
            topSpeed: 300, // Speed back to top (ms)
            animation: 'fade', // Fade, slide, none
            animationInSpeed: 200, // Animation in speed (ms)
            animationOutSpeed: 200, // Animation out speed (ms)
            scrollText: '<i class="fa fa-angle-double-up"></i>', // Text for element
            activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
        });


    });

})(jQuery);