

http://127.0.0.1:5000/

Domain: kh-binance-faisel-btc-eth: https://5i3mr7mjmc.eu-central-1.awsapprunner.com/ - https://killerhedge.bullparrot.com/
Domain: binance-websocket: https://i43nqeej25.eu-central-1.awsapprunner.com/ - https://binance.bullparrot.com/


#### Git commit & push - When push to github main, AWS will automatically update to server
#### Change update date in templates/layouts/main.jinja2
git add .
git commit -m 'Price data updated'
git push origin main


# Run locallyflask --app application.py --debug run
flask --app application.py --debug run


# AWS App Runner deployment
: Open AWS App Runner
: Create an App Runner service
: Select: Source code repository
: Connect gitHub and select repo
: Deployment Settings: Automatic
: Runtime: Python3
: Build Command: pip install -r requirements.txt
: Start Command: python application.py
: Post: 80 (Very very important)
: Configure service: all default




  {
    "e": "markPriceUpdate",     // Event type
    "E": 1562305380000,         // Event time
    "s": "BTCUSDT",             // Symbol
    "p": "11794.15000000",      // Mark price
    "i": "11784.62659091",      // Index price
    "P": "11784.25641265",      // Estimated Settle Price, only useful in the last hour before the settlement starts
    "r": "0.00038167",          // Funding rate
    "T": 1562306400000          // Next funding time
  }