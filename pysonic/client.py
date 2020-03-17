import socket


class Connection:
    """
    TCP socket wrapper
    """
    def __init__(self, socket):
        self._socket = socket

    @classmethod
    def make_connection(cls, ip, port):
        s = socket.socket.connect((ip, port))
        return cls(s)


class Pool:
    """
    Pool to manage number of connections
    """
    def __init__(self, ip, port, size=10):
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

    def __init__(self, host: str = '127.0.0.1', port: int = 1491):
        self.host = host
        self.port = port

        self._pool = Pool()

    def ping(self):
        return self._pool.get_connection().send(b'PING')
