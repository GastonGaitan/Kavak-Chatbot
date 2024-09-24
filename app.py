from flask import Flask

app = Flask(__name__)

@app.route('/kavak-assistant', methods=['POST'])
def process_message():
    return 'Hello, World!'