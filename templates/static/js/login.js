jQuery(function () {
    var bPhone = true;
    var data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};

    function clickSwipe() {
        bPhone = !bPhone;
        if ($('#title').text() === 'Телефон') {
            $('#title').text('Вход / регистрация');
        } else {
            $('#title').text('Телефон');
        }
        if ($('#subtext').text() === 'Пришлем на него смс с кодом') {
            $('#subtext').text('');
        } else {
            $('#subtext').text('Пришлем на него смс с кодом');
        }
        if ($('.btn-down').text() === 'Вход по телефону') {
            $('.btn-down').text('Регистрация / вход по логину');
        } else {
            $('.btn-down').text('Вход по телефону');
        }
        if ($('label').text() === 'Логин') {
            $('label').text('Номер телефона');
        } else {
            $('label').text('Логин');
        }
        if ($('input').attr('type') == 'number') {
            $('input[type="number"]').attr('type', 'text');
        } else {
            $('input[type="text"]').attr('type', 'number');
        }
    }

    function clickNext() {

        if (bPhone) {
            $('.btn-down').hide();
            $('.btn-next').hide();
            data["number"] = $('input[type="number"]').val();
            $.ajax({
                url: "set_number",
                method: 'POST',
                data: data,
                success: function (data) {
                    console.log(data);
                    if (data.status) {
                        $('nav').show();
                        $('#repeat').show();
                        $('#title').text('Код из смс');
                        $('#subtext').text('Код из смс на телефон ' + data.number);
                        $('input[type="number"]').val('');
                        $('input[type="number"]').addClass('code');
                        $('input[type="number"]').attr('maxlength', '4');
                        $('label').text('');
                    }
                }
            });
        } else {
            $('.btn-down').hide();
            data["login"] = $('input[type="text"]').val();
            $.ajax({
                url: 'find_user',
                method: 'POST',
                data: data,
                success: function (data) {
                    if (data.status) {
                        $('nav').show();
                        $('#title').text('Войти');
                        $('#subtext').text('в аккаунт ' + $('input[type="text"]').val());
                        $('input[type="text"]').val('');
                        $('input[type="text"]').attr('type', 'password');
                        $('label').text('Пароль');
                        $('.btn-next').addClass('login');
                        $('.btn-next').removeClass('star');
                    } else {
                        $('nav').show();
                        $('title').text("Создайте пароль");
                        $('input[type="text"]').val('');
                        $('input[type="text"]').addClass('pswd');
                        $('input[type="text"]').attr('type', 'password');
                        $('label').text('Пароль');
                        $('div[align="left"]').after(`<div id="repeat" align="left" style="margin-bottom: 3%; margin-top: 3%">
                                                            <label class="form-label semi f-16 grey">Повторите пароль</label>
                                                            <div class="input-group mb-3">
                                                                <input type="password" class="form-control text-input pswd_repeat">
                                                            </div>
                                                        </div>`);
                        $('.btn-next').text("Регистрация");
                        $('.btn-next').addClass('regist');
                        $('.btn-next').removeClass('star');

                    }
                }
            });
        }
    }

    function clickBack() {
        if (bPhone) {
            $('nav').hide();
            $('#repeat').hide();
            $('#title').text('Телефон');
            $('#subtext').text('Пришлем на него смс с кодом');
            $('input[type="number"]').val('');
            $('input[type="number"]').removeAttr('maxlength');
            $('input[type="number"]').removeClass('code');
            $('label').text('Номер телефона');
            $('.btn-next').show();
            $('.btn-down').show();
        } else {
            $('nav').hide();
            $('#repeat').remove();
            $('#title').text('Вход / регистрация');
            $('#subtext').text('');
            $('input[type="password"]').attr('type', 'text');
            $('input[type="text"]').val('');
            $('input[type="text"]').removeClass('pswd');
            $('label').text('Логин');
            $('.btn-next').text("Дальше");
            $('.btn-down').show();
            $('.btn-next').removeClass('regist');
            $('.btn-next').addClass('star');
            $('.btn-next').removeClass('login');
        }
    }

    $('body').on('click', '.btn-next.login', function () {
        data['pswd'] = $('input[type="password"]').val();
        console.log(data)
        $.ajax({
            url: 'login',
            method: "POST",
            data: data,
            success: function (data) {
                if(data.status){
                    document.location.href = document.location.origin + '/' + data.path
                }else{
                    $('#alert_pass').show();
                }
            }
        });
    });

    $('body').on('click', '.btn-next.regist', function () {
        if ($('input[type="password"].pswd').val() !== $('input[type="password"].pswd_repeat').val()) {
            $('#alert_pass_reg').show();
        }
        if ($('input[type="password"].pswd').val() == $('input[type="password"].pswd_repeat').val()) {
            data['pswd'] = $('input[type="password"].pswd').val();
            console.log(data)
            $.ajax({
                url: 'registration',
                method: "POST",
                data: data,
                success: function (data) {
                    document.location.href = document.location.origin + '/fillprofile';
                }
            });
        }
    });


    $('body').on("keyup", 'input[type="number"].code', function () {
        if ($(this).val().length === 4) {
            data['code'] = $(this).val();
            $.ajax({
                url: 'valid_code',
                method: 'POST',
                data: data,
                success: function (data) {
                    if (data.status) {
                        document.location.href = document.location.origin + '/' + data.path;
                    } else {
                        $('#alert_code .divform_error div').text(data.msg);
                        $('#alert_code').show();
                    }
                }
            });
        }
        if ($(this).val().length < 4) {
            $('#alert_code').hide();
        }
    });

    $('.btn-down').click(function () {
        clickSwipe();
    });

    $('body').on('click', '.btn-next.star', function () {
        clickNext();
    });

    $('#back').click(function () {
        clickBack();
    })


});