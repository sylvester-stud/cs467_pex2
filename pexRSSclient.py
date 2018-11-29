"""
    # TCP_CLient.py

    Author: C1C Joey Lapiana, C2C Christian Sylvester, November 2016

    The client for the RSS feed for the pex.
"""

import socket
import sys
import webbrowser
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------
def main():
    # Implement an IPv4 socket over TCP
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(sys.argv[1])

    host_url = urlparse(sys.argv[1])

    # Three way handshake
    server_name = socket.gethostbyname(host_url[1])  # Gets the address of the url
    server_port = 80
    print('connecting to {} at {} on port {}'.format(sys.argv[1], server_name, server_port))
    my_socket.connect((server_name, server_port))

    # The size of the TCP receive buffer
    buffer_size = 1024

    try:
        http_req = "get {} HTTP/1.0\r\nHOST: {} \r\n\r\n".format(host_url[2], host_url[1])

        while amount_received < amount_expected:
            response = my_socket.recv(buffer_size)
            print("Server response: ", response)
            amount_received += len(response)
            # build response from multiple packets
            total_response += response.decode('utf-8', 'replace')

        print("The total response from the server was:\n" + total_response)

    finally:
        my_socket.close()

    del my_socket

# ---------------------------------------------------------------------
if __name__ == '__main__':
    main()
