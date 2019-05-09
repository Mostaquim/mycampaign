$(document).ready(function () {
    $(".checkbox").labelauty({ minimum_width: "170px" });
});
$('#target_postcode_select').select2({
    minimumInputLength: 2,
    tags: [],
    ajax: {
        url: 'http://127.0.0.1:8000/ajax/postcodes/',
        dataType: 'json',
        type: 'GET',
        quietMillis: 20,
        data: function (params) {
            var query = {
                q: params.term,
            }
            return query;
        },
        processResults: function (response) {
            console.log(response)
            return {
                results: response.items
            };
        },
    }
});

// var drop = $("div#dropzone-upload").dropzone({
//     dictDefaultMessage: "Upload your digital content here",
//     paramName: "file",
//     url: '\\ajax\\files\\',
//     maxFilesize: 10,
//     success: function (e) {
//         console.log(e)
//         var response = JSON.parse(e.xhr.response);
//         var inp = document.createElement('input');
//         $(inp).attr('hidden', true);
//         $(inp).attr('name', 'file_' + z);
//         z++;
//         $(inp).attr('value', response.result);
//         $('#hidden-input').append(inp);
//     }
// });
// drop.on("addedfile", function (file) {
//     file.previewElement.addEventListener("click", function () {
//         myDropzone.removeFile(file);
//     });
// });



var myDropzone = new Dropzone("div#dropzone-upload", { url: "\\ajax\\files\\" });

myDropzone.on("sending", function (file, xhr, formData) {
    // Will send the filesize along with the file as POST data.
    formData.append("csrfmiddlewaretoken", csrftoken);
});
myDropzone.on("success", function (e) {
    opt = document.createElement('option')
    $(opt).val(e.xhr.response)
    $('#attachment-select').append(opt)
    $(opt).prop("selected", true);
})