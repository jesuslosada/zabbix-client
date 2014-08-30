# -*- coding: utf-8 -*-

import socket
from .exceptions import TransportError, TimeoutError
from .zabbix_protocol import NETWORK_TIMEOUT, ZabbixProtocol


def dumps(key):
    return key.encode('utf-8') + b'\n'


def loads(response):
    return response.decode('utf-8').rstrip('\r\n')


class ZabbixGetter(object):

    def __init__(self, host, port=10050, timeout=NETWORK_TIMEOUT,
                 source_address=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        if source_address is None:
            self.source_address = source_address
        else:
            self.source_address = (source_address, 0)

    def get(self, key):
        address = (self.host, self.port)
        connection = None
        try:
            connection = ZabbixProtocol.create_connection(
                address,
                timeout=self.timeout,
                source_address=self.source_address
            )

            try:
                connection.sendall(dumps(key))
            except socket.timeout as e:
                raise TimeoutError(e)
            except socket.error as e:
                raise TransportError(e)

            return loads(ZabbixProtocol.recv(connection))
        finally:
            if connection:
                connection.close()
