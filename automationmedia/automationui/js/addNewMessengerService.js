var addNewMessengerService = (function($){
    var messageDisplay = null;
    var addNewMessengerService = function(){
    };
    addNewMessengerService.prototype.changeMessageDisplay = function(newMessageDisplay){
        this.messageDisplay = newMessageDisplay;
    };
    addNewMessengerService.prototype.displayMessage=function(options){
        if(!this.messageDisplay){
            console.log("Message display is not defined.");
        }
        var messageName = options.message;
        var messageType = options.messageType;
        var message = this.messages[messageName];
        //We might get the message to display,rather than the key.
        if(!message){
            message = messageName;
        }
        var css_class = options.type=="success"?'alert-success':'alert-danger';
        var displayHTML = '<div class="alert '+css_class+' flw100 alert_box"><span class="sprite"></span>'+options.message+'</div>';
        this.messageDisplay.html(displayHTML);
    };
    addNewMessengerService.prototype.messages = {
        confirm: "Are you sure that you want to submit the saved information for verification to HTCampus?",
        submit: "Data submitted successfully",
        save: "Data saved successfully",
        invalid: "Still some fields are required",
        error: "Error in saving data",
        delete :"Are you sure that you want to delete this information?"
    };
    return addNewMessengerService;
})($);
