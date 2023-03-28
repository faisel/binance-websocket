import json
import threading
import time
import os
import logging
from datetime import datetime
from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
from stream.stream_trigger import websocket_price_triggered

#logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures")

def is_empty_message(message):
    if message is False:
        return True
    if '"result":null' in message:
        return True
    if '"result":None' in message:
        return True
    return False


def handle_price_change(symbol, timestamp, price):
    current_time = datetime.now()
    current_time_string = current_time.strftime("%b")+" "+current_time.strftime("%d")+" "+current_time.strftime("%H")+":"+current_time.strftime("%M")+":"+current_time.strftime("%S")

    websocket_price_triggered({
        "apptime": current_time_string,
        "timestamp": round(datetime.timestamp(current_time), 0),
        "symbol": symbol,
        "price": price
    })

    chakka = {
        "apptime": current_time_string,
        "timestamp": round(datetime.timestamp(current_time), 0),
        "symbol": symbol,
        "price": price
    }
    #print(chakka)


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
            data = oldest_data_dict['data']            #  Handle price change
            #print(data)
            handle_price_change(symbol=data['s'], timestamp=data['T'], price=data['p'])

# def start_websocket_listener():
#     binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures")
#     channels = {'markPrice', }    
#     binance_websocket_api_manager.create_stream(channels, markets=lc_symbols)    # Start a worker process to move the received stream_data from the stream_buffer to a print function

#     worker_thread = threading.Thread(target=process_stream_data, args=(binance_websocket_api_manager,))
#     worker_thread.start()


def start_websocket_listener(start_or_stop):
    sendData = ({
        "status": False,
        "message": "Started",
        "Triggered": "start_websocket_listener"
    })
    if(start_or_stop == "START"):
        channels = {'markPrice', }
        binance_websocket_api_manager.create_stream(channels, markets=lc_symbols)    # Start a worker process to move the received stream_data from the stream_buffer to a print function
        sendData["status"] = True
        sendData["message"] = "Successfully create_stream"
        print("Successfully create_stream")
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
    lc_symbols.append(symbol.lower())#  Initialize binance client



#start_websocket_listener()