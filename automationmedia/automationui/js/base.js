$(document).ready(function(){
// Tabs JS Starts Here
	$('.tabwrap .tab-content').hide();
	$('.tab-content:first','.tabwrap').show();
	$('li:first','.tabwrap ul.tabs').addClass('tab-active');
	$('.tabwrap ul li a').click(function(){
		$('.tabwrap ul li').removeClass('tab-active');
			$(this).parent().addClass('tab-active');
		var currentTab = $(this).attr('href');
		$('.tabwrap .tab-content').hide();
		$(currentTab).show();
		return false;
	});// Tabs JS Ends Here
		
	//select option changes function
	$("body").on("change","select",function () {
		var str = "";
		str = $(this).find(":selected").text();
		$(this).next(".out").text(str);
	}).trigger('change');//select option changes function
	
	// tooltip functio starst here
	$(".showOpieToolTip").OpieTooltip({
		position: "tc:bc", //TooltipPosition : arrowPosition,
		event : "mouseover", 
		eventout : "mouseout",
		fade : "10",
		fadeout : "200"
	});	// tooltip functio starst here
	
});// Tabs JS Ends Here


	// range Slider JS Satrts here
	$("[data-slider]")
    .each(function () {
      var input = $(this);
      $("<span>")
        .addClass("output")
        .insertAfter($(this));
    })
    .bind("slider:ready slider:changed", function (event, data) {
      $(this)
        .nextAll(".output:first")
          .html(data.value.toFixed(3));
    });// range Slider JS ends here

	
	//Sortable Function starts here
	$(function() {
		$('.sortable').sortable();
		$('.handles').sortable({
			handle: 'span'
		});
		$('.connected').sortable({
			connectWith: '.connected'
		});
		$('.exclude').sortable({
			items: ':not(.disabled)'
		});
	});//Sortable Function Ends here
/*

	$(".setting-list").hide();
	$(".setting-content").click(function(e){
    	$(this).toggleClass("set-active");
		$(this).next("ul").toggle();
		e.stopPropagation();
		//$(".setting-list").toggle();
	});
	
	$(document).click(function(){
		$(".setting-list").hide();
		$(".setting-content").removeClass("set-active");
	});
		
*/
	
function setUpOnSelectMoveUp(containerID){
    var container = $('#'+containerID);
    console.log(container);
    container.on("change",function(ev){
        console.log("changed");
        $(container.find('input:checked').get().reverse()).each(function(){
            //Find the li element i.e a parent of the input element.
            //Prepend it to the container.
            var closestLI = $(this).parent().closest('li');
            container.prepend(closestLI);
        });
    });
    container.trigger("change");
}
function setUpFilter(textContainerID,filterContainerID){
    var textContainer = $('#'+textContainerID);
    var filterContainer = $('#'+filterContainerID);
    textContainer.on("keyup",function(){
        var filterText = textContainer.val().trim().toLowerCase();
        filterContainer.find('input').each(function(){
            var parentLI = $(this).parent().parent();
            var trimmedText = $(this).parent().text().trim().toLowerCase();
            if(trimmedText.indexOf(filterText)>-1){
                parentLI.show();
            }
            else{
                parentLI.hide();
            }
        });
    });
}
