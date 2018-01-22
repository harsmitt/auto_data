video_app = {}
video_app.tag = "video"
video_app.static_data = {}
video_app.validation_constraints = {"title":["manditory"], "link":["manditory", "url"]}

video_app.item= function(data){
    data = data || {}
    this.id = m.prop(data.id || null)
    this.title = m.prop(data.video_title|| "");
    this.link = m.prop(data.video_url || "");
    this.album_id = m.prop(data.album)
    this.moderation_status = m.prop(data.moderation_status || "")
    this.deleted =m.prop(data.deleted || "")
    this.tag=m.prop('collegealbumvideo')
}

video_app.process_api_data = function(data){
    video_app.static_data.albums = data.albums
    var ret = data.videos.map(function(item){
        return new video_app.item(item)
    })
    return ret
}

video_app.fetch_items = function(){
    var item_list =  m.request({method:"GET", url:"/college-data-capture/api/video_api"}).then(video_app.process_api_data);
    return item_list
}

video_app.save = function(data){
    data_send = data.id() ? 
                 {'id':data.id(), 'video_title': data.title(), 'video_url': data.link(), 'album': data.album_id()}
                :{'video_title': data.title(), 'video_url': data.link(), 'album': data.album_id()}
    url = '/college-data-capture/gallery/'
    return common.save(url, data_send)
}

video_app.delete_handler = function(item){
    m.request({method: "POST", url:"", data:{tag:'video', id:item.id()}})
}

video_app.widget_controller  = common.widget_controller(video_app)
video_app.widget_view = common.widget_view(video_app)

video_app.list_editor_controller = common.list_editor_controller(video_app)
video_app.list_editor_view = common.list_editor_view(video_app, "Videos", "You can add, delete or edit the videos", "title")

video_app.form_controller = common.form_controller({"album":"album_id"})
video_app.form_view = function(ctrl){
    return m(".video-form", [
            m(".white-box.flw100.marginBottom-0",[
                common.form_view_component.form_header("Video Gallery", "Please fill in the youtube link of the Video"),
                m("ul.form-list", [
                    m("li", [
                        common.form_view_component.input_text_box(ctrl, "Video Title", "title")
                    ]),
                    m("li", [
                        common.form_view_component.input_text_box(ctrl, "Video Link", "link")
                    ]),
                    m("li", [
                        common.form_view_component.star_input_select_div("album", ctrl,"exampleInputEmail1","Album", "album_id", video_app.static_data.albums, "id", "name" )
                    ])

                ])
            ]),

            common.form_view_component.submit_box(video_app, ctrl, "Save Video", "Save and Add Video")

     ])
}

m.mount(document.getElementById("videocomp"), {controller:video_app.widget_controller, view: video_app.widget_view})
