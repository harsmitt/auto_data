
function toTitleCase(str) {
    return str.replace(/(?:^|\s)\w/g, function(match) {
        return match.toUpperCase();
    });
}



function change_comp(elm){
    item = $(elm).val().trim()
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    subsection =$(elm).parent().parent().closest('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    existing_sec = $(elm).parent().parent().closest('.existing_sec').find('input[type=text]')[0].value
    if (confirm('Are you sure you want to move ***'+ toTitleCase(existing_sec) +'*** to ***' +  toTitleCase(item)  +'***?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/ajax_update_component/',
            data: {'item':item,'c_id':company_id,'subsection':subsection,'section':section,'existing_sec':existing_sec},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                $("#test").html(data)
            }
        });   // Ajax Call
        }
};

function move_s2section(elm){
    item = $(elm).val().trim()
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    s2section = $(elm).parent().parent().closest('.s2section').find('input[type=text]')[0].value
    subsection =$(elm).parent().parent().closest('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    existing_sec = $(elm).parent().parent().closest('.existing_s2sec').find('input[type=text]')[0].value
    if (confirm('Are you sure you want to move ***'+ toTitleCase(existing_sec) +'*** to ***' +  toTitleCase(item)  +'***?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/ajax_update_component/',
            data: {'item':item,'c_id':company_id,'s2sec':s2section,'subsection':subsection,'section':section,'existing_sec':existing_sec},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                $("#test").html(data)
            }
        });   // Ajax Call
    }
};

function add_s2row(elm){
$(elm).parent().parent().after('<div class="existing_sec"><div class="col-md-3"><input type="text" style="border:None;padding-left :120px;color:red" name="existing_sec" value="ADD NEW ROW"></div><div class="col-md-1"><input style="border:None" name="exist_q1" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q2" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q3" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q4" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y1" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y2" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y3" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y4" type="text" value="0"></div><div class="col-md-1"><input style="border:None" onclick="SaveRow2(this)" type="button" value="Save Row"></div>');

};

function add_row(elm){
$(elm).parent().parent().after('<div class="existing_sec"><div class="col-md-3"><input type="text" style="border:None;padding-left :80px;color:red" name="existing_sec" value="ADD NEW ROW"></div><div class="col-md-1"><input style="border:None" name="exist_q1" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q2" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q3" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_q4" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y1" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y2" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y3" type="text" value="0"></div><div class="col-md-1"><input style="border:None" name="exist_y4" type="text" value="0"></div><div class="col-md-1"><input style="border:None" type="button" onclick="SaveRow(this)" value="Save Row"></div>');
};


function SaveRow(elm){
    item = $(elm).parent().parent().closest('.existing_sec').find('input[type=text]').val()
    var new_row=[]
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    subsection =$(elm).parent().parent().prev('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    $(elm).parent().parent().closest('.existing_sec').find('input[type=text]').each(function() {
        new_row.push($(this).val());
        });
    alert(new_row)
    if (confirm('Are you sure you want to add ***'+ toTitleCase(item)  +'***?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/add_row/',
            data: {'item':item,'c_id':company_id,'subsection':subsection,'section':section,'new_row':new_row},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                $("#test").html(data)
            }
        });   // Ajax Call
    }
};

function SaveRow2(elm){
    item = $(elm).parent().parent().closest('.existing_s2sec').find('input[type=text]').val()
    var new_row=[]
    company_id = elm.baseURI.split('?')[1].split('=')[1]
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
            data: {'item':item,'c_id':company_id,'s2sec':s2section,'subsection':subsection,'section':section,'new_row':new_row},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                $("#test").html(data)
            }
        });   // Ajax Call
    }
};

function delete_row(elm){
    item = $(elm).parent().parent().closest('.existing_sec').find('input[type=text]').val()
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    subsection =$(elm).parent().parent().closest('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    if (confirm('Are you sure you want to Delete ***'+ toTitleCase(item)  +'*** from '+toTitleCase(subsection) )) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/delete_row/',
            data: {'item':item,'c_id':company_id,'subsection':subsection,'section':section},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                $("#test").html(data)
            }
        });   // Ajax Call
    }
};

function delete_row2(elm){
    item = $(elm).parent().parent().closest('.existing_s2sec').find('input[type=text]').val()
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    s2section = $(elm).parent().parent().closest('.s2section').find('input[type=text]')[0].value
    subsection =$(elm).parent().parent().closest('.subsection').find('input[type=text]')[0].value
    section = $(elm).parent().parent().closest('.section').find('input[type=text]')[0].value
    if (confirm('Are you sure you want to add ***'+ toTitleCase(item)  +'*** from '+toTitleCase(subsection))) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/delete_row/',
            data: {'item':item,'c_id':company_id,'s2sec':s2section,'subsection':subsection,'section':section},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                $("#test").html(data)
            }
        });   // Ajax Call
    }
};

//