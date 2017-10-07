 $(document).ready(function() {
   $("img").unveil();
   $("a > img").parent().attr('data-fancybox', 'gallery').fancybox({
    'transitionIn'    : 'none',
    'transitionOut'   : 'none',
    caption: function() {
      return $('<a/>').attr({
        style: 'background-color: #2f6fbf; padding: 10px; text-decoration: none',
        href: $(this).data('full-size'),
        download: true
      }).text('Download full size image')[0].outerHTML;
    }
   });
});
