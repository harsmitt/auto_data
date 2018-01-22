/**
* Created by mahima on 7/4/16.
*/

function get_city_list(){
    state_name = document.getElementById('id_state').value;
    jQuery.ajax({
        type: 'GET',
        url: '/get-city-list/',
        data: {'state':state_name},
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
            jQuery("#id_city option").each( function() {
                jQuery(this).remove();
            });
            var city_array = new Array();
            city_array = data.city_list.split(';');
            for(i=0;i<(city_array.length-1);i++){
                jQuery("#id_city").append('<option value="'+city_array[i]+'">'+city_array[i]+'</option>');
            }
        }
    });   // Ajax Call
};
var clickedel,isSubmit;
$("#college_overview").customValidator({
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
            field.closest('.white-box').find('.file_error').empty()
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
    bindSubmitEvent:function(obj,$form){
        $('button[name="submit"]').on('click',function(e){
            isSubmit = $(this).attr('value')=='submit'?true:false;
            clickedel = $(this);
            obj.validate(e);
        })
    },
    onvalidform: function(valuelist,$form,submitIt){
        if(!App.Request.ismsaved()){
            submitIt(false);
            return false;            
        }        
        if(isSubmit && !App.Request.isconfimred()){
            submitIt(false);
            return false;
        }        
        var $form = $("#college_overview");
        var ajaxData = new FormData($form.get(0));

        if ($form.hasClass('is-uploading')) return false;
        $form.addClass('is-uploading').removeClass('is-error');
        if (droppedFiles_brochure) {
            $.each( droppedFiles_brochure, function(i, file) {
                ajaxData.append( "ebrochure", file );
            });
        }
        if (droppedFiles_logo) {
            $.each( droppedFiles_logo, function(i, file) {
                ajaxData.append( "college_logo", file );
            });
        }
        if(clickedel){
            if (isSubmit){
                ajaxData.append('identifier','final');
                ajaxData.append('submit','final-submit');
            }
            else{
                ajaxData.append('submit','save');
            }
        }
        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            data: ajaxData,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            complete: function() {
                $form.removeClass('is-uploading');
            },
            success: function(data) {
                //console.log(data);
                submitIt(false);
                if(data.success && data.redirect) {
                    window.location.href = data.redirect;
                }
                else if(data.success){
                    App.Request.SuccessAlert('submit');
                }
                else if(data.error){
                    App.Request.FailureAlert(data.error);
                }
            },
            error: function() {
                submitIt(false);
                App.Request.FailureAlert('invalid');
            }
        });
    }
});
 $('.chosen-select').chosen({width: "100%"})
droppedFiles_brochure = false;
droppedFiles_logo = false;
var $dnd_el = $("#tab3")
var $logo_el = $("#logo_id")
$dnd_el.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
})
        .on('dragover dragenter', function() {
            $dnd_el.addClass('is-dragover');
        })
        .on('dragleave dragend drop', function() {
            $dnd_el.removeClass('is-dragover');
        })
        .on('drop', function(e) {
            droppedFiles_brochure = e.originalEvent.dataTransfer.files;
        });
$logo_el.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
})
        .on('dragover dragenter', function() {
            $logo_el.addClass('is-dragover');
        })
        .on('dragleave dragend drop', function() {
            $logo_el.removeClass('is-dragover');
        })
        .on('drop', function(e) {
            droppedFiles_logo = e.originalEvent.dataTransfer.files;
        });

function openFileOption(id){
    document.getElementById(id).click();
    return false;
}
function show_file_error(id,label_id,lblerror){
    var val = $('#'+id).val();
    if(!val.trim().length) return true;
    $('#'+label_id).empty();
    $('#'+label_id).append(val);
    var allowedFiles = [".pdf"];
    var fileUpload = $('#'+id).val()
    var lblError = $('#'+lblerror);
    var regex = new RegExp("([a-zA-Z0-9\s_\\.\-:])+(" + allowedFiles.join('|') + ")$");
    if (!regex.test(fileUpload)) {
        lblError.innerHTML = "Please upload files having extensions: <b>" + allowedFiles.join(', ') + "</b> only.";
        $('#'+label_id).empty();
        $('#'+id).value ='' ;
        return false;
    }
    else{
        lblError.empty();
    }
    lblError.innerHTML = "";
    
    return true;
};
$(document).ready(function(){
    $(".editor").jqte();
    $('#header1').scrollToFixed({zIndex:200});
    $('#header2').scrollToFixed({marginTop:67,zIndex:100});
    $('#right-pannel').scrollToFixed({marginTop:151});
    jQuery.ajax({
        type: 'GET',
        url: '/college-data-capture/progress_bar/',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
            completed_percentage = Math.ceil(data.val)%10*10;
            completed_percentage = completed_percentage?completed_percentage:100;
            document.getElementById('progress_data').innerHTML= 'College Profile is '+completed_percentage+' % Completed';
            document.getElementById('progress_div').style.width =data.val+'%';
            for(i in data.progress_bar_data){
                var section=document.getElementById(i);
                if ($(section).length && data.progress_bar_data[i]==1){
                    section.className="his-select";
                }
                else{
                    $('#'+i).removeClass("sprite");
                }
            }
        }
    });

});
$(function() {
    var pgurl = window.location.href.substr(window.location.href.indexOf("/")+1);
    if (pgurl.split('/')[3]==''){
        url ="/"+pgurl.split('/')[2]+"/"
    }
    else{
        url="/"+pgurl.split('/')[2]+"/"+pgurl.split('/')[3]+"/"
    }
    $("#nav ul li a").each(function(){
        if($(this).attr("href") == url || $(this).attr("href") == '' )
            $(this).addClass("active");
    })
});
if(Request.isSubmitted){
    $('.container').find('input, textarea, button, select').attr('disabled','disabled');
}

$(".check-institute").on("change", function(){
    $(".is-institute").toggle();
});