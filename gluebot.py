#!/usr/bin/python3

from flask import Flask, request
from waitress import serve
from werkzeug.middleware.proxy_fix import ProxyFix
import requests
import os
import logging
from logging.handlers import RotatingFileHandler
import schedule
import time
import threading

CONTROL_SERVER_PORT = os.environ.get('CONTROL_SERVER_PORT')
API_KEY = os.environ.get('API_KEY')
RESTART_TIME = os.environ.get('RESTART_TIME')
CONTROL_SERVER_ENDPOINT = os.environ.get('CONTROL_SERVER_ENDPOINT', '/v1/openvpn/status')

if not CONTROL_SERVER_PORT:
    raise ValueError("CONTROL_SERVER_PORT must be set")

app = Flask(__name__)
# Apply the ProxyFix middleware to correctly capture the client's real IP address
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

API_URL = f'http://127.0.0.1:{CONTROL_SERVER_PORT}${CONTROL_SERVER_ENDPOINT}'
DATA = {
    'status': 'stopped'
}
HEADERS = {
    'x-api-key': API_KEY,
}

# --- Logging setup ---
# Define a file to store logs
LOG_FILE = 'server.log'
# Create a rotating file handler to prevent the log file from growing indefinitely
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10240, backupCount=5)
# Set the log level for the file handler
file_handler.setLevel(logging.INFO)
# Configure a format for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# Add the file handler to the Flask application's logger
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

def restart_job():
    app.logger.info(f"Restart time triggered")
    # TODO: add try logic from trigger_put
    response = requests.put(API_URL, json=DATA, headers=HEADERS)
    app.logger.info(f'PUT request sent. Status code: {response.status_code}, Response: {response.text}')

if RESTART_TIME:
    schedule.every().day.at(RESTART_TIME).do(restart_job)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/', methods=['POST'])
def trigger_put():
    app.logger.info(f"Received POST request from {request.remote_addr}. Data: {request.get_data()}")

    try:
        response = requests.put(API_URL, json=DATA, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        app.logger.info(f'PUT request sent. Status code: {response.status_code}, Response: {response.text}')
        
        # Return a 200 OK with a success message
        return f'PUT request successful. Status code: {response.status_code}', 200
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f'PUT request failed: {e}')
        
        # Return an error message with a non-200 status code
        return f'PUT request failed: {e}', 500


@app.route('/', methods=['GET'])
def show_logs():
    """
    Handle GET requests by reading and displaying the logs from the file.
    """
    try:
        with open(LOG_FILE, 'r') as f:
            logs = f.read()
        
        # Display the logs in a basic HTML format
        return f'<pre>{logs}</pre>'
    except FileNotFoundError:
        return "Log file not found."

if __name__ == '__main__':
    if RESTART_TIME:
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.start()
    serve(app, host='0.0.0.0', port=4040)
