from flask import Flask, request, redirect, render_template, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# Your Facebook App credentials
APP_ID = 'YOUR_APP_ID'
APP_SECRET = 'YOUR_APP_SECRET'
REDIRECT_URI = 'http://localhost:5000/callback'

def exchange_code_for_token(code):
    token_url = 'https://graph.facebook.com/v19.0/oauth/access_token'
    params = {
        'client_id': APP_ID,
        'redirect_uri': REDIRECT_URI,
        'client_secret': APP_SECRET,
        'code': code
    }
    response = requests.get(token_url, params=params)
    return response.json()

def get_profile_name(access_token):
    url = "https://graph.facebook.com/me"
    params = {'access_token': access_token}
    response = requests.get(url, params=params)
    data = response.json()
    if 'name' in data:
        return data['name']
    return None

@app.route('/')
def index():
    profile_name = session.get('profile_name')
    access_token = session.get('access_token')
    owner_name = "𝗟𝗘𝗚𝗘𝗡𝗗 𝗬𝗨𝗩𝗜𝗜 𝗜𝗡𝗦𝗜𝗗𝗘"
    return render_template('index.html', profile_name=profile_name, access_token=access_token, owner_name=owner_name)

@app.route('/login')
def login():
    facebook_login_url = (
        f"https://www.facebook.com/v19.0/dialog/oauth"
        f"?client_id={APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=email,public_profile"
    )
    return redirect(facebook_login_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Authorization failed."

    token_response = exchange_code_for_token(code)
    access_token = token_response.get('access_token')

    if not access_token:
        return "Token exchange failed."

    profile_name = get_profile_name(access_token)
    session['access_token'] = access_token
    session['profile_name'] = profile_name

    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
