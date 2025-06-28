from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)
app.debug = True

# Function to get the user's Facebook name using the access token
def get_profile_name(access_token):
    url = "https://graph.facebook.com/me"
    params = {'access_token': access_token}
    response = requests.get(url, params=params)
    data = response.json()
    if 'name' in data:
        return data['name']
    return None

# Home route with form and results
@app.route('/', methods=['GET', 'POST'])
def index():
    profile_name = None
    error_message = None

    if request.method == 'POST':
        access_token = request.form.get('access_token')
        profile_name = get_profile_name(access_token)
        if profile_name is None:
            error_message = "Invalid access token. Please try again."

    # Inline HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>𝗟𝗘𝗚𝗘𝗡𝗗 𝗬𝗨𝗩𝗜𝗜 𝗜𝗡𝗦𝗜𝗗𝗘 | Facebook Token Checker</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 30px; }
            h1 { color: #333; }
            form { margin-top: 20px; }
            input[type=text] { padding: 8px; width: 300px; }
            input[type=submit] { padding: 8px 15px; }
            .result { margin-top: 20px; font-size: 18px; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>𝗟𝗘𝗚𝗘𝗡𝗗 𝗬𝗨𝗩𝗜𝗜 𝗜𝗡𝗦𝗜𝗗𝗘</h1>
        <p>Enter your Facebook access token to check profile name:</p>
        <form method="post">
            <input type="text" name="access_token" placeholder="Enter Access Token" required />
            <input type="submit" value="Check" />
        </form>

        {% if profile_name %}
            <div class="result">✅ Profile Name: <strong>{{ profile_name }}</strong></div>
        {% elif error_message %}
            <div class="result error">❌ {{ error_message }}</div>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html_template, profile_name=profile_name, error_message=error_message)

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
