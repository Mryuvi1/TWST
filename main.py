from flask import Flask, request, render_template, redirect, url_for, session
import requests
import os
from uuid import uuid4

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# Configuration - Replace these with your Facebook App credentials
FB_APP_ID = 'YOUR_FACEBOOK_APP_ID'
FB_APP_SECRET = 'YOUR_FACEBOOK_APP_SECRET'
FB_REDIRECT_URI = 'http://localhost:5000/callback'  # Update with your actual domain
OWNER_NAME = "𝗟𝗘𝗚𝗘𝗡𝗗 𝗬𝗨𝗩𝗜𝗜 𝗜𝗡𝗦𝗜𝗗𝗘"

@app.route('/')
def index():
    return render_template('index.html', 
                         owner_name=OWNER_NAME,
                         profile_name=session.get('profile_name'),
                         access_token=session.get('access_token'))

@app.route('/login')
def login():
    # Generate a unique state token to prevent CSRF
    state = str(uuid4())
    session['state'] = state
    
    # Facebook OAuth URL
    fb_auth_url = (
        f"https://www.facebook.com/v12.0/dialog/oauth?"
        f"client_id={FB_APP_ID}"
        f"&redirect_uri={FB_REDIRECT_URI}"
        f"&state={state}"
        f"&scope=public_profile,email"
        f"&response_type=code"
    )
    return redirect(fb_auth_url)

@app.route('/callback')
def callback():
    # Verify state matches
    if request.args.get('state') != session.get('state'):
        return "State mismatch error", 400
    
    # Get authorization code
    code = request.args.get('code')
    if not code:
        return "Authorization failed", 400
    
    # Exchange code for access token
    token_url = (
        f"https://graph.facebook.com/v12.0/oauth/access_token?"
        f"client_id={FB_APP_ID}"
        f"&redirect_uri={FB_REDIRECT_URI}"
        f"&client_secret={FB_APP_SECRET}"
        f"&code={code}"
    )
    
    response = requests.get(token_url)
    if response.status_code != 200:
        return "Failed to get access token", 400
    
    data = response.json()
    access_token = data.get('access_token')
    if not access_token:
        return "No access token received", 400
    
    # Get user profile
    profile_url = f"https://graph.facebook.com/me?access_token={access_token}&fields=name,id"
    profile_response = requests.get(profile_url)
    if profile_response.status_code != 200:
        return "Failed to get profile", 400
    
    profile_data = profile_response.json()
    session['profile_name'] = profile_data.get('name')
    session['access_token'] = access_token
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
