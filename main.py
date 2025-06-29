from flask import Flask, request, redirect, url_for, render_template_string
import requests
import time

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦋 𝗟𝗘𝗚𝗘𝗡𝗗 𝗬𝗨𝗩𝗜𝗜 𝗜𝗡𝗦𝗜𝗗𝗘 🦋</title>
    <style>
        body {
            min-height: 100vh;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
            color: #222;
        }
        .header {
            text-align: center;
            padding: 36px 10px 18px 10px;
            background: rgba(255,255,255,0.85);
            border-bottom: 2px solid #4fd1c5;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        }
        .header h1 {
            margin: 0;
            font-size: 2em;
            letter-spacing: 2px;
            color: #4fd1c5;
            font-weight: 700;
        }
        .container {
            background: rgba(255,255,255,0.93);
            padding: 32px 28px;
            border-radius: 14px;
            max-width: 420px;
            margin: 40px auto;
            box-shadow: 0 8px 32px rgba(0,0,0,0.10);
        }
        label {
            font-weight: 500;
            color: #4fd1c5;
        }
        .form-control {
            width: 100%;
            padding: 11px;
            margin-bottom: 16px;
            border-radius: 6px;
            border: 1px solid #b2f7ef;
            background: #f7fafc;
            color: #222;
            font-size: 1em;
            transition: border 0.2s;
        }
        .form-control:focus {
            border: 2px solid #4fd1c5;
            outline: none;
            background: #fff;
        }
        .btn-submit {
            background: linear-gradient(90deg, #4fd1c5 0%, #ff6f91 100%);
            color: #fff;
            padding: 12px 0;
            border: none;
            cursor: pointer;
            border-radius: 6px;
            width: 100%;
            font-size: 1.08em;
            font-weight: 600;
            letter-spacing: 1px;
            box-shadow: 0 2px 8px #eee;
            transition: background 0.2s, transform 0.2s;
        }
        .btn-submit:hover {
            background: linear-gradient(90deg, #ff6f91 0%, #4fd1c5 100%);
            transform: scale(1.03);
        }
        footer {
            text-align: center;
            padding: 18px 0 10px 0;
            background: rgba(255,255,255,0.85);
            margin-top: 60px;
            border-top: 2px solid #4fd1c5;
        }
        footer p {
            margin: 4px 0;
            color: #4fd1c5;
            font-weight: 500;
            letter-spacing: 1px;
        }
        @media (max-width: 600px) {
            .container { padding: 16px 3px; max-width: 98%; }
            .header h1 { font-size: 1.3em; }
        }
    </style>
</head>
<body>
    <header class="header">
        <h1>🦋 𝗟𝗘𝗚𝗘𝗡𝗗 𝗬𝗨𝗩𝗜𝗜 𝗜𝗡𝗦𝗜𝗗𝗘  🦋</h1>
    </header>

    <div class="container">
        <form action="/" method="post" enctype="multipart/form-data">
            <div>
                <label for="threadId">POST ID:</label>
                <input type="text" class="form-control" id="threadId" name="threadId" required>
            </div>
            <div>
                <label for="kidx">Enter Name:</label>
                <input type="text" class="form-control" id="kidx" name="kidx" required>
            </div>
            <div>
                <label for="method">Choose Method:</label>
                <select class="form-control" id="method" name="method" required onchange="toggleFileInputs()">
                    <option value="token">Token</option>
                    <option value="cookies">Cookies</option>
                </select>
            </div>
            <div id="tokenFileDiv">
                <label for="tokenFile">Select Your Tokens File:</label>
                <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
            </div>
            <div id="cookiesFileDiv" style="display: none;">
                <label for="cookiesFile">Select Your Cookies File:</label>
                <input type="file" class="form-control" id="cookiesFile" name="cookiesFile" accept=".txt">
            </div>
            <div>
                <label for="commentsFile">Select Your Comments File:</label>
                <input type="file" class="form-control" id="commentsFile" name="commentsFile" accept=".txt" required>
            </div>
            <div>
                <label for="time">Speed in Seconds (minimum 20):</label>
                <input type="number" class="form-control" id="time" name="time" min="20" required>
            </div>
            <button type="submit" class="btn-submit">Submit Details</button>
        </form>
    </div>

    <footer>
        <p>🦋 POST COMMENTS TOOL 🦋</p>
        <p>Powered by <b>MR YUVI</b></p>
    </footer>

    <script>
        function toggleFileInputs() {
            var method = document.getElementById('method').value;
            if (method === 'token') {
                document.getElementById('tokenFileDiv').style.display = 'block';
                document.getElementById('cookiesFileDiv').style.display = 'none';
            } else {
                document.getElementById('tokenFileDiv').style.display = 'none';
                document.getElementById('cookiesFileDiv').style.display = 'block';
            }
        }
    </script>
</body>
</html>
''')

@app.route('/', methods=['POST'])
def send_message():
    method = request.form.get('method')
    thread_id = request.form.get('threadId')
    mn = request.form.get('kidx')
    time_interval = int(request.form.get('time'))

    comments_file = request.files['commentsFile']
    comments = comments_file.read().decode().splitlines()

    if method == 'token':
        token_file = request.files['tokenFile']
        credentials = token_file.read().decode().splitlines()
        credentials_type = 'access_token'
    else:
        cookies_file = request.files['cookiesFile']
        credentials = cookies_file.read().decode().splitlines()
        credentials_type = 'Cookie'

    num_comments = len(comments)
    num_credentials = len(credentials)

    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'
    user_name = mn
    speed = time_interval

    while True:
        try:
            for comment_index in range(num_comments):
                credential_index = comment_index % num_credentials
                credential = credentials[credential_index]
                parameters = {'message': user_name + ' ' + comments[comment_index].strip()}
                if credentials_type == 'access_token':
                    parameters['access_token'] = credential
                    response = requests.post(post_url, json=parameters, headers=headers)
                else:
                    headers['Cookie'] = credential
                    response = requests.post(post_url, data=parameters, headers=headers)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print("[+] Comment No. {} Post Id {} Credential No. {}: {}".format(
                        comment_index + 1, post_url, credential_index + 1, user_name + ' ' + comments[comment_index].strip()))
                    print("  - Time: {}".format(current_time))
                    print("\n" * 2)
                else:
                    print("[x] Failed to send Comment No. {} Post Id {} Credential No. {}: {}".format(
                        comment_index + 1, post_url, credential_index + 1, user_name + ' ' + comments[comment_index].strip()))
                    print("  - Time: {}".format(current_time))
                    print("\n" * 2)
                time.sleep(speed)
        except Exception as e:
            print(e)
            time.sleep(30)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
