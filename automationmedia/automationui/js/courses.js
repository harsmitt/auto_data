course_app = {}
course_app.tag = "course"
course_app.static_data = {}
course_app.static_data.duration_month = [0,1,2,3,4,5,6,7,8,9,10,11]
course_app.static_data.duration_year = [0,1,2,3,4,5,6,7]
course_app.static_data.qualification_levels = []
course_app.static_data.flagship_options = [{id:0, name: 'NO'},{id:1, name:'Yes'}]
course_app.static_data.delivery_options = [{id:0, name:'N.A.'}, {id:1, name:'Full Time - Class Room'}, {id:2, name: 'Part Time - Class Room'}, {id:3, name:'Distance/Correspondence'}, {id:4, name: 'Online/E-Learning'}, {id:5, name: 'Executive'}]
course_app.static_data.degree_options = [{id:0, name:'BBA'}, {id:1, name:'MBA'}, {id:2, name:'B.Sc.'}, {id:3, name:'B.Com'}, {id:4, name:'B.A'}, {id:10, name:'Diploma in Animation & Multimedia'}, {id:11, name:'Bachelor in Multimedia'}, {id:12, name:'Master in Multimedia'}, {id:13, name:'CMM (Certificate in Mass Media)'}, {id:14, name:'DMC(Diploma in Mass Communication)'}, {id:15, name:'BMM (Bachelor of Mass Media)'}, {id:16, name:'MMC (Master of Mass Communication)'}, {id:17, name:'ANM'}, {id:18, name:'BDS'}, {id:19, name:'MDS'}, {id:20, name:'MD'}, {id:21, name:'B.Com'}, {id:22, name:'M.Com'}, {id:23, name:'Diploma in Engineering'}, {id:24, name:'B.E/B.Tech'}, {id:25, name:'M.E/M.Tech'}, {id:26, name:'Ph.D/M.Phil'}, {id:27, name:'Diploma in Food Production and Catering Technology'}, {id:28, name:'B.Sc (Aviation)'}, {id:29, name:'M.Sc {id:Aviation}'}, {id:30, name:'BBA/BBM'}, {id:31, name:'MBA/PGDM'}, {id:32, name:'Ph.D/M.Phil'}, {id:33, name:'Computer Certificate Courses'}, {id:34, name:'Diploma in Information & Data Management'}, {id:35, name:'BCA'}, {id:36, name:'MCA'}, {id:37, name:'Ph.D/M.Phil'}, {id:38, name:'LLB'}, {id:39, name:'LLM'}, {id:40 , name:'Ph.D/M.Phil'}, {id:41, name:'B.Ed'}, {id:42, name:'M.Ed'}, {id:43, name:'Certificate in Creative Arts'}, {id:44, name:'Diploma in Fine Arts'}, {id:45, name:'B.A'}, {id:46, name:'M.A'}, {id:47, name:'Ph.D/M.Phil'}, {id:48, name:'B.Sc'}, {id:49, name:'M.Sc'}, {id:5, name:'Certificate in Ceramic Design'}, {id:50, name:'Ph.D/M.Phil'}, {id:51, name:'Distance MBA'}, {id:6, name:'Advance Diploma in Fashion Technology'}, {id:7, name:'B.Des'}, {id:8, name:'M.Des'}, {id:9, name:'Certificate in Web Designing'}]


course_app.static_data.accreditations = []
course_app.static_data.affiliations = []
course_app.static_data.categories = []
course_app.static_data.subcategories = []
course_app.static_data.exams = []
course_app.validation_constraints = { "flagship":["manditory"], "delivery":["manditory"],"categories":['manditory'], "subcategories":["manditory"],"duration_months":["manditory"],"accreditation_id":['manditory'],"affiliation_id":['manditory'],"categories":['manditory'],"qualification_level_id":["manditory"], "description":["manditory"], "duration_years":["manditory"], "fee_lakhs":["manditory"], "fee_thousands":["manditory"],  "_name": ["manditory"] }

course_app.item = function(course, seats, categories, subcategories, exams,cutoff){
    var originalexamcutoff=cutoff || {};
    course = course || {}
    this.id = m.prop(course.id || "")
    this.flagship = m.prop(course.flagship_course?1:0)
    this._name = m.prop(course.name || "")
    this.delivery = m.prop(common.utils.default_select(course.course_delivery))
    this.degree = m.prop(common.utils.default_select(course.degree))
    this.qualification_level_id = m.prop(course.qualification_level || "")
    this.description = m.prop(course.description || "")
    this.categories = m.prop(categories || [])
    this.subcategories = m.prop(subcategories || [])
    this.exams = m.prop(exams || [])
    this.eligibility = m.prop(course.minimum_eligibility || "")
    this.eligibility_pdf = m.prop(null)
    this.usp = m.prop(course.course_usp || "")
    this.seats = m.prop(seats || get_default_seats())
    this.prev_cutoff_pdf = m.prop(null)
    this.duration_months = m.prop(common.utils.default_select((course.course_duration_months) % 12)  )
    this.duration_years = m.prop(common.utils.default_select(Math.floor(course.course_duration_months/12)))
    this.fee_thousands = m.prop(common.utils.default_select((course.course_fees_thousands) % 100))
    this.fee_lakhs = m.prop(Math.floor(common.utils.default_select((course.course_fees_thousands)/100)))
    this.accreditation_id = m.prop(course.accreditation || "")
    this.affiliation_id = m.prop(course.affiliation || "")
    this.notification_date = m.prop(common.utils.default_select(course.admission_notification_date || ""))
    this.deadline_date = m.prop(common.utils.default_select(course.application_deadline_date || ""))
    this.first_session_date = m.prop(common.utils.default_select(course.first_session_date || ""))
    this.moderation_status = m.prop(course.moderation_status || "")
    this.deleted =m.prop(course.deleted || "")
    this.tag=m.prop('domesticcourse')
    this.examcutoff = m.prop($.extend(get_default_exam_cutoff(),originalexamcutoff))
    this.origexamcutoff = m.prop(originalexamcutoff)
}

function get_default_exam_cutoff(exams){
    exams = exams || {};
    var allexams = course_app.static_data.exams,cur;
    var ret={};
    for(var i=0;i<allexams.length;i++){
        cur = allexams[i];
        if(exams[cur.id]){
            ret[cur.id]=parseInt(exams[cur.id])
        }
        else{
            ret[cur.id]=0
        }
    }
    return ret;
}
function get_default_seats(seats){
    var seatlist=["General","OBC","SC","ST","PH","ALL"],seatmap={};
    var newseat=[],seats=seats || [];
    for(var i=0;i<seatlist.length;i++){
            var current = seatlist[i],exist=[];
            if(seats.length){
                exist=seats.filter(function(item){
                    return item.category==current;
                });
            }
            if(exist.length) newseat.push(exist[0])
            else
            newseat.push({category:seatlist[i],seats:0})
    }
    return newseat
}
course_app.process_api_data = function(data){
    course_app.static_data.qualification_levels = data.qualification_levels_key;
    var courses = data.courses_key;
    var seats = data.seats_key;
    course_app.static_data.categories = data.category_key
    course_app.static_data.subcategories = data.subcategory_key
    course_app.static_data.exams = data.exam_key
    course_app.static_data.accreditations = data.accreditation_key;
    course_app.static_data.affiliations = data.affiliation_key;
    course_app.static_data.seats = data.seats_key;
    course_app.static_data.course_cutoff = data.course_exam_cutoff;
    var month_list=[];
    for(var i=0;i<data.month_list.length;i++){
        var current = data.month_list[i];
        var key=Object.keys(current)[0];
        month_list.push({id:current[0],name:current[1]})
    }
    course_app.static_data.months = month_list;
    
//    var seatlist=["General","OBC","SC","ST","PH"],seatmap={};
//    for(var i=0;i<seats.length;i++){
//        current = seats[i];
//        seatmap[current.category] = {category:current.category,seats:current.seats}
//    }
    var newseat=[]
    var course_cutoff=course_app.static_data.course_cutoff;

    course_app.static_data.seats = newseat;
    var ret =  courses.map(function(course){
        var seats_1 = seats.filter(function(seat){
            if(seat.course_id) {
                return seat.course_id == course.id
            }
            else {return true}
        });
        var cutoff = course_cutoff[course.id];
        var curcutoff={};
        for(var i=0;i<cutoff.length;i++){
            curcutoff[cutoff[i].exam_id]=cutoff[i].cutoff
        }
        seats_1=get_default_seats(seats_1);

        return new course_app.item(course, seats_1, data.course_category_key[course.id], data.course_subcategory_key[course.id], data.course_exam_key[course.id],curcutoff)
    })

    return ret
}

course_app.fetch_items = function(){
    return m.request({method:"GET", url:"/college-data-capture/api/course_api/"}).then(course_app.process_api_data)
}

course_app.delete_handler = function(item){
    m.request({method: "POST", url:"/college-data-capture/delete/", data:{tag:'course', id:item.id()}})
}

course_app.save = function(data){
    var checked_exams = data.exams();
    var cutoffs = data.examcutoff(),origcutoff=data.origexamcutoff();
    var cutoffdata = [],cur_id;
    for(var i=0;i<checked_exams.length;i++){
        cur_id = checked_exams[i];
//        if(parseInt(cutoffs[cur_id]) !== parseInt(origcutoff[cur_id])){
            cutoffdata.push(cur_id+':'+cutoffs[cur_id])
//        }
    }
    data_send = data.id() ?
    {"id":data.id(),"flagship_course":data.flagship(),"seats":data.seats(), "exams": data.exams(), "name":data._name(), "course_delivery":data.delivery(),"degree":data.degree(), "qualification_level":data.qualification_level_id(), "description":data.description(), "category":data.categories(), "subcategory": data.subcategories(), "minimum_eligibility": data.eligibility(), "course_usp":data.usp(), "course_duration_months":( parseInt(data.duration_months())+12*parseInt(data.duration_years())), "course_fees_thousands":(parseInt(data.fee_thousands())+100*parseInt(data.fee_lakhs())), "accreditation": data.accreditation_id(), "affiliation": data.affiliation_id(), "admission_notification_date": data.notification_date(), "application_deadline_date": data.deadline_date(), "first_session_date": data.first_session_date(),"exam_cut_off":cutoffdata  }

        :{"flagship_course":data.flagship(), "seats":data.seats(), "exams": data.exams(),"name":data._name(), "course_delivery":data.delivery(),"degree":data.degree(), "qualification_level":data.qualification_level_id(), "description":data.description(), "category": data.categories(), "subcategory": data.subcategories(), "minimum_eligibility": data.eligibility(), "course_usp":data.usp(),  "course_duration_months":( parseInt(data.duration_months())+12*parseInt(data.duration_years())), "course_fees_thousands":(parseInt(data.fee_thousands())+100*parseInt(data.fee_lakhs())), "accreditation": data.accreditation_id(), "affiliation": data.affiliation_id(), "admission_notification_date": data.notification_date(), "application_deadline_date": data.deadline_date(), "first_session_date": data.first_session_date(),"exam_cut_off":cutoffdata}
    data_send.seats=JSON.stringify(data.seats());
    form_data = new FormData()
    for (key in data_send){
        form_data.append(key, data_send[key])
    }
    form_data.append("eligibility", data.eligibility_pdf())
    form_data.append("cutoff", data.prev_cutoff_pdf())
    url = "/college-data-capture/courses/"
    return m.request({method:"POST", url:url, data:form_data, serialize:function(value){return value}, extract: function (xhr, xhrOptions) {
        if (xhr.status === 500) return xhr.status;
        else return xhr.responseText;
    }}).then(common.on_post_success, common.on_post_error)
}

course_app.widget_controller = common.widget_controller(course_app)
course_app.widget_view = common.widget_view(course_app)

course_app.list_editor_controller = common.list_editor_controller(course_app)
course_app.list_editor_view = common.list_editor_view(course_app,"College Courses" ,"You can add, edit or delete all the course related information here", "_name")

course_app.form_controller = common.form_controller({"select_div_1":"flagship", "select_div_2":"delivery", "select_div_3":"qualification_level_id", "select_div_4":"duration_years", "select_div_5":"duration_months","select_div_6":"notification_date",
    "select_div_7":"deadline_date","select_div_8":"first_session_date",
    "select_div_9":"accreditation_id", "select_div_10":"affiliation_id",'select_div_11':"degree"},
    {"eligibility":5}, ["category", "subcategory", "exams","seats"] )

var form_config=function(element,is_init) {
    if(!is_init){
        common.scrollToTarget('#mainform');
    }
    
}
course_app.form_view =  function(ctrl){
    var eligibility_tab = ctrl.tab_selected()["eligibility"]
    return m(".white-box.flw100.marginBottom-0.paddingBottom-0#mainform",{config:form_config}, [
        m(".col-md-12", [
            m("h2", "Add/Edit Course Details"),
            common.form_view_component.star_input_text_box(ctrl, "Course Title", "_name", "Enter Course Title")
        ]),

        m("ul.form-list.flw100", [
            m("li", [
                common.form_view_component.star_input_select_div("select_div_1", ctrl, "exampleInputEmail1", "Flagship Course", "flagship", course_app.static_data.flagship_options,"id","name")
            ]),
            m("li", [
                common.form_view_component.star_input_select_div("select_div_2", ctrl, "exampleInputEmail1", "Course Delivery", "delivery", course_app.static_data.delivery_options, "id", "name")
            ]),

            common.form_view_component.star_search_checkboxes({
                label: "Choose category",
                search_label: "Search Category",
                search_value: ctrl.search_value["category"],
                checklist: course_app.static_data.categories,
                checked: ctrl.item().categories(),
                moderation_status: ctrl.item().moderation_status(),
                error:ctrl.error()['categories'],
                ctrl:ctrl,
                item_field:'categories',
            }),
            common.form_view_component.star_search_checkboxes({
                label: "Choose  Subcategory",
                search_label: "Search Subcategory",
                search_value: ctrl.search_value["subcategory"],
                checklist: course_app.static_data.subcategories,
                checked: ctrl.item().subcategories(),
                moderation_status: ctrl.item().moderation_status(),
                error:ctrl.error()['subcategories'],
                ctrl:ctrl,
                item_field:'subcategories',
            }),

            m("li", [
                common.form_view_component.star_input_select_div("select_div_3", ctrl, "exampleInputEmail1", "Course Level", "qualification_level_id", course_app.static_data.qualification_levels, "id", "name")
            ]),
            
              m("li", [
                common.form_view_component.input_select_div("select_div_11", ctrl, "exampleInputEmail1", "Course Degree", "degree", course_app.static_data.degree_options, "id", "name")
            ]),
            /*

             m("li", [
             m(".form-group", [
             m("label", {for:"exampleInputEmail1"}, [
             "Course Degree",
             m("span.red-star", "*")
             ]),
             m(".selectdiv", [
             m("select.selectboxdiv", [
             m("option", "Select"),
             args.item().map(function(item){
             return m("option", item.degree())
             })
             ]),
             m(".out", "Select Level")
             ])
             ])
             ])
             */
        ]),

        m(".col-md-12", [
            common.form_view_component.star_input_text_area(ctrl, "exampleInputEmail1", "Course Description", "description", {rows:"2"},star=true)
        ]),
         m(".col-md-12", [
            common.form_view_component.star_input_text_area(ctrl, "exampleInputEmail1", "Course Eligibility", "eligibility", {rows:"2"})
        ]),
        m(".col-md-12.tabwrap", {id:"db_tabwrap"}, [


            m("#tab5.tab-content", [
                common.form_view_component.star_input_text_area(ctrl, "exampleInputEmail1", "Course USP", "usp", {rows:"2"}),
                m("ul.form-list.row", [
                    common.form_view_component.search_checkboxes({
                        label:"Exams Accepted",
                        search_label: "Search Exams",
                        search_value: ctrl.search_value["exams"],
                        checklist: course_app.static_data.exams,
                        checked: ctrl.item().exams(),
                        moderation_status: ctrl.item().moderation_status(),
                        fieldvals:ctrl.item().examcutoff()
                    }),

                    common.form_view_component.multiple_input(ctrl.item().seats(),ctrl.item().moderation_status())

                ])
            ])
        ]),
        m(".col-md-12", [
            m(".row", [
                m(".col-md-3", [
                    common.form_view_component.star_input_select_div("select_div_4",ctrl, "exampleInputEmail1", "Course Duration", "duration_years", course_app.static_data.duration_year,null,null,null,'Years')
                ]),
                m(".col-md-3", [
                    common.form_view_component.star_input_select_div("select_div_5", ctrl, "exampleInputEmail1", "", "duration_months", course_app.static_data.duration_month,null,null,null,'Months')
                ]),
                m(".col-md-3", [
                    common.form_view_component.star_input_text_box(ctrl, "Course Fees", "fee_lakhs",'in Lakhs',"Lakhs")
                ]),
                m(".col-md-3", [
                    common.form_view_component.star_input_text_box(ctrl, "", "fee_thousands",'in Thousands',"Thousands")
                ])
            ]),
            common.form_view_component.star_input_select_div("select_div_9", ctrl, "exampleInputEmail1", "Accreditation", "accreditation_id", course_app.static_data.accreditations, "id", "name"),
            common.form_view_component.star_input_select_div("select_div_10", ctrl, "exampleInputEmail1", "Affiliation", "affiliation_id", course_app.static_data.affiliations, "id", "name"),

            m("ul.form-list.row", [
                m("li", [
                    common.form_view_component.input_select_div("select_div_6", ctrl, "exampleInputEmail1", "Application Start Month", "notification_date", course_app.static_data.months, "id", "name"),
                    //common.form_view_component.input_date_box(ctrl, "Application On Start Date", "notification_date", {size:"16"})
                ]),
                m("li", [
                    common.form_view_component.input_select_div("select_div_7", ctrl, "exampleInputEmail1", "Application End Month", "deadline_date", course_app.static_data.months, "id", "name"),

                ]),
                m("li", [
                    common.form_view_component.input_select_div("select_div_8", ctrl, "exampleInputEmail1", "Session starting from", "first_session_date", course_app.static_data.months, "id", "name"),


                ])
            ]),
            m(".row", [
                m(".col-md-6")
            ])
        ]),
        common.form_view_component.submit_box(course_app, ctrl, "Save Course", "Save And Add Course")
    ])
}

m.mount(document.getElementById("coursecomp"),{controller: course_app.widget_controller, view: course_app.widget_view})
