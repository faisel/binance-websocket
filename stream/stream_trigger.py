from flask import jsonify
import json, requests, logging
import schedule
import time
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv, find_dotenv

start_time = time.time()

def job():
    is_websocket_working()
    print("Schedule Triggered " + str(time.time() - start_time))


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


#Get the trigger from hedge_stream_websocket
def websocket_price_triggered(data):
    if(data):
        if(data["symbol"]):
            if(data["price"]):
                if((data["apptime"]) and data["timestamp"]):
                    trigger_webhook(data) #Trigger the new price to webhook
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

#Trigger the new price to webhook
def trigger_webhook(price_data):
    sendData = {
        "passphrase" : "0cce3DB04ed7-e645-4b16-8786-b260a34f5Z47433ab32",
        "data" : price_data
    }

    print(sendData)

    url = "https://killerhedge.bullparrot.com/crypto-webhook"
    if(price_data):
        r = requests.post(url, data=json.dumps(sendData), headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})

    return True



#Check if the websocket is working properly
def is_websocket_working():

    print("is_websocket_working yes every 5 minutes")

    data = None

    # Opening JSON file
    btc_price = open('price_btc.json')
    eth_price = open('price_eth.json')

    # returns JSON object as a dictionary
    btc_data = None
    try:
        btc_data = json.load(btc_price)
    except json.JSONDecodeError:
        print("Empty response - price_btc.json - is_websocket_working")
        pass

    eth_data = None
    try:
        eth_data = json.load(eth_price)
    except json.JSONDecodeError:
        print("Empty response - price_eth.json - is_websocket_working")
        pass
    
    now = datetime.now()
    current_time = datetime.timestamp(now)

    if(btc_data):
        current_time_reduced_2_min = current_time - 120
        btc_timestamp = btc_data["timestamp"]
        if(btc_timestamp < current_time_reduced_2_min):
            send_noti = Email_Alert(10, "Danger!!!! App crushed, BTC price NOT LIVE, Urgent!!!! restart app aws elastic beanstalk, Websocket is not woring, is_websocket_working")
            print("Danger!!!! App crushed, BTC price NOT LIVE, Urgent!!!! restart app aws elastic beanstalk, Websocket is not woring, is_websocket_working")
            logging.error("Danger!!!! App crushed, BTC price NOT LIVE, Urgent!!!! restart app aws elastic beanstalk, Websocket is not woring, is_websocket_working")
    else:
        print("NO btc_data - is_websocket_working")

    if(eth_data):
        current_time_reduced_2_min = current_time - 120
        eth_timestamp = eth_data["timestamp"]
        if(eth_timestamp < current_time_reduced_2_min):
            send_noti = Email_Alert(10, "Danger!!!! App crushed, ETH price NOT LIVE, Urgent!!!! restart app aws elastic beanstalk, Websocket is not woring, is_websocket_working")
            print("Danger!!!! App crushed, ETH price NOT LIVE, Urgent!!!! restart app aws elastic beanstalk, Websocket is not woring, is_websocket_working")
            logging.error("Danger!!!! App crushed, ETH price NOT LIVE, Urgent!!!! restart app aws elastic beanstalk, Websocket is not woring, is_websocket_working")
    else:
        print("NO eth_data - is_websocket_working")

    return True

#Get the environment variable
def get_env_var():
    sendData = ({
        "status": False,
        "message": "get_env_var Started",
        "data": None
    }) 

    SEND_EMAIL = os.getenv("SEND_EMAIL")
    SEND_EMAIL_PASSWORD = os.getenv("SEND_EMAIL_PASSWORD")
    RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

    if(SEND_EMAIL and SEND_EMAIL_PASSWORD and RECEIVER_EMAIL):
        sendData["data"] = {
            "send_email" : SEND_EMAIL,
            "send_email_password" : SEND_EMAIL_PASSWORD,
            "receiver_email" : RECEIVER_EMAIL,
        }
        sendData["status"] = True
        sendData["message"] = "Yes we have env variables"
    else:
        sendData["status"] = False
        sendData["message"] = "No we dont have env variables"

    return sendData


#Email Alert  ####ITS DONE####
def Email_Alert(DANGER_LEVEL, MESSAGE):
    
    config_data = get_env_var()

    sendData = ({
        "status": False,
        "message": "Started"
    }) 

    if(config_data["status"]):
        now = datetime.now()
        current_time = round(datetime.timestamp(now))
        date_time_str = datetime.fromtimestamp(current_time).strftime('%d.%m.%y %H:%M')

        Alert_Message = "DANGER_LEVEL: " + str(DANGER_LEVEL) +"\n MESSAGE: "+MESSAGE

        try:
            email_address = config_data["data"]["send_email"]
            email_password = config_data["data"]["send_email_password"]

            if email_address is None or email_password is None:
                # no email address or password
                # something is not configured properly
                print("Did you set email address and password correctly?")
                sendData["message"] = "Did you set email address and password correctly?"
                return sendData

            # create email
            msg = EmailMessage()

            if(DANGER_LEVEL >=2):
                if(DANGER_LEVEL == 10):
                    msg['Subject'] = "❗️❗️❗️[URGENT] Danger_Alert : BullParrot " + str(date_time_str)
                else:
                    msg['Subject'] = "❗️❗️❗️ Danger_Alert : BullParrot " + str(date_time_str)
            else:
                msg['Subject'] = "ℹ️ 🔸 Info_Alert : BullParrot" + str(date_time_str)

            msg['From'] = email_address
            msg['To'] = config_data["data"]["receiver_email"]
            msg.set_content(Alert_Message)

            # send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_address, email_password)
                smtp.send_message(msg)

            sendData["status"] = True
            sendData["message"] = MESSAGE
            return sendData
        except Exception as e:
            print("Problem during send email")
            sendData["message"] = "Problem during send email"+str(e)
            print(str(e))
            pass
    else:
        sendData["message"] = "No config data from database"

    return sendData