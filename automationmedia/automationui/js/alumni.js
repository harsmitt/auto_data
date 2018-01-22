alum_app = {}
alum_app.tag = "alumni"
alum_app.static_data = {}
alum_app.validation_constraints = {"_name":["manditory"], "batch":["manditory"], "company":["manditory"]}

alum_app.item= function(data){
    data = data || {}
    this.id = m.prop(data.id || "")
    this._name = m.prop(data.name || "")
    this.batch = m.prop(data.batch|| "");
    this.company = m.prop(data.company_id || "");
    this.moderation_status = m.prop(data.moderation_status || "")
    this.deleted =m.prop(data.deleted || "")
    this.tag=m.prop('alumni')
}

alum_app.process_api_data = function(data){
    alum_app.static_data.company = data.cd
    return data.ad.map(function(data){
        return new alum_app.item(data)
    })
}

alum_app.fetch_items = function(){
    return m.request({method:"GET", url:"/college-data-capture/api/alumni_api/"}).then(alum_app.process_api_data);
}

alum_app.save = function(data){
    data_send = data.id() ? 
                 {'id':data.id(), 'name': data._name(), 'batch': data.batch(), 'company':data.company(), 'tag': 'alum'}
                :{'name': data._name(), 'batch': data.batch(), 'company':data.company(), 'tag': 'alum'}
    url = '/college-data-capture/alumni/'
    return common.save(url, data_send)
}


alum_app.widget_controller = common.widget_controller(alum_app)
alum_app.widget_view = common.widget_view(alum_app)

alum_app.list_editor_controller = common.list_editor_controller(alum_app)
alum_app.list_editor_view = common.list_editor_view(alum_app, "Alumni", "You can add, delete or edit all the alumni related information here", "_name")

alum_app.form_controller = common.form_controller({"select_div_1": "company"})

alum_app.form_view = function(ctrl){
    return  m(".video-form", [
                m(".white-box.flw100.marginBottom-0",[
                    m(".col-md-12",[
                        m("h2", "Add/Edit Alumni"),
                        m("p.c9", "Please fill in the required alumni details below"),
                        common.form_view_component.star_input_text_box(ctrl,"Name", "_name"),
                    ]),
                    m("ul.form-list.flw100",[

                        m("li", [
                            common.form_view_component.star_input_select_div("select_div_1", ctrl, "exampleInputEmail1",  "Company", "company", alum_app.static_data.company, "id", "name")
                        ]),
                        m("li", [
                            common.form_view_component.star_input_text_box(ctrl, "Batch", "batch")
                        ])
                    ])
                ]),

                common.form_view_component.submit_box(alum_app, ctrl, "Save Alumni", "Save and add Alumni")
            ])
}

m.mount(document.getElementById("alumcomp"), {controller:alum_app.widget_controller, view:alum_app.widget_view})
