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

    # Three way handshake
    server_name = socket.gethostbyname(sys.argv[0])  # Gets the address of the url
    server_port = 80
    print('connecting to {} at {} on port {}'.format(sys.argv[0], server_name, server_port))
    my_socket.connect((server_name, server_port))

    # The size of the TCP receive buffer
    buffer_size = 1024

    try:
        # Send the server a message.
        # The first parameter is a byte array. The prefix b' makes the string a byte array. Note that
        # TCP might break the message into smaller packets before it sends the data to the server.
        message = b'This is a long request to show how streaming works! It is only a test!'
        print('sending "' + str(message) + '" to the server.')
        my_socket.sendall(message)

        # Wait for the response from the server. Because the server might send the
        # response in multiple packets, we need to potentially call recv multiple times.
        # Note that recv function blocks until there is data in the TCP receive buffer.
        amount_received = 0

        # This is based on the fact that the server is going to echo the message back to the
        # client. In a more normal case, you would read the input buffer until you found a
        # special character that was recognized as the "end of message" character. OR,
        # the server would include in its response the size of the message that is coming.
        amount_expected = len(message)
        total_response = ""

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
