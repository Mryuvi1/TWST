from flask import Flask, request, render_template, redirect, url_for, session
import requests
import json
import os
from uuid import uuid4

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# Configuration
OWNER_NAME = "MR YUVI XD"  # Changed from "𝗟𝗘𝗚𝗘𝗡𝗗 𝗬𝗨𝗩𝗜𝗜 𝗜𝗡𝗦𝗜𝗗𝗘" to "MR YUVI XD"
FB_APP_ID = 'YOUR_APP_ID'  # Replace with your Facebook App ID
FB_APP_SECRET = 'YOUR_APP_SECRET'  # Replace with your Facebook App Secret
REDIRECT_URI = 'http://localhost:5000/fb_callback'  # Update with your actual domain

def cookie_to_token(cookie):
    try:
        headers = {
            'authority': 'graph.facebook.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://www.facebook.com',
            'referer': 'https://www.facebook.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'cookie': cookie
        }
        
        # First get the user ID
        user_id_response = requests.get('https://graph.facebook.com/me', headers=headers)
        if user_id_response.status_code != 200:
            return None, "Failed to get user ID from cookie"
        
        user_id = user_id_response.json().get('id')
        if not user_id:
            return None, "No user ID found in response"
        
        # Then get the access token
        token_response = requests.get(
            f'https://graph.facebook.com/{user_id}/accounts?access_token={cookie.split("sb=")[1].split(";")[0]}'
        )
        
        if token_response.status_code != 200:
            return None, "Failed to convert cookie to access token"
        
        token_data = token_response.json()
        if 'access_token' not in token_data:
            return None, "No access token in response"
        
        return token_data['access_token'], None
    
    except Exception as e:
        return None, f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    access_token = None
    profile_info = None
    
    if request.method == 'POST':
        cookie = request.form.get('cookie')
        if cookie:
            access_token, error = cookie_to_token(cookie)
            
            if access_token:
                # Get profile info
                profile_url = f'https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}'
                profile_response = requests.get(profile_url)
                
                if profile_response.status_code == 200:
                    profile_info = profile_response.json()
                else:
                    error = "Got token but failed to fetch profile info"
    
    return render_template(
        'index.html',
        owner_name=OWNER_NAME,
        access_token=access_token,
        profile_info=profile_info,
        error=error
    )

@app.route('/token_maker')
def token_maker():
    return render_template('token_maker.html', owner_name=OWNER_NAME)

@app.route('/fb_login')
def fb_login():
    # Generate state token to prevent CSRF
    state = str(uuid4())
    session['oauth_state'] = state
    
    # Facebook OAuth URL
    auth_url = (
        f"https://www.facebook.com/v12.0/dialog/oauth?"
        f"client_id={FB_APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state={state}"
        f"&scope=public_profile,email,manage_pages,publish_pages"
        f"&response_type=code"
    )
    return redirect(auth_url)

@app.route('/fb_callback')
def fb_callback():
    # Verify state matches
    if request.args.get('state') != session.get('oauth_state'):
        return "State mismatch error", 400
    
    # Get authorization code
    code = request.args.get('code')
    if not code:
        return "Authorization failed", 400
    
    # Exchange code for access token
    token_url = (
        f"https://graph.facebook.com/v12.0/oauth/access_token?"
        f"client_id={FB_APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&client_secret={FB_APP_SECRET}"
        f"&code={code}"
    )
    
    response = requests.get(token_url)
    if response.status_code != 200:
        return "Failed to get access token", 400
    
    token_data = response.json()
    access_token = token_data.get('access_token')
    if not access_token:
        return "No access token received", 400
    
    # Get long-lived token (optional)
    long_token_url = (
        f"https://graph.facebook.com/v12.0/oauth/access_token?"
        f"grant_type=fb_exchange_token"
        f"&client_id={FB_APP_ID}"
        f"&client_secret={FB_APP_SECRET}"
        f"&fb_exchange_token={access_token}"
    )
    
    long_response = requests.get(long_token_url)
    if long_response.status_code == 200:
        long_token_data = long_response.json()
        long_token = long_token_data.get('access_token')
        if long_token:
            access_token = long_token
    
    # Get user profile
    profile_url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
    profile_response = requests.get(profile_url)
    
    if profile_response.status_code != 200:
        return "Failed to get profile", 400
    
    profile_data = profile_response.json()
    
    return render_template(
        'token_result.html',
        owner_name=OWNER_NAME,
        access_token=access_token,
        profile_info=profile_data
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
