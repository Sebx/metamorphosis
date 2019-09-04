import os
import threading
import webbrowser
from http.server import CGIHTTPRequestHandler, HTTPServer


def start_server(path, port=8000):
    """Start a simple webserver serving path on port"""
    os.chdir(path)
    httpd = HTTPServer(("", port), CGIHTTPRequestHandler)
    httpd.serve_forever()


# Start the server in a new thread
port = 8000

daemon = threading.Thread(name="daemon_server",
                          target=start_server,
                          args=(".", port))

# Set as a daemon so it will be killed once the main thread is dead.
daemon.setDaemon(True)
daemon.start()

# Open the web browser
webbrowser.open("http://localhost:{}".format(port))
