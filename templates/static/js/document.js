jQuery(function () {
    var div = ['#lk', '#doc', '#address']




    $('.btngroup button').click(function () {
        $('.btngroup button').each(function () {
           $(this).removeClass('selected');
        });
        $(this).addClass('selected');
     var id = $(this).data('value');
     for (const i of div){
         if (i == id){
             $(i).show();
         }else{
             $(i).hide();
         }
     }
  });
});