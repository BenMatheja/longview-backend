import datetime
import gzip
import json
import logging
import uuid
from logging.handlers import RotatingFileHandler

from flask import Flask, request, jsonify, g

app = Flask(__name__)


@app.before_first_request
def setup_logging():
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",
                              "%Y-%m-%d %H:%M:%S")
    handler = RotatingFileHandler('longview-backend.log', maxBytes=2000000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


@app.before_request
def log_request_info():
    # app.logger.debug('Headers: %s', request.headers)
    # app.logger.debug('Body: %s', request.get_data())
    g.begin_time = datetime.datetime.now()
    if 'trace-id' not in request.headers:
        g.event_id = uuid.uuid4().__str__()
    else:
        g.event_id = request.headers.get('trace-id')
    if 'X-Real-IP' not in request.headers:
        g.real_ip = request.remote_addr.__str__()
    else:
        g.real_ip = request.headers.get('X-Real-IP')


@app.route('/longview', methods=['POST'])
def handle_post():
    if 'User-Agent' not in request.headers:
        raise
    
    file = request.files.get('data').stream
    uncompressed = gzip.GzipFile(fileobj=file, mode='rb')
    with uncompressed as fin:
        json_bytes = fin.read()
        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)

    process_json(data)

    log_info(g.begin_time, g.real_ip, 'accepted', g.event_id,
             'Processing completed')

    return jsonify({'status': "accepted",
                    'trace-id': g.event_id}), 200


@app.route('/longview', methods=['GET'])
def handle_get():
    with open('payload.json') as data_file:
        data = json.load(data_file)
    process_json(data)
    log_info(g.begin_time, g.real_ip, 'accepted', g.event_id,
             'Processing completed')

    return jsonify({'status': "accepted",
                    'trace-id': g.event_id}), 200


@app.errorhandler(500)
def internal_error(exception):
    return jsonify({'status': "internal error"}), 500


def process_json(data):
    longterm = data["payload"][0]["LONGTERM"]
    instant = data["payload"][0]["INSTANT"]

    event_object = {}

    event_object['host'] = instant['SysInfo.hostname']
    event_object['timestamp'] = data["payload"][0]['timestamp']

    # Omit Keys for Processes
    for key, value in longterm.iteritems():
        if 'Processes.' not in key:
            event_object[key] = value

    #app.logger.debug(json.dumps(event_object))


def log_info(begin_time, request_ip, status, trace_id, message, service='handle_post'):
    end = datetime.datetime.now()
    processing_time = (end - begin_time).microseconds.__str__()
    app.logger.info(
        trace_id + ' - ' + request_ip + ' - ' + service + ' - ' + processing_time + ' - ' + status + ' - ' + message)


def log_debug(begin_time, request_ip, status, trace_id, message, service='handle_post'):
    end = datetime.datetime.now()
    processing_time = (end - begin_time).microseconds.__str__()
    app.logger.debug(
        trace_id + ' - ' + request_ip + ' - ' + service + ' - ' + processing_time + ' - ' + status + ' - ' + message)


if __name__ == '__main__':
    app.run(debug=False)
