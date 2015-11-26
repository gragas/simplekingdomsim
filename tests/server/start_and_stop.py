import sys
sys.path[0] = sys.path[0][:-12]
import os
import socket
import time
import threading
import tornado.ioloop
import tornado.iostream
import tornado.tcpclient
import tornado.tcpserver
import server

def main():
    print("Server start and stop tests...")
    s = "TEST 1..."
    try:
        IP, port = "localhost", 8888
        def server_thread_func():
            test_server = server.Server()
            test_server.bind(8888)
            test_server.start(1)
            tornado.ioloop.IOLoop.current().start()
        server_thread = threading.Thread(target=server_thread_func)
        server_thread.start()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stream = tornado.iostream.IOStream(client)
    except Exception as e:
        print("ERROR: Could not initialize TEST 1!\n")
        raise e
    try:
        def on_connect():
            stream.write(bytes("exit\n", "UTF-8"))
            stream.read_until(bytes("\n", "UTF-8"))
        stream.connect((IP, port), on_connect)
    except Exception as e:
        s += "FAILED!"
        raise e
    else:
        s += "PASSED"
    server_thread.join()
    print(s + "\n")
    s = "TEST 2..."
    try:
        IP, port = "localhost", 8888
        def server_thread_func():
            test_server = server.Server()
            test_server.bind(8888)
            test_server.start(1)
            tornado.ioloop.IOLoop.current().start()
        server_thread = threading.Thread(target=server_thread_func)
        server_thread.start()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stream = tornado.iostream.IOStream(client)
    except Exception as e:
        print("ERROR: Could not initialize TEST 1!\n")
        raise e
    try:
        def on_connect():
            stream.write(bytes("register tom\n", "UTF-8"))
            def on_read(data):
                data = str(data)[2:-3]
                if data == "registered":
                    print("Successfully registered with server...")
                    stream.write(bytes("exit\n", "UTF-8"))
            stream.read_until(bytes("\n", "UTF-8"), on_read)
        stream.connect((IP, port), on_connect)
    except Exception as e:
        s += "FAILED!"
        raise e
    else:
        s += "PASSED"
    server_thread.join()
    print(s + "\n")


if __name__ == "__main__":
    main()
