"""
Pulls data from specified iLO and presents as Prometheus metrics
"""
from __future__ import print_function
from _socket import gaierror
import sys
import hpilo
import ssl
import os

import time
import prometheus_metrics
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ForkingMixIn
from prometheus_client import generate_latest, Summary
from urllib.parse import parse_qs
from urllib.parse import urlparse

from logger import get_module_logger

def print_err(*args, **kwargs):
    get_module_logger("exporter").error(*args, file=sys.stderr, **kwargs)


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary(
    'request_processing_seconds', 'Time spent processing request')


class ForkingHTTPServer(ForkingMixIn, HTTPServer):
    max_children = 30
    timeout = 30


class RequestHandler(BaseHTTPRequestHandler):
    """
    Endpoint handler
    """
    def return_error(self):
        self.send_response(500)
        self.end_headers()

    def do_GET(self):
        """
        Process GET request

        :return: Response with Prometheus metrics
        """
        # this will be used to return the total amount of time the request took
        start_time = time.time()
        # get parameters from the URL
        url = urlparse(self.path)
        # following boolean will be passed to True if an error is detected during the argument parsing
        error_detected = False
        query_components = parse_qs(urlparse(self.path).query)

        # 127.0.0.1 - - [03/Aug/2020 10:15:09] "GET /metrics?ilo_host=192.168.220.188&ilo_port=443&ilo_user=prometheus&ilo_password=xzcwjikomEvkqidm4t HTTP/1.1" 200 -

        get_module_logger("exporter").info("{} GET {}".format(self.client_address ,self.path))

        ilo_host = None
        ilo_port = None
        ilo_user = None
        ilo_password = None
        try:
            ilo_host = query_components.get('ilo_host', [''])[0] or os.environ['ILO_HOST']
            ilo_port = int(query_components.get('ilo_port', [''])[0] or os.environ['ILO_PORT'])
            ilo_user = query_components.get('ilo_user', [''])[0] or os.environ['ILO_USER']
            ilo_password = query_components.get('ilo_password', [''])[0] or os.environ['ILO_PASSWORD']

        except KeyError as e:
            get_module_logger("exporter").error("missing parameter %s" % e)
            self.return_error()
            error_detected = True

        if url.path == self.server.endpoint and ilo_host and ilo_user and ilo_password and ilo_port:

            ilo = None
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            # Sadly, ancient iLO's aren't dead yet, so let's enable sslv3 by default
            ssl_context.options &= ~ssl.OP_NO_SSLv3
            ssl_context.check_hostname = False
            ssl_context.set_ciphers(('ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
            'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
            '!eNULL:!MD5'))

            try:
                ilo = hpilo.Ilo(hostname=ilo_host,
                                login=ilo_user,
                                password=ilo_password,
                                port=ilo_port, timeout=10,
                                ssl_context=ssl_context)
            except hpilo.IloLoginFailed:
                get_module_logger("exporter").error("ILO login failed")
                self.return_error()
            except gaierror:
                get_module_logger("exporter").error("ILO invalid address or port")
                self.return_error()
            except hpilo.IloCommunicationError as e:
                get_module_logger("exporter").error(e)
                self.return_error()

            # get product and server name
            try:
                product_name = ilo.get_product_name()
            except:
                product_name = "Unknown HP Server"

            try:
                server_name = ilo.get_server_name()
                if server_name == "":
                    server_name = ilo_host
            except:
                server_name = ilo_host

            # get health
            embedded_health = ilo.get_embedded_health()
            health_at_glance = embedded_health['health_at_a_glance']
            


            if health_at_glance is not None:
                for key, value in health_at_glance.items():
                    for status in value.items():
                        if status[0] == 'status':
                            gauge = 'hpilo_{}_gauge'.format(key)
                            if status[1].upper() == 'OK':
                                prometheus_metrics.gauges[gauge].labels(product_name=product_name,
                                                                        server_name=server_name).set(0)
                            elif status[1].upper() == 'DEGRADED':
                                prometheus_metrics.gauges[gauge].labels(product_name=product_name,
                                                                        server_name=server_name).set(1)
                            else:
                                prometheus_metrics.gauges[gauge].labels(product_name=product_name,
                                                                        server_name=server_name).set(2)

            # get firmware version
            fw_version = ilo.get_fw_version()["firmware_version"]
            # prometheus_metrics.hpilo_firmware_version.set(fw_version)
            prometheus_metrics.hpilo_firmware_version.labels(product_name=product_name,
                                                             server_name=server_name).set(fw_version)
            # get temperature informations
            for temp in embedded_health['temperature']:
                value = embedded_health['temperature'][temp]['currentreading'][0]
                if value != "N":
                    prometheus_metrics.hpilo_temperature_status_gauge.labels(product_name=product_name,
                                                            server_name=server_name,
                                                            sensor=temp).set(value)


            # get the amount of time the request took
            REQUEST_TIME.observe(time.time() - start_time)
            get_module_logger("exporter").info("REQUEST_TIME: {}s".format(str(REQUEST_TIME._sum._value)))

            # generate and publish metrics
            metrics = generate_latest(prometheus_metrics.registry)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(metrics)

        elif url.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write("""<html>
            <head><title>HP iLO Exporter</title></head>
            <body>
            <h1>HP iLO Exporter</h1>
            <p>Visit <a href="/metrics">Metrics</a> to use.</p>
            </body>
            </html>""")

        else:
            if not error_detected:
                self.send_response(404)
                self.end_headers()

    def log_message(self, format, *args):
        return

class ILOExporterServer(object):
    """
    Basic server implementation that exposes metrics to Prometheus
    """

    def __init__(self, address='0.0.0.0', port=8080, endpoint="/metrics"):
        self._address = address
        self._port = port
        self.endpoint = endpoint

    def print_info(self):
        get_module_logger("exporter").info("Starting exporter on: http://{}:{}{}".format(self._address, self._port, self.endpoint))

    def run(self):
        self.print_info()

        server = ForkingHTTPServer((self._address, self._port), RequestHandler)
        server.endpoint = self.endpoint

        try:
            while True:
                server.handle_request()
        except KeyboardInterrupt:
            get_module_logger("exporter").info("Killing exporter")
            server.server_close()
