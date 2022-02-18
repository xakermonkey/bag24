jQuery(function () {
    Dropzone.autoDiscover = false;
    var pk = document.location.href.split("/")
    var imgURL = document.location.origin + '/static/images/PlusCircle.svg'
    pk = pk[pk.length - 1]
    var firstScan = new Dropzone("#firstScan", {
        url: document.location.origin + "/staff/refound_lostitems/" + pk + '/file-upload',
        paramName: 'first',
        maxFiles: 1,
        autoProcessQueue: false,
        addRemoveLinks: true,
        init: function () {
            $(this.element).html(this.options.dictDefaultMessage);
        },
        sending: function (file, xhr, formData) {
            formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
        },
        dictDefaultMessage: `<div class="dz-message" ><img src="${imgURL}" alt=""></div>`,
        acceptedFiles: 'image/*',
    })
    var secondScan = new Dropzone("#secondScan", {
        url: document.location.origin + "/staff/refound_lostitems/" + pk + '/file-upload',
        paramName: 'second',
        maxFiles: 1,
        autoProcessQueue: false,
        addRemoveLinks: true,
        init: function () {
            $(this.element).html(this.options.dictDefaultMessage);
        },
        sending: function (file, xhr, formData) {
            formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
        },
        dictDefaultMessage: `<div class="dz-message" ><img src="${imgURL}"  alt=""></div>`,
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
        file.previewElement.addEventListener("click", function () {
            firstScan.removeFile(file);
        });
    });

    secondScan.on("addedfile", function (file) {
        file.previewElement.addEventListener("click", function () {
            secondScan.removeFile(file);
        });
    });

    var firstDoc = new Dropzone("#firstDoc", {
        url: document.location.origin + "/staff/refound_lostitems/" + pk + '/file-upload',
        paramName: 'firstDoc',
        maxFiles: 1,
        autoProcessQueue: false,
        addRemoveLinks: true,
        init: function () {
            $(this.element).html(this.options.dictDefaultMessage);
        },
        sending: function (file, xhr, formData) {
            formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
        },
        dictDefaultMessage: `<div class="dz-message" ><img src="${imgURL}"  alt=""></div>`,
        acceptedFiles: 'image/*',
        success: function (file, response) {
        },
        error: function (file, response) {

        },
    })
    var secondDoc = new Dropzone("#secondDoc", {
        url: document.location.origin + "/staff/refound_lostitems/" + pk + '/file-upload',
        paramName: 'secondDoc',
        maxFiles: 1,
        autoProcessQueue: false,
        addRemoveLinks: true,
        init: function () {
            $(this.element).html(this.options.dictDefaultMessage);
        },
        sending: function (file, xhr, formData) {
            formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
        },
        dictDefaultMessage: `<div class="dz-message" ><img src="${imgURL}"  alt=""></div>`,
        acceptedFiles: 'image/*',
        success: function (file, response) {

        },
        error: function (file, response) {
            file.previewElement.classList.add("dz-error");
        },
    })

    firstDoc.on("addedfile", function (file) {
        file.previewElement.addEventListener("click", function () {
            firstScan.removeFile(file);
        });
    });

    secondDoc.on("addedfile", function (file) {
        file.previewElement.addEventListener("click", function () {
            secondScan.removeFile(file);
        });
    });

    $('#save_refund').click(function () {
        var data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()}
        data['fio'] = $('#fio').val()
        data['series_number'] = $('#series_number').val()
        data['date_get'] = $('#date_get').val()
        data['how_get'] = $('#how_get').val()
        data['birthday'] = $('#birthday').val()


        $.ajax({
            url: pk + '/save',
            method: "POST",
            data: data,
            success: function (data) {
                if (data.status) {
                    firstScan.processQueue();
                    secondScan.processQueue();
                    firstDoc.processQueue();
                    secondDoc.processQueue();
                    document.location.href = document.location.origin + '/staff/panel'
                }
            },
            error: function (data) {
                console.log(data)

            }

        })
    })

})