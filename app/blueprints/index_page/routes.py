from flask import Blueprint, make_response, render_template, current_app
import json

blueprint = Blueprint(
    'index',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@blueprint.route("/", methods=["get"])
def index_route():
    return make_response(
        render_template(
            "index.jinja2",
        )
    )


@blueprint.route('/price', methods=['GET', 'POST'])
def price_page():

    data = None

    # Opening JSON file
    btc_price = open('app/data/price_btc.json')
    eth_price = open('app/data/price_eth.json')

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