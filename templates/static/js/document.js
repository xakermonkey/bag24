//=================================================== fill_profile.html

jQuery(function () {
    Dropzone.autoDiscover = false;
    var data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
    var data_doc = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
    var data_adr = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
    var div = ['#lk', '#doc', '#address'];
    $('.btngroup button').click(function () {
        $('.btngroup button').each(function () {
            $(this).removeClass('selected');
        });
        $(this).addClass('selected');
        var id = $(this).data('value');
        for (const i of div) {
            if (i == id) {
                $(i).show();
            } else {
                $(i).hide();
            }
        }
    });


    $('#close').click(function () {
        $.ajax({
            url: 'is_phone',
            method: 'GET',
            success: function (data) {
                if (data.status) {
                    document.location.href = document.location.origin + '/mainmenu';
                } else {
                    $('#document').hide();
                    $('#close').hide();
                    $('#not_phone').show();
                }
            }
        });
    });

    $('#back_setting').click(function () {
        $('#document').show();
        $('#close').show();
        $('#not_phone').hide();
    });

    // =====================Личные данные==================================
    $('input[name="phone"]').keyup(function () {
        if ($(this).val().length > 0) {
            $('#btn_phone').removeAttr('disabled');
        } else {
            $('#btn_phone').attr('disabled', 'disabled');
        }
    });

    $('#btn_phone').click(function () {
        data['number'] = $('input[name="phone"]').val();
        $.ajax({
            url: 'set_number_in_fill',
            method: 'POST',
            data: data,
            success: function (data) {
                if (data.status) {
                    $('.phone_code').show();
                    $('#btn_phone').text("Подтвердить");
                    $('#btn_phone').addClass('sub');
                } else {
                    console.log(data.msg);
                }
            }
        });
    });
    $('body').on('click', '#btn_phone.sub', function () {
        data['code'] = $('input[name="code_phone"]').val();
        $.ajax({
            url: 'valid_code_in_fill',
            method: 'POST',
            data: data,
            success: function (data) {
                if (data.status) {
                    $('#phone_modal .close').trigger('click');
                    $('#success_phone').show();
                    setTimeout($('#success_phone').hide, 5000);
                } else {
                    $('#alert_phone').show();
                }
            }
        });
    });

    $('input[name="card"]').keyup(function () {
        if ($(this).val().length > 0) {
            $('#btn_card').removeAttr('disabled');
        } else {
            $('#btn_card').attr('disabled', 'disabled');
        }
    });

    $('#btn_card').click(function () {
        data['number'] = $('input[name="card"]').val();
        $.ajax({
            url: 'set_number_in_card',
            method: 'POST',
            data: data,
            success: function (data) {
                if (data.status) {
                    $('.card_code').show();
                    $('#btn_card').text("Подтвердить");
                    $('#btn_card').addClass('sub');
                } else {
                    console.log(data.msg);
                }
            }
        });
    });
    $('body').on('click', '#btn_card.sub', function () {
        data['code'] = $('input[name="code_card"]').val();
        $.ajax({
            url: 'valid_code_in_card',
            method: 'POST',
            data: data,
            success: function (data) {
                if (data.status) {
                    $('#card_modal .close').trigger('click');
                    $('#success_card').show();
                    setTimeout($('#success_card').hide, 5000);
                } else {
                    $('#alert_card').show();
                }
            }
        });
    });

    $('input[name="username"]').change(function () {
        if ($(this).val().length < 1) {
            $('#btn_lk').attr('disabled', 'disabled');
        } else {
            data['username'] = $(this).val();
        }
    });
    $('input[name="password"]').change(function () {
        if ($(this).val().length < 1) {
            $('#btn_lk').attr('disabled', 'disabled');
        } else {
            data['pswd'] = $(this).val();
        }
    });

    $('#lk input').change(function () {
        $('#btn_lk').removeAttr('disabled');
    });

    $('#btn_lk').click(function () {
        data['email'] = $('input[name="email"]').val();
        $.ajax({
            url: 'save_change_user',
            method: 'POSt',
            data: data,
            success: function (data) {
                $('#btn_lk').attr('disabled', 'disabled')
            }
        });
    });
    // ==========================================================================


    // ===================================== Паспортные данные ==================


    var re_series = new RegExp("[0-9]{4}\s[0-9]{6}");

    $('#doc input').change(function () {
        $('#btn_doc').removeAttr('disabled');
        $('#doc input').each(function () {
            if ($(this).val() === "" || typeof $(this).val() === 'undefined') {
                $('#btn_doc').attr('disabled', 'disabled');
            }
        });
    });

    $('input[name="series"]').change(function () {
        if (re_series.test($(this).val())) {
            $('#alert_series').show();
        } else {
            $('#alert_series').hide();
        }
    });

    $('#btn_doc').click(function () {
        data_doc['fio'] = $('input[name="fio"]').val();
        data_doc['series'] = $('input[name="series"]').val();
        data_doc['date_get'] = $('input[name="date_get"]').val();
        data_doc['how_get'] = $('input[name="how_get"]').val();
        data_doc['birthday'] = $('input[name="birthday"]').val();
        firstScan.processQueue();
        secondScan.processQueue();

        $.ajax({
            url: 'save_change_document',
            method: 'POST',
            data: data_doc,
            success: function (data) {
                console.log(data);
            }
        });
    });


    $('#firstDoc').click(function () {
        var data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
        data['scan'] = 'first'
        $.ajax({
            url: document.location.origin + '/file-remove',
            method: "POST",
            data: data,
            success: function () {
                $(this).hide()
                $('#firstScan').show()
            },
            error: function () {

            }
        });
    });
    $('#secondDoc').click(function () {
        var data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
        data['scan'] = 'second'
        $.ajax({
            url: document.location.origin + '/file-remove',
            method: "POST",
            data: data,
            success: function () {
                $(this).hide()
                $('#firstScan').show()
            },
            error: function () {

            }
        });
    });

    var firstScan = new Dropzone("#firstScan", {
        url: document.location.origin + '/file-upload',
        paramName: 'first',
        maxFiles: 1,
        autoProcessQueue: false,
        addRemoveLinks: true,
        init: function () {
            $(this.element).html(this.options.dictDefaultMessage);
        },
        sending: function(file, xhr, formData){
                formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
                },
        dictDefaultMessage: '<div class="dz-message" ><img src="static/images/PlusCircle.svg" id="plusFirst" alt=""></div>',
        acceptedFiles: 'image/*',
        success: function (file, response) {
            $('.dz-progress').hide()
            $('.dz-details').hide()
            $('.dz-error-message').hide()
            $('.dz-success-mark').hide()
            $('.dz-error-mark').hide()
        },
        error: function (file, response) {
            file.previewElement.classList.add("dz-error");
        },
    })
    var secondScan = new Dropzone("#secondScan", {
        url: document.location.origin + '/file-upload',
        paramName: 'second',
        maxFiles: 1,
        autoProcessQueue: false,
        addRemoveLinks: true,
        init: function () {
            $(this.element).html(this.options.dictDefaultMessage);
        },
        sending: function(file, xhr, formData){
                formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
                },
        dictDefaultMessage: '<div class="dz-message" ><img src="static/images/PlusCircle.svg" id="plusFirst" alt=""></div>',
        acceptedFiles: 'image/*',
        success: function (file, response) {
            var imgName = response;
            file.previewElement.classList.add("dz-success");
            console.log("Successfully uploaded :" + imgName);
        },
        error: function (file, response) {
            file.previewElement.classList.add("dz-error");
        },
    })

    firstScan.on("addedfile", function (file) {
        $('#btn_doc').removeAttr('disabled')
        file.previewElement.addEventListener("click", function () {
            firstScan.removeFile(file);
        });
    });

    secondScan.on("addedfile", function (file) {
        $('#btn_doc').removeAttr('disabled')
        file.previewElement.addEventListener("click", function () {
            secondScan.removeFile(file);
        });
    });


    // ========================================================================

    // ======================== Адреса =================================


    $('#address input').change(function () {
        if ($(this).val() !== "" || typeof $(this).val() !== 'undefined') {
            $(this).removeClass('bad_input');
        }
    });

    function isNotNull() {
        $('#address input').each(function () {
            if ($(this).val() === "" || typeof $(this).val() == 'undefined') {
                return false;
            }
        });
        return true;
    }

    $('#add_address').click(function () {
        $('#address input').each(function () {
            data_adr[$(this).attr('name')] = $(this).val();
            if ($(this).val() === "" || typeof $(this).val() == 'undefined') {
                $(this).addClass('bad_input');
            } else {
                $(this).removeClass('bad_input');
            }
        });
        if (isNotNull()) {
            $.ajax({
                url: 'add_address',
                method: 'POST',
                data: data_adr,
                success: function (data) {
                    if (data.status) {
                        $('.not-address').remove();
                        $('#address input').each(function () {
                            $(this).val("");
                        });
                        $('.div-my-addresses').append(`<div id="address${data.id}" class="form-check">
                                <input class="form-check-input" type="radio" name="flexRadioDefault"
                                       id="flexRadioDefault1">
                                <label class="form-check-label" for="flexRadioDefault1">
                                    ${data.name} <label class="semi f-16 grey"></label>
                                    <br>
                                    ${data.address}, подъезд ${data.entrance}, ${data.floor} этаж, кв. ${data.apartment}. Код домофона: ${data.code}
                                    <br>
                                    <a class="reform" data-value="${data.id}" href="#" style="color: #3333FF">Редактировать</a>
                                    <a class="remove" href="#" data-value="${data.id}" style="color: #BF4040">Удалить</a>
                                </label>
                            </div>`);
                    }
                }
            });
        } else {
            $('#alert_address').show();
            setTimeout($('#alert_address').hide, 5000);
        }
    });

    $('body').on('click', '.remove', function () {
        var id = $(this).data('value');
        var data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
        data['id'] = id;
        var tag_id = '#address' + id;
        $(tag_id).remove();
        $.ajax({
            url: 'remove_address',
            method: "POST",
            data: data,
            success: function (data) {
                if (data.count === 0) {
                    $('.div-my-addresses').append(`<div class="form-check not-address">
                                <div>У вас еще нет адресов!</div>
                            </div>`);
                }
            }
        })
    });


});

//=================================================== main_menu.html
jQuery(function () {
    var div = ['#in-storage', '#awaiting-delivery', '#delivered'];
    $('.btn-group-item button').click(function () {
        $('.btn-group-item button').each(function () {
            $(this).removeClass('selected');
        });
        $(this).addClass('selected');
        var id = $(this).data('value');
        for (const i of div) {
            if (i == id) {
                $(i).show();
            } else {
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
    $('#pick-up').click(function () {
        $('#choose-delivery').hide();
        $('#pick-up-ls').show();
    });
});