from flask import Flask, render_template
import json
from stream.websockets import start_websocket_listener

application = Flask(__name__)

# Start the websocket
start_websocket_listener("START")

###API Home Page
@application.route('/')
def hello_world():
    return render_template("index.jinja2", message="Hello 5cel! Its up & running")



@application.route('/price', methods=['GET', 'POST'])
def price_page():

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

    eth_data = None
    try:
        eth_data = json.load(eth_price)
    except json.JSONDecodeError:
        print("Empty response - price_eth.json - /price")

    if(btc_data and eth_data):
        data = {
            "btc" : {
                        "apptime": btc_data["apptime"],
                        "timestamp": btc_data["timestamp"],
                        "symbol": btc_data["symbol"],
                        "price": btc_data["price"]
                    },
            "eth" : {
                    "apptime": eth_data["apptime"],
                    "timestamp": eth_data["timestamp"],
                    "symbol": eth_data["symbol"],
                    "price": eth_data["price"]
                }
        }
    else:
        print("NO btc_data or NO eth_data - /price")

    return data






if __name__ == "__main__":
  application.run(host="0.0.0.0",port=80, debug=True)
  