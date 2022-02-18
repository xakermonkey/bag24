jQuery(function () {
    const airport = new CustomSelect('#select-1');
    const staffKh = new CustomSelect('#staff-kh');
    const staffSab = new CustomSelect('#staff-sab');

    function filterThing() {
                    var date_from = $('#from_date').val()
                    var date_to = $('#to_date').val()
                    $('.thing').hide();
                    $('.thing').each(function () {
                        var date = new Date($(this).find('#date-find').data('value'))
                        var find = true
                        var color = 0
                        $('.form-check-input[type="radio"]').each(function () {
                            if ($(this).is(":checked")) {
                                color = $(this).val()
                            }
                        })
                        if (date_from != "" && date <= new Date(date_from)){
                            find = false
                        }
                        if (date_to != "" && date >= new Date(date_to)){
                            find = false
                        }
                        if (color !== 0 && color != $(this).data('color')) {
                            find = false
                        }
                        if ($('#search').val() != "") {
                            var reg = new RegExp($('#search').val(), 'i')
                            if (!reg.test($(this).find('.comment').text())){
                                find = false
                            }
                        }
                        if (airport.value != 0 && airport.value != $(this).find('.airport').data('value')) {
                            find = false
                        }
                        if (staffKh.value != 0 && staffKh.value != $(this).find('.staff-kh').data('value')) {
                            find = false
                        }
                        if (staffSab.value != 0 && staffSab.value != $(this).find('.staff-sab').data('value')) {
                            find = false
                        }
                        if (find) {
                            $(this).show()
                        }
                    })
                }

                $('#search').change(function () {
                    filterThing()
                })

                $('#from_date').change(function () {
                    filterThing()

                })
                $('#to_date').change(function () {
                    filterThing()
                })
                document.querySelector('#select-1').addEventListener('select.change', (e) => {
                    filterThing()
                });
                document.querySelector('#staff-kh').addEventListener('select.change', (e) => {
                    filterThing()
                });
                document.querySelector('#staff-sab').addEventListener('select.change', (e) => {
                    filterThing()
                });
                $('.form-check-input').click(function () {
                    filterThing()
                })
})