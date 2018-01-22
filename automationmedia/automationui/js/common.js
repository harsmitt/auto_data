common = {}
common.showloading=function() {
    $('#loaderdiv').show();
}

common.hideloading=function() {
    $('#loaderdiv').hide();
}

common.editor=function(){
     $(".editor").jqte();
}

common.xhrConfig = function(xhr) {
    xhr.setRequestHeader("Content-Type", "application/json");
    return "Success"
}

common.reload =function(){
window.location.reload()
}

common.on_post_success = App.Request.on_post_success
common.on_post_error = App.Request.on_post_error

common.save = function(url, data_dict){
    common.showloading();
    return m.request({
        method: 'POST', 
        url:url, 
        data:data_dict, 
        extract: function (xhr, xhrOptions) {
            if (xhr.status === 500 || xhr.status === 404 || xhr.status === 403) return xhr.status;
            else return xhr.responseText;
        }
    }).then(common.on_post_success, common.on_post_error)
}

common.delete_handler = function(item){
    return App.Request.mdelete() && m.request({method: "POST", url:"/college-data-capture/delete/", data:{tag:this.item.tag, id:this.item.id()}
    }).then(common.reload)}

common.widget_controller = function(app_object){
    return function(args){
        this.items = app_object.fetch_items()
        this.current_item = m.prop(null)
        this.form_controller = m.prop(new app_object.form_controller(this.current_item, this.save,this.items))
        this.list_editor_controller = m.prop(new app_object.list_editor_controller(this.items, this.current_item, this.form_controller))
    }
}

common.widget_view = function(app_object){
//    common.editor();
    return function(ctrl){
               return [
                        app_object.list_editor_view(ctrl.list_editor_controller()),
                        ctrl.current_item() ? app_object.form_view(ctrl.form_controller()): null
                      ]
    }
}

// Returns a function whose 1st argument(the value to be copied) should be primitive type, obj with values as primitive types or an array with elements of primitive type

common.set_item = function(app_object){
    return function(val, container){
                if (!container()){container(new app_object.item())}
                for (prop in container()){
                    var val_prop = val[prop]()
                    var prop_type = null
                    prop_type = Object.prototype.toString.call(val_prop).slice(8).slice(0,-1)
                    if (prop_type == "Array"){
                        var copy_array = []
                        for (i in val_prop){
                            copy_array.push(val_prop[i])
                        }
                        container()[prop](copy_array)
                    }
                    else if( prop_type == "Object"){
                        var copy_obj = {}
                        for (key in val_prop){
                            copy_obj[key] = val_prop[key]
                        }
                        container()[prop](copy_obj)
                    }
                    else{
                        container()[prop](val[prop]())
                    }
                }
    }
}

common.list_editor_controller = function(app_object){
    return function(items, current_item, form_controller){
                this.items = items
                this.current_item = current_item
                this.set_item = common.set_item(app_object)
                this.form_controller = form_controller
    }
}

common.list_editor_view = function(app_object, heading, description, item_name_field){
    return function(ctrl){
        that = this;
        show_add_new = true
        if (app_object.static_data && app_object.static_data.flag && app_object.static_data.flag() == 0){show_add_new = false}
        return m("div", [
                   m(".white-box.flw100.marginBottom-0", [
                    m(".col-md-8",[
                        m("h2", heading),
                        m("p.c9.paddingBottom-0", description)
                      ]),
                       show_add_new ?
                    m(".col-md-4", [
                        m("button.btn.btn-success.pull-right", {onclick: function(){App.Request.setStatus();if (!ctrl.current_item()) {ctrl.current_item(new app_object.item()); ctrl.form_controller(new app_object.form_controller(ctrl.current_item, app_object.save))}}},[
                            m("span.sprite.plus-icon"),
                            "Add New"
                        ])
                    ]) : ""
                   ]),
                    m(".grey-box.flw100",[
                      m(".col-md-12",[
                        m("ul.sortable.college-list",
                            ctrl.items().map(function(item){
                               return  m("li",[
                                        m("div", [
                                            m("span.sprite.sortingBar_icon"),
                                            m("label.item_text", item[item_name_field]()),


                                            item.deleted()? m("span.delete_text", "Deleted"): item.moderation_status()==2? m("span.delete_text", "Approval Pending"):'',
//                                            'deleted',
                                            m("span.sprite.edit_icon",{onclick: function(){App.Request.setStatus();ctrl.set_item(item, ctrl.current_item); ctrl.form_controller(new app_object.form_controller(ctrl.current_item, app_object.save))}}),
                                            item.moderation_status()? '' : m("span.sprite.delete_icon", {onclick: common.delete_handler.bind({'item': item})})
                                        ])
                                    ])
                             })
                         )
                      ])
                    ])
                ])
    }
}

common.utils = {}

common.utils.default_select = function(value){
    if (value || value === 0){
        return value
    }
    return ""
}

common.utils.default_select_controller = function(value){
    if (value || value === 0){
        return value
    }
    return "Select"
}


common.form_controller = function(select_obj, tab_obj, search_obj){
    return function(current_item, save_function,items){
        var that = this
        this.items = items;
        this.item = current_item
        this.save = save_function
        this.error = m.prop({})
        this.tab_selected = m.prop({})
        var out_select_obj = {}
        for (div in select_obj){
            if (current_item()){
                out_select_obj[div] = common.utils.default_select_controller(current_item()[select_obj[div]]())
            }
        }
        for (tab in tab_obj){
                this.tab_selected()[tab] = tab_obj[tab]
        }

        this.out_select_text = m.prop(out_select_obj)
        this.out_select_text_start = {}
        for (prop in out_select_obj){
            this.out_select_text_start[prop] = "Select"
        }
        this.on_file_drop = function(files, id){
            that.item()[id](files[0])
        }

        this.search_value = {}
        for (i in search_obj){
            var key = search_obj[i]
            this.search_value[key] = m.prop("")
        }
        this.new_id = m.prop(null)
    }
}

common.error_message = function(error_class){
    if (error_class == "manditory"){
        return "Field is mandatory"
    }
    if (error_class == "special_character"){
        return "Special Characters are not allowed"
    }
    if(error_class == "phone"){
        return "Not a valid phone number"
    }
    if(error_class == "email"){
        return "Not a valid email"
    }
    if(error_class == "url"){
        return "Not a valid URL"
    }
    if(error_class == "file"){
        return "Not a valid File"
    }
    return "Error"
}

common.constraint_satisfied = function(constraint, value){
    if (constraint == "manditory"){
        if (typeof value == "string"){value = value.trim()}
        if($.isArray(value)){
           return value.length;
        }
        if ((value && value != "Select") || (value === 0)) {return true}
        else {return false}
    }
    if (constraint == "special_character"){
        if(!/[^a-zA-Z0-9]/.test(value)) {return true}
        else {return false}
    }
    if (constraint == "phone"){
        var re = /^[7-9]\d{9}$/;   //10 digit mobile number starting with 7,8 or 9
        if(re.test(value)){
            return true;
            }
        return false;

    }
    if(constraint == "email"){
        var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (re.test(value)){return true}
        else {return false}
    }
    if(constraint == "url"){
        var re = /(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?/
        if (re.test(value)){return true}
        else {return false}
    }
    if(constraint == "file"){
        if(!value) return true;
        var allowedFiles=["pdf"];
        var regex = new RegExp("([a-zA-Z0-9\s_\\.\-:])+(" + allowedFiles.join('|') + ")$");
        return regex.test(value.name);
    }
}

common.validate = function(constraints, ctrl){
    var item = ctrl.item()
    for (var prop in item){
        var field_constraints = constraints[prop]
        if (field_constraints){
            for (each in field_constraints){
                var each = field_constraints[each]
                var satisfied = common.constraint_satisfied(each, item[prop]())
                if (!satisfied) {
                    ctrl.error()[prop] = each;
                    //break;
                }
            }
        }
    }

    if (!(Object.keys(ctrl.error())).length){ App.Request.setStatus();return "validated"}
    App.Request.resetStatus();
    return "Not Validated"
}

common.on_save_click = function(){
    var that = this;
    var post_save = function(e){
        if (e === "Success"){
            that.ctrl.item(null)
            that.ctrl.items = that.app_object.fetch_items();

            window.location.reload()
        }
    }
    var validation = common.validate(this.app_object.validation_constraints, this.ctrl)
    if (validation == "validated"){
        common.showloading();
        this.ctrl.save(this.ctrl.item()).then(post_save).then(common.hideloading)
    }
}

common.on_save_add_click = function(){
    var that = this
    var post_save = function(e){
        if (e === "Success"){
            that.ctrl.item(new that.app_object.item());
            that.ctrl.tab_selected({});
            that.ctrl.out_select_text(that.ctrl.out_select_text_start);
            that.ctrl.new_id(null);
        }
    }

    var validation = common.validate(this.app_object.validation_constraints, this.ctrl)
    if (validation == "validated"){
        this.ctrl.save(this.ctrl.item()).then(post_save)
    }
}

common.form_view_component = {}

common.form_view_component.submit_box = function(app_object, ctrl, save_heading, save_and_add_heading){
    return m(".grey-box.flw100", [
                m(".col-md-10", [
                    m("button.btn.btn-default.marginRight-12",{onclick: common.on_save_click.bind({app_object:app_object, ctrl:ctrl})}, save_heading),
                    
                    save_and_add_heading?m("button.btn.btn-success",{onclick: common.on_save_add_click.bind({app_object:app_object, ctrl:ctrl})}, save_and_add_heading):''
                ]),
                m(".col-md-2.text-right", [
                    m("a[href=#]", {onclick: function(){App.Request.resetStatus();ctrl.error({});ctrl.item(null)}}, "Cancel")
                ])
            ])
}

common.form_view_component.input_box_attr = function(arg){
    var attributes = {}
    if (arg.type){
        attributes["type"] = arg.type
    }
    attributes[arg.event] = m.withAttr(arg.value, arg.ctrl.item()[arg.item_field])
    attributes[arg.value] = arg.ctrl.item()[arg.item_field]()
    attributes["onfocus"] = function(){delete arg.ctrl.error()[arg.item_field]}
    if (arg.placeholder){
        attributes["placeholder"] = arg.placeholder
    }
    if(arg.ctrl.item().moderation_status() ==2 ){
        attributes["disabled"] = "disabled"
    }
    return attributes
}

common.form_view_component.input_text_box = function(ctrl, label, item_field){
    var error_class = ctrl.error()[item_field]
    var arg = {
            type:"text",
            ctrl:ctrl,
            event:"oninput",
            item_field:item_field,
            value:"value"
    }
    return m(".form-group", error_class ? {class:"error"}:{} ,[
                m("label", {for:"exampleInputEmail1"}, label),
                m("input.form-control#exampleInputEmail1.manditory", common.form_view_component.input_box_attr(arg)),
                error_class ? m(".message", common.error_message(error_class)): null
             ])
}

common.form_view_component.star_input_text_box = function(ctrl, label, item_field, placeholder,help_text,freeze_new){
    var error_class = ctrl.error()[item_field]
    var arg = {
        type:"text",
        ctrl:ctrl,
        event:"oninput",
        item_field:item_field,
        value:"value",
        placeholder:placeholder
    }

     var input_attr = common.form_view_component.input_box_attr(arg)
     if (freeze_new){
        if (ctrl.item().id())
            input_attr["disabled"] = "disabled"
    }
    if(help_text =="Lakhs" || help_text == "Thousands") {
        return m(".form-group", error_class ? {class: "error"} : {}, [
            m("span.error-mgs", "No special character allowed"),
            m("label", {for: "exampleInputEmail1"}, [
                label,
                m("span.red-star", "*")
            ]), m("label", [
                help_text,]),
            m("input.form-control#exampleInputEmail1.manditory", common.form_view_component.input_box_attr(arg)),
            error_class ? m(".message", common.error_message(error_class)) : null
        ])
    }
    else{
        return m(".form-group", error_class ? {class: "error"} : {}, [
            m("span.error-mgs", "No special character allowed"),
            m("label", {for: "exampleInputEmail1"}, [
                label,
                m("span.red-star", "*")
            ]),
            m("input.form-control#exampleInputEmail1.manditory", input_attr),
            error_class ? m(".message", common.error_message(error_class)) : null
        ])
    }

}


common.form_view_component.form_header = function(heading, description){
    return  m(".col-md-12",[
                m("h2", heading),
                m("p.c9", description)
            ])
}

common.form_view_component.star_input_select_div = function(id, ctrl, for_label, label, item_field, option_list, option_value_field, option_name_field, freeze_new, select_name) {
    var error_class = ctrl.error()[item_field]
    var arg = {
        ctrl: ctrl,
        event: "onchange",
        item_field: item_field,
        value: "value"
    }
    var input_attr = common.form_view_component.input_box_attr(arg)
    if (freeze_new) {
        if (ctrl.item().id())
            input_attr["disabled"] = "disabled"
    }
    var select_onchange = function () {
        var select_val = this.options[this.selectedIndex].value
        this.value = select_val
        ctrl.out_select_text()[id] = select_val
        ctrl.item()[item_field](select_val)
        if (freeze_new) {
            ctrl.new_id(select_val)
        }
    }
    input_attr["id"] = id
    input_attr["onchange"] = select_onchange
    var get_out_text = function (value) {
        if (value == "Select") {
            return "Select " + select_name
        }
        if ((value !== 0) && (!value)) {
            return "Select "
        }
        if (option_value_field && option_name_field) {
            var arr = option_list
            for (var i = 0, i_len = arr.length; i < i_len; i++) {
                if (arr[i][option_value_field] == value) return arr[i][option_name_field];
            }
        }
        else {
            return value
        }
    }

    if (select_name == "Years" || select_name == "Months") {
        var ret = m(".form-group", error_class ? {class: "error"} : {}, [
            m("label", {for: for_label}, [
                label,
                m("span.red-star", "*")
            ]), m("label", [
                select_name]),
            m(".selectdiv", [
                m("select.selectboxdiv", input_attr,
                    function () {
                        var arr = option_list.map(function (op) {
                            if (option_name_field && option_value_field) {
                                return m("option", {value: op[option_value_field]}, op[option_name_field])
                            }
                            else {
                                return m("option", op)
                            }

                        });
                        if (!select_name) {
                            select_name = ""
                        }
                        arr.unshift(m("option", "Select " + select_name))
                        return arr
                    }.call()
                ),
                m(".out", get_out_text(ctrl.out_select_text()[id])),
                error_class ? m(".message", common.error_message(error_class)) : null
            ])
        ])
        return ret

        }

    else{
        var ret = m(".form-group", error_class ? {class: "error"} : {}, [
                m("label", {for: for_label}, [
                    label,
                    m("span.red-star", "*")
                ]),
                m(".selectdiv", [
                    m("select.selectboxdiv", input_attr,
                        function () {
                            var arr = option_list.map(function (op) {
                                if (option_name_field && option_value_field) {
                                    return m("option", {value: op[option_value_field]}, op[option_name_field])
                                }
                                else {
                                    return m("option", op)
                                }

                            });
                            if (!select_name) {
                                select_name = ""
                            }
                            arr.unshift(m("option", "Select " + select_name))
                            return arr
                        }.call()
                    ),
                    m(".out", get_out_text(ctrl.out_select_text()[id])),
                    error_class ? m(".message", common.error_message(error_class)) : null
                ])
            ])
            return ret

            }
    }
common.form_view_component.input_select_div = function(id, ctrl, for_label, label, item_field, option_list, option_value_field, option_name_field, freeze_new, select_name){

    var error_class = ctrl.error()[item_field]
    var arg = {
            ctrl:ctrl,
            event:"onchange",
            item_field:item_field,
            value:"value"
    }
    var input_attr = common.form_view_component.input_box_attr(arg)
    if (freeze_new){
        if (ctrl.item().id())
        input_attr["disabled"] = "disabled"
    }
    var select_onchange = function(){
        var select_val = this.options[this.selectedIndex].value
        this.value = select_val
        ctrl.out_select_text()[id] = select_val
        ctrl.item()[item_field](select_val)
        if (freeze_new){
            ctrl.new_id(select_val)
        }
    }
    input_attr["id"] = id
    input_attr["onchange"] = select_onchange
    var get_out_text = function(value) {
      if (value == "Select"){return "Select " +select_name}
      if ((value !== 0) && (!value)){return "Select "}
      if (option_value_field && option_name_field){
          var arr = option_list
          for (var i=0, i_len=arr.length; i<i_len; i++) {
            if (arr[i][option_value_field] == value) return arr[i][option_name_field];
          }
      }
      else {return value}
    }

    var ret =  m(".form-group", error_class? {class:"error"}:{}, [
            m("label", {for:for_label}, [
                label,

            ]),
            m(".selectdiv", [
                m("select.selectboxdiv", input_attr,
                    function(){
                        var arr =  option_list.map(function(op){
                            if (option_name_field && option_value_field){
                                return m("option", {value:op[option_value_field]}, op[option_name_field])
                            }
                            else{
                                return m("option", op)
                            }

                        });
                        if (!select_name){select_name = ""}
                        arr.unshift(m("option", "Select "+select_name))
                        return arr
                    }.call()

                ),
                m(".out", get_out_text(ctrl.out_select_text()[id])),
                error_class ? m(".message", common.error_message(error_class)): null
            ])
        ])
     return ret

}

common.form_view_component.star_input_select2_div = function(id, ctrl, for_label, label, item_field, option_list, option_value_field, option_name_field){
    var error_class = ctrl.error()[item_field]
    var arg = {
            ctrl:ctrl,
            event:"onchange",
            item_field:item_field,
            value:"value"
    }
    var input_attr = common.form_view_component.input_box_attr(arg)
    input_attr["id"] = id
    input_attr["config"] = function(element, is_init){
       var el = $(element)
       if (!is_init) {
            el.select2()
                .on("select2-selecting", function(e) {
                    el.select2("data",e.choice);
                    var select_val = el.select2("val");
                    m.startComputation();
                    ctrl.item()[item_field](select_val)
                    m.endComputation();
                })
        }

    }
    var ret =  m(".form-group", error_class? {class:"error"}:{}, [
            m("label", {for:for_label}, [
                label,
                m("span.red-star", "*")
            ]),
                m("select.selectboxdiv", input_attr,
                    function(){
                        var arr =  option_list.map(function(op){
                            if (option_name_field && option_value_field){
                                return m("option", {value:op[option_value_field]}, op[option_name_field])
                            }
                            else{
                                return m("option", op)
                            }

                        });
                        arr.unshift(m("option", "Select"))
                        return arr
                    }.call()

                ),
                error_class ? m(".message", common.error_message(error_class)): null
            ])
     return ret

}


common.form_view_component.star_input_text_area = function(ctrl, for_label, label, item_field, attrs,star=false){
    console.log('rendering buddy')
    console.log(ctrl.error())
    var error_class = ctrl.error()[item_field]
    var arg = {
        ctrl:ctrl,
        event: "onchange",
        item_field: item_field,
        value: "value",
        star:star,
    }
        var formconfig=function(el,isInit,context){

                var $el=$(el);
                $el.data('jqte',false);
                $el.jqte({
                        focus:function(){

                            delete arg.ctrl.error()[arg.item_field]
                            m.redraw();
                                                        //$el.closest('.form-group').removeClass('error').find('.message').hide();

                        },



                        change:function(){
                            var value=$el.val()
                            arg.ctrl.item()[arg.item_field](value);
                        }

                });



                if(ctrl.item().moderation_status()==2){
                    $el.closest('.jqte').find('.jqte_editor').prop('contenteditable','false')
                }
        }
   var input_attr = common.form_view_component.input_box_attr(arg)


   input_attr.config = formconfig;


   for (key in attrs){
       input_attr[key] = attrs[key]
   }

   if (arg.star){
      var ret = m(".form-group", error_class? {class:"error"}:{}, [
                 m("label", {for: for_label}, [
                     label,
                     m("span.red-star", "*")
                  ]),
                 m("textarea.form-control editor", input_attr),
                error_class ? m(".message", common.error_message(error_class)): null

             ])
        }
    else{

        var ret = m(".form-group", error_class? {class:"error"}:{}, [
                 m("label", {for: for_label}, [
                     label
                  ]),
                 m("textarea.form-control editor", input_attr),
                error_class ? m(".message", common.error_message(error_class)): null
             ])

    }
   return ret
}

common.form_view_component.input_checkbox = function(ctrl, checklist){
    var get_input_attr = function(item){
        var input_attr = {}
        var in_array = function isInArray(value, array) {
          return array.indexOf(value) > -1;
        }
        input_attr["type"] = "checkbox"
        input_attr["id"] = "inlineCheckBox1"
        input_attr["value"] = item.id
        input_attr["checked"] = in_array(item.id, ctrl.item().feature_ids())
        input_attr["onchange"] = function(){
            if (this.checked){
                ctrl.item().feature_ids().push(item.id)
            }
            else{
                ctrl.item().feature_ids(ctrl.item().feature_ids().filter(
                        function(feature_id){
                            return feature_id !== item.id
                        }
                ))
            }
        }
        if (ctrl.item().moderation_status() ==2){
            input_attr["disabled"] = "disabled"
        }
        return input_attr
    }

    return m("ul.checkbox.facility_type.flw100)",
             checklist.map(function(item){
                 return m("li", [
                         m("label.checkbox-inline", [
                             m("input", get_input_attr(item)),
                             item.name
                          ])
                       ])
             })
          )
}

common.form_view_component.input_date_box = function(ctrl, label, item_field, attrs){
   var arg = {
    ctrl:ctrl,
    event: "onchange",
    item_field: item_field,
    value: "value"
   }
   var input_attr = common.form_view_component.input_box_attr(arg)
   for (key in attrs){
       input_attr[key] = attrs[key]
   }
   var add_picker = function(element, is_init){
       /*
       if (!is_init){
           var $form_date = $(element)
           $form_date.datetimepicker({
                minView: 2,
                format: 'dd-mm-yyyy HH:ii',
                startDate: new Date,
                autoclose: true,
           });
       }
       */
   }
   return m(".form-group", [
                m("label.control-label", label),
                m(".input-group.date", {config:add_picker}, [
                    m("input.form-control.borderRight-0", input_attr),
                    m("span.input-group-addon", [
                        m("span.glyphicon-calender")
                    ])
                ]),
                //m("input#dtp_input2",{type:"hidden", value:""})
           ])
}


common.form_view_component.image_upload = function(ctrl, id){
    var dragdrop = function(element, options) {
        options = options || {}
        element.addEventListener("dragover", activate)
        element.addEventListener("dragleave", deactivate)
        element.addEventListener("dragend", deactivate)
        element.addEventListener("drop", deactivate)
        element.addEventListener("drop", update)

        function activate(e) {
            e.preventDefault()
        }
        function deactivate() {}
        function update(e) {
            e.preventDefault()
            if (typeof options.onchange == "function") {
                options.onchange((e.dataTransfer || e.target).files, id)
            }
        }
    }
    var onBrowse=function(el,isInit,context){
        if(!isInit){
            var $el=$(el);
            $el.on('click',function(e) {
                e.preventDefault();
                var $this=$(this);
                var hiddeninput = $this.closest('.upload-wrap').find('.fileinput');
                hiddeninput.trigger('click');
            })
        }
    }

    return  m("div.text-center.upload-wrap",{
        config: function(element, is_initialized){
            if (!is_initialized){
                dragdrop(element, {onchange:ctrl.on_file_drop})
            }
        }
    },[
                m("span.sprite.doc-iocn"),
                m("input[type=file].fileinput",{style:"display:none",
                    onchange:function(){
                        ctrl.on_file_drop(this.files,id)
                    },
                }),
                m("p",[
                    "You can drop or ",
                    m("a",{ config:onBrowse },[
                        m("strong","Browse"),
                    ]),
                    " pdf file here to upload"
                ]),
                m("p.fs-12.c9","Maximum file size is 10mb")
            ])
}

common.form_view_component.image_upload1 = function(ctrl, id){
    var dragdrop = function(element, options) {
        options = options || {}
        element.addEventListener("dragover", activate)
        element.addEventListener("dragleave", deactivate)
        element.addEventListener("dragend", deactivate)
        element.addEventListener("drop", deactivate)
        element.addEventListener("drop", update)

        function activate(e) {
            e.preventDefault()
        }
        function deactivate() {}
        function update(e) {
            e.preventDefault()
            if (typeof options.onchange == "function") {
                options.onchange((e.dataTransfer || e.target).files, id)
            }
        }
    }
    var onBrowse=function(el,isInit,context){
        if(!isInit){
            var $el=$(el);
            $el.on('click',function(e) {
                e.preventDefault();
                var $this=$(this);
                var hiddeninput = $this.closest('.upload-wrap').find('.fileinput');
                hiddeninput.trigger('click');
            })
        }
    }

    return  m("div.text-center.upload-wrap",{
        config: function(element, is_initialized){
            if (!is_initialized){
                dragdrop(element, {onchange:ctrl.on_file_drop})
            }
        }
    },[
                m("span.sprite.doc-iocn"),
                m("input[type=file].fileinput",{style:"display:none",
                    onchange:function(){
                        ctrl.on_file_drop(this.files,id)
                    },
                }),
                m("p",[
                    "You can drop or ",
                    m("a",{ config:onBrowse },[
                        m("strong","Browse"),
                    ]),
                    " images here to upload"
                ]),
                m("p.fs-12.c9","Maximum file size is 10mb")
            ])
}

common.form_view_component.star_search_checkboxes = function(args){
    args.star =true;
    return common.form_view_component.search_checkboxes.call(this,args);
}

common.form_view_component.search_checkboxes = function(args){
    var error_class= args.error;
    var ctrl = args.ctrl;
    var label = args.label
    var search_label = args.search_label
    var search_value = args.search_value
    var checked = args.checked
    var fieldvals = args.fieldvals || false
    var checklist = args.checklist.filter(function(item){
        var string_starts_with = function (string, prefix) {
            return string.slice(0, prefix.length) == prefix;
        }
        return string_starts_with(item.name.toLowerCase(), search_value().toLowerCase())
    })
    .sort(function(item1,item2){
        var item1_exist = (checked.indexOf(item1.id)>-1)?1:0,item2_exist = (checked.indexOf(item2.id)>-1)?1:0
        return item2_exist-item1_exist;
    });
    var moderation_status = args.moderation_status
    var check_input_attr = function(item){
        var attrs = {}
        if (moderation_status == 2){
            attrs.disabled = "disabled";
        }
        attrs.onclick = function(){
            var that=this;
             args.star?delete ctrl.error()[args.item_field]:'';
            var delete_from_list = function(array, elem){
                var index = array.indexOf(elem)
                array.splice(index, 1)
            }
            if (that.checked){
                checked.push(item.id)
            }
            else{
                delete_from_list(checked, item.id)
            }
        }
        attrs.checked = (checked.indexOf(item.id) > -1)
        return attrs
    }
    var scrollconfig = function(elem, is_init){
        if (! is_init){
            var $elem = $(elem)
            $elem.mCustomScrollbar({
                set_height:"195px",
                mouseWheel:true
            });
        }
    }
    var set_fieldval=function(item) {
        return function(e){
            var $input = $(e.target);
            fieldvals[item.id]=parseInt($input.val())
            console.log(fieldvals[item.id]);
        }
    }
    return m("li", [
        m(".form-group",error_class ? {class:"error"}:{}, [
            error_class?m("div.message", "Fields are mandatory"):"",
            m("label", {for:"exampleInputEmail1"}, [
                    label,
                    args.star?m("span.red-star", "*"):""
                ]),

                        m(".greyBorder-box.padding-0", [
                    m(".filter_search", [
                        m(".search_wrap", [
                            m("a.filter_search_icon[href='#']"),
                            m("input[name=''][type='text']",{placeholder:search_label, oninput:m.withAttr("value", search_value), value: search_value()})
                        ])
                    ]),
                    m(".content_12.mCustomScrollbar._mCS_1", {style: {"height": " 195px"}, config:scrollconfig}, [m(".mCustomScrollBox.mCS-light.mCSB_vertical.mCSB_inside[id='mCSB_1'][tabindex='0']", [m(".mCSB_container[dir='ltr'][id='mCSB_1_container']", {style: {"position": " relative", " top": " 0px", " left": " 0px"}}, [
                                m("ul.fliters",
                                    checklist.map(function(item){
                                        return m("li", {key:item.name},[
                                                m("label.checkbox-inline", [
                                                    m("input[id='inlineCheckbox1'][type='checkbox']", check_input_attr(item)),
                                                    item.name,
                                                    fieldvals?m('input[type="text"].textsearch-inline',{onchange:set_fieldval(item),value:fieldvals[item.id] || 0}):''

                                                    ]),
                                                ])

                                    })
                                )
                            ]),m(".mCSB_scrollTools.mCSB_1_scrollbar.mCS-light.mCSB_scrollTools_vertical[id='mCSB_1_scrollbar_vertical']", {style: {"display": " block"}}, [m(".mCSB_draggerContainer", [m(".mCSB_dragger[id='mCSB_1_dragger_vertical'][oncontextmenu='return false;']", {style: {"position": " absolute", " min-height": " 30px", " display": " block", " height": " 124px", " max-height": " 185px", " top": " 0px"}}, [m(".mCSB_dragger_bar", {style: {"line-height": " 30px"}})]),m(".mCSB_draggerRail")])])])])

                ])


            ]),
                    "\
        "
            ])
}

common.form_view_component.multiple_input = function(seats,moderation_status){
    
    var get_input_attr = function(index){
        var input_attr = {}
        if (moderation_status == 2){
            input_attr.disabled = "disabled";
        }
        input_attr.oninput = function(){
            seats[index].seats = this.value
        }

        if(seats[index])
        {
            input_attr.value = seats[index].seats
        }
        else
        {
            input_attr.value = 0
        }
        return input_attr
    }
    var total_seats = 0
    $.each(seats, function(){
        if(!isNaN(this.seats)){
            total_seats += parseInt(this.seats)
        }
    })
    count = -1
    return [m("li", [
        m(".form-group", [
            m("label[for='exampleInputEmail1']", ["Seats Available "]),
            m(".seat-available", [
                m("ul", seats.map(function(seat){
                    count++
                    return m('li', [seat.category, m("input.seat", get_input_attr(count))])
                }),
                    m("li.bold", ["Total ",m("strong", total_seats)])
                )
            ])
        ])
    ])]
}
common.scrollToTarget=function(target){
    $('html,body').animate({
        scrollTop:$(target).offset().top-100,
    },1000);
}
