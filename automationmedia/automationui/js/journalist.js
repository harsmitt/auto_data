journalist_app = {}
journalist_app.tag = "journalist"

journalist_app.validation_constraints = {"_name":["manditory"], "email":["email"], "contact":["phone"]}

journalist_app.item= function(data){
    data = data || {}
    this.id = m.prop(data.id || "")
    this._name = m.prop(data.name|| "");
    // this.designation = m.prop(data.designation || "");
    this.email = m.prop(data.email || "")
    this.contact = m.prop(data.contact_number || "")
    this.moderation_status = m.prop(data.moderation_status || "")
    this.deleted =m.prop(data.deleted || "")
    this.tag=m.prop('journalist')
}

journalist_app.process_api_data = function(data){
    return data.map(function(data){
        return new journalist_app.item(data)
    })
}

journalist_app.fetch_items = function(){
    var item_list =  m.request({method:"GET", url:"/college-data-capture/api/journalist_api/"}).then(journalist_app.process_api_data);
    return item_list
}

journalist_app.delete_handler = function(item){
   m.request({method:"POST", url:"/college-data-capture/delete/", data:{'tag':'journalist', 'id':this.id}})
}

journalist_app.save = function(data){
    data_send = data.id() ? 
                 {'id':data.id(), 'name': data._name(),  'email': data.email(), 'contact_number': data.contact()}
                :{'name': data._name(),  'email': data.email(), 'contact_number': data.contact()}
    url = '/college-data-capture/api/journalist_api/'
    return common.save(url, data_send)
}

journalist_app.widget_controller = common.widget_controller(journalist_app)
journalist_app.widget_view = common.widget_view(journalist_app)

journalist_app.list_editor_controller = common.list_editor_controller(journalist_app)
journalist_app.list_editor_view = common.list_editor_view(journalist_app, "Campus Journalist", "You can add, delete or edit all the campus related information here", "_name")

journalist_app.form_controller = common.form_controller()
journalist_app.form_view =  function(ctrl){
           return  m(".white-box.flw100.marginBottom-0",[
                    common.form_view_component.form_header("Add/Edit Campus Journalist related details below", "Please fill the required contact details below"),
                    m("ul.form-list",[
                        m("li", [
                            common.form_view_component.star_input_text_box(ctrl, "Name", "_name","Enter Name")
                        ]),
                        // m("li", [
                        //     common.form_view_component.star_input_text_box(ctrl, "Designation", "designation","Enter Designation")
                        // ]),
                        m("li", [
                            common.form_view_component.star_input_text_box(ctrl, "Email", "email","Enter Email")
                        ]),
                        m("li", [
                            common.form_view_component.star_input_text_box(ctrl, "Contact Number", "contact","Enter Contact Number")
                        ])

                    ]),

                common.form_view_component.submit_box(journalist_app, ctrl, "Save Campus Journalist", "Save and Add Campus Journalist")
                ])
}


m.mount(document.getElementById("journalistcomp"), {controller: journalist_app.widget_controller,view:journalist_app.widget_view})
