# -*- coding: utf-8 -*-

"""
zabbix-client
~~~~~~~~~~~~~

zabbix-client is a Zabbix API wrapper written in Python. Zabbix API was
introduced in Zabbix 1.8 and allows you to create, update and fetch
Zabbix objects (like hosts, items, graphs and others) through the
JSON-RPC 2.0 protocol.

Zabbix API documentation:
https://www.zabbix.com/documentation/1.8/api/getting_started
https://www.zabbix.com/documentation/2.2/manual/api
https://www.zabbix.com/documentation/2.2/manual/api/reference

JSON-RPC 2.0 specification:
http://www.jsonrpc.org/specification
"""

__version__ = '0.1.0'
__author__ = 'Jesús Losada Novo'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2014 Jesús Losada Novo'


from .api_wrapper import (
    ZabbixServerProxy, Transport, RequestsTransport, UrllibTransport
)
from .exceptions import (
    ZabbixClientError, TransportError, TimeoutError, HTTPError, ResponseError,
    ContentDecodingError, InvalidJSONError, JSONRPCError
)


# Add a do-nothing logging handler.
# https://docs.python.org/3/howto/logging.html#library-config
import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
