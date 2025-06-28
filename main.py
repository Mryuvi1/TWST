from flask import Flask, request, render_template, redirect, url_for, session
import requests
import json
import os
from uuid import uuid4

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# Configuration
OWNER_NAME = "𝗟𝗘𝗚𝗘𝗡𝗗 𝗬𝗨𝗩𝗜𝗜 𝗜𝗡𝗦𝗜𝗗𝗘"

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
