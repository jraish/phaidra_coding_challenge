import requests
import sys

def test_that_service_is_running(port):
    r = requests.get(f'http://0.0.0.0:{port}')

    assert r.status_code == 200

def test_health_check_endpoint(port):
    r = requests.get(f'http://0.0.0.0:{port}/health')

    assert r.status_code == 200

def test_that_invalid_endpoints_respond_with_404(port):
    r = requests.get(f'http://0.0.0.0:{port}/bad_path')

    assert r.status_code == 404

def test_that_empty_post_call_responds_with_400(port):
    r = requests.post(f'http://0.0.0.0:{port}/')

    assert r.status_code == 400

def test_that_well_formed_call_responds_with_200(port):
    headers = {
        "Content-Type": "application/json",
    }
    json_data = {
        "url": "http://www.phaidra.com"
    }
    r = requests.post(f'http://0.0.0.0:{port}/', headers=headers, json=json_data)

    assert r.status_code == 200

def test_that_well_formed_call_responds_with_correct_content(port):
    headers = {
        "Content-Type": "application/json",
    }
    json_data = {
        "url": "http://www.phaidra.com"
    }
    r = requests.post(f'http://0.0.0.0:{port}/', headers=headers, json=json_data).json()
    
    assert ('html' in r.get('content') and 'body' in r.get('content') and r.get('status_code') == 200)

def run_all_tests(port):
    test_that_service_is_running(port)
    test_health_check_endpoint(port)
    test_that_invalid_endpoints_respond_with_404(port)
    test_that_empty_post_call_responds_with_400(port)
    test_that_well_formed_call_responds_with_200(port)
    test_that_well_formed_call_responds_with_correct_content(port)

if __name__ == '__main__':
    if sys.argv[1:]:
        port = sys.argv[1]
        run_all_tests(port)
    else:
        print('Please provide service port as the first argument')
