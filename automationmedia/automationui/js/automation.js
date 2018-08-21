function save_sec(elm){
    $(".loader-back").show();
    sec_name = $(elm).closest('th').text().trim();
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet';
    }
    else{type='pnl'}
    var subsec_dict= {};
    var exist_data=[]
    sub_sec_name =''
    var s2sec_dict = {}
    s2_sec_name =''
    next_elm = $(elm).parent().parent().parent().next();
    var i=1;
    while (!$(next_elm).hasClass("sec_block")){

        if ($(next_elm).hasClass('sub_block'))
            {
                if (exist_data && sub_sec_name && !(s2_sec_name)){
                    exist = JSON.stringify(exist_data)
                    subsec_dict[sub_sec_name].push(exist)
                    exist_data=[]
                    sub_sec_name=''
                }
                else if(s2_sec_name && sub_sec_name){
                    exist = JSON.stringify(exist_data)
                    s2sec_dict[s2_sec_name].push(exist)
                    exist_data=[]
                    s2_sec_name=''
                    s2sec  = JSON.stringify(s2sec_dict)
                    subsec_dict[sub_sec_name].push(s2sec)
                    s2sec_dict={}
                    sub_sec_name=''

                }
                sub_sec_name =$(next_elm).find('div.text').text();
                subsec_dict[sub_sec_name]=[];
            }
        else if($(next_elm).hasClass('s2sec_block'))
        {
            if (exist_data && s2_sec_name){
                    exist = JSON.stringify(exist_data)
                    s2sec_dict[s2_sec_name].push(exist)
                    exist_data=[]
                    s2_sec_name=''
                }

            s2_sec_name =$(next_elm).find('div.text').text();
            s2sec_dict[s2_sec_name]=[];

        }
        else if($(next_elm).hasClass('existing_block'))
            {
                exist_sec_name = $(next_elm).find('div.text').text();
                var values = [];
                values.push(exist_sec_name)
                $(next_elm).find('td').each(function() {
                    values.push($(this).text());
                });
                values= JSON.stringify(values)
                exist_data.push(values)
            }
        next_elm = $(next_elm).next();
        if ($(next_elm).hasClass("sec_block") && exist_data && sub_sec_name)
        {
            exist = JSON.stringify(exist_data)
            subsec_dict[sub_sec_name].push(exist)
            exist_data=[]
            sub_sec_name=''

        }
        i++;
        if (i==54){
            break;
        }
    }
    data1 = JSON.stringify(subsec_dict)
    datadict = {'type':type,'section':sec_name,'c_id':company_id,'new_data':data1}
    if (confirm('Are you sure you want to update: '+ sec_name /*toTitleCase(item)*/  +' ?')) {
        jQuery.ajax({
            type: 'POST',
            url: '/automation/update_section/',
            data: datadict,
            dataTypes: "text",
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

function SaveMultipleRow(elm)
{
    $(".loader-back").show();
    var s2section=''
    sub_sec = $(elm).parent().parent().parent()
    if (sub_sec.hasClass('sub_block')){
        subsection= sub_sec.find('div.text').text().trim()
        check_class = 'sub_block'
        if (sub_sec.prev().hasClass('sec_block'))
        {
            section = sub_sec.prev('.sec_block').first().find('div.text').text().trim()
        }
        else
        {
            section =sub_sec.prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
        }
    }
    else{
        s2section= sub_sec.find('div.text').text().trim()
        check_class = 's2sec_block'
        if (sub_sec.prev().hasClass('sub_block'))
        {
            subsection = sub_sec.prev('.sub_block').first().find('div.text').text().trim()
        }
        else
        {
            subsection = sub_sec.prevAll('.s2sec_block').prev('.sub_block').first().find('div.text').text().trim()
        }
        section = sub_sec.prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
    }

    company_id = elm.baseURI.split('?')[1].split('=')[1]
     if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else
    {type='pnl'}
    next_elm = $(elm).parent().parent().parent().next();
    var i=1;

    var exist_data=[]
    while (!$(next_elm).hasClass(check_class)){
        if($(next_elm).hasClass('existing_block'))
            {
                var exist_sec ={}
                exist_sec_name = $(next_elm).find('div.text').text();
                var values = [];
                values.push(exist_sec_name)
                $(next_elm).find('td').each(function() {
                    values.push($(this).text());
                });
                exist_data.push(values)
            }
        next_elm = $(next_elm).next();
        i++;
        if (i==25){
            break;
        }
    }

    data =JSON.stringify(exist_data)
    datadict = {'type':type,'section':section,'c_id':company_id,'subsection':subsection,'new_data':data,'s2section':s2section}
    console.log(exist_data)
    if (confirm('Are you sure you want to save section: '+section  /*toTitleCase(item)*/  +' ?')) {
        jQuery.ajax({
            type: 'POST',
            url: '/automation/save_multiple/',
            data: datadict,
            dataTypes: "text",
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
    }
}

function DeleteMultipleRow(elm)
{
    $(".loader-back").show();
    var s2section=''
    sub_sec = $(elm).parent().parent().parent()
    if (sub_sec.hasClass('sub_block')){
        subsection= sub_sec.find('div.text').text().trim()
        check_class = 'sub_block'
        if (sub_sec.prev().hasClass('sec_block'))
        {
            section = sub_sec.prev('.sec_block').first().find('div.text').text().trim()
        }
        else
        {
            section =sub_sec.prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
        }
    }
    else{
        s2section= sub_sec.find('div.text').text().trim()
        check_class = 's2sec_block'
        if (sub_sec.prev().hasClass('sub_block'))
        {
            subsection = sub_sec.prev('.sub_block').first().find('div.text').text().trim()
        }
        else
        {
            subsection = sub_sec.prevAll('.s2sec_block').prev('.sub_block').first().find('div.text').text().trim()
        }
        section = sub_sec.prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
    }
    company_id = elm.baseURI.split('?')[1].split('=')[1]
     if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else
    {type='pnl'}
    next_elm = $(elm).parent().parent().parent().next();
    var i=1;

    var exist_data=[]
    while (!$(next_elm).hasClass(check_class)){
        if($(next_elm).hasClass('existing_block') && $(next_elm).find('input').is(":checked"))
            {
                exist_sec_name = $(next_elm).find('div.text').text();
                exist_data.push(exist_sec_name)
            }
        next_elm = $(next_elm).next();
        i++;
        if (i==25){
            break;
        }
    }

    data =JSON.stringify(exist_data)
    datadict = {'type':type,'section':section,'c_id':company_id,'subsection':subsection,'delete_data':data,'s2section':s2section}
    console.log(exist_data)
    if (confirm('Are you sure you want to Delete from section: '+section  /*toTitleCase(item)*/  +' ?')) {
        jQuery.ajax({

            type: 'POST',
            url: '/automation/delete_multiple/',
            data: datadict,
            dataTypes: "text",

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
    }


}

function swap_multiple(elm)
{
    $(".loader-back").show();
    item = $(elm).val().trim()
    var s2section=''
    sub_sec = $(elm).parent().parent().parent()
    if (sub_sec.hasClass('sub_block')){
        subsection= sub_sec.find('div.text').text().trim()
        check_class = 'sub_block'
        if (sub_sec.prev().hasClass('sec_block'))
        {
            section = sub_sec.prev('.sec_block').first().find('div.text').text().trim()
        }
        else
        {
            section =sub_sec.prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
        }
    }
    else{
        s2section= sub_sec.find('div.text').text().trim()
        check_class = 's2sec_block'
        if (sub_sec.prev().hasClass('sub_block'))
        {
            subsection = sub_sec.prev('.sub_block').first().find('div.text').text().trim()
        }
        else
        {
            subsection = sub_sec.prevAll('.s2sec_block').prev('.sub_block').first().find('div.text').text().trim()
        }
        section = sub_sec.prevAll('.sub_block').prev('.sec_block').first().find('div.text').text().trim()
    }
//    section =  sub_sec.prev('.sec_block').first().find('div.text').text().trim()
     company_id = elm.baseURI.split('?')[1].split('=')[1]
     if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else
    {type='pnl'}
    next_elm = $(elm).parent().parent().parent().next();
    var i=1;

    var exist_data=[]
    while (!$(next_elm).hasClass(check_class)){
        if($(next_elm).hasClass('existing_block') && $(next_elm).find('input').is(":checked"))
            {
                exist_sec_name = $(next_elm).find('div.text').text();
                exist_data.push(exist_sec_name)
            }
        next_elm = $(next_elm).next();
        i++;
        if (i==25){
            break;
        }
    }

    data =JSON.stringify(exist_data)
    datadict={'type':type,'section':section,'c_id':company_id,'subsection':subsection,'s_data':data,'item':item,'s2section':s2section}
    console.log(exist_data)
    if (confirm('Are you sure you want to Delete from section: '+section  /*toTitleCase(item)*/  +' ?')) {
        jQuery.ajax({

            type: 'POST',
            url: '/automation/swap_multiple/',
            data: datadict,
            dataTypes: "text",
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
        elm.selectedIndex =0 ;
	    $(".loader-back").hide();
	//console.log('closed');
        //location.reload();
    }


}

function multiply(elm)
{
    var text = prompt("Multiplication", "PLease enter number with you want to multiply your row.");
    console.log(text)
    if (text)
    {
        sec_name =$(elm).parent().parent().parent().find('div.text').text()
        index_col = $(elm).parent().parent().prevAll('td').length

        if ($($(elm).parent().parent().parent().find('td')[0]).hasClass('section_td'))
            {
//                  sec_name =''

                $('.existing_block').each(function(){
                     val_td= $(this).find('td');
                     if ($(this).prevAll('.sub_block').prev('.sec_block').first().find('div.text').text() == sec_name)
                     {
                        console.log(eval(parseFloat($(val_td[index_col]).text())) * parseFloat(text))
                        $(val_td[index_col]).html(eval(parseFloat($(val_td[index_col]).text())) * parseFloat(text))
                     }


                });

        }

        else {

                $(elm).parent().parent().parent().find('td').each(function() {
                    $(this).html(eval(parseFloat($(this).text())) * parseFloat(text))
                    });
            }

            if ($(location).attr('href').split('?')[0].split('/')[4]=='balance-sheet')
                {
                    bs_total()
                }
            else
                {
                    pnl_total()
                }
    }

}

function divide(elm)
{
    var text = prompt("Division", "PLease enter number with you want to divide your row.");
    if(text){

        sec_name =$(elm).parent().parent().parent().find('div.text').text()
        index_col = $(elm).parent().parent().prevAll('td').length

        if ($($(elm).parent().parent().parent().find('td')[0]).hasClass('section_td'))
        {
            $('.existing_block').each(function(){
                 val_td= $(this).find('td');
                 if ($(this).prevAll('.sub_block').prev('.sec_block').first().find('div.text').text() == sec_name)
                 {
                    $(val_td[index_col]).html(eval(parseFloat($(val_td[index_col]).text())) / parseFloat(text))
                 }

            });

        }

        else {
            $(elm).parent().parent().parent().find('td').each(function() {
                $(this).html(eval(parseFloat($(this).text())) / parseFloat(text))
                });
            }


        if ($(location).attr('href').split('?')[0].split('/')[4]=='balance-sheet')
            {
                bs_total()
            }
        else
            {
                pnl_total()
            }
            }
}



function add_browse(elm)
{
    console.log($(elm))
    yend = $('#year_end')[0].value

    jQuery.ajax({
            type: 'GET',
            url: '/automation/get_list/',
            data: {"type":$(elm)[0].value,'yend':yend},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                console.log(data)
                val = data.split('##')
                html=""
                for (var i = 1; i <val.length+1; i++)
                    {
                        if (i%4!=0){
//                            html+= '<li><input type="checkbox" name="override" style ="width:6% !important"value='+val[i]+'>'+ val[i]+'</li>'
                            html+="<div class='col-sm-3'><h5><span>"+val[i-1]+"</span></h5><div class='input-div flt100'><input type='file' style='color:white!important;margin:0px' name="+val[i-1].replace(' ','_')+" ></div></div>"
                        }
                        else{

                            html+="<div class='col-sm-3'><h5><span>"+val[i-1]+"</span></h5><div class='input-div flt100'><input type='file' style='color:white!important;margin:0px' name="+val[i-1].replace(' ','_')+" ></div></div></div><div class='row'>"
                        }

                    }
                    html+='</ul>'
                     $('#browse').html(html)
            }
        });

}

function percentage(elm)
{
    var text = prompt("Percentage", "Please enter number with you want to calculate with % your row.");
    if (text){

        sec_name =$(elm).parent().parent().parent().find('div.text').text()
        index_col = $(elm).parent().parent().prevAll('td').length

        if ($($(elm).parent().parent().parent().find('td')[0]).hasClass('section_td'))

            {
            $('.existing_block').each(function(){
                     val_td= $(this).find('td');
                     if ($(this).prevAll('.sub_block').prev('.sec_block').first().find('div.text').text() == sec_name)
                     {
                        $(val_td[index_col]).html(eval(parseFloat(($(val_td[index_col]).text())) * parseFloat(text))/100)
                     }


                });

            }
         else {
                $(elm).parent().parent().parent().find('td').each(function() {

                    $(this).html(eval(parseFloat(($(this).text())) * parseFloat(text))/100)

                });

            }

        if ($(location).attr('href').split('?')[0].split('/')[4]=='balance-sheet')
            {
                bs_total()
            }
        else
            {
                pnl_total()
        }
    }

}



function neg_ro(elm)
{
    console.log($(elm))
    if(Date.parse($(elm).closest('th').text().trim()))
    {
        index_col = $(elm).parent().parent().prevAll('th').length
        $('.existing_block').each(function(){
            val_td= $(this).find('td');
             $(val_td[index_col]).html(-(parseFloat(0)))


        });

    }
    else{
        $(elm).parent().parent().parent().find('td').each(function() {
            $(this).html(-(parseFloat($(this).text())))
            });

            if ($(location).attr('href').split('?')[0].split('/')[4]=='balance-sheet')
                {
                    bs_total()
                }
            else
                {
                    pnl_total()
                }
        }
}



function calc(elm){
html = '<img style ="widht:10px; height:15px;" src="/media/automationui/images/minus_icon.png"  title="interchange values sign" onclick="neg_ro(this);" >'
html+='<img style ="widht:10px; height:15px;" src="/media/automationui/images/multiply_2.png"  title="Multiply"  onclick="multiply(this);" >'
html+='<img style ="widht:10px; height:15px;" src="/media/automationui/images/divide_icon.png" title="Divide"  onclick="divide(this);" >'
html+='<img style ="widht:10px; height:15px;" src="/media/automationui/images/percentage_icon.png"  title="Percentage" onclick="percentage(this);" >'
console.log($(elm))
$(elm).replaceWith(html)
}


function calc_col(elm){
//html = '<img style ="widht:10px; height:15px;" src="/media/automationui/images/minus_icon.png"  title="interchange values sign" onclick="neg_ro(this);" >'
html='<img style ="widht:10px; height:15px;" src="/media/automationui/images/multiply_2.png"  title="Multiply"  onclick="multiply(this);" >'
html+='<img style ="widht:10px; height:15px;" src="/media/automationui/images/divide_icon.png" title="Divide"  onclick="divide(this);" >'
html+='<img style ="widht:10px; height:15px;" src="/media/automationui/images/percentage_icon.png"  title="Percentage" onclick="percentage(this);" >'
console.log($(elm))
$(elm).replaceWith(html)
}


function movesecmultiple(elm){
     if (elm.baseURI.split('?')[0].split('/')[4]=='balance-sheet')
    {
        type = 'balance-sheet'
    }
    else{type='pnl'}
    html= '<select id="new_comp" style="width: 100px;" name="b_comp" onchange="swap_multiple(this);"><option value ="" selected>Select Head</option>'
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



function cal_q2(elm){
$(".loader-back").show();
    console.log($(elm))
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    word_length = $(elm).parent().parent().text().trim().split('  ').length
    cal_qtr = $(elm).parent().parent().text().trim().split('  ')[word_length-1].trim()

    elm_name = $(elm).parent().parent().text().trim().split('  ')[0].trim()
    jQuery.ajax({
            type: 'GET',
            url: '/automation/cal_qtr_pnl/',
            data: {'c_id':company_id,'q_val':elm_name,'cal_qtr':cal_qtr},
            contentType: "text/html; charset=utf-8",
            success: function(data) {
                console.log(data)

                $(".loader-back").hide();
            }
    });


}


function deleted_rows(elm)
{
    company_id = elm.baseURI.split('?')[1].split('=')[1]
    window.location = '/automation/deleted_row/?c_id='+company_id;

}




