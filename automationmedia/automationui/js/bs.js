
function toTitleCase(str) {
    return str.replace(/(?:^|\s)\w/g, function(match) {
        return match.toUpperCase();
    });
}

function calculate(val){
    $(val).html(eval($(val).text()))
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
    if ($(elm).parent().parent().parent().prev().hasClass('sub_block'))
    {
        subsection = $(elm).parent().parent().parent().prev('.sub_block').first().find('div.text').text().trim()
    }
    else
    {
        subsection = $(elm).parent().parent().parent().prevAll('.existing_block').prev('.sub_block').first().find('div.text').text().trim()
    }
//    subsection = $(elm).parent().parent().prev().find('td.subsection').text()
    section = $(elm).parent().parent().parent().prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
    existing_sec =  $(elm).closest('tr').find('div.text').text().trim()
    if (confirm('Are you sure you want to move: '+ toTitleCase(existing_sec) +' to ' +  toTitleCase(item)  +' ?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/ajax_update_component/',
            data: {'type':type,'item':item,'c_id':company_id,'subsection':subsection,'section':section,'existing_sec':existing_sec},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 1000);
                  $(".loader-back").hide();

            }
        });   // Ajax Call
        }
    else{
//        location.reload();
    $(".loader-back").hide();

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

     if (($(elm).parent().parent().parent().prev().hasClass('s2sec_block')))
    {
            s2section = $(elm).parent().parent().parent().prev('.s2sec_block').first().find('div.text').text().trim()
    }
    else
    {
         s2section = $(elm).parent().parent().parent().prevAll('.existing_block').prev('.s2sec_block').first().find('div.text').text().trim()
    }
//    }
//     s2section = $(elm).parent().parent().prev().find('td.s2sec').text()
    subsection = $(elm).parent().parent().parent().prevAll('.s2sec_block').prev('.sub_block').first().find('div.text').text().trim()
    section = section = $(elm).parent().parent().parent().prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
    existing_sec =  $(elm).closest('tr').find('div.text').text().trim()
    if (confirm('Are you sure you want to move '+ toTitleCase(existing_sec) +' to ' +  toTitleCase(item)  +' ?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/ajax_update_component/',
            data: {'type':type,'item':item,'c_id':company_id,'s2sec':s2section,'subsection':subsection,'section':section,'existing_sec':existing_sec},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 1000);
                  $(".loader-back").hide();
            }
        });   // Ajax Call
    }
    else{
//        location.reload();
    $(".loader-back").hide();
    }
};

function remove_row(elm){

   $(elm).closest('tr').remove();

};


function add_row2(elm){
    html = '<tr class="existing_block"><th class="headcol existing_sec"><div class="text sub_block" contenteditable="true">Item Name</div><div class="sub_block options_list"><input style = "height: 15px;width: 13px;margin-left: 19px;"  type="checkbox" value=""><img style ="widht:10px; height:10px;" src="/media/automationui/images/save.png" onclick="SaveRow2(this);">    <img style ="widht:10px; height:10px;" src="/media/automationui/images/delete-sign.png" onclick="remove_row(this);" ></div></th>';
    len =$(elm).parent().parent().parent().find('td').length
    for (var i = 0; i <len; i++) {
        html+='<td class="long existing_td"  contenteditable="true">0</td>'
    }
    html+='</tr>'
    $(elm).parent().parent().parent().after(html)
};


function del_row(elm){

$(elm).remove();

return false;
}

function add_row(elm){
    html = '<tr class="existing_block"><th class="headcol existing_sec" ><div class="text sub_block" contenteditable="true">Item Name</div><div class="sub_block options_list"><input style = "height: 15px;width: 13px;margin-left: 19px;"  type="checkbox" value=""><img style ="widht:10px; height:10px;" src="/media/automationui/images/save.png" onclick="SaveRow(this);">    <img style ="widht:10px; height:10px;" src="/media/automationui/images/delete-sign.png" onclick="remove_row(this);"></div></th>';
    len =$(elm).parent().parent().parent().find('td').length
    for (var i = 0; i <len; i++) {
        html+='<td class="long existing_td"  contenteditable="true">0</td>'
    }
    html+='</tr>'
    
    $(elm).parent().parent().parent().after(html)
};

function movesec(elm){
     if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else{type='pnl'}
    html= '<select id="new_comp" style="width: 100px;" name="b_comp" onchange="swap_muliple(this);"><option value ="" selected>Select Head</option>'
    jQuery.ajax({
            type: 'GET',
            url: '/automation/section_list/',
            data: {'type':type},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                val = data.split('##')
                for (i=0;i<val.length;i++){
                    html+='<option>'+val[i]+'</option>'
                }
               html+='</select>'
               if ($(elm).next('select').length==0){
	               $(elm).after(html)
		}
            }
        });


}

function move_s2sec(elm){
     if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else{type='pnl'}
    html= '<select id="new_comp" style="width: 100px;" name="b_comp" onchange="move_s2section(this);"><option value ="" selected>Select Head</option>'
    jQuery.ajax({
            type: 'GET',
            url: '/automation/section_list/',
            data: {'type':type},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                val = data.split('##')
                for (i=0;i<val.length;i++){
                    html+='<option>'+val[i]+'</option>'
                }
               html+='</select>'
               if ($(elm).next('select').length==0){
	               $(elm).after(html)
		}
            }
        });


}

function SaveRow(elm){
    $(".loader-back").show();
    item = $(elm).closest('th').text().trim();
    var new_row=[]
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else{type='pnl'}

    if ($(elm).parent().parent().parent().prev().hasClass('sub_block'))
    {
        subsection = $(elm).parent().parent().parent().prev('.sub_block').first().find('div.text').text().trim()
    }
    else
    {
        subsection = $(elm).parent().parent().parent().prevAll('.existing_block').prev('.sub_block').first().find('div.text').text().trim()
    }

    section = $(elm).parent().parent().parent().prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
    $(elm).parent().parent().parent().find('td').each(function() {

        new_row.push($(this).text());
        });
    //alert(new_row)
    if (confirm('Are you sure you want to add: '+ item /*toTitleCase(item)*/  +' ?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/add_row/',
            data: {'type':type,'item':item,'c_id':company_id,'subsection':subsection,'section':section,'new_row':new_row},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 1000);
                  $(".loader-back").hide();
            }
        });   // Ajax Call
    }
    else{
	$(".loader-back").hide();
	//console.log('closed');
        //location.reload();
    }
};

function SaveRow2(elm){
    $(".loader-back").show();
    item = $(elm).closest('th').text().trim()
    var new_row=[]
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else
    {type='pnl'}
    if (($(elm).parent().parent().parent().prev().hasClass('s2sec_block')))
    {
            s2section = $(elm).parent().parent().parent().prev('.s2sec_block').first().find('div.text').text().trim()
    }
    else
    {
         s2section = $(elm).parent().parent().parent().prevAll('.existing_block').prev('.s2sec_block').first().find('div.text').text().trim()
    }
    subsection = $(elm).parent().parent().parent().prevAll('.s2sec_block').prev('.sub_block').first().find('div.text').text().trim()
    section = $(elm).parent().parent().parent().prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
    $(elm).parent().parent().parent().find('td').each(function() {
        new_row.push($(this).text());
        });
    alert(new_row)

    if (confirm('Are you sure you want to add: '+ item/*toTitleCase(item)*/  +' ?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/add_row/',
            data: {'type':type,'item':item,'c_id':company_id,'s2sec':s2section,'subsection':subsection,'section':section,'new_row':new_row},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 1000);
                  $(".loader-back").hide();
            }
        });   // Ajax Call
    }
    else{
	$(".loader-back").hide();
//        location.reload();
    }
};



function delete_row(elm){
    $(".loader-back").show();
//    item = $(elm).closest('tr').find('td.existing_sec').text()
    item=$(elm).closest('tr').find('div.text').text().trim()
    company_id = elm.baseURI.split('?')[1].split('=')[1]
     if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else
    {type='pnl'}
    if ($(elm).parent().parent().parent().prev().hasClass('sub_block'))
    {
        subsection = $(elm).parent().parent().parent().prev('.sub_block').first().find('div.text').text().trim()
    }
    else
    {
        subsection = $(elm).parent().parent().parent().prevAll('.existing_block').prev('.sub_block').first().find('div.text').text().trim()
    }
    section = $(elm).parent().parent().parent().prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
    if (confirm('Are you sure you want to Delete: '+ toTitleCase(item)  +' from '+ toTitleCase(subsection) )) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/delete_row/',
            data: {'type':type,'item':item,'c_id':company_id,'subsection':subsection,'section':section},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                setTimeout(function()
                  {
                    location.reload();  //Refresh page
                  }, 1000);$(".loader-back").hide();
            }
        });   // Ajax Call
    }
    else{
        //location.reload();
	    $(".loader-back").hide();
    }
};

function delete_row2(elm){
    $(".loader-back").show();
//    item = $(elm).parent().parent().find('td.existing_sec').text()
    item = $(elm).closest('tr').find('div.text').text().trim()
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else
    {type='pnl'}
    if (($(elm).parent().parent().parent().prev().hasClass('s2sec_block')))
    {
            s2section = $(elm).parent().parent().parent().prev('.s2sec_block').first().find('div.text').text().trim()
    }
    else
    {
         s2section = $(elm).parent().parent().parent().prevAll('.existing_block').prev('.s2sec_block').first().find('div.text').text().trim()
    }

    subsection = $(elm).parent().parent().parent().prevAll('.s2sec_block').prev('.sub_block').first().find('div.text').text().trim()
    section = $(elm).parent().parent().parent().prevAll('.s2sec_block').prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
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
                  }, 1000);
                  $(".loader-back").hide();
            }
        });   // Ajax Call
    }
    else{
//        location.reload();
    $(".loader-back").hide();   

 }
};

function get_existing_date(elm){
    console.log($(elm))
        elm_name = $(elm).val()
        jQuery.ajax({
                type: 'GET',
                url: '/automation/get_existing_date/',
                data: {'c_name':elm_name},
                contentType: "text/html; charset=utf-8",
                success: function(data) {
                    console.log(data)
                    val = data.split('##')
                    $("#check1").empty()
                    html = '<ul>'
                    for (var i = 0; i <val.length; i++)
                    {
                        if (val[i]!='This is a new company'){
                            html+= '<li><input type="checkbox" name="override" style ="width:6% !important"value='+val[i]+'>'+ val[i]+'</li>'

                        }

                    }
                    html+='</ul>'
                    $("#check1").html(html);
                    $("#li_div").css('display','block')

                    $(".loader-back").hide();
                }
        });

}
function form_save(form) {
    $(".loader-back").show();
	$('#'+form).submit();
	$(".loader-back").hide();
    }

function change_sum(e,val){

    if (e.which==13){
        $(val).text(eval($(val).text()))

         $( '.s2sec_block').each(function() {
                    existing_sum(this);

             });
        $( '.sub_block').each(function() {
                sub_sum(this);

         });

         $( '.sec_block').each(function() {
                sec_sum(this);

         });
         total_sum();
    }
}

function bs_total(){
    $( '.s2sec_block').each(function() {
            existing_sum(this);

     });
    $( '.sub_block').each(function() {
            sub_sum(this);

     });

     $( '.sec_block').each(function() {
            sec_sum(this);

     });

     total_sum();


}

function pnl_total(){
    $( '.s2sec_block').each(function() {
            existing_sum(this);

     });
    $( '.sub_block').each(function() {
            sub_sum(this);

     });

     $( '.sec_block').each(function() {
            sec_sum(this);

     });

    total_sum_pnl();


}


function total_sum_pnl(){
    all_total = $('.total_block')
    for (total=0;total<all_total.length;total++)
    {
        val_td= $(all_total[total]).find('td');
        for (var i = 0; i <val_td.length; i++){
         $(val_td[i]).html(parseFloat(0))
        }
        if ($(all_total[total]).find('div.text').text()!='Controlling Shareholders')
        {

            all_sec = $(all_total[total]).prevAll('.sec_block')
            for (var k=0;k<all_sec.length;k++)
            {
              sec_td = $(all_sec[k]).find('td')
              for (var k1 = 0; k1 <val_td.length; k1++)
                  {
                     $(val_td[k1]).html(parseFloat($(val_td[k1]).text()) + parseFloat($(sec_td[k1]).text()));
                  }

            }
        }
        else
        {
            prev_total = $(all_total[total]).prevAll('.total_block')[0]
            prev_sec = $(all_total[total]).prevAll('.sec_block')[0]

            total_td = $(prev_total).find('td')
            sec_td = $(prev_sec).find('td')
            for (var k1 = 0; k1 <val_td.length; k1++)
              {
                 $(val_td[k1]).html(parseFloat($(total_td[k1]).text()) - parseFloat($(sec_td[k1]).text()));
                 $(val_td[k1]).css('color', 'black');
                 $(val_td[k1]).css('background-color', '#FF00FF');
              }

        }

    }



}

$(document).ready(function(){
    if ($(location).attr('href').split('?')[0].split('/')[4]=='balance-sheet')
    {
        bs_total()
    }
    else
    {
        pnl_total()
    }
});


function existing_sum(val){

    if ($(val).next().hasClass('existing_block'))
     {
        val_td= $(val).find('td');
        for (var i = 0; i <val_td.length; i++){
         $(val_td[i]).html(parseFloat(0))
        }
        next_elm = $(val).next();
        var i=1;
        while (next_elm.hasClass('existing_block'))
        {
            exist_td = $(next_elm).find('td');
            for (var p1 = 0; p1 <val_td.length; p1++) {
            html = parseFloat($(val_td[p1]).text()) + parseFloat($(exist_td[p1]).text())

//               $(val_td[p1]).html(parseFloat($(val_td[p1]).text()) + parseFloat($(exist_td[p1]).text()));
//               $(val_td[p1]).after('<div class="option_list"><img style ="widht:10px; height:10px;" src="/media/automationui/images/calc.png"  title="Calculate section Column"  onclick="calc_col(this);" ></div>')
            $(val_td[p1]).html(html)
            }
            next_elm = next_elm.next();

        }
     }


}
function sub_sum(val){

     existing_sum(val)

     if($(val).next().hasClass('s2sec_block'))
     {
        val_td= $( val).find('td');
        for (var i = 0; i <val_td.length; i++){
         $(val_td[i]).html(parseFloat(0))
        }
        next_elm = $(val).next();
        while (!$(next_elm).hasClass("sub_block"))
        {
            s2sec_td = $(next_elm).find('td');
            if ($(next_elm).hasClass('s2sec_block')){
                 for (var i = 0; i <val_td.length; i++)
                {
                    html = parseFloat($(val_td[i]).text()) + parseFloat($(s2sec_td[i]).text())
                   $(val_td[i]).html(html);
                }
            }

            next_elm = $(next_elm).next();
//            i++;
//            if (i==15){
//            break;
//            }
        }
     }
}

function total_sum()
{

    //total assets
    all_total = $('.total_block')
    val_td= $(all_total[0]).find('td');

    for (var i = 0; i <val_td.length; i++){
     $(val_td[i]).html(parseFloat(0))
    }

    all_sec = $(all_total[0]).prevAll('.sec_block')
    for (var k=0;k<all_sec.length;k++)
    {
      sec_td = $(all_sec[k]).find('td')
      for (var k1 = 0; k1 <val_td.length; k1++)
          {
             $(val_td[k1]).html(parseFloat($(val_td[k1]).text()) + parseFloat($(sec_td[k1]).text()));
          }

    }

    //total liabilities
    all_sec2 = $(all_total[0]).nextAll('.sec_block')
    val_td2= $(all_total[1]).find('td');

    for (var j1 = 0; j1 <val_td2.length; j1++){
     $(val_td2[j1]).html(parseFloat(0))
    }

    for (var j=0;j<all_sec2.length;j++)
    {

        if (!$(all_sec2[j]).prev().hasClass('total_block') || j==0){
          sec2_td = $(all_sec2[j]).find('td')
          for (var j2 = 0; j2 <val_td2.length; j2++)
                  {
                     $(val_td2[j2]).html(parseFloat($(val_td2[j2]).text()) + parseFloat($(sec2_td[j2]).text()));
                  }
        }

    }


    //total liabilities and assets
    all_sec3 = $(all_total[0]).nextAll('.sec_block')
    val_td_1= $(all_total[2]).find('td');

    for (var j1 = 0; j1 <val_td_1.length; j1++){
     $(val_td_1[j1]).html(parseFloat(0))
    }

    for (var j=0;j<all_sec3.length;j++)
    {

        if (!$(j).prev().hasClass('total_block')){
          sec_td1 = $(all_sec3[j]).find('td')
          for (var j2 = 0; j2 <val_td_1.length; j2++)
                  {
                     $(val_td_1[j2]).html(parseFloat($(val_td_1[j2]).text()) + parseFloat($(sec_td1[j2]).text()));
                  }
        }

    }


    all_total_sec = $(all_total[3]).prevAll('.total_block')
    val_td3= $(all_total[3]).find('td');

    for (var t1 = 0; t1 <val_td3.length; t1++){
     $(val_td3[t1]).html(parseFloat(0))
    }

    for (var t2=0;t2<all_total_sec.length;t2++)
    {
          total_td = $(all_total_sec[t2]).find('td')
          if (t2==2){
              for (var t3 = 0; t3 <val_td2.length; t3++)
                      {
                         $(val_td3[t3]).html(parseFloat($(val_td3[t3]).text()) + parseFloat($(total_td[t3]).text()));
                      }
                }
          else if (t2==0){
                $(val_td3[0]).css('background-color', 'yellow');
                for (var t3 = 0; t3 <val_td2.length; t3++)
                      {
                         $(val_td3[t3]).html(parseFloat($(val_td3[t3]).text()) - parseFloat($(total_td[t3]).text()));
                         $(val_td3[t3]).css('background-color', 'yellow');
                      }
          }

    }

}

function sec_sum(val){

     if($(val).next().hasClass('sub_block'))
     {
        val_td= $( val).find('td');
        for (var i = 0; i <val_td.length; i++){
         $(val_td[i]).html(parseFloat(0))
        }
        next_elm = $(val).next();
        var j=1;
        while (!$(next_elm).hasClass("sec_block"))
        {

            if ($(next_elm).hasClass('sub_block')){
                sub_td = $(next_elm).find('td');
                 for (var i = 0; i <val_td.length; i++)
                {
                    html = parseFloat($(val_td[i]).text()) + parseFloat($(sub_td[i]).text())
                    html+='<div class="option_list"><img style ="widht:10px; height:10px;" src="/media/automationui/images/calc.png"  title="Calculate section Column"  onclick="calc_col(this);" ></div>'
                   $(val_td[i]).html(html);
                }
            }

            next_elm = $(next_elm).next();
            j++;
            if (j==50){
            break;
            }
        }
     }
}


//function google() {
//    window.location = "http://google.com";
//}
function go_to_next(elm){
    $(".loader-back").show();
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    window.location = '/automation/profit-loss/?c_id='+company_id;
    $(".loader-back").hide()
}

function go_to_back(elm){
    $(".loader-back").show();
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    window.location = '/automation/balance-sheet/?c_id='+company_id;
    $(".loader-back").hide()
}

function calculate_pnl_qtr(elm){
    $(".loader-back").show();
    company_id = elm.baseURI.split('?')[1].split('=')[1]
//    window.location = '/automation/profit-loss/?c_id='+company_id;
//    $(".loader-back").hide()

    jQuery.ajax({
                type: 'GET',
                url: '/automation/pnl_last_qtr/?c_id='+company_id,
//                data: {c_id':company_id},
                contentType: "text/html; charset=utf-8",
                success: function(data) {
                    setTimeout(function()
                      {
                        location.reload();  //Refresh page
                      }, 1000);
                      $(".loader-back").hide();
                }
     });   // Ajax Call
}



function calculate_bs_qtr(elm){
    $(".loader-back").show();
    company_id = elm.baseURI.split('?')[1].split('=')[1]
//    window.location = '/automation/balance-sheet/?c_id='+company_id;
//    $(".loader-back").hide()
    jQuery.ajax({
                type: 'GET',
                url: '/automation/bs_last_qtr/?c_id='+company_id,
//                data: {c_id':company_id},
                contentType: "text/html; charset=utf-8",
                success: function(data) {
                    setTimeout(function()
                      {
                        location.reload();  //Refresh page
                      }, 1000);
                      $(".loader-back").hide();
                }
     });   // Ajax Call
}


function generate(elm){
    $(".loader-back").show();
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    window.location = '/automation/download-pdf/?c_id='+company_id;
    $(".loader-back").hide()

    jQuery.ajax({
                type: 'GET',
                url: '/automation/download-pdf/',
                data: {'c_id':company_id},
                contentType: "text/html; charset=utf-8",
                success: function(data) {
                    setTimeout(function()
                      {
                        location.reload();  //Refresh page
                      }, 1000);
                      $(".loader-back").hide();
                }
     });   // Ajax Call
}



function download_dump(elm){
    $(".loader-back").show();
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    window.location = '/automation/download-dump/?c_id='+company_id;
    $(".loader-back").hide()

    jQuery.ajax({
                type: 'GET',
                url: '/automation/download-dump/',
                data: {'c_id':company_id},
                contentType: "text/html; charset=utf-8",
                success: function(data) {
                    setTimeout(function()
                      {
                        location.reload();  //Refresh page
                      }, 1000);
                      $(".loader-back").hide();
                }
     });   // Ajax Call
}