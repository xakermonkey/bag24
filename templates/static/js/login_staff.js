jQuery(function () {
   var data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
    $('button').click(function () {
        data['login'] = $('input[name="username"]').val();
        data['password'] = $('input[name="password"]').val();
        $.ajax({
            url: 'login',
            method: 'POST',
            data: data,
            success: function (data) {
                if (data.status){
                    document.location.href = document.location.origin + '/staff/panel';
                }else{
                    $('#alert_pass').show();
                }
            }
        });
    });
});