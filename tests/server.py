import os
import socketserver
import sys
from http.server import SimpleHTTPRequestHandler


class MockServer:
    def __init__(self) -> None:
        SimpleHTTPRequestHandler.extensions_map = {
            k: f"{v};charset=UTF-8" for k, v in SimpleHTTPRequestHandler.extensions_map.items()
        }
        self.httpd = socketserver.TCPServer(("", 4000), SimpleHTTPRequestHandler)

    def run(self, directory=None):
        if directory is None:
            directory = sys.argv[1] if len(sys.argv) > 1 else "html"
        os.chdir(directory)
        print("Mock server running at port 4000")
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()


if __name__ == "__main__":
    mock = MockServer()
    try:
        mock.run()
    except (SystemError, SystemExit, KeyboardInterrupt):
        mock.stop()
