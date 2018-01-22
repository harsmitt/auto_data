testimonial_app = {}
testimonial_app.tag = "testimonial"
testimonial_app.static_data = {}

testimonial_app.validation_constraints = {"_name":["manditory"], "batch":["manditory"], "course":["manditory"],"testimonial":['manditory']}

testimonial_app.item= function(data){
    data = data || {}
    this.id = m.prop(data.id || "")
    this._name = m.prop(data.name || "")
    this.batch = m.prop(data.batch|| "");
    this.course = m.prop(data.course || "");
    this.testimonial = m.prop(data.testimonial || "");
    this.moderation_status = m.prop(data.moderation_status || "")
    this.deleted =m.prop(data.deleted || "")
    this.tag=m.prop('testimonial')
}

testimonial_app.process_api_data = function(data){
    testimonial_app.static_data.courses = data.cd
    return data.td.map(function(data){
        return new testimonial_app.item(data)
    })
}

testimonial_app.fetch_items = function(){
    return m.request({method:"GET", url:"/college-data-capture/api/testimonial_api/"}).then(testimonial_app.process_api_data)
}

testimonial_app.save = function(data){
    data_send = data.id() ? 
                 {'id':data.id(), 'name': data._name(), 'batch': data.batch(), 'course':data.course(), 'testimonial':data.testimonial(),'tag': 'testimonial'}
                :{'name': data._name(), 'batch': data.batch(), 'course':data.course(), 'testimonial':data.testimonial(), 'tag': 'testimonial'}
    url = "/college-data-capture/alumni/"
    return common.save(url, data_send)
}


testimonial_app.widget_controller = common.widget_controller(testimonial_app)
testimonial_app.widget_view = common.widget_view(testimonial_app)

testimonial_app.list_editor_controller = common.list_editor_controller(testimonial_app)
testimonial_app.list_editor_view = common.list_editor_view(testimonial_app,"Student Testimonials","You can add, edit or delete all the testimonial related information here", "_name")
testimonial_app.form_controller = common.form_controller({"select_div_2":"course"})


testimonial_app.form_view = function(ctrl){
       return  m(".video-form", [
                m(".white-box.flw100.marginBottom-0",[
                    m(".col-md-12", [
                        m("h2", "Add/Edit Testimonials"),
                        m("p.c9", "Please fill the required testimonial details below"),
                        m("li", [
                             common.form_view_component.star_input_text_box(ctrl, "Name", "_name")
                        ]),
                   m("li", [
                             common.form_view_component.star_input_text_box(ctrl, "Testimonial", "testimonial")
                        ]),
                    ]),

                    m("ul.form-list.flw100",[


                        m("li", [
                            common.form_view_component.star_input_select_div("select_div_2", ctrl, "exampleInputEmail1", "Course", "course", testimonial_app.static_data.courses, "id", "name")
                        ]),
                        m("li", [
                            common.form_view_component.star_input_text_box(ctrl, "Batch", "batch")
                        ])
                    ])
                ]),

                common.form_view_component.submit_box(testimonial_app, ctrl, "Save Testimonials", "Save and Add Testimonials")
            ])
}

m.mount(document.getElementById("testimonialcomp"),{controller:testimonial_app.widget_controller, view:testimonial_app.widget_view})
