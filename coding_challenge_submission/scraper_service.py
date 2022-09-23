from flask import Flask, request
import prometheus_client
import requests
from prometheus_flask_exporter import PrometheusMetrics

prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)

def custom_rule(req):
    return req.json.get('url')

app = Flask(__name__)
metrics = PrometheusMetrics(app, group_by=custom_rule, export_defaults=False)

@app.route('/', methods=['POST'])
@metrics.do_not_track()
@metrics.counter(
    'http_get',
    'Requests by url and status code',
    labels={'url': lambda: request.json.get(
        'url'), 'code': lambda r: r.status_code},
)
def make_external_call():
    request_body = request.json
    r = requests.get(request_body.get('url'))

    return {
        'content': r.text,
        'status_code': r.status_code
    }

@app.route('/health')
@metrics.do_not_track()
def health():
    return '', 200

@app.route('/ready')
@metrics.do_not_track()
def ready():
    return '', 200

@app.route('/')
@metrics.do_not_track()
def default():
    return '', 200

prometheus_client.start_http_server(port=9095)
app.run(host='0.0.0.0',port=8080)
