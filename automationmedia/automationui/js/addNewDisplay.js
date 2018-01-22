/**
 * Add new display component,that will attach itself to display component giving it add new functionality.
 */
/**
 *Add new display functionality for CDC.
 *
 *cancel method- Delete the div.
 *save method -Send post request to formURL after serializing input elements of appended div.
 *saveAndAddMethod - Call save then call open (in addNew component) if save return's successfully.
 */
var addNewDisplay = (function($,addValidation,addNewMessengerService){
    var addNewSuccesFullCallback = undefined;
    var addNewDisplay = function(options){
        options = options || {};
        this.displayDivID = options.displayDivID;
        this.preInit = options.preInit || $.noop;
        this.postInit = options.postInit || $.noop;
        addNewSuccesFullCallback= options.addNewSuccesFullCallback;
        this.formURL=options.formURL;
        this.loaderDiv = $('#loaderdiv');
        this.getMoveTarget = options.getMoveTarget || this.getDefaultMoveTarget;
        this.insertAndSetMessageDisplay = options.insertAndSetMessageDisplay || this.insertAndSetMessageDisplay;
        this.messengerService = new addNewMessengerService();
        this.displayDiv = $('#'+ this.displayDivID);
    };
    addNewDisplay.prototype.insertAndSetMessageDisplay=function(){
        this.displayDiv.prepend('<div class="messageDisplay"></div>');
        this.messageDisplay = $(this.displayDiv.find('.messageDisplay')[0]);
    };
    addNewDisplay.prototype.init = function(newFormHTML){
        this.preInit(this.displayDiv,newFormHTML);
        this.displayDiv.html(newFormHTML);
        this.displayDiv.wrap("<form></form>");
        this.displayDiv = this.displayDiv.parent();
        this.insertAndSetMessageDisplay();
        this.messengerService.changeMessageDisplay(this.messageDisplay);
        this.validationAdapter = new addValidation(this.displayDiv);
        this.customFormValidator = this.displayDiv.data("custom-validator");
        var that=this;
        this.displayDiv.on("click",".save_add_new",function(event){
            that.save(event);
        });
        this.displayDiv.on("click",".save_and_add_add_new",function(event){
            that.saveAndAddAnother(event);
        });
        this.displayDiv.on("click",".cancel_button",function(){
            that.cancel();
        });
        if(this.isSubmitted){
            this.displayDiv.find('input, textarea, button, select').attr('disabled','disabled');
        }
        this.postInit(this.displayDiv);
    };
    addNewDisplay.prototype.cancel=function(){
        this.close(true);
    };
    addNewDisplay.prototype.save = function(event){
        this.validationAdapter.ANsetCallback($.proxy(this.saveCallback,this));
        this.customFormValidator.validate(event);
    };
    
    /**
     * dataErrorhandler handles the case when the server sends a 200 Response.
     * but adds error in status field(sent in response).
     * For handling of 500 or 404 response check errorHandler.
     */
    addNewDisplay.prototype.dataErrorHandler = function(data){
        if(data['status']!="errors"){
            return;
        }
        var error = data['error'];
        var options = {};
        options.type="error";
        options.message = error;
        this.messengerService.displayMessage(options);
        this.scrollToTarget($(this.messageDisplay.find('.alert')[0]));
    };
    addNewDisplay.prototype.scrollToTarget = function(newTarget){
        $('html,body').animate({
            scrollTop:newTarget.position().top-50
        },1000);
    };
    addNewDisplay.prototype.close=function(external){
        this.displayDiv = this.displayDiv.children('#'+this.displayDivID).first();
        this.displayDiv.unwrap();
        this.displayDiv.empty();
        if(this.overlay){
            this.overlay.remove();
        }
        if(this.messageDisplay && external){
            this.messageDisplay.remove();
        }
    };
    addNewDisplay.prototype.errorHandler = function(error){
        var options = {};
        options.type="error";
        options.message = "error";
        this.messengerService.displayMessage(options);
    };
    addNewDisplay.prototype.serializeDisplayDiv = function(){
        //var serialized = this.displayDiv.find("select, textarea, input,input:hidden").serialize();
        var fd  = new FormData(this.displayDiv[0]);
        //var serialized = this.displayDiv.serialize();
        return fd;
        //return serialized;
    };
    
    addNewDisplay.prototype.sendRequest = function(serialized,successCallback){
        $.post(this.formURL,serialized,successCallback);
    };
    addNewDisplay.prototype.dataSuccessHandler = function(data,fOptions){
        fOptions= fOptions ||{};
        if(data['status']!='success'){
            return;
        }
        var options= {};
        options.message = "Data saved successfully";
        options.type="success";
        this.close();//End everything but message.
        this.messengerService.displayMessage(options);
        setTimeout($.proxy(function(){
            //$('.alert_box').remove();
            this.messageDisplay.remove();
            addNewSuccesFullCallback(fOptions,data);
        },this),2000);
    };
    /**
     *Save callback responsibities are:-
     * To send post request to server.
     */
    addNewDisplay.prototype.saveCallback=function(fOptions){
        this.loaderDiv.show();
        var serialized = this.serializeDisplayDiv();
        $.ajax({
            url : this.formURL,
            type: "POST",
            data : serialized,
            processData: false,
            contentType: false,
            dataType: 'json',
            accepts:{
                "json":"application/json"
            },
            success:$.proxy(function(data, textStatus, jqXHR){
                this.loaderDiv.hide();
                this.dataErrorHandler(data);
                this.dataSuccessHandler(data,fOptions);
            },this),
            error: $.proxy(function(jqXHR, textStatus, errorThrown){
                //if fails
                this.loaderDiv.hide();
                this.errorHandler(errorThrown);
            },this)
        });
    };
    addNewDisplay.prototype.getDefaultMoveTarget=function(){
        return $(this.displayDiv.find('.white-box')[0]);
    };
    addNewDisplay.prototype.getMoveTarget = addNewDisplay.prototype.getDefaultMoveTarget;

    addNewDisplay.prototype.saveAndAddAnother=function(event){
        this.validationAdapter.ANsetCallback($.proxy(this.saveAndAddAnotherCallback,this));
        this.customFormValidator.validate(event);
    };
    addNewDisplay.prototype.saveAndAddAnotherCallback=function(){
        var option = {};
        option.openLater = true;
        var fOptions= {};
        fOptions.openLater=true;
        this.saveCallback(option,fOptions);
    };
    return addNewDisplay;
}($,addValidation,addNewMessengerService));
