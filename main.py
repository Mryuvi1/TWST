from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
import os
from uuid import uuid4

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# Facebook App Credentials (replace with your real credentials)
FB_APP_ID = 'YOUR_FACEBOOK_APP_ID'
FB_APP_SECRET = 'YOUR_FACEBOOK_APP_SECRET'
FB_REDIRECT_URI = 'http://localhost:5000/callback'
OWNER_NAME = "𝗟𝗘𝗚𝗘𝗡𝗗 𝗬𝗨𝗩𝗜𝗜 𝗜𝗡𝗦𝗜𝗗𝗘"

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ owner_name }} | Facebook Token Generator</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f4f6f8;
            text-align: center;
            padding: 40px;
            color: #333;
        }
        h1 {
            color: #1877f2;
            font-size: 32px;
        }
        .box {
            background: #fff;
            border-radius: 10px;
            padding: 20px;
            display: inline-block;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
            margin-top: 30px;
            width: 90%;
            max-width: 600px;
        }
        .btn {
            background: #1877f2;
            color: #fff;
            text-decoration: none;
            padding: 10px 20px;
            display: inline-block;
            border-radius: 6px;
            font-size: 16px;
            margin-top: 20px;
        }
        .token {
            word-break: break-all;
            background: #eee;
            padding: 10px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 14px;
            margin-top: 10px;
        }
        .logout {
            display: block;
            margin-top: 30px;
            font-size: 14px;
            color: #888;
        }
    </style>
</head>
<body>

    <h1>{{ owner_name }}</h1>
    <h2>Facebook Access Token Generator</h2>

    <div class="box">
        {% if profile_name %}
            <p><strong>👤 Logged in as:</strong> {{ profile_name }}</p>
            <p><strong>🔑 Your Facebook Access Token:</strong></p>
            <div class="token">{{ access_token }}</div>
            <a href="{{ url_for('logout') }}" class="logout">🔒 Logout</a>
        {% else %}
            <p>Click the button below to generate your Facebook access token securely.</p>
            <a href="{{ url_for('login') }}" class="btn">Login with Facebook</a>
        {% endif %}
    </div>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template,
                                  owner_name=OWNER_NAME,
                                  profile_name=session.get('profile_name'),
                                  access_token=session.get('access_token'))

@app.route('/login')
def login():
    state = str(uuid4())
    session['state'] = state
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
    if request.args.get('state') != session.get('state'):
        return "State mismatch error", 400

    code = request.args.get('code')
    if not code:
        return "Authorization failed", 400

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
