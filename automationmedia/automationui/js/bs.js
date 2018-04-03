
function toTitleCase(str) {
    return str.replace(/(?:^|\s)\w/g, function(match) {
        return match.toUpperCase();
    });
}



function change_comp(elm){
    $(".loader-back").show();
    item = $(elm).val().trim()
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else{type='pnl'}
    subsection =$(elm).parent().parent().closest('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    existing_sec = $(elm).parent().parent().closest('.existing_sec').find('input[type=text]')[0].value
    if (confirm('Are you sure you want to move ***'+ toTitleCase(existing_sec) +'*** to ***' +  toTitleCase(item)  +'***?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/ajax_update_component/',
            data: {'type':type,'item':item,'c_id':company_id,'subsection':subsection,'section':section,'existing_sec':existing_sec},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 5000);
                  $(".loader-back").hide();

            }
        });   // Ajax Call
        }
};

function move_s2section(elm){
    $(".loader-back").show();
    item = $(elm).val().trim()
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else
    {type='pnl'}
    s2section = $(elm).parent().parent().closest('.s2section').find('input[type=text]')[0].value
    subsection =$(elm).parent().parent().closest('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    existing_sec = $(elm).parent().parent().closest('.existing_s2sec').find('input[type=text]')[0].value
    if (confirm('Are you sure you want to move ***'+ toTitleCase(existing_sec) +'*** to ***' +  toTitleCase(item)  +'***?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/ajax_update_component/',
            data: {'type':type,'item':item,'c_id':company_id,'s2sec':s2section,'subsection':subsection,'section':section,'existing_sec':existing_sec},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 5000);
                  $(".loader-back").hide();
            }
        });   // Ajax Call
    }
};

function add_s2row(elm){
$(elm).parent().parent().after('<div class="existing_sec"><div class="col-md-3"><input type="text" style="border:None;padding-left :120px;color:red" name="existing_sec" value="ADD NEW ROW"></div><div class="col-md-1"><input style="border:None" name="exist_q1" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q2" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q3" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q4" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y1" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y2" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y3" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y4" type="text" value="0"></div><div class="col-md-1"><input style="border:None" onclick="SaveRow2(this)" type="button" value="Save Row"></div>');

};

function add_row(elm){
$(elm).parent().parent().after('<div class="existing_sec"><div class="col-md-3"><input type="text" style="border:None;padding-left :80px;color:red" name="existing_sec" value="ADD NEW ROW"></div><div class="col-md-1"><input style="border:None" name="exist_q1" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q2" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q3" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q4" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y1" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y2" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y3" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y4" type="text" value="0"></div><div class="col-md-1"><input style="border:None" type="button" onclick="SaveRow(this)" value="Save Row"></div>');};


function SaveRow(elm){
    $(".loader-back").show();
    item = $(elm).parent().parent().closest('.existing_sec').find('input[type=text]').val()
    var new_row=[]

    company_id = elm.baseURI.split('?')[1].split('=')[1]
    if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else{type='pnl'}
    subsection =$(elm).parent().parent().closest('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    $(elm).parent().parent().closest('.existing_sec').find('input[type=text]').each(function() {
        new_row.push($(this).val());
        });
    alert(new_row)
    if (confirm('Are you sure you want to add ***'+ toTitleCase(item)  +'***?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/add_row/',
            data: {'type':type,'item':item,'c_id':company_id,'subsection':subsection,'section':section,'new_row':new_row},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 5000);
                  $(".loader-back").hide();
            }
        });   // Ajax Call
    }
};

function SaveRow2(elm){
    $(".loader-back").show();
    item = $(elm).parent().parent().closest('.existing_s2sec').find('input[type=text]').val()
    var new_row=[]
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else
    {type='pnl'}
    s2section = $(elm).parent().parent().closest('.s2section').find('input[type=text]')[0].value
    subsection =$(elm).parent().parent().closest('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    $(elm).parent().parent().closest('.existing_s2sec').find('input[type=text]').each(function() {
        new_row.push($(this).val());
        });
    if (confirm('Are you sure you want to add ***'+ toTitleCase(existing_sec)  +'***?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/add_row/',
            data: {'type':type,'item':item,'c_id':company_id,'s2sec':s2section,'subsection':subsection,'section':section,'new_row':new_row},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 5000);
                  $(".loader-back").hide();
            }
        });   // Ajax Call
    }
};

function delete_row(elm){
    $(".loader-back").show();
    item = $(elm).parent().parent().closest('.existing_sec').find('input[type=text]').val()
    company_id = elm.baseURI.split('?')[1].split('=')[1]
     if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else
    {type='pnl'}
    subsection =$(elm).parent().parent().closest('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    if (confirm('Are you sure you want to Delete ***'+ toTitleCase(item)  +'*** from '+toTitleCase(subsection) )) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/delete_row/',
            data: {'type':type,'item':item,'c_id':company_id,'subsection':subsection,'section':section},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 5000);$(".loader-back").hide();
            }
        });   // Ajax Call
    }
};

function delete_row2(elm){
    $(".loader-back").show();
    item = $(elm).parent().parent().closest('.existing_s2sec').find('input[type=text]').val()
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else
    {type='pnl'}
    s2section = $(elm).parent().parent().closest('.s2section').find('input[type=text]')[0].value
    subsection =$(elm).parent().parent().closest('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    if (confirm('Are you sure you want to add ***'+ toTitleCase(item)  +'*** from '+toTitleCase(subsection))) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/delete_row/',
            data: {'type':type,'item':item,'c_id':company_id,'s2sec':s2section,'subsection':subsection,'section':section},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 5000);
                  $(".loader-back").hide();
            }
        });   // Ajax Call
    }
};

function form_save(form) {
	$('#'+form).submit();
    }
//
$(document).ready(function(){
    $( '.existing_sec').each(function() {
            sec_sum(this);

     });

    $( '.existing_sec').each(function() {
        sum_initail(this);
    });

    $( '.existing_s2sec').each(function() {
            sum_s2sec(this);
        });
});

function sec_sum(val){
    $( val).children('div').find('input').each(function() {
            g_index = this.name.split('_')[1]
            index_dict = {'q1':1,'q2':2,'q3':3,'q4':4,'y1':5,'y2':6,'y3':7,'y4':8}
             if (g_index in index_dict)
            {
                $(this).parent().parent().closest('.subsection').find('input[type=text]')[index_dict[g_index]].value= 0
                $(this).parent().parent().closest('.section').find('input[type=text]')[index_dict[g_index]].value= 0
//                $(this).parent().parent().closest('.s2section').find('input[type=text]')[index_dict[g_index]].value= 0

            }
        });

};
function sum_initail(val){

    $( val).children('div').find('input').each(function() {

        item = this.value
        g_index = this.name.split('_')[1]
        index_dict = {'q1':1,'q2':2,'q3':3,'q4':4,'y1':5,'y2':6,'y3':7,'y4':8}
        if (g_index in index_dict)
        {

            parent_n = $(this).parent().parent().closest('.subsection').find('input[type=text]')[index_dict[g_index]].value
            parent_sec_n = $(this).parent().parent().closest('.section').find('input[type=text]')[index_dict[g_index]].value


            $(this).parent().parent().closest('.subsection').find('input[type=text]')[index_dict[g_index]].value = parseInt(item) +parseInt(parent_n)
//            new_subsec = $(this).parent().parent().closest('.subsection').find('input[type=text]')[index_dict[g_index]].value


            $(this).parent().parent().closest('.section').find('input[type=text]')[index_dict[g_index]].value = parseInt(parent_sec_n) +parseInt(item)
        }

    });

};

function sum_s2sec(val){
    console.log(val)
    $( val).children('div').find('input').each(function() {
        console.log(this)
        item = this.value
        g_index = this.name.split('_')[1]
        index_dict = {'q1':1,'q2':2,'q3':3,'q4':4,'y1':5,'y2':6,'y3':7,'y4':8}
        if (g_index in index_dict)
        {
            parent_s2 = $(this).parent().parent().closest('.s2section').find('input[type=text]')[index_dict[g_index]].value
            parent_n = $(this).parent().parent().closest('.subsection').find('input[type=text]')[index_dict[g_index]].value
            parent_sec_n = $(this).parent().parent().closest('.section').find('input[type=text]')[index_dict[g_index]].value

            $(this).parent().parent().closest('.s2section').find('input[type=text]')[index_dict[g_index]].value = parseInt(item) +parseInt(parent_s2)
            $(this).parent().parent().closest('.subsection').find('input[type=text]')[index_dict[g_index]].value = parseInt(item) +parseInt(parent_n)
//            new_subsec = $(this).parent().parent().closest('.subsection').find('input[type=text]')[index_dict[g_index]].value


            $(this).parent().parent().closest('.section').find('input[type=text]')[index_dict[g_index]].value = parseInt(parent_sec_n) +parseInt(item)
        }

    });

};


function sum_val(val){
    item = val.value
    g_index =val.name.split('_')[1]
    index_dict = {'q1':1,'q2':2,'q3':3,'q4':4,'y1':5,'y2':6,'y3':7,'y4':8}
    $(val).parent().parent().closest('.subsection').find('input[type=text]')[index_dict[g_index]].value = 0
    $(val).parent().parent().closest('.section').find('input[type=text]')[index_dict[g_index]].value = 0

    $(val).parent().parent().closest('.subsection').find('input[type=text]').closest('input[name='+val.name+']').each(function() {
        item = this.value
        console.log(this.value)
        parent_n = $(this).parent().parent().closest('.subsection').find('input[type=text]')[index_dict[g_index]].value
        $(this).parent().parent().closest('.subsection').find('input[type=text]')[index_dict[g_index]].value = parseInt(item) +parseInt(parent_n)

//        parent_sec_n = $(this).parent().parent().closest('.section').find('input[type=text]')[index_dict[g_index]].value
//        $(this).parent().parent().closest('.section').find('input[type=text]')[index_dict[g_index]].value = parseInt(parent_sec_n) +parseInt(item)
     });
     sum_sub = 0
     $(val).parent().parent().closest('.section').children().each(function() {
        item = $(this).find('input[type=text]')[index_dict[g_index]].value
        console.log(item)
        sum_sub = sum_sub + parseInt($(this).find('input[type=text]')[index_dict[g_index]].value)

       $(this).closest('.section').find('input[type=text]')[index_dict[g_index]].value = sum_sub
     });
};