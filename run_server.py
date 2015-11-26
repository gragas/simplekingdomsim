import sys
from server import Server

def main(port):
    server = Server(port)

if __name__ == "__main__":
    args = sys.argv
    port = 8000
    if len(args) == 2:
        port = args[1]
    main(port)
