import multiprocessing

wsgi_app: str = "config.wsgi.application"
bind = "0.0.0.0:8000"

# The number of worker processes for handling requests.
workers: int = multiprocessing.cpu_count() * 2 + 1
threads: int = multiprocessing.cpu_count() * 2

# Log to stdout.
accesslog = "-"
errorlog = "-"

# Set to * to disable checking of Front-end IPs (useful for setups where you don't know in advance the IP address of Front-end, but you still trust the environment).  # noqa: E501
forwarded_allow_ips = "*"
proxy_allow_ips = "*"

# Automatically restart the worker after 750-1250 requests to avoid memory leaks.
max_requests = 1000
max_requests_jitter = 250
