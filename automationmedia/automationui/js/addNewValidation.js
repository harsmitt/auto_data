var addValidation = (function($){
    var onValidFormCallback = undefined;
    var addValidation = function(toValidateContainer){
        toValidateContainer.customValidator({
            oninvalidfield:function(field,message){
                var $field=$(field);
                if($field.attr('type')=='file'){
                    $field.closest('.white-box').find('.file_error').html(message);        
                }
                else{ 
                    $(field).closest('.form-group').addClass('error').prepend($('<div class="message"><span class="error_arrow "></span>'+message+'</div>'));
                }
                // $(field).focus();
            },
            onupload:function(field,error) {
                var $field=$(field); 
                if(!error){
                    $field.closest('.white-box').find('.filetext').html($field.val());
                }
                else{
                    $field.closest('.white-box').find('.filetext').empty();
                    
                }
            },
            'clearError':function(field,form) {
                if(field.attr('type')=='file'){
                    field.closest('.white-box').find('.file_error').empty();
                }
                else{
                    var $lielem= field.closest('.form-group');
                    $lielem.removeClass('error');
                    $lielem.find('.message').remove();
                }
            },
            'oninvalidform':function(valuelist,$form,submitIt){
                var target=$('.error',$form).eq(0);
                if(!target.length){
                    target = $('.file_error',$form);
                }
                if(target.length){
                    $('html,body').animate({
                        scrollTop:target.offset().top-200
                    },1000);
                    submitIt(false);
                }
            },
            onvalidform: function(valuelist,$form,submitIt){
                onValidFormCallback(valuelist,$form,submitIt);
                //So that we can call validation in  form again.
                submitIt(false);
            }
        });
    };
    addValidation.prototype.ANsetCallback = function(onValidFormCallbackp){
//            console.log("Callback logged");
            onValidFormCallback = onValidFormCallbackp;
        };
    return addValidation;
})($);
