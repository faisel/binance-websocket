from flask import Flask, jsonify, render_template
import json
import schedule
from threading import Thread
from stream.websockets import start_websocket_listener

from stream.stream_trigger import get_env_var, run_schedule, job

application = Flask(__name__)

#This is for to schedule for create new hedge
#schedule.every(5).seconds.do(job)
schedule.every(2).minutes.do(job)
t = Thread(target=run_schedule)
t.start()



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

    response = jsonify(data)
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response



if __name__ == "__main__":
  application.run(host="0.0.0.0",port=80, debug=True)
  