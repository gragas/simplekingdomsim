import tornado.ioloop
import tornado.iostream
import tornado.tcpserver

class Connection:
    def __init__(self, stream, address, server):
        self.server = server
        self.stream = stream
        self.address = self.IP, self.port = address
        self.stream.set_close_callback(self._on_close)
        self.stream.read_until(bytes("\n", "UTF-8"), self._on_read)

    def _on_read(self, data):
        data = str(data)[2:-3]
        print("Received \"{}\" from {}:{}".format(data, self.IP, str(self.port)))
        elems = data.split(" ")
        if data == "exit":
            self.server.stop()
            tornado.ioloop.IOLoop.current().stop()
        elif len(elems) > 1 and elems[0] == "register":
            self.name = " ".join(elems[1:])
            self.stream.write(bytes("registered\n", "UTF-8"), self._on_write)

    def _on_write(self):
        if not self.stream.reading():
            self.stream.read_until(bytes("\n", "UTF-8"), self._on_read)

    def _on_close(self):
        del self.server.connections[self.address]
        for key in self.server.connections.keys():
            connection = self.server.connections[key]
            connection.stream.write(bytes("end {}".format(self.address), "UTF-8"))

class Server(tornado.tcpserver.TCPServer):
    def __init__(self):
        tornado.tcpserver.TCPServer.__init__(self)
        self.connections = dict()

    def handle_stream(self, stream, address):
        self.connections[address] = Connection(stream, address, self)
