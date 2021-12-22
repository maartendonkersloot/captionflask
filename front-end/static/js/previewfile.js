function previewFile(input) {
    var file = $("input[type=file]").get(0).files[0];

    if (file) {
        var reader = new FileReader();

        reader.onload = function () {
            $("#preview_img").attr("src", reader.result);
            $("#preview_img2").attr("src", reader.result);
        }

        reader.readAsDataURL(file);
    }
}