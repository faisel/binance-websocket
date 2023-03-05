


window.addEventListener('load', function () {
    // Your document is loaded.
    var fetchInterval = 1000; // 1 seconds.

    // Invoke the request every 1 seconds.
    setInterval(fetchprice, fetchInterval);
});
  
  
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
    const price_btc_time = document.getElementById('price-btc-time');

    const price_eth_danger_alert = document.getElementById('eth-danger-alert');
    const price_eth = document.getElementById('price-eth');
    const price_eth_time = document.getElementById('price-eth-time');

    price_btc.innerHTML=parseFloat(data["btc"]["price"]).toFixed(3);
    price_eth.innerHTML=parseFloat(data["eth"]["price"]).toFixed(3);

    price_btc_time.innerHTML=data["btc"]["apptime"];
    price_eth_time.innerHTML=data["eth"]["apptime"];

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


$(document).ready(function () {
    fetchprice();
});