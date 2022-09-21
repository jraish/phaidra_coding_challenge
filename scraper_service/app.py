from flask import Flask, request
import requests

app = Flask(__name__)
 
@app.route('/', methods = ['POST'])
def make_external_call():
    request_body = request.json
    r = requests.get(request_body.get('url'))
    
    return {
        'content': r.text,
        'status_code': r.status_code
    }

@app.route('/')
def readiness_probe():
    pass
 
if __name__ == '__main__':
    app.run()