jQuery(function () {
    var id = document.location.href.split('/')
    id = id[id.length - 1]
    let acceptItem = new WebSocket("ws://" + document.location.host + "/ws/accept_item/" + $('.thing').data('value'))
    let data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()}
    const ls = new CustomSelect('#kh')
    const category = new CustomSelect('#category')
    const kind = new CustomSelect('#kind')

    function get_kind(val) {
        data['category'] = val
        $.ajax({
            url: 'get_kind',
            method: 'POST',
            data: data,
            success: function (data) {
                $('#kind_options .select__option').remove()
                for (let i = 0; i < data.kind.length; i++) {
                    $('#kind_options').append(`<li class="select__option" data-select="option"
                                                        data-value="${data.kind[i].id}"
                                                        data-index="${i}">
                                                        ${data.kind[i].name}
                                                    </li>`)
                    $('button[name="kind"]').data('index', 0);
                    $('button[name="kind"]').val(data.kind[0].id);
                    $('button[name="kind"]').text(data.kind[0].name);
                }
            }
        })
    }

    get_kind(category.value);
    document.querySelector('#category').addEventListener('select.change', (e) => {
        const btn = e.target.querySelector('.select__toggle');
        get_kind(btn.value)
    });

    $('#cancel').click(function () {
        acceptItem.send(JSON.stringify({'status': false, 'id': id}))
        document.location.href = document.location.origin + '/staff/panel'
    })

    $('#save_item').click(function () {
        data['kh'] = ls.value;
        data['tag'] = $('input[name="birka"]').val()
        data['kind'] = kind.value;
        data['comment_sab'] = $('#com_sab').val()
        data['comment'] = $('#com_kh').val()
        $('.form-check-input').each(function () {
            if ($(this).is(":checked")) {
                data['color'] = $(this).val()
            }
        });
        $.ajax({
            url: document.location.href + '/save_lostitem',
            method: "POST",
            data: data,
            success: function (data) {
                if (data.status) {
                    acceptItem.send(JSON.stringify({'status': true, 'id': id}))
                    document.location.href = document.location.origin + '/staff/panel';
                }
            },
            error: function (data) {

            }
        })
    })
})