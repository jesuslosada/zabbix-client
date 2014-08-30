# -*- coding: utf-8 -*-

def recv_bytes(sock, nbytes):
    buf = b''
    while len(buf) < nbytes:
        chunk = sock.recv(nbytes - len(buf))
        if not chunk:
            return buf
        buf += chunk
    return buf
