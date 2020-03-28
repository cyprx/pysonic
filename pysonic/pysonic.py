from __future__ import annotations

import socket
import logging
from enum import Enum
from typing import List


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pysonic')


class Command(Enum):
    START = 'START'


class Mode(str, Enum):
    SEARCH = 'search'
    INGEST = 'ingest'


class Connection:
    """
    TCP socket wrapper
    """
    def __init__(self, socket):
        self._socket = socket
        self._reader = self._socket.makefile('rb', 0)
        self._writer = self._socket.makefile('wb', 0)

    @classmethod
    def make_connection(cls, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.settimeout(10)
        s.connect((ip, port))
        buf = s.recv(1024)
        if b'CONNECTED' in buf:
            print("Connected.")
            return cls(s)

    @property
    def reader(self):
        return self._reader

    @property
    def writer(self):
        return self._writer

    def close(self):
        return self._socket.close()


class Pool:
    """
    Pool to manage socket connections
    """
    def __init__(self, ip, port, size=1):
        self.size = size

        self.conn_in_used = set()
        self.pool = []
        for i in range(size):
            conn = Connection.make_connection(ip, port)
            self.pool.append(conn)

    def get_connection(self):
        for conn in self.pool:
            if conn not in self.conn_in_used:
                self.conn_in_used.add(conn)
                return conn


class Client:
    """
    API to communicate with Sonic db
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 1491, password: str = 'SecretPassword'):
        self.host = host
        self.port = port
        self.password = password

        self.conn = None
        self._pool = Pool(host, port)

    def __enter__(self):
        self.conn = self._pool.get_connection()

    def __exit__(self, *args):
        self.conn.close()

    def ping(self):
        self.conn.writer.write(b'PING')
        return self.conn.reader.readline()

    def mode(self, mode: Mode):
        """

        TODO: read buffer value to breakdown command
        """
        self.conn.writer.write(bytes(f'START {mode} {self.password}\n', 'utf-8'))
        while True:
            line = self.conn.reader.readline()
            if b'STARTED search' in line:
                return b'CONNECTED'

    def query(self, collection: str, bucket: str, terms: str, limit=10, offset=0):
        cmd = bytes(f'QUERY {collection} {bucket} "{terms}"\n', 'utf-8')
        self.conn.writer.write(cmd)
        event_id = None
        while True:
            line = self.conn.reader.readline()
            if b'PENDING' in line:
                event_id = self._parse_event_id(line)
                print(f'Waiting for event {event_id}')
            elif event_id and event_id in line:
                return self._parse_query_results(line)

    @staticmethod
    def _parse_event_id(line: bytes):
        id_ = line.split(b' ')[1]
        return id_.replace(b'\n', b'').replace(b'\r', b'')


    @staticmethod
    def _parse_query_results(line: bytes) -> List[str]:
        parts = line.replace(b'\n', b'').replace(b'\r', b'').split(b' ')
        bucket = parts[3]
        results = parts[4:]
        return [r.decode('utf-8') for r in results]
