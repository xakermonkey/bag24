//=================================================== fill_profile.html
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

//=================================================== main_menu.html
jQuery(function () {
    var div = ['#in-storage', '#awaiting-delivery', '#delivered']
    $('.btn-group-item button').click(function () {
        $('.btn-group-item button').each(function () {
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

//=================================================== main_menu.html in-storage
jQuery(function () {
    $('#go-arrange').click(function () {
        $('#choice-type-order').hide();
        $('#choose-delivery').show();
  });
    $('#deliver-address').click(function () {
        $('#choose-delivery').hide();
        $('#arrange-delivery').show();
  });
});