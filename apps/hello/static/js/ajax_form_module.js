var AJAXFORM;

AJAXFORM = (function(){
    var moduleName = 'AJAXFORM',
        that,
        options = {
            dataType: 'json',
            beforeSubmit: handleFormData,
            //success: handleResponseData,
            error: handleResponseData
        };

    function handleFormData(){
        $("#form_submit_state").hide();
        blockForm()
    }
    function handleResponseData(data) {
        setTimeout(function () {
            $('#id_submit_btn')
                .replaceWith('<button id="id_submit_btn" type="submit" class="btn btn-primary">Submit</button>');
            unblockForm();
            showSuccessMsg()
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
    return{
        init: function(){
            $('#id_edit_form').submit(function() {
                $(this).ajaxSubmit(options);
                return false;
            });
        }
    };
}());
AJAXFORM.init();
