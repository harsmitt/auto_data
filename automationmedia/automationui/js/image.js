
(function(){

function viewModelMap (signature) {
    var map={}
    return function(key){
        if(!map[key]){
            map[key] = {};
            for(var prop in signature) map[key][prop] = m.prop(signature[prop]())
        }
        return map[key]
    }
}
var album_app = {};
album_app.tag = "image"
var in_array = function(arr, obj){
    return (arr.indexOf(obj) != -1);
}

album_app.item = function(data){
    data = data || {}
    this.id = m.prop(data.id || null)
    this._name = m.prop(data.name || "")
    this.count = m.prop(data.count || 0)
    this.images = m.prop(data.images)
}

var AlbumApi ={
    get:function(){
        return m.request({method:"GET",url:"/college-data-capture/api/album_api/", type: album_app.item})
    },
    update:function() {
        
    }
}

album_app.controller = function(){
    var ctrl=this;
    ctrl.albums = AlbumApi.get(),
    ctrl.modal = new album_app.modal.controller()
    ctrl.albumsVM =  viewModelMap({
        showsetting : m.prop(false)
    });
    ctrl.on_delete = function(){
        m.request({method:"POST", url:"", data:{'tag':'album', 'id':this.id}})
    }
}

album_app.modal = {};
album_app.validation_constraints = {'_name': ['manditory']}
album_app.modal.controller = function(options) {
    var ctrl = this;
    ctrl.item = m.prop(false);
    ctrl.deleted_pics = m.prop([]);
    ctrl.image_upload = m.prop(undefined);
    ctrl.on_file_drop = function(files){
        ctrl.image_upload(files[0])
    }
    ctrl.error = m.prop({})
    ctrl.on_save = function(){
        var validation = common.validate(album_app.validation_constraints, ctrl)
        if (validation == "validated"){
            data_send = new FormData()
            if (ctrl.item().id()){
                data_send.append('album_id', ctrl.item().id())
            }
            data_send.append('album_name', ctrl.item()._name())
            data_send.append('deleted_pics', ctrl.deleted_pics())
            data_send.append('file', (ctrl.image_upload() || ""))
            url = "/college-data-capture/api/album_api/"
            m.request({method: "POST", url:url, data:data_send, serialize: function(val){return val}}).then(function(){ctrl.item(false); ctrl.deleted_pics([]); ctrl.image_upload(undefined); ctrl.error({});})
        }
    }
}

album_app.modal.view = function(ctrl) {
    var album = ctrl.item();
    var on_input_name = function(){
        ctrl.item()._name(this.value)
    }
    var name_error_class = ctrl.error()["_name"]
    return album?
    [m(".modal-box",{style:"display:block;"},[
        m("header",[
            m("a.close.sprite",{onclick:function(){ctrl.item(false); ctrl.deleted_pics([]); ctrl.error({});}}),
            m("h2",[
                "Create/Update Album",
                m("a.showOpieToolTip.sprite.info-icon")
            ])
        ]),
        m(".modal-body",[
            m("div.form-group",name_error_class ? {class:"error"}:{},[
                m("span.error-mgs","No Special Character Allowed"),
                m("label",[
                    "Album Name",
                    m("span.red-star","*")
                ]),
                m("input.form-control",{type:"text",oninput:on_input_name,value:album._name(), onfocus: function(){delete ctrl.error()["_name"]}}),
                name_error_class ? m(".message", common.error_message(name_error_class)): null
            ]),
            common.form_view_component.image_upload(ctrl),
            m("h4","Pictures"),
            album.images() && album.images().length?
                m("ul.gallery-list.flw100",
                    album.images().map(function(image){
                        var deleted_pics = ctrl.deleted_pics();
                        var close_onclick = function(){
                            var id = this.id
                            if (in_array(deleted_pics, id)){
                                var index = deleted_pics.indexOf(id)
                                deleted_pics.splice(index, 1)
                            }
                            else{
                                deleted_pics.push(id)
                            }
                        }
                        var get_style = function(id){
                            if (in_array(deleted_pics, id)){
                                return {style: {"background-color":"red"}}
                            }
                            else{
                                return {}
                            }
                        }
                        return m("li",get_style(image.id),[
                            m("span",[
                                m("sup.sprite.close-white-icon", {onclick: close_onclick.bind({'id':image.id})}),
                            ]),
                            m("a",[
                                m("img",{width:"70px",height:"70px",src:image.image})
                            ])
                        ])
                    })
                ):""
        ]),
        m("div.clearfix"),
        m("footer.flw100",[
            m("button.btn.btn-default.pull-left", {onclick: ctrl.on_save},"Save"),
            m("a.pull-right.marginTop-15",{onclick:function(){ctrl.item(false); ctrl.deleted_pics([]); ctrl.error({});}},"Cancel")
        ])
    ]),m(".modal-overlay",{style:"opacity:0.7;"})]:"";
    
}


album_app.view = function(ctrl){
    var header = m(".col-md-12", [
                    m("h2", "Picture Albums"),
                    m("p.c9", "You can create multiple albums and upload pictures here")
                ]);
    var create = m(".col-md-4", [
                    m("a.create-album.text-center.table-cell",{onclick:function(){ctrl.modal.item(new album_app.item())}},[ 
                        m("span.sprite.plus-icon-big"),
                        m("p", "Create Album")
                    ])
                ]);
    var list = ctrl.albums().map(function(album){
        var vm = ctrl.albumsVM(album.id())
        return m(".col-md-4", 
                m(".create-album.album-box", [
                    m("a", {onclick:function(){ common.set_item(album_app)(album, ctrl.modal.item)}}, [
                        m("img")
                    ])
                ]),
                m(".pull-left", [
                    m("h3", album._name()),
                    m("p.c9.fs-12.paddingBottom-0", album.count()+" Pictures")
                ]),
                m(".setting-wrap.pull-right", [
                    m("a.setting-content#setting",{onclick:function(){ vm.showsetting(!vm.showsetting())}}, [
                        m("span.sprite.setting-icon")
                    ]),
                    vm.showsetting()?
                    m("ul.setting-list",  [
                        m("li", [
                            m("a[href=#]",{onclick: function(){ ctrl.modal.item(album)}}, "Edit Album")
                        ]),
                        m("li", [
                            m("a[href=#]",{onclick: ctrl.on_delete.bind({'id':album.id()})}, "Delete")
                        ])
                    ]):""
                ])
            )
    });
    return m(".white-box.flw100",[header,create,album_app.modal.view(ctrl.modal)].concat(list));
}


m.module(document.getElementById('imagecomp'), album_app)
})();
