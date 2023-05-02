import json
import threading
import time
import os
import logging
from datetime import datetime
import pytz
from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
from stream.stream_trigger import websocket_price_triggered

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

# create instance of BinanceWebSocketApiManager for Binance.com Futures
binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures")

# set api key and secret for userData stream
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")
userdata_stream_id = binance_websocket_api_manager.create_stream(["arr"],
                                                                 ["!userData"],
                                                                 api_key=binance_api_key,
                                                                 api_secret=binance_api_secret)

def is_empty_message(message):
    if message is False:
        return True
    if '"result":null' in message:
        return True
    if '"result":None' in message:
        return True
    return False

def handle_price_change(symbol, timestamp, price, price_big_p, price_i):
    zurich_timezone = pytz.timezone('Europe/Zurich')
    current_time = datetime.now(zurich_timezone)

    current_time_string = current_time.strftime("%b")+" "+current_time.strftime("%d")+" "+current_time.strftime("%H")+":"+current_time.strftime("%M")+":"+current_time.strftime("%S")
    current_time_string_price_time = (datetime.fromtimestamp(round((timestamp/1000),0))).astimezone(zurich_timezone).strftime('%b %d %H:%M:%S')

    if(symbol and price and current_time_string and current_time_string_price_time):
        websocket_price_triggered({
            "apptime": current_time_string_price_time,
            "servertime":current_time_string,
            "timestamp": round(datetime.timestamp(current_time), 0),
            "symbol": symbol,
            "price": price, #// Mark price
            "price_big_p": price_big_p, #// Index price
            "price_i": price_i, #// Estimated Settle Price, only useful in the last hour before the settlement starts
            "price_diff": None,
            "is_big_diff": False
        })
    else:
        if((not symbol) and (not price) and (not current_time_string)):
            print("NO symbol or price or current_time_string - handle_price_change")
            logging.error("NO symbol or price or current_time_string - handle_price_change")
        else:
            if(not symbol):
                print("NO symbol - handle_price_change")
                logging.error("NO symbol - handle_price_change")
            if(not price):
                print("NO price - handle_price_change")
                logging.error("NO price - handle_price_change")
            if(not current_time_string):
                print("NO current_time_string - handle_price_change")
                logging.error("NO current_time_string - handle_price_change")


def process_stream_data(binance_websocket_api_manager):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_data = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()        
        is_empty = is_empty_message(oldest_data)
        if is_empty:
            time.sleep(0.01)
        else:
            oldest_data_dict = json.loads(oldest_data)
            data = oldest_data_dict['data'] #Handle price change
            handle_price_change(symbol=data['s'], timestamp=data['E'], price=data['p'], price_big_p=data['P'], price_i=data['i'])


def start_websocket_listener(start_or_stop):
    sendData = ({
        "status": False,
        "message": "Started",
        "Triggered": "start_websocket_listener"
    })
    if(start_or_stop == "START"):
        #channels = {'markPrice', }
        channels = {'markPrice@1s', }
        binance_websocket_api_manager.create_stream(channels, markets=lc_symbols) # Start a worker process to move the received stream_data from the stream_buffer to a print function
        sendData["status"] = True
        sendData["message"] = "Successfully create_stream"
        worker_thread = threading.Thread(target=process_stream_data, args=(binance_websocket_api_manager,))
        worker_thread.start()

    elif(start_or_stop == "STOP"):
        stream_list = binance_websocket_api_manager.get_active_stream_list()
        if(stream_list):
            for p_id, p_info in stream_list.items():
                if(stream_list[p_id]['stream_id']):
                    binance_websocket_api_manager.stop_stream(stream_list[p_id]['stream_id'])
                    print("Successfully stop_stream", stream_list[p_id]['stream_id'])
                    sendData["status"] = True
                    sendData["message"] = "Successfully stop_stream " + stream_list[p_id]['stream_id']
                else:
                    sendData["status"] = True
                    sendData["message"] = "No open streams"
        else:
            sendData["message"] = "No stream_list - start_websocket_listener"
            print("No stream_list - start_websocket_listener")
    else:
        print("start_or_stop is not defined - start_websocket_listener")
        sendData["message"] = "start_or_stop is not defined - start_websocket_listener"

    return sendData


#  Define symbols
symbols = ['ETHUSDT', 'BTCUSDT']
lc_symbols = []
for symbol in symbols:
    lc_symbols.append(symbol.lower()) #Initialize binance client

#start_websocket_listener()

