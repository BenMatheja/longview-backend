from flask import Flask, request, jsonify
import gzip, StringIO, json
from logging.handlers import RotatingFileHandler
import logging
import datetime

app = Flask(__name__)


@app.before_first_request
def setup_logging():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler('longview-backend.log', maxBytes=2000000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    # app.logger.debug('Body: %s', request.get_data())


@app.route('/longview', methods=['POST'])
def handle_post():
    begin_time = datetime.datetime.now()
    # app.logger.debug(request.files)
    # for filename, file in request.files.iteritems():
    #   app.logger.debug(request.files[filename].name)
    # app.logger.debug(request.files.get('data'))

    file = request.files.get('data').stream
    uncompressed = gzip.GzipFile(fileobj=file, mode='rb')
    with uncompressed as fin:
        json_bytes = fin.read()
        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)

    process_json(data)
    return jsonify({'status': 'accepted'}), 200

@app.route('/longview', methods=['GET'])
def handle_get():
    with open('payload.json') as data_file:
        data = json.load(data_file)
    process_json(data)
    return jsonify({'status': 'accepted'}), 200

def process_json(data):
    longterm = data["payload"][0]["LONGTERM"]
    instant = data["payload"][0]["INSTANT"]
    #app.logger.debug(longterm)
    #app.logger.debug(instant)

    app.logger.debug(longterm["Network.Interface.eth0.tx_bytes"])
    app.logger.debug(longterm["Network.Interface.eth0.rx_bytes"])
    app.logger.debug(longterm["CPU.cpu0.system"])
    app.logger.debug(longterm["CPU.cpu0.user"])
    app.logger.debug(longterm["CPU.cpu0.wait"])

if __name__ == '__main__':
    app.run(debug=False)
