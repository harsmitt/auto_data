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
    next_elm = $(elm).parent().parent().parent().next();
    var i=1;
    while (!$(next_elm).hasClass("sec_block")){

        if ($(next_elm).hasClass('sub_block'))
            {
                if (exist_data && sub_sec_name){
                    exist = JSON.stringify(exist_data)
                    subsec_dict[sub_sec_name].push(exist)
                    exist_data=[]
                    sub_sec_name=''
                }
                sub_sec_name =$(next_elm).find('div.text').text();
                subsec_dict[sub_sec_name]=[];
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
    data = JSON.stringify(subsec_dict)
    if (confirm('Are you sure you want to update: '+ sec_name /*toTitleCase(item)*/  +' ?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/update_section/',
            data: {'type':type,'section':sec_name,'c_id':company_id,'new_data':data},
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
        if($(next_elm).hasClass('existing_block') && $(next_elm).find('input').is(":checked"))
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
    console.log(exist_data)
    if (confirm('Are you sure you want to save section: '+section  /*toTitleCase(item)*/  +' ?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/save_multiple/',
            data: {'type':type,'section':section,'c_id':company_id,'subsection':subsection,'new_data':data,'s2section':s2section},
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
    console.log(exist_data)
    if (confirm('Are you sure you want to Delete from section: '+section  /*toTitleCase(item)*/  +' ?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/delete_multiple/',
            data: {'type':type,'section':section,'c_id':company_id,'subsection':subsection,'delete_data':data,'s2section':s2section},
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


}

function swap_muliple(elm)
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
    console.log(exist_data)
    if (confirm('Are you sure you want to Delete from section: '+section  /*toTitleCase(item)*/  +' ?')) {
        jQuery.ajax({
            type: 'GET',
            url: '/automation/swap_multiple/',
            data: {'type':type,'section':section,'c_id':company_id,'subsection':subsection,'s_data':data,'item':item,'s2section':s2section},
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


}

function multiply(elm)
{
    var text = prompt("Multiplication", "PLease enter number with you want to multiply your row.");
    if (text)
    {
        $(elm).parent().parent().parent().find('td').each(function() {
            $(this).html(eval(parseInt($(this).text()) * parseInt(text)))
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

function divide(elm)
{
    var text = prompt("Division", "PLease enter number with you want to divide your row.");
    if(text){
        $(elm).parent().parent().parent().find('td').each(function() {
            $(this).html(eval(parseInt($(this).text()) / parseInt(text)))
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

function percentage(elm)
{
    var text = prompt("Percentage", "Please enter number with you want to calculate with % your row.");
    if (text){
        $(elm).parent().parent().parent().find('td').each(function() {
            $(this).html(eval(parseInt(($(this).text()) * parseInt(text))/100))
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



function neg_ro(elm)
{
    $(elm).parent().parent().parent().find('td').each(function() {
        $(this).html(-Math.abs(parseInt($(this).text())))
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


function positive(elm)
{

    console.log($(elm))

    $(elm).parent().parent().parent().find('td').each(function() {
        $(this).html(Math.abs(parseInt($(this).text())))
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