//form validation library
var CustomValidator=(function(){
	function validateField(domObj,validattr){
		var error = false;
		var typeArr = $(domObj)[validattr[0]](validattr[1]);
		if(!typeArr) return error;
		typeArr = typeArr.split('|');
		for(var j = 0; j < typeArr.length;j++){
			var attrtype = $.trim(typeArr[j]).split('='),
				type=attrtype[0],attrarg=attrtype[1] || null;
			var val = $.trim(domObj.value);
			var fieldName=type;
			if(!type) continue;
			switch(type){
				case 'name':
					error = !isValidName(val);
					break;
				case 'email':
					error = !isValidEmailAddress(val);
					break;
				case 'password':
					error = !ValidateNotEmpty(domObj);
					break;
				case 'integer':
					error = !ValidateInteger(domObj);
					break;
				case 'cellnum':
					error = !isValidMobileNumber(val);
					break;
				case 'checkbox':
					error = (domObj.checked)? false:true;
					break;
				case 'not_empty':
				case 'notempty':
					error = !ValidateNotEmpty(domObj);
					break;
				case 'maxlen':
					error= !validatelength($(domObj).val(),attrarg,'max');
					break;
				case 'minlen':
					error= !validatelength($(domObj).val(),attrarg,'min');
					break;
				case 'maxval':
					error= !validatevalue($(domObj).val(),attrarg,'max');
					break;
				case 'minval':
					error= !validatevalue($(domObj).val(),attrarg,'min');
					break;

				case 'url':
					error = !isUrl(val);
					break;
				case 'file':
					error = !isValidFile(val,attrarg)
					break;
				case 'csv':
					error = !isCommaSeparatedValue(val,attrarg)
					break;					
				default:
					if(type[0]==='c' && attrarg){
						var name=type.substring(1),exp=attrarg;
						error=!ValidateCustomRegex(exp,name,val);
						fieldName=name;
					}
					break;
			}
			if(error){
				var error = getMsg(fieldName,attrarg);
				error = error.replace(/%fname%/, type);
				break;
			}
		}
		return error;
	}
	function isValidFile(val,attrarg){
	    if(!val) return true;
            var allowedFiles = attrarg.split(',');
            var regex = new RegExp("([a-zA-Z0-9\s_\\.\-:])+(" + allowedFiles.join('|') + ")$");
            return regex.test(val);

	}
	function validatelength(text,len,check){
		if(check=='max'){
			return text.length<=parseInt(len);
		}
		else{
			return text.length>=parseInt(len);
		}
	}


	function isValidName(name){
		var re = /^[a-zA-Z].*$/;   //only charecters in name
		if(name.match(re))
		{
			return true;
		}
		return false;
	}

	function validatevalue(val,len,check){
		if (check == 'max'){
			return val <=parseInt(len);
		}
		else{
			return val >= parseInt(len)
		}
	}
	function isValidEmailAddress(emailAddress){
		var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
		return pattern.test(emailAddress);
	}
	function ValidateCustomRegex(regex,name,value){
		var re=new RegExp(regex);
		return re.test(value);
	}

	function ValidateNotEmpty(objEle){
		var strValue = $.trim(GetElementValue(objEle));
		var dfltvalue=$.trim(objEle.defaultValue);
		var blnResult = true;
		if(strValue == ""){
			blnResult = false;
		}
		return blnResult;
	}


	function ValidateInteger(objEle){
		var strString = GetElementValue(objEle);
		var strChar;
		var strValidChars = '0123456789';
		var blnResult = true;
		// test strString consists of valid characters listed above
		for (i = 0; i < strString.length && blnResult == true; i++){
			strChar = strString.charAt(i);
			if (strValidChars.indexOf(strChar) == -1){
				blnResult = false;
			}
		}
		return blnResult;
	}


	function GetElementValue(objEle){
		var result = '';
		switch(objEle.type){
			case "text":
			case "hidden":
			case "textarea":
			case "email":
			case "password":
				result = objEle.value;
				break;

			case "select-one":
			case "select-multiple":
			case "select":
				if(objEle.selectedIndex >= 0){
					result = objEle.options[objEle.selectedIndex].value;
					if(result == -1 || result == ''){
						result = '';
					}
				}
				break;

			case "radio":
			case "checkbox":
				for (var i=0; i<objEle.form.elements.length; i++){
					if (objEle.form.elements[i].name == objEle.name){
						if (objEle.form.elements[i].checked){
							result += objEle.form.elements[i].value+",";
						}
					}
				}
				break;
			}
		return result;
	}



	function isValidMobileNumber(number){
		var re = /^[7-9]\d{9}$/;   //10 digit mobile number starting with 7,8 or 9
		if(number.match(re)){
			return true;
			}
		return false;
	}


	
	function isUrl(s) {
		if(!s.length) return true;
	  var regex = new RegExp("^(http[s]?:\\/\\/(www\\.)?|ftp:\\/\\/(www\\.)?|www\\.){1}([0-9A-Za-z-\\.@:%_\+~#=]+)+((\\.[a-zA-Z]{2,3})+)(/(.)*)?(\\?(.)*)?");
	  if (regex.test(s)){
		 return true;
	  }
		return false;
	 }

	function isCommaSeparatedValue(value){
		if(!value.length) return true;
		var regex = new RegExp('^[0-9]{2,15}(,[0-9]{2,15})*$')
	  	if (regex.test(value)){
		 return true;
	  	}
		return false;		
	}
	function isInteger(s){
		var i;
		if (s.length>10 || s.length<10)
			return false;
		for (i = 0; i < s.length; i++){
			// Check that current character is number.
			var c = s.charAt(i);
			if (((c < "0") || (c > "9"))) return false;
			}
		// All characters are numbers.
		return true;
	}


	function getMsg(type,arg){
		return (CustomValidator.MESSAGES[type])?CustomValidator.MESSAGES[type].replace('%value%',arg):'This field is manadatory';
	}
	var a=function(element,options){
		this.validating=false;
		this.$element=$(element);
		this.options=$.extend({},CustomValidator.DEFAULTS,options);
		this._init();
	}

	a.prototype={
		_init:function(){
			var that=this;
			this.options.bindSubmitEvent(this,this.$element);
			this.$element.on('focus','input,textarea,[contenteditable]',function(){
				that.clearError(this);
			}).on('change','select',function(){
				that.clearError(this);
			})
                        .on('change','input[type="file"]',function(){
                            that.clearError(this);
                            var error=validateField(this,that.options.validattr)
                            if(error){
                                that.options.oninvalidfield($(this),error);
                            }
                            if(that.options.onupload){
                                that.options.onupload($(this),error);
                            }
                        })
			
			;
			this.options.validattr=this.options.validattr.split('-');
		},

		validate:function(e){
			if(this.validating) return false;
			this.validating=true;
			var $frm=this.$element,valid=true,config=this.options,valuelist={},customError=false;
			this.clearErrors();

			var mand_fields=$frm.find('.manditory');
			mand_fields.each(function(){
				var $this=$(this),jObj=null;
				valuelist[$this.prop('name')]=$this.val();
				var error = validateField(this,config.validattr);
				if(error){
					if(config.oninvalidfield){
						config.oninvalidfield($this,error);
					}
					valid=false;
				}
				else{
					if(config.onvalidfield){
						config.onvalidfield($this);	
					}
				}
			
			});
			if(valid && config.customValidation){
				var felem=null
				customError=config.customValidation(valuelist,this.$element);	
				if(!!customError){
					valid=!customError;
					for(var i in customError){
						felem=$('.manditory[name="'+i+'"]',$frm);	
						try{
							config.oninvalidfield(felem,customError[i]);
						}catch(e){
							valid=false;
						}
					}
				}

			}
			var next=$.proxy(this.onComplete,this);

			if(valid){

				config.onvalidform(valuelist,this.$element,next);
			}	
			else{
				config.oninvalidform(valuelist,this.$element,next);
			}
			e.preventDefault();
			return false;

		},
		clearErrors:function(){
			if(this.options.onclear){
				this.options.onclear(this.$element);
			}
		},
		clearError:function(elem) {
			elem=$(elem);
			if(this.options.clearError){
				this.options.clearError(elem,this.$element);
			}
		},
		onComplete:function(submitform){
			this.validating=false;
			if(submitform){
				this.$element[0].submit();
			}
		}
	}
	return a;
})();
CustomValidator.DEFAULTS={
	/**
	//validstr
		specifies the field from ehere the validation name is to be picked
		values:
			data-valid - picks name from data-valid attr
			attr-valid - picks name from valid attr
	**/
	'validattr':'data-valid',
	'onclear':function(elem){
		elem.find('li.error').removeClass('error');
		elem.find('div.message').remove();
	},
	'clearError':function(field,form) {
		var $lielem= field.closest('li');
		$lielem.removeClass('error');
		$lielem.find('.message').remove();
	},
	'oninvalidfield':function(field,message){
		var $field=$(field), 
			$lielem = $field.closest('li');
			$lielem.addClass('error');
			$lielem.prepend($('<div class="message"><span class="error_arrow "></span>'+message+'</div>'));
		$field.focus()
	},
	'onvalidfield':function(field){
		return true;	
	},
	'onvalidform':function(valuelist,$form,submitIt){
		submitIt(true);
	},
	'oninvalidform':function(valuelist,$form,submitIt){
		submitIt(false);

	},
	'customValidation':function(){
		return false;
	},
	bindSubmitEvent:function(obj,$form){
		$form.on('submit',$.proxy(obj.validate,obj));
	}
};
CustomValidator.MESSAGES={
	'name': 'Only alphabetical characters in your name',
	'email': 'Invalid Email ID',
	'password': 'password mismatch',
	"integer": 'Only Integers are allowed',
	'cellnum': 'Enter only a 10 digit number',
	'checkbox': 'Please check the %fname%',
	'chklen': 'Please enter a valid 10 digit mobile number',
	'not_empty': 'Field is mandatory',
	'notempty': 'Fields are mandatory',
	'maxlen':'Field must not be more than %value% characters',
	'minlen':'Field must not be less than %value% characters',
	'maxval':"Value must not be more than %value% ",
	'minval':"Value must not be less than %value%",
	'file':'Please upload files having extensions: <b> %value% </b> only.',
	'url': 'Enter a Valid Url',
	'csv':'Enter 10 to 15 digit number separated by commas',
}
$.fn.customValidator=function(option){
	return this.each(function(){
		var $this=$(this);
		var data=$this.data('custom-validator');
		var options=typeof option=='object' && option
		if(!data) $this.data('custom-validator',(data=new CustomValidator(this,options)));
	});
}

