// Dyanmic URL change for confirmation
$("#confirmation").click(function(){
    // Form serialize
    let form_data = $("#feedback_form").serialize();
    // Ajax call
    $.ajax({
        url: "ticket/create",
        type: "POST",
        data: form_data,
        success: function(data){
            // reload page
            location.reload();
        },
        error: function(data){
            // reload page
            location.reload();
        }
    });
});

// Dynamic UPDATE for clear ticket
$(".tickets").click(function(){
    let id = $(this).attr("id");
    $("#clear_ticket").attr("data-id", id);
});

// Checkbox
$(".complaint_reasons").click(function(){
    // get id
    let id = $(this).data("reason");
    // mark checkbox checked
    $("#"+id).prop("checked", true);

})


function SensorDataProcessing(data){

    let temp = data.temp;
    let humi = data.humidity;
    let o2 = data.o2;
    let co2 = data.co2;
    let pm = data.pm25;
    let ammonia = data.ammonia;

    $("#temp").html(temp);
    $("#humi").html(humi);
    $("#o2").html(o2);
    $("#co2").html(co2);
    $("#pm").html(pm);
    $("#ammonia").html(ammonia);

    // Temp Design Color
    if(parseFloat(temp) < 19.00) {
        RemoveAlert("temperature");
        $(".temp").addClass("text-primary");
    }else if(parseFloat(temp) > 20.00 && parseFloat(temp) <= 23.00){
        RemoveAlert("temperature");
        $(".temp").addClass("text-success");
    }else if(parseFloat(temp) > 23.00 && parseFloat(temp) <= 26.00){
        RemoveAlert("temperature");
        $(".temp").addClass("text-warning");
    }else if (parseFloat(temp) > 26.00){
        createAlert({"sensor": "temperature", "value": temp});
        $(".temp").addClass("text-danger");
    }

    // Humi desing color
    if(parseFloat(humi) <= 25.00 || humi >= 70.00) {
        createAlert({"sensor": "humidity", "value": humi});
        $(".humi").addClass("text-danger");
    }else if((parseFloat(humi) >= 25.00 && parseFloat(humi) <= 30.00)){
        RemoveAlert("humidity");
        $(".humi").addClass("text-warning");
    }else if(parseFloat(humi) >= 30.00 && parseFloat(humi) <= 60.00){
        RemoveAlert("humidity");
        $(".humi").addClass("text-success");
    }else if (parseFloat(humi) >= 60.00 && parseFloat(humi) <= 70.00){
        RemoveAlert("humidity");
        $(".humi").addClass("text-warning");
    }

    // // o2 Design Color
    // if(parseFloat(o2) <= 15.00) {
    //     createAlert({"sensor": "o2", "value": o2});
    //     $(".o2").addClass("text-danger");
    // }else if(parseFloat(o2) > 16.00 && parseFloat(o2) < 18.00){
    //     RemoveAlert("o2");
    //     $(".o2").addClass("text-warning");
    // }else if(parseFloat(o2) >= 19.00){
    //     RemoveAlert("o2");
    //     $(".o2").addClass("text-success");
    // }


    // // co2 Design Color
    // if(parseInt(co2) >= 3000) {
    //     createAlert({"sensor": "co2", "value": co2});
    //     $(".co2").addClass("text-danger");
    // }else if(parseInt(co2) >= 1000 && parseInt(co2) <= 3000){
    //     RemoveAlert("co2");
    //     $(".co2").addClass("text-warning");
    // }else if(parseInt(co2) >= 350 && parseInt(co2) <= 1000){
    //     RemoveAlert("co2");
    //     $(".co2").addClass("text-success");
    // }


    // PM2.5 Design Color
    if(parseInt(pm) >= 95) {
        createAlert({"sensor": "pm", "value": pm});
        $(".pm").addClass("text-danger");
    }else if(parseInt(pm) >= 60 && parseInt(pm) <= 90){
        $(".pm").addClass("text-warning");
        RemoveAlert("pm");
    }else if(parseInt(pm) >= 0 && parseInt(pm) <= 60){
        $(".pm").addClass("text-success");
        RemoveAlert("pm");
    }


    // ammonia Design Color
    if(parseFloat(ammonia) >= 100) {
        createAlert({"sensor": "ammonia", "value": ammonia});
        $(".ammonia").addClass("text-danger");
    }else if(parseFloat(ammonia) >= 60.00 && parseFloat(ammonia) <= 100.00){
        $(".ammonia").addClass("text-warning");
        RemoveAlert("ammonia");
    }else if(parseFloat(ammonia) <= 60.00){
        $(".ammonia").addClass("text-success");
        RemoveAlert("ammonia");
    }
        
}


function BinLevelDataProcessing(data){

    //convert bin level to integer
    bin_level = parseInt(data);
    $("#bin_level").html(bin_level);

    if(bin_level === 0){
        $("#bin_icon").attr("src", "/static/images/bin/empty.png");
    }else if(bin_level <= 25 && bin_level > 10){
        $("#bin_icon").attr("src", "/static/images/bin/25.png");
    }else if(bin_level <= 50 && bin_level >= 26){
        $("#bin_icon").attr("src", "/static/images/bin/50.png");
    }else if(bin_level <= 75 && bin_level >= 51){
        $("#bin_icon").attr("src", "/static/images/bin/75.png");
    }else if(bin_level <= 100 && bin_level >= 76){
        createAlert({"sensor": "BinLevel", "value": bin_level});
        $("#bin_icon").attr("src", "/static/images/bin/full.png");
    }else if(bin_level >= 100){
        $("#bin_icon").attr("src", "/static/images/bin/full.png");
    }
    
}



function FootfallDataProcessing(data){

    let data_array = data.split(":");
    let value = data_array[1].split(" ")[1]

    if(data_array[0] == "ENTRY"){
        $("#in").html(value)
    }else if(data_array[0] == "EXIT"){
        $("#out").html(value)
    }
}


function createAlert(value){
    $.ajax({
        type: "POST",
        url: "/manage/alert/create",
        headers: {
            'X-CSRFToken': $("#csrf_token").val()
       },
        data: {
        'data': value // from form
        },
        success: function (res) {
        console.log("success" + res);
        }
    });
}

function RemoveAlert(value){
    $.ajax({
        type: "POST",
        url: "/manage/alert/clear",
        headers: {
            'X-CSRFToken': $("#csrf_token").val()
       },
        data: {
        'data': value // from form
        },
        success: function (res) {
        console.log("success" + res);
        }
    });
}

function getSensorStatus(){
    $.ajax({
        type: "GET",
        url: "/sensor/status",
        success: function (res) {
            console.log(res);
        }
    });
}

getSensorStatus();


function getSensorData(){
    $.ajax({
        type: "GET",
        url: "/sensor/view",
        success: function (res) {
            SensorDataProcessing(res.air_quality);
            BinLevelDataProcessing(res.bin_level);

            let created_at = (res.created_at).split("T");
            let date = created_at[0];
            let time = created_at[1].split(".")[0];
            $("#last_update").html(date + "-" + time);
        }
    });
}

getSensorData();