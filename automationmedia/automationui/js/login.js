function get_dit_list(elm)
{
    sector_name = $(elm)[0].value;
    jQuery.ajax({
            type: 'GET',
            url: '/automation/dit_list/',
            data: {'sector':sector_name},
            contentType: "text/html; charset=utf-8",
            success: function(data) {

                console.log(data)
                val = data.split('##')
                    for (var i = 0; i <val.length; i++)
                    {
                        jQuery("#dit").append('<option value="' +val[i]+ '" >'+val[i]+'</option>');
                    }

                  $(".loader-back").hide();
            }
        });   // Ajax Call


}
function form_submission(form_id)
        {
//            error_message ="Enter Detail"
//            list_id = ['id_user','id_password']
//            for (i=0;i<2;i++)
//            {
//
//                if (list_id[i] =='id_user')
//                {
//                     $('#detail').attr('hidden','hidden');
//                           $('#error_msg').html(error_message);
//                                         return false;
//
//                }
//                else if(list_id[i] == 'id_password' && $('#'+list_id[i]).val() =='')
//                {
//                     $('#detail').attr('hidden','hidden');
//                     $('#error_msg').html('Please enter Password');
//                                         return false;
//                }
//
//            }

            $('#'+form_id).submit();
        }