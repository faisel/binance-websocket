import json




#Get the trigger from hedge_stream_websocket
def websocket_price_triggered(data):
    if(data):
        if(data["symbol"]):
            if(data["price"]):
                if((data["apptime"]) and data["timestamp"]):
                    save_price_locally(data) #Save the data locally
                else:
                    print("No apptime or No timestamp websocket_price_triggered "+data["symbol"]+" "+data["price"])
            else:
                print("No price websocket_price_triggered "+data["symbol"])
        else:
            print("No symbol websocket_price_triggered")

    return True


#Save the data locally to update template
def save_price_locally(data):
    # Serializing json
    json_object = json.dumps(data, indent=4)
    
    if(data["symbol"] == "BTCUSDT"):
        # Writing to sample.json
        with open("price_btc.json", "w") as outfile:
            outfile.write(json_object)

    if(data["symbol"] == "ETHUSDT"):
        # Writing to sample.json
        with open("price_eth.json", "w") as outfile:
            outfile.write(json_object)

    return True