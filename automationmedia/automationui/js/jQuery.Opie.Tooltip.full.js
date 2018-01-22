/**
 * Some usefule functions
 */
var Utils = new function() {
/**
	 * DefaultValue for functions like php function($value = "2") in js you use like this
	 * @param {Mixed} value
	 * @param {Object} _default
	 * @return {Mixed} 
	 */
	this.defaultValue = function(value, _default) {
		_default = (!Is.defined(_default)) ? false : _default;
		if (!Is.defined(value)) 
		{
			return _default;
		}
		return value;
	}
/**
	 * Function to round numbers
	 * @param integer num -
	 * @param integer dec - how many decimals after comma
	 */
	this.roundNumber = function(number, dec) {
		var result = Math.round(number * Math.pow(10, dec)) / Math.pow(10, dec);
		return result;
	}
};
/**
 * Useful jquery extension
 * @author gen Taliaru
 */
jQuery.fn.doCheck = function(check) {
	this.each(function() {
		var $th = jQuery(this);
		if (typeof jQuery.fn.prop == "function") 
		{
			if (check) 
			{
				$th.prop("checked", "checked")
			}
			else 
			{
				$th.removeProp("checked")
			}
		}
		if (check) 
		{
			$th.attr("checked", "checked")
		}
		else 
		{
			$th.removeAttr("checked")
		}
		$th.get(0).checked = check;
	})
	return this;
};
jQuery.fn.setAttr = function(name, value) {
	return jQuery(this).attr("data-opie-" + name, value);
};
jQuery.fn.getAttr = function(name) {
	return jQuery(this).attr("data-opie-" + name);
};
jQuery.fn.getData = function(name) {
	return jQuery(this).data("opie-" + name);
};
jQuery.fn.setData = function(name, value) {
	if (String(name) === '[object Object]' && typeof value == "undefined") 
	{
		for (var i in name) 
		{
			jQuery(this).data("opie-" + i, name[i]);
		}
		return this;
	}
	else 
	{
		return jQuery(this).data("opie-" + name, value);
	}
};
jQuery.fn.setEvent = function(name, func) {
	return jQuery(this).bind("opie-" + name, func);
};
jQuery.fn.reverse = [].reverse;
/**
 * Useful class to check variable type casting
 * @author gen Taliaru
 */
var Is = new function() {
/**
	 * Is value css selector
	 * @param {Object} v
	 */
	this.cssSelector = function(v) {
		if (Is.string(v)) 
		{
			if (v == "#") 
			{
				return false;
			}
			if (v.substr(0, 1) == "#" || v.substr(0, 1) == "." || v.substr(0, 1) == ":") 
			{
				return true;
			}
		}
		return false;
	}
/**
	 * Is value has some kind of value
	 * @param {Object} v
	 */
	this.defined = function(v) {
		return typeof v !== "undefined";
	}
/**
	 * Is value typeof string
	 * @param {Object} v
	 */
	this.string = function(v) {
		return typeof v === 'string';
	}
};

/**
 * Class to handle plugin options
 * @param {Object} opts
 * @param {Object} jq
 */
var Opts = function(opts, jq) {
	this.opts = opts;
	this.jq = jq;
}
Opts.prototype = 
{
	/**
	 * Just get options
	 * @param {String} name
	 */
	get: function(name) {
		return this.parse(this.opts[name]);
	},
	/**
	 * Just get options
	 * @param {String} name
	 */
	set: function(name, value) {
		this.opts[name] = value;
		return this;
	},
	
	/**
	 * Just get options
	 * @param {String} name
	 */
	string: function(name) {
		return this.parse(this.opts[name], true);
	},
	
	/**
	 * Get option value as number
	 * @param {String} name
	 */
	number: function(name) {
		return parseFloat(this.get(name));
	},
	
	/**
	 * Get option value as number
	 * @param {String} name
	 */
	bool: function(name) {
		var v = this.get(name);
		if (v == "1" || v === true) 
		{
			return true;
		}
		return false;
	},
	
	/**
	 * Get option selector jquery object
	 * @param {String} name
	 */
	selector: function(name) {
		return this.jq(this.get(name));
	},
	
	
	/**
	 * Get option selector jquery object
	 * @param {String} name
	 */
	func: function(name) {
		return this.parse(this.opts[name], true, true);
	},
	
	/**
	 * Private function parse option value
	 * @param {Object} val
	 * @param {Boool} voidCssSelector
	 */
	parse: function(val, voidCssSelector, voidFunctionCall) {
		if (typeof val == "undefined") 
		{
			return "";
		}
		var v = val.valueOf();
		if (typeof v == "function") 
		{
			if (voidFunctionCall == true) 
			{
				return v;
			}
			return v();
		}
		else if (Is.cssSelector(v) && voidCssSelector !== true) 
		{
			var $th = this.jq(v);
			if ($th.size() <= 0) 
			{
				debug("Opts.parse " + v + " not found");
				return false;
			}
			var isCheckbox = ($th.get(0).tagName == "INPUT" && $th.attr("type").toString().toLowerCase() == "checkbox");
			if (isCheckbox) 
			{
				return $th.is(":checked");
			}
			return $th.val();
		}
		else 
		{
			return v;
		}
	}
};


(function($) {
	"use strict";
	var _OpieToolTipCounter = 0;
	$.fn.OpieTooltip = function(options, args) {
		var defaults = 
		{
			position: "bc:tc",
			event: "mouseover",
			eventout: "mouseout",
			fade: 50,
			fadeout: 200
		};
		if (options === "defaults") 
		{
			return defaults;
		}
		var Opt = new Opts($.extend(defaults, options), $);
		
		var PG;
		this.each(function() {
			PG = new $.OpieTooltip(Opt, $(this), arguments);
			if (options === "initCSS3") 
			{
				IS.initCSS3.apply(PG, args);
			}
			else 
			{
				PG.init();
			}
		});
		
		return this;
	}
	
	$.OpieTooltip = function(Opt, $th, allArgs) {
		var me = this;
		
		/**
		 * Initialize tooltip
		 */
		this.init = function() {
			var eventOpt = me.getOpt($th, "event");
			var eventIn = (eventOpt) ? eventOpt : "mouseover";
			
			$th.on(eventIn, function(e) {
				var $target = $(this);
				var $tooltip = me.draw($target);
				if (e.type == "click") 
				{
					$tooltip.find(".o-tooltip-close").show();
				}
				else 
				{
					$tooltip.find(".o-tooltip-close").hide();
				}
				if (!$target.getData("title") && !$target.attr("title") && !me.getOpt($target, "template") && !$target.attr("alt") && $target.attr('href') == '#') 
				{
					return;
				}
				var fadeOpt = me.getOpt($target, "fade");
				$tooltip.stop().fadeTo(fadeOpt, 1);
				if (!$target.getData("title")) 
				{
					$target.setData('title', $target.attr("title")).attr("title", "");
					$target.setData('alt', $target.attr("alt")).attr("alt", "");
				}
				
				me.setContent($target, $tooltip);
				
				
				var aSP = me.getOpt($target, "position").split(":");
				var tooltipPos = aSP[0];
				var arrowPos = aSP[1];
				me.updatePosition($tooltip, $target, tooltipPos, arrowPos);
				
			});
			
			if (eventIn == "click") 
			{
				var eventOut = "void";
			}
			else 
			{
				var eventOpt = me.getOpt($th, "eventout");
				var eventOut = (eventOpt) ? eventOpt : "mouseout";
			}
			
			if (eventOut != "void") 
			{
				$th.on(eventOut, function(e) {
					var $target = $(this);
					if (e.type != "click") 
					{
						var $tooltip = me.draw($target);
						$tooltip.find(".o-tooltip-close").hide();
					}
					me.close($target);
				});
			}
		}
		
		this.close = function($target) {
			var $tooltip = me.draw($target);
			var fadeOutOpt = me.getOpt($target, "fadeout");
			var fadeOut = (fadeOutOpt) ? parseFloat(fadeOutOpt) : null;
			$tooltip.stop().fadeTo(fadeOut, 0, function() {
				$tooltip.remove()
			});
		}
		
		/**
		 * Draw tooltip html
		 * @param {Object} $target - target jquery element
		 */
		this.draw = function($target) {
			var ID = $target.getData("opie-tool-tip-id");
			if (ID) 
			{
				var $tooltip = $("#" + ID);
				if ($tooltip.size() > 0) 
				{
					return $tooltip;
				}
			}
			if ($target.getData("tooltip-id")) 
			{
				var tooltipID = $target.getData("tooltip-id");
			}
			else 
			{
				var tooltipID = "opieTooltip-" + _OpieToolTipCounter;
				_OpieToolTipCounter++;
			}
			var $tooltip = $('<div class="o-tooltip" id="' + tooltipID + '"><div class="o-tooltip-arrow"></div><div class="o-tooltip-close"><span>x</span></div><div class="o-tooltip-inner"></div></div>');
			$tooltip.find(".o-tooltip-close").on("click", function() {
				me.close($(this).parents(".o-tooltip").getData("target"));
			});
			$tooltip.setData("target", $target);
			$target.setData("opie-tool-tip-id", tooltipID);
			$tooltip.setEvent("updatePosition", function(e, $target, tooltipPos, arrowPos, voidSecondRecCall) {
				me.updatePosition($(this), $target, tooltipPos, arrowPos, voidSecondRecCall);
			})
			$('body').append($tooltip);
			
			$tooltip.hide()
			return $tooltip;
		}
		
		this.getOpt = function($target, optName, getAsString) {
			if (Is.defined($target.getAttr(optName))) 
			{
				return $target.getAttr(optName);
			}
			return (getAsString) ? Opt.string(optName) : Opt.get(optName);
		}
		
		this.setContent = function($target, $tooltip) {
			var $inner = $tooltip.find(".o-tooltip-inner");
			var template = me.getOpt($target, "template", true);
			if (template) 
			{
				if (!$tooltip.getData("template")) 
				{
					if (!Is.cssSelector(template)) 
					{
						template = "<div>" + template + "</div>";
					}
					var $template = $(template);
					$tooltip.setData("template", $template.html());
				}
				var appendHTML = $tooltip.getData("template");
				if (!Is.defined($tooltip.getData("template"))) 
				{
					return false;
				}
				$.each($tooltip.getData("template").match(/\{.*?\}/img), function(i, match) {
					var attr = match.replace("{", "").replace("}", "");
					var c = $target.attr(attr);
					if (attr == "title") 
					{
						c = $target.getData("title");
					}
					appendHTML = appendHTML.replace(match, c);
				})
				$tooltip.find(".o-tooltip-inner").html(appendHTML);
			}
			else 
			{
				$tooltip.find(".o-tooltip-inner").html($target.getData("title"));
			}
			var eventIn = (eventOpt) ? eventOpt : "mouseover";
			var $close = $tooltip.find(".o-tooltip-close");
			if (eventIn == "click") 
			{
				var eventOut = "void";
				$close.show();
			}
			else 
			{
				var eventOpt = me.getOpt($th, "eventout");
				var eventOut = (eventOpt) ? eventOpt : "mouseout";
				$close.hide();
			}
		}
		
		this.updatePosition = function($tooltip, $target, tooltipPos, arrowPos, voidSecondRecCall) {
			if (!$target) 
			{
				$target = $tooltip.getData("target");
				var aSP = me.getOpt($target, "position").split(":");
				var tooltipPos = aSP[0];
				var arrowPos = aSP[1];
			}
			var targetTop = $target.offset().top;
			var targetLeft = $target.offset().left;
			var targetHeight = $target.outerHeight();
			var targetWidth = $target.outerWidth();
			
			var tooltipTop = $tooltip.offset().top;
			var tooltipLeft = $tooltip.offset().left;
			var tooltipHeight = $tooltip.outerHeight();
			var tooltipWidth = $tooltip.outerWidth();
			
			var Css = 
			{
				top: 0,
				left: 0
			}
			$tooltip.css(Css).width(tooltipWidth).height(tooltipHeight);
			$tooltip.attr("class", "o-tooltip " + arrowPos);
			if (tooltipPos.charAt(0) == "t") 
			{
				Css.top = targetTop;
			}
			else if (tooltipPos.charAt(0) == "m") 
			{
				Css.top = targetTop + (targetHeight / 2);
			}
			else if (tooltipPos.charAt(0) == "b") 
			{
				Css.top = targetTop + targetHeight;
			}
			
			if (tooltipPos.charAt(1) == "l") 
			{
				Css.left = targetLeft;
			}
			else if (tooltipPos.charAt(1) == "c") 
			{
				Css.left = targetLeft + (targetWidth / 2);
			}
			else if (tooltipPos.charAt(1) == "r") 
			{
				Css.left = targetLeft + targetWidth;
			}
			
			if (arrowPos.charAt(0) == "m") 
			{
				Css.top -= (tooltipHeight / 2);
			}
			else if (arrowPos.charAt(0) == "b") 
			{
				Css.top -= tooltipHeight;
			}
			
			if (arrowPos.charAt(1) == "r") 
			{
				Css.left -= tooltipWidth;
			}
			else if (arrowPos.charAt(1) == "c") 
			{
				Css.left -= (tooltipWidth / 2);
			}
			$tooltip.css(Css);
			if (voidSecondRecCall !== true) 
			{
				var tooltipTop = $tooltip.offset().top;
				var tooltipLeft = $tooltip.offset().left;
				
				var scrollTop = $(window).scrollTop();
				var scrollLeft = $(window).scrollLeft();
				var tooltipBottom = tooltipTop + $tooltip.outerHeight() - scrollTop;
				var tooltipRight = tooltipLeft + $tooltip.outerWidth() - scrollLeft;
				var screenBottom = $(window).height();
				var screenRight = $(window).width();
				var oppositePositions = 
				{
					"b": "t",
					"t": "b",
					"l": "r",
					"r": "l"
				}
				if (tooltipTop < scrollTop) 
				{
					var cantbe = "b"
				}
				else if (tooltipBottom > screenBottom) 
				{
					var cantbe = "t"
				}
				var newToolTipPos = tooltipPos;
				var newArrowPos = arrowPos;
				if (tooltipTop < scrollTop || tooltipBottom > screenBottom) 
				{
					if (tooltipPos.charAt(0) != cantbe) 
					{
						oppositePositions.m = "b";
						if (tooltipBottom > screenBottom) 
						{
							oppositePositions.m = "t";
						}
						newToolTipPos = oppositePositions[tooltipPos.charAt(0)] + tooltipPos.charAt(1);
					}
					
					if (arrowPos != "ml" && arrowPos != "mr") 
					{
						newArrowPos = oppositePositions[arrowPos.charAt(0)] + arrowPos.charAt(1);
					}
				}
				tooltipPos = newToolTipPos;
				arrowPos = newArrowPos;
				
				var newToolTipPos = tooltipPos;
				var newArrowPos = arrowPos;
				if (tooltipLeft < 0) 
				{
					if (arrowPos.charAt(0) == "m") 
					{
						newToolTipPos = "mr"
						newArrowPos = "ml"
					}
					else 
					{
						newArrowPos = arrowPos.charAt(0) + "l"
					}
				}
				if (tooltipRight > screenRight) 
				{
					newArrowPos = arrowPos.charAt(0) + "r"
				}
				tooltipPos = newToolTipPos;
				arrowPos = newArrowPos;
				if (tooltipTop < scrollTop || tooltipBottom > screenBottom || tooltipLeft < 0 || tooltipRight > screenRight) 
				{
					me.updatePosition($tooltip, $target, tooltipPos, arrowPos, true);
				}
			}
		}
		
	}
})(jQuery);