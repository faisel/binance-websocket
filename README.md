

http://127.0.0.1:5000/api

Domain: https://i43nqeej25.eu-central-1.awsapprunner.com/



#### Git commit & push - When push to github main, AWS will automatically update to server
git add .
git commit -m 'Flask-Cors updated'
git push origin main


# Run locally
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
