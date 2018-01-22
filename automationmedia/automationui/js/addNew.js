/**
 * Add new component,that will attach itself to a component giving it add new functionality.
 *The displayDiv represents the HTML that comes after user clicks on the add new button.
 *The displayDiv may contain save,save and add another and cancel button.
 */
/**
 *Add new functionality for CDC.
 *Initialize with URL of the add new form.
 *
 *open method - Send request to get new form and append it to div.
 *edit method - Send request to get new form with id and append it to div.
 *delete method- Delete the div.
 */
var addNew = (function($,addNewDisplay){
    /**
     *Constructor for addNew.
     */
    var addNew = function(formURL,addNewButtonID,displayDivID,parentDivID,displayOptions){
        this.displayOptions = displayOptions || {};
        this.displayOptions.displayDivID = displayDivID;
        this.displayOptions.formURL = formURL;
        this.displayOptions.addNewSuccesFullCallback = $.proxy(this.addNewSuccesFullCallback,this);
        this.formURL=formURL;
        this.isSubmitted = false;
        if(window.moderation_status){
            if(window.moderation_status==2){
                this.isSubmitted = true;
            }
        }
        this.addNewButton = $('#'+ addNewButtonID);
        //We reuse the ID of the add button as the class of editbutton.
        this.editButton = $('#'+parentDivID +' .edit_icon');
        this.deleteButton = $('#'+parentDivID +' .delete_icon');
        this.displayDivID = displayDivID;
        this.loaderDiv = $('#loaderdiv');
        var that = this;
        this.editButton.on("click",function(ev){
            that.edit(ev);
        });
        this.addNewButton.on("click",function(){
            that.open();
        });
        this.deleteButton.on("click",function(ev){
           that.delete(ev);
        });
    };
    /**
     *Get ID for edit and delete button in entries listing.
     */
    addNew.prototype.getID=function(elem){
        return elem.parent().closest('div').data('id');
    };
    addNew.prototype.getTag=function(elem){
        return elem.parent().closest('div').data('tag');
    };
    addNew.prototype.delete=function(ev){
        var confirmStatus = confirm("Are you sure that you want to delete this information?");
        if(!confirmStatus){
            return;
        }
        var id = this.getID($(ev.target));
        var tag = this.getTag($(ev.target));
        var postDict = {};
//        console.log("id"+id);
//        console.log("tag"+tag);
        postDict['id'] = id;
        postDict['tag'] = tag;
        $.ajax({
            type:'POST',
            url:deleteURL,
            data:JSON.stringify(postDict),
            success:$.proxy(function(data){
//                console.log('hello')
//                console.log('hello')
//                debugger;
//                $(ev.target).parent().closest('li').delete();
                 window.location.reload();
            }),
            contentType: "application/json",
            dataType: 'json'
        });
    },
    addNew.prototype.open=function(id){
        this.loaderDiv.show();
        var that=this;
        var getDict = undefined;
        if(id){
            getDict = {};
            getDict['id'] = id;
        }
        $.get(this.formURL,getDict,function(data){
            that.loaderDiv.hide();
            that.show(data);
        }).fail($.proxy(function(data){
            that.loaderDiv.hide();
        }),that);
    };
    addNew.prototype.setDisplayDiv= function(){
        if(this.displayDiv){
            return this.displayDiv;
        }
        else{
            this.displayDiv =  new addNewDisplay(this.displayOptions);
            return this.displayDiv;
        };
    };
    addNew.prototype.show = function(newFormHTML){
        this.setDisplayDiv().init(newFormHTML);
        var newTarget = this.displayDiv.getMoveTarget();
        this.displayDiv.scrollToTarget(newTarget);
        //Little bit of a hack and assumption.
        //Triggers select boxes,so that they show the select text in "div" "out".
        $(".selectboxdiv").trigger('change');
    };
    addNew.prototype.initializeDisplayDiv=function(displayDiv){
    };
    addNew.prototype.edit=function(ev){
        var id = this.getID($(ev.target));
        this.open(id);
    };
    addNew.prototype.addNewSuccesFullCallback = function(fOptions,data){
        if(fOptions.openLater){ 
            this.open();
        }
        else{
            window.location.reload();
        }
    };
    return addNew;
})($,addNewDisplay);
