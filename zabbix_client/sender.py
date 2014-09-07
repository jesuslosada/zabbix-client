# -*- coding: utf-8 -*-

import socket
import json
import re
import logging
from .exceptions import (
    TransportError, TimeoutError, ResponseError, InvalidJSONError,
    ZabbixProtocolError
)
from .zabbix_protocol import NETWORK_TIMEOUT, ZabbixProtocolConnection


ZBX_RESPONSE_INFO_RE = (r'processed:? (\d+);? failed:? (\d+);? ' +
                        r'total:? (\d+);? seconds spent:? (\d+(?:\.\d{,6})?)')

logger = logging.getLogger(__name__)


def dumps(values):
    request = {
        'request': 'sender data',
        'data': values
    }
    data = json.dumps(request, separators=(',', ':')).encode('utf-8')

    if logger.isEnabledFor(logging.INFO):
        request_str = json.dumps(request, sort_keys=True)
        logger.info("Request: {0}".format(request_str))

    return data


def loads(response):
    try:
        zabbix_response = json.loads(response.decode('utf-8'))
    except ValueError as e:
        raise InvalidJSONError(e)

    if zabbix_response.get('response', '') != 'success':
        exception_message = 'Sender request failed: {0}'.format(zabbix_response)
        raise ZabbixProtocolError(exception_message, response=zabbix_response)

    if logger.isEnabledFor(logging.INFO):
        response_str = json.dumps(zabbix_response, sort_keys=True)
        logger.info("Response: {0}".format(response_str))

    info = zabbix_response.get('info', '')
    matched = re.match(ZBX_RESPONSE_INFO_RE, info, re.I)
    if not matched:
        raise ResponseError('Could not parse the response')

    return {
        'processed': int(matched.group(1)),
        'failed': int(matched.group(2)),
        'total': int(matched.group(3)),
        'seconds_spent': float(matched.group(4))
    }


class ZabbixSender(object):

    def __init__(self, server, port=10051, timeout=NETWORK_TIMEOUT,
                 source_address=None):
        self.server = server
        self.port = port
        self.timeout = timeout
        if source_address is None:
            self.source_address = source_address
        else:
            self.source_address = (source_address, 0)

    def send(self, values):
        if not values:
            return

        address = (self.server, self.port)
        connection = None
        try:
            connection = ZabbixProtocolConnection(
                address,
                timeout=self.timeout,
                source_address=self.source_address
            )

            try:
                connection.send(dumps(values))
            except socket.timeout as e:
                raise TimeoutError(e)
            except socket.error as e:
                raise TransportError(e)

            return loads(connection.recv())
        finally:
            if connection:
                connection.close()
