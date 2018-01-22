var App = App || {};
App.Response = {
    status:false,
    set:function(attr,value){
        App.Response[attr]=value;
    },
    setStatus:function(){
        App.Response.set('status',true);        
    },
    resetStatus:function(){
        App.Response.set('status',false);        
    },      
};
App.Request = {
    status:false,
    set:function(attr,value){
        App.Request[attr]=value;
    },
    setStatus:function(){
        App.Request.set('status',true);
    },
    resetStatus:function(){
        App.Request.set('status',false);
    },
    isconfimred:function(){
        return confirm(App.Request.messages.confirm);
    },
    ismsaved:function(){
        App.Request.msave();
        //#TODO:Sync Execution
        //console.log(App.Request.status,App.Response.status);
        return App.Request.status&&App.Response.status;
    },
    msave:function(){
        $msaveEl=$("button.btn.btn-default.marginRight-12");
        console.log($msaveEl);
        if($msaveEl.length){
            //console.log('clicked');
            $msaveEl.click();
        }
        else{
            App.Request.setStatus();
            App.Response.setStatus();
        }
    },
    mdelete:function(){
        return confirm(App.Request.messages.delete);
    },
    save:function(){
        if(App.Request.ismsaved()){
            window.location=Request.saveUrl;
        }
        if(App.Request.status){
            Request.$saveEl.html('Next');
        };
    },
    submit:function(callback){            
        if(App.Request.ismsaved() && App.Request.isconfimred()){
            jQuery.ajax({
                type: 'POST',
                url: Request.submitUrl,
                data: Request.data,
                success: function(data) {
//                    console.log(data);
                    App.Request.SuccessAlert('submit');
                },
                error: function(data) {
                    App.Request.FailureAlert(data.error);
                }                
            });
        }
    },
    Alert:function(options){
        $el = $('h1').next('p');
        $alertEl = $el.next('.alert_box');
        $alertEl.length?$alertEl.remove():null;
        css_class = options.type=="success"?'alert-success':'alert-danger';
        $el.after('<div class="alert '+css_class+' flw100 alert_box"><span class="sprite"></span>'+options.message+'</div>');
        $('html, body').animate({scrollTop: 0}, "slow");
    },
    SuccessAlert:function(type){
        message=App.Request.messages[type]||type;
        options={message:message,type:'success'};
        App.Request.Alert(options);
    },
    FailureAlert:function(type){
        message=App.Request.messages[type]||type;
        options={message:message,type:'danger'};
        App.Request.Alert(options);
    },
    on_post_success:function(data){
        common.hideloading();
        if (data.status=='errors'){
            App.Request.FailureAlert(data.error)
            return "Error";
            }

        App.Request.SuccessAlert('save');
        App.Response.setStatus();
        return "Success";
    },
    on_post_error:function(){
        common.hideloading();
        App.Request.FailureAlert('error');
        App.Response.resetStatus();
        return "Error";
    },
    messages:{
        confirm: "Are you sure that you want to submit the saved information for verification to HTCampus?",
        submit: "Data submitted successfully",
        save: "Data saved successfully",
        invalid: "Still some fields are required",
        error: "Error in saving data",
        delete :"Are you sure that you want to delete this information?",
    },

};
