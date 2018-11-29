"""
    # TCP_CLient.py

    Author: C1C Joey Lapiana, C2C Christian Sylvester, November 2016

    A demonstration of a typical client using the TCP protocol. A client typically runs
    for a short time. The client must know the host name and process port number that
    it wants to communicate with.
"""

# The socket library allows for the creation and use of the TCP and UDP protocols.
# See https://docs.python.org/3/library/socket.html
import socket
import sys
import webbrowser
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------
def main():
    # Create a new socket to communicate with a remote server
    #   AF_INET means we want an IPv4 protocol
    #   SOCK_STREAM means we want to communicate using a TCP stream
    # The socket is assigned a random port number. Clients typically have random port numbers.
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create a TCP virtual connection to the server. This does the 3-way handshake with the
    # server. The server and the client have now agreed on how they will number the packets
    # so that they can guarantee accurate delivery.
    # The parameter to the connect function is a tuple: (address, port_number)
    server_name = '127.0.0.1'  # localhost
    server_port = 1055
    print('connecting to {} on port {}'.format(server_name, server_port))
    my_socket.connect((server_name, server_port))

    # The size of the TCP receive buffer
    buffer_size = 16

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
        # Close the socket, which releases all of the memory resources the socket used.
        my_socket.close()

    # Delete the socket from memory to again reclaim memory resources.
    del my_socket

# ---------------------------------------------------------------------
if __name__ == '__main__':
    main()
