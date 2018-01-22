infra_app ={}
infra_app.tag = "infrastructure"
infra_app.static_data = {}
infra_app.static_data.all_features_list = []
infra_app.static_data.all_features = {}
infra_app.static_data.facility_list = []
infra_app.static_data.summary = m.prop(undefined)
infra_app.static_data.moderation_status = m.prop(undefined)
infra_app.validation_constraints = {"details":["manditory"]}
infra_app.static_data.flag = m.prop(undefined)

infra_app.summary_view = function(ctrl){
    var val = infra_app.static_data.summary() || ""
    var disabled = infra_app.static_data.moderation_status() ? "disabled" : ""
    var formconfig=function(el,isInit,context){
                var $el=$(el);
                $el.data('jqte',false);
                $el.jqte();
                if(infra_app.static_data.moderation_status()==2){
                    $el.closest('.jqte').find('.jqte_editor').prop('contenteditable','false')
                }
        }

    var input_attr = function(){
       var ret = {}
       ret.oninput = m.withAttr("value", infra_app.static_data.summary)
       ret.value = val
       if (disabled){
           ret.disabled = "disabled"
       }
        ret.config = formconfig;
       return ret
    }
    return m(".white-box.flw100", [
            m(".form-group.marginBottom-0.col-md-12", [
                m("label", {for:"exampleInputEmail1"},[ 
                    "Infrastructure Summary",
                    m("span.red-star", "*")
                ]),
                m("textarea.form-control editor", input_attr())
            ])
           ])
}

infra_app.item = function(data, item_features){
    data = data || {}
    item_features = item_features || []
    this.id = m.prop(data.id || "")
    this._name = m.prop(data.name || "")
    this.details = m.prop(data.details || "")
    this.feature_ids = m.prop(item_features || "")
    this.new_id = m.prop(null)
    this.moderation_status = m.prop(data.moderation_status || "")
    this.deleted =m.prop(data.deleted || "")
    this.tag=m.prop('infrastructurefacility')

}

infra_app.process_api_data = function(data){
    infra_app.static_data.all_features = data.all_features
    infra_app.static_data.flag(data.flag)
    for (id in data.all_features){
        infra_app.static_data.all_features_list = infra_app.static_data.all_features_list.concat(data.all_features[id])
    }

    
    if(infra_app.static_data.summary() == undefined){
        infra_app.static_data.summary(data.infra.summary)
        infra_app.static_data.moderation_status(data.infra.moderation_status)
    }
    var facilities = data.facilities
    var total_facilities = data.total_facilities
    for (i in total_facilities){
        infra_app.static_data.facility_list.push(total_facilities[i])
    }
    var ret= facilities.map(function(item){
        return new infra_app.item(item, data.features[item.id].map(
            function(feature){
                return feature['id']
            }
        ))
    })
    return ret
}

infra_app.fetch_items = function(){
    return m.request({method:"GET", url:"/college-data-capture/api/infra_api/"}).then(infra_app.process_api_data)
}

infra_app.delete_handler = function(item){
   m.request({method:"POST", url:"/college-data-capture/delete/", data:{'tag':this.tag, 'id':this.id}})
}

infra_app.save = function(data){
    data.id()?
    data_send = {"id":data.id(), "detail": data.details(), "feature": data.feature_ids()}
    :data_send = {"new_id":data.new_id(), "detail": data.details(), "feature": data.feature_ids()}
    url = "/college-data-capture/infrastructure/"
    return common.save(url, data_send)
}

infra_app.widget_controller = common.widget_controller(infra_app)
infra_app.widget_view = common.widget_view(infra_app)

infra_app.list_editor_controller = common.list_editor_controller(infra_app)
infra_app.list_editor_view = common.list_editor_view(infra_app, "Facilities", "You can add, edit or delete all the facility related information here", "_name", infra_app.static_data.flag())

infra_app.form_controller = common.form_controller({"select_div_1":"new_id"})


infra_app.form_view =  function(ctrl){ 
    var checklist = ctrl.item().id() ?
                    infra_app.static_data.all_features[ctrl.item().id()]
                    :infra_app.static_data.all_features_list
    if (!ctrl.item().id()){
        if(ctrl.new_id()){
            checklist = infra_app.static_data.all_features[ctrl.new_id()]
        }
    }
    return m(".white-box.flw100.paddingBottom-0",[
                 m(".col-md-12", [
                     m("h2", "Add/Edit Facility"),
                     m("p.c9", "Please fill the required facility details below"),
                     ctrl.item().id()?common.form_view_component.star_input_text_box( ctrl, "Facility Name", "_name", "Select Facility Name",'',1):common.form_view_component.star_input_select_div("select_div_1", ctrl, "exampleInputEmail1", "Facility Name", "new_id", infra_app.static_data.facility_list, "id", "name", 1),

                      common.form_view_component.star_input_text_area(ctrl, "exampleInputEmail1", "Facility Details", "details", {placeholder:"Enter facility detail", rows:2, name:"facility_detail"}),
                     m("div", [
                             "Available Features",
                             m("span.red-star", "*")
                      ]),

                     common.form_view_component.input_checkbox(ctrl, checklist),
                 common.form_view_component.submit_box(infra_app, ctrl, "Save Facility")
               ])
             ])
                            
}

m.mount(document.getElementById("infraSummaryComp"), {view:infra_app.summary_view})
m.mount(document.getElementById("infracomp"), {controller:infra_app.widget_controller, view:infra_app.widget_view})
