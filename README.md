# Phaidra Coding Challenge

Hello!

This repo contains two main sections that are completely independent of one another.

In the `coding_challenge_submission` section, you'll find a finished, working prototype of the `scraper_service` that (I think) meets all of the requirements outlined in the challenge. There are still a few kinks that I would like to work out with more time and coding support - for example, the Prometheus server is still supplying a Gauge metric that I can't seem to get rid of, and lord did I try. But the basic functionality is all there.

The `coding_challenge_attempt` section is a first draft of how I wanted to address this challenge. It's a little more ambitious, and would probably be the "right" way to implement this service in production. But it proved a little bit too much to implement in the time I had to do this, and I didn't quite get it to work.

The main difference between the two is that the finished submission is a single Python script that creates two servers, a Flask server and a Prometheus server, on two different ports, while the unfinished section was an attempt at putting each part of that into its own Kubernetes pod. Full transparency: the problem with the more ambitious first attempt was that I just didn't have enough experience with Prometheus or Kubernetes to combine the two effectively - I've done some Kubernetes practice before and tinkered with existing deployments, but Prometheus was brand new. I did my best to pick up enough practical Kubernetes in the time allotted to fully implement this, but I just wasn't confident I could get it working correctly. (And reading Kubernetes and Prometheus documentation for a week was beginning to cost me my sanity.) But I still wanted to include the whole working process in this repo so you could see how I approached the problem.

So without further ado, documentation on how to run and test each version.

## coding_challenge_submission, or, "Once more with feeling"

This service is comprised of a single Python script and a Dockerfile to build an image. To build that image, run
```docker build -t scraper_service:latest .```
(Of course, you can tag it with whatever you'd like - I'm going to assume you've stuck with my tags for this README.)
Then run it with 
```docker run -p 8085:8080 -p 9095:9095 scraper_service:latest```
(Again, you can choose which ports to map to the container ports. Within the Docker container, port 8080 will reach the `scraper_service`, while port 9095 will hit the Prometheus server. Just map those to any unused external ports.)
Once it's running, you can hit the `scraper_service` by running
```curl 0.0.0.0:8085```
There are a few endpoints available for health and liveness checks. The main endpoint from the coding challenge can be hit like this:
```curl --header "Content-Type: application/json" --request POST --data '{"url": "http://www.phaidra.com"}' 0.0.0.0:8085```
It should respond with the HTML response from the url you hit.
To hit the Prometheus server, run
```curl localhost:9095/metrics```
You should see counters of all the endpoints you've hit, and the status codes you've received - like so:
```
# HELP http_get_total Requests by url and status code
# TYPE http_get_total counter
http_get_total{code="200",url="http://www.google.com"} 1.0
```
