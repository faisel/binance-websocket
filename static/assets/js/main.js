


window.addEventListener('load', function () {
    // Your document is loaded.
    var fetchInterval = 1000; // 1 seconds.
    // Invoke the request every 1 seconds.
    setInterval(fetchprice, fetchInterval);

    var fetchTriggerInterval2Sec = 2000; // 2 seconds.
    setInterval(fetchTriggerData, fetchTriggerInterval2Sec);

    var fetchInterval5min = 60000; // 5 Minutes.
    setInterval(testwebsocket, fetchInterval5min);

});


  
function testwebsocket() {
    const url = '/test-websocket';
    fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
        if(data) {
            updateSocketValues(data)
            console.log("test-websocket_data", data);
        }
    })
    .catch(function(error) {
        // $("#btc-danger-alert").show();
        // $("#eth-danger-alert").show();
        console.log("ERROR test-websocket", error);
    });
}

function updateSocketValues(data) {

    const btc_test_div = document.getElementById('btc-live-price-test-success-time');
    const eth_test_div = document.getElementById('eth-live-price-test-success-time');

    if(data["is_btc_data_ok"]) {
        $('#btc-live-price-test-success').removeClass('price-error');
        btc_test_div.innerHTML=data["test_time"]+" ✅";
    } else {
        $('#btc-live-price-test-success').addClass("price-error");
        btc_test_div.innerHTML=data["btc_data"]["apptime"]+" ⛔️⛔️";
    }
    
    if(data["is_eth_data_ok"]) {
        $('#eth-live-price-test-success').removeClass("price-error");
        eth_test_div.innerHTML=data["test_time"]+" ✅";
    } else {
        $('#eth-live-price-test-success').addClass("price-error");
        eth_test_div.innerHTML=data["eth_data"]["apptime"]+" ⛔️⛔️";
    }
    
}

//Fetch Price
function fetchprice() {
    const url = '/price';
    fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
        if(data) {
            updateValues(data)
            console.log("data", data);
            
        }
    })
    .catch(function(error) {
        $("#btc-danger-alert").show();
        $("#eth-danger-alert").show();
        console.log(error);
    });
}



function updateValues(data) {

    // FETCHING DATA FROM JSON FILE
    const price_btc_danger_alert = document.getElementById('btc-danger-alert');
    const price_btc = document.getElementById('price-btc');
    const price_btc_big_p = document.getElementById('price-btc-big-p');
    const price_btc_i = document.getElementById('price-btc-i');
    const price_btc_time = document.getElementById('price-btc-time');
    const price_btc_price_diff = document.getElementById('btc-live-price-diff');


    const price_eth_danger_alert = document.getElementById('eth-danger-alert');
    const price_eth = document.getElementById('price-eth');
    const price_ethbig_p = document.getElementById('price-eth-big-p');
    const price_eth_i = document.getElementById('price-eth-i');
    const price_eth_time = document.getElementById('price-eth-time');
    const price_eth_price_diff = document.getElementById('eth-live-price-diff');

    price_btc.innerHTML=parseFloat(data["btc"]["price"]).toFixed(3);
    price_btc_big_p.innerHTML=parseFloat(data["btc"]["price_big_p"]).toFixed(3);
    price_btc_i.innerHTML=parseFloat(data["btc"]["price_i"]).toFixed(3);

    price_eth.innerHTML=parseFloat(data["eth"]["price"]).toFixed(3);
    price_ethbig_p.innerHTML=parseFloat(data["eth"]["price_big_p"]).toFixed(3);
    price_eth_i.innerHTML=parseFloat(data["eth"]["price_i"]).toFixed(3);
    

    price_btc_time.innerHTML=data["btc"]["apptime"];
    price_eth_time.innerHTML=data["eth"]["apptime"];

    var btc_big_diff = "Yes Huge Diff, BTC Volatile Market"
    var btc_color_class = "color-yellow"
    if(!data["btc"]["is_big_diff"]) {
        btc_big_diff = "No Huge Diff"
        btc_color_class = ""
    }
    $(price_btc_price_diff).html('<h4 class='+btc_color_class+'>'+btc_big_diff+'</h4> <h4 class='+btc_color_class+'>'+data["btc"]["price_diff"]+'</h4>')


    var eth_big_diff = "Yes Huge Diff, ETH Volatile Market"
    var eth_color_class = "color-yellow"
    if(!data["eth"]["is_big_diff"]) {
        eth_big_diff = "No Huge Diff"
        eth_color_class = ""
    }
    $(price_eth_price_diff).html('<h4 class='+eth_color_class+'>'+eth_big_diff+'</h4> <h4 class='+eth_color_class+'>'+data["eth"]["price_diff"]+'</h4>')


    var current_time = parseInt(parseFloat(Date.now()/1000).toFixed(0));
    if(current_time && data["btc"]["timestamp"]) {
        //Reduce 2 minutes 
        var current_time_reduced_2_min = current_time - 120

        if(data["btc"]["timestamp"] < current_time_reduced_2_min) {
            $(price_btc_danger_alert).show();
            console.log("Danger!!!! App crushed, BTC price NOT LIVE, Urgent!!!! restart app aws elastic beanstalk");
            console.log("current_time", current_time);
            console.log("btc", data["btc"]["timestamp"]);
        } else {
            $(price_btc_danger_alert).hide();
        }

        if(data["eth"]["timestamp"] < current_time_reduced_2_min) {
            $(price_eth_danger_alert).show();
            console.log("Danger!!!! App crushed, ETH price NOT LIVE, Urgent!!!! restart app aws elastic beanstalk");
            console.log("current_time", current_time);
            console.log("eth", data["eth"]["timestamp"]);
        } else {
            $(price_eth_danger_alert).hide();
        }

    }

}



//Fetch TriggerData
function fetchTriggerData() {
    const url = '/trigger';
    fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
        if(data) {
            updateTriggerValues(data);
            console.log("Trigger", data);
            
        }
    })
    .catch(function(error) {
        // $("#btc-danger-alert").show();
        // $("#eth-danger-alert").show();
        console.log(error);
    });
}

function updateTriggerValues(trigger_data) {
    const price_btc = document.getElementById('webhook-btc-trigger');
    const price_eth = document.getElementById('webhook-eth-trigger');

    var statusColorBtc = "color-red"
    if(trigger_data["btc"]["trigger_status"] == "success") {
        statusColorBtc = "color-green"
    }
    $(price_btc).html('<h5 class='+statusColorBtc+'>'+trigger_data["btc"]["trigger_status"]+'</h5> <h5>'+trigger_data["btc"]["trigger_time"]+'</h5> <h5>'+trigger_data["btc"]["trigger_symbol"]+'</h5> <h5>'+trigger_data["btc"]["trigger_price"]+'</h5> <h5>'+trigger_data["btc"]["trigger_webhook"]+'</h5>');

    var statusColorEth = "color-red"
    if(trigger_data["eth"]["trigger_status"] == "success") {
        statusColorEth = "color-green"
    }
    $(price_eth).html('<h5 class='+statusColorEth+'>'+trigger_data["eth"]["trigger_status"]+'</h5> <h5>'+trigger_data["eth"]["trigger_time"]+'</h5> <h5>'+trigger_data["eth"]["trigger_symbol"]+'</h5> <h5>'+trigger_data["eth"]["trigger_price"]+'</h5> <h5>'+trigger_data["eth"]["trigger_webhook"]+'</h5>');
}





$(document).ready(function () {
    fetchprice();
    testwebsocket();
    fetchTriggerData()
});