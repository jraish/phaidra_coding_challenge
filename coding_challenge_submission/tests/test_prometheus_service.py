import requests
import sys

def test_that_service_is_running(prom_port):
    r = requests.get(f'http://0.0.0.0:{prom_port}')

    assert r.status_code == 200

def test_that_scraper_service_is_running(ss_port):
    r = requests.get(f'http://0.0.0.0:{ss_port}')

    assert r.status_code == 200

def test_that_prom_server_connects_to_ss_server(prom_port):
    r = requests.get(f'http://0.0.0.0:{prom_port}')
    output = r.content.decode('utf8').replace("'", '"').split('\n')
    assert len(output) >= 3
    assert output[0] == '# HELP http_get_total Requests by url and status code'
    assert output[1] == '# TYPE http_get_total counter'

def test_that_call_to_ss_results_in_prom_output(ss_port, prom_port):
    test_url = "http://www.phaidra.com"
    call_count = 5

    headers = {
        "Content-Type": "application/json",
    }
    json_data = {
        "url": test_url
    }

    for i in range(0, call_count):
        r = requests.post(f'http://0.0.0.0:{ss_port}/', headers=headers, json=json_data)

    prom_r = requests.get(f'http://0.0.0.0:{prom_port}')
    output = prom_r.content.decode('utf8').replace("'", '"').split('\n')
    phaidra_results = [s for s in output if test_url in s]
    num_of_calls = float(phaidra_results[0].split(' ')[-1])
    
    assert num_of_calls >= call_count

def run_all_tests(prom_port, ss_port):
    test_that_service_is_running(prom_port)
    test_that_scraper_service_is_running(ss_port)
    test_that_prom_server_connects_to_ss_server(prom_port)
    test_that_call_to_ss_results_in_prom_output(ss_port, prom_port)

if __name__ == '__main__':
    try:
        prom_port = sys.argv[1]
        ss_port = sys.argv[2]
        run_all_tests(prom_port, ss_port)
    except IndexError as e:
        print('Please provide the Prometheus port as the first argument and the scraper service port as the second')
