jQuery(function () {
    var bPhone = true;

    function clickSwipe() {
        bPhone = !bPhone;
        if ($('#title').text() === 'Телефон'){
            $('#title').text('Вход / регистрация');
        }else{
            $('#title').text('Телефон');
        }
        if ($('#subtext').text() === 'Пришлем на него смс с кодом'){
            $('#subtext').text('');
        }else{
            $('#subtext').text('Пришлем на него смс с кодом');
        }
        if ($('.btn-down').text() === 'Вход по телефону'){
            $('.btn-down').text('Регистрация / вход по логину');
        }else{
            $('.btn-down').text('Вход по телефону');
        }
        if ($('label').text() === 'Логин'){
            $('label').text('Номер телефона');
        }else {
            $('label').text('Логин');
        }
        if ($('input').attr('type')=='number'){
            $('input').attr('type', 'text');
        }else{
            $('input').attr('type', 'number');
        }
    }

    function clickNext() {
        if (bPhone){
            $('nav').show();
            $('#repeat').show();
            $('#title').text('Код из смс');
            $('#subtext').text('Код из смс на телефон '+$('input[type="number"]').val());
            $('input[type="number"]').val('');
            $('label').text('');
        } else {
                        // if find users
            $('nav').show();
            $('#title').text('Войти');
            $('#subtext').text('в аккаунт '+$('input[type="text"]').val());
            $('input[type="text"]').val('');
            $('label').text('Пароль');
        //    else
        //     ...
        }
    }

    function clickBack() {
        if (bPhone){
            $('nav').hide();
            $('#repeat').hide();
            $('#title').text('Телефон');
            $('#subtext').text('Пришлем на него смс с кодом');
            $('input[type="number"]').val('');
            $('label').text('Номер телефона');
        }else {
            $('nav').hide();
            $('#title').text('Вход / регистрация');
            $('#subtext').text('');
            $('input[type="number"]').val('');
            $('label').text('Логин');
        }
    }

   $('.btn-down').click(function () {
       clickSwipe();
   });

    $('.btn-next').click(function () {
        clickNext();
    });

    $('#back').click(function () {
        clickBack();
    })


});