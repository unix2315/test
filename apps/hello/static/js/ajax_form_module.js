var AJAXFORM;

AJAXFORM = (function(){
    var moduleName = 'AJAXFORM',
        that,
        validOpts,
        ajaxSubmitOpts,
        mockData;
    mockData = {
        'status': 'OK',
        'person_photo': "/static/img/test_frontend.jpg"
    };
    ajaxSubmitOpts = {
        dataType: 'json',
        beforeSubmit: handleFormData,
        //success: handleResponseData,
        error: handleResponseData
    };
    validOpts = {
        rules: {
            name: "required",
            last_name: "required",
            date_of_birth: "required",
            email: "email",
            jabber: "email"
        },
        submitHandler: function(form) {
            $(form).ajaxSubmit(ajaxSubmitOpts)
        }
    };
    function handleFormData(){
        $("#form_submit_state").hide();
        blockForm()
    }
    function handleResponseData() {
        setTimeout(function () {
            $('#id_submit_btn')
                .replaceWith('<button id="id_submit_btn" type="submit" class="btn btn-primary">Submit</button>');
            unblockForm();
            if (mockData['status'] == 'OK') {
                showSuccessMsg();
                photoUpdate(mockData)
            }
        }, 1000);
    }
    function unblockForm() {
            $('#loading_state').hide();
            $('textarea').removeAttr('disabled');
            $('input').removeAttr('disabled');
            $('#id_submit_btn').removeAttr('disabled')
        }
    function blockForm() {
            $("#loading_state").show();
            $('textarea').attr('disabled', 'disabled');
            $('input').attr('disabled', 'disabled');
            $('#id_submit_btn').attr('disabled', 'disabled')
        }
    function showSuccessMsg(){
        $("#form_submit_state").show();
        setTimeout(function () {
            $("#form_submit_state").hide()
        }, 1500)
    }
    function photoUpdate(mockData){
        var $photoImg = $('#person_img'),
            $photoClear = $('#photo-clear_id'),
            $photoInput = $('#id_photo');
        if ($photoInput.val()!=''){
            if($photoClear.length){
                $photoClear.replaceWith('<input id="photo-clear_id" name="photo-clear" type="checkbox" />')
            }
            else{
                $photoInput.before('<input id="photo-clear_id" name="photo-clear" type="checkbox" />' +
                                '<label for="photo-clear_id">Clear</label>')
            }
            $photoImg.replaceWith('<img id="person_img" src="' + mockData['person_photo'] + '">');
            $photoInput.replaceWith('<input id="id_photo" name="photo" type="file" />')
        }
        if ($photoClear.is(':checked')){
            $photoImg.replaceWith('<img id="person_img" src="/static/img/no_photo.jpg">');
            if($photoClear.length){
                $photoClear.next().remove();
                $photoClear.remove()
            }
        }
    }
    return{
        init: function(){
            $(function(){
                $('#id_edit_form').validate(validOpts)
            });
        }
    };
}());


AJAXFORM.init();
