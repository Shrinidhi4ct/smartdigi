$(".add_negative").click(function () {
   // hide feedback_container
    $(".feedback_container").css("display", "none");
    // show negative_feedback_container
    $(".negative_feedback_container").css("display", "block");
});

// Checkbox
$(".reasons").click(function(){
    // get id
    let id = $(this).data("reason");
    // check if the checkbox already checked
    if($("#"+id).is(":checked")){
        $("#"+id).prop("checked", false);
    }
    else{
        $("#"+id).prop("checked", true);
    }
});

// reload page
$(".reload").click(function(){
    location.reload();
});

// Reload page every 3 min
setInterval(function(){
    location.reload();
}
, 180000);

