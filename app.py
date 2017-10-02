import datetime
import gzip
import json
import logging
import uuid
from functools import wraps
from logging.handlers import RotatingFileHandler

from flask import Flask, request, jsonify, g, abort

import settings

app = Flask(__name__)


def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if 'User-Agent' not in request.headers:
            abort(401)
        else:
            sent_key = request.headers.get('User-Agent').split("client: ", 1)[1].strip()

        if sent_key in settings.APPKEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function


@app.before_first_request
def setup_logging():
    # Application Logging
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
    handler = RotatingFileHandler('longview-backend.log', maxBytes=2000000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Event Logging Output
    backend_event_logger = logging.getLogger('backend_event_logger')
    backend_event_logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(settings.EVENT_LOG, maxBytes=2000000, backupCount=1)
    backend_event_logger.addHandler(handler)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
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
@require_appkey
def handle_post():
    if 'User-Agent' not in request.headers:
        abort(500)
    if 'data' not in request.files:
        abort(500)

    uncompressed = gzip.GzipFile(fileobj=request.files.get('data').stream, mode='rb')
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
@require_appkey
def handle_get():
    #with open('payload.json') as data_file:
    #    data = json.load(data_file)
    #process_json(data)

    log_info(g.begin_time, g.real_ip, 'accepted', g.event_id,
             'Processing completed')

    return jsonify({'status': "accepted",
                    'trace-id': g.event_id}), 200


@app.errorhandler(500)
def internal_error(exception):
    log_info(g.begin_time, g.real_ip, 'rejected', g.event_id,
             'internal error occured')
    return jsonify({'status': "internal error"}), 500


@app.errorhandler(401)
def unauthorized(exception):
    log_info(g.begin_time, g.real_ip, 'rejected', g.event_id,
             'unauthorized')
    return jsonify({'status': "unauthorized"}), 401


def process_json(data):
    longterm = data["payload"][0]["LONGTERM"]
    instant = data["payload"][0]["INSTANT"]

    event_object = {}

    event_object['host'] = instant['SysInfo.hostname']
    event_object['trace-id'] = g.event_id
    event_object['@timestamp'] = datetime.datetime.fromtimestamp(data["payload"][0]['timestamp']).isoformat()

    log_debug(g.begin_time, g.real_ip, 'processing', g.event_id,
             'Take ' + data["payload"][0]['timestamp'].__str__() + ' and write ' + event_object['@timestamp'].__str__())

    # Omit Keys for Processes
    for key, value in longterm.iteritems():
        if 'Processes.' not in key:
            event_object[key] = value
    backend_event_logger = logging.getLogger('backend_event_logger')
    backend_event_logger.debug(json.dumps(event_object))


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
