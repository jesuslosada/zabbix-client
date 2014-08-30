# -*- coding: utf-8 -*-

import socket
import struct
import sys
from .exceptions import TransportError, TimeoutError, ResponseError
from .utils import recv_bytes


# Default network timeout (in seconds)
NETWORK_TIMEOUT = 30

# Maximum response size: 128 MiB
ZBX_MAX_RECV_DATA_SIZE = 128 * 1024 * 1024


class ZabbixProtocol(object):

    ZBX_TCP_HEADER_DATA = b'ZBXD'
    ZBX_TCP_HEADER_VERSION = 1
    ZBX_TCP_HEADER = struct.pack('<4sB', ZBX_TCP_HEADER_DATA,
                                 ZBX_TCP_HEADER_VERSION)

    @staticmethod
    def create_connection(address, timeout=None, source_address=None):
        try:
            if sys.version_info < (2, 7):
                return socket.create_connection(address, timeout=timeout)
            else:
                return socket.create_connection(address, timeout=timeout,
                                                source_address=source_address)
        except socket.timeout as e:
            raise TimeoutError(e)
        except (socket.error, socket.gaierror) as e:
            raise TransportError(e)

    @classmethod
    def send(cls, sock, data):
        data_len = struct.pack('<Q', len(data))
        zabbix_request = cls.ZBX_TCP_HEADER + data_len + data

        try:
            sock.sendall(zabbix_request)
        except socket.timeout as e:
            raise TimeoutError(e)
        except socket.error as e:
            raise TransportError(e)

    @classmethod
    def recv(cls, sock):
        try:
            header = recv_bytes(sock, len(cls.ZBX_TCP_HEADER))
            if not header:
                raise ResponseError('Empty response')
            if header != cls.ZBX_TCP_HEADER:
                raise ResponseError('Wrong header')

            data_len_chunk = recv_bytes(sock, 8)
            if len(data_len_chunk) < 8:
                raise ResponseError('Response is shorter than expected')

            data_len = struct.unpack('<Q', data_len_chunk)[0]
            if ZBX_MAX_RECV_DATA_SIZE < data_len:
                raise ResponseError('Response exceeds the maximum allowed size')

            data = sock.recv(data_len)
            if len(data) < data_len:
                raise ResponseError('Response is shorter than expected')

            return data
        except socket.timeout as e:
            raise TimeoutError(e)
        except socket.error as e:
            raise TransportError(e)
