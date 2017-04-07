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
    }
    function handleResponseData(data) {
        setTimeout(function () {
            $('#id_submit_btn')
                .replaceWith('<button id="id_submit_btn" type="submit" class="btn btn-primary">Submit</button>');
        }, 1000);
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
