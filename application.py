from flask import Flask, jsonify, render_template
import json
from stream.websockets import start_websocket_listener
from stream.stream_trigger import get_env_var, is_websocket_working

application = Flask(__name__)


# Start the websocket
start_websocket_listener("START")

###API Home Page
@application.route('/')
def index():
    env_var = get_env_var()

    sendData = ({
        "env_var": env_var
    })
    return render_template("index.jinja2", message="Hello 5cel! Its up & running", data=sendData)


@application.route('/test-websocket', methods=['GET'])
def test_websocket():
    data = None
    check_websocket = is_websocket_working()
    if(check_websocket):
        data = check_websocket

    response = jsonify(data)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@application.route('/price', methods=['GET'])
def price():

    data = None

    # Opening JSON file
    btc_price = open('price_btc.json')
    eth_price = open('price_eth.json')

    # returns JSON object as a dictionary
    btc_data = None
    try:
        btc_data = json.load(btc_price)
    except json.JSONDecodeError:
        print("Empty response - price_btc.json - /price")
        pass

    eth_data = None
    try:
        eth_data = json.load(eth_price)
    except json.JSONDecodeError:
        print("Empty response - price_eth.json - /price")
        pass

    if(btc_data and eth_data):
        data = {
            "btc" : {
                        "apptime": btc_data["apptime"],
                        "timestamp": btc_data["timestamp"],
                        "symbol": btc_data["symbol"],
                        "price": btc_data["price"],
                        "price_big_p": btc_data["price_big_p"],
                        "price_i": btc_data["price_i"]
                    },
            "eth" : {
                    "apptime": eth_data["apptime"],
                    "timestamp": eth_data["timestamp"],
                    "symbol": eth_data["symbol"],
                    "price": eth_data["price"],
                    "price_big_p": eth_data["price_big_p"],
                    "price_i": eth_data["price_i"]
                }
        }
    else:
        print("NO btc_data or NO eth_data - /price")

    response = jsonify(data)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@application.route('/trigger', methods=['GET'])
def trigger():

    data = None

    # Opening JSON file
    btc_price = open('webhook_trigger_btc.json')
    eth_price = open('webhook_trigger_eth.json')

    # returns JSON object as a dictionary
    btc_data = None
    try:
        btc_data = json.load(btc_price)
    except json.JSONDecodeError:
        print("Empty response - webhook_trigger_btc.json - /trigger")
        pass

    eth_data = None
    try:
        eth_data = json.load(eth_price)
    except json.JSONDecodeError:
        print("Empty response - webhook_trigger_eth.json - /trigger")
        pass

    if(btc_data and eth_data):
        data = {
            "btc" : {
                    "trigger_webhook" : btc_data["trigger_webhook"],
                    "trigger_status" : btc_data["trigger_status"],
                    "trigger_time" : btc_data["trigger_time"],
                    "trigger_timestamp" : btc_data["trigger_timestamp"],
                    "trigger_symbol" : btc_data["trigger_symbol"],
                    "trigger_price" : btc_data["trigger_price"]
                    },
            "eth" : {

                    "trigger_webhook" : eth_data["trigger_webhook"],
                    "trigger_status" : eth_data["trigger_status"],
                    "trigger_time" : eth_data["trigger_time"],
                    "trigger_timestamp" : eth_data["trigger_timestamp"],
                    "trigger_symbol" : eth_data["trigger_symbol"],
                    "trigger_price" : eth_data["trigger_price"]
                }
        }
    else:
        print("NO btc_data or NO eth_data - /price")

    response = jsonify(data)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response




if __name__ == "__main__":
  application.run(host="0.0.0.0",port=80, debug=True)
  