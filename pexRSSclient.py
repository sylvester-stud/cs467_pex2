"""
    # TCP_CLient.py

    Author: C1C Joey Lapiana, C2C Christian Sylvester, November 2016

    The client for the RSS feed for the pex.

    Documentation: None
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

    try:
        host_url = urlparse(sys.argv[1])
    except ValueError:
        print("Invalid URL supplied.  Cannot parse URL.")
        exit(1)

    try:
        # Three way handshake
        server_name = socket.gethostbyname(host_url[1])  # Gets the address of the url
        server_port = 80
        print('connecting to {} at {} on port {}'.format(sys.argv[1], server_name, server_port))
        my_socket.connect((server_name, server_port))
        my_socket.settimeout(10)
    except OSError:
        print("Really bad URL.  Try again.")
        exit(1)

    # The size of the TCP receive buffer
    buffer_size = 1024

    try:
        http_req = "GET {} HTTP/1.1\r\nHOST: {} \r\nUser-Agent: {}\r\n\r\n".format(host_url[2],
                                                                                   host_url[1],
                                                                                   webbrowser.WindowsDefault())
        my_socket.sendall(bytes(http_req, 'UTF-8'))

        try:
            response_over = False
            xml_text = ""
            while not response_over:
                response = my_socket.recv(buffer_size)
                xml_text += response.decode('UTF-8', 'replace')
                if "</rss>" in xml_text:
                    response_over = True
        except socket.timeout:
            print("Socket timed out.  Check site and debugging")

        parsed_data = parse_xml(xml_text)
        choice = ""
        while choice != 'quit':
            i = 1
            for article in parsed_data:
                print(i, article[0], article[1])
                i += 1
            choice = input("""Select an article number to read.  Enter "quit" to exit. """)
            if choice.isdigit():
                if int(choice) <= i and parsed_data[int(choice) - 1][0] != "Error Value.":
                    get_article(parsed_data[int(choice) - 1][1], my_socket)

    finally:
        my_socket.close()

    del my_socket


def get_article(url, my_socket):
    # Grab html from url
    page_url = urlparse(url)
    http_req = "GET {} HTTP/1.1\r\nHOST: {} \r\nUser-Agent: {}\r\n\r\n".format(page_url[2],
                                                                               page_url[1],
                                                                               webbrowser.Chrome())
    my_socket.sendall(bytes(http_req, 'UTF-8'))

    try:
        response_over = False
        html_text = ""
        while not response_over:
            response = my_socket.recv(1024)
            html_text += response.decode('UTF-8', 'replace')
            if "</html>" in html_text:
                response_over = True
    except socket.timeout:
        print("Socket timed out.  Check site and debugging")

    if html_text.find("<HTML>") > 0:
        web_page = html_text[html_text.find("<HTML>"):html_text.find("</HTML>")]
    else:
        web_page = "File is not html"

    # Save page to file
    filename = os.path.dirname(os.path.abspath(__file__)) + "/temp.html"
    print("Saving web page to ... -->", filename)
    with open(filename, 'w') as f:
        f.write(remove_non_ascii_characters(web_page))

    # Open the file
    print("Opening the web page in a browser")
    webbrowser.open_new('file:://' + filename)


def remove_non_ascii_characters(text):
    new_text = ''
    for c in text:
        if ord(c) <= 127:
            new_text += c

    return new_text


def parse_xml(text):
    """ Parse a HTML/XML data string that is a typical RSS feed into
        information about individual article
    :param text: A HTML/XML data string
    :return: A list of articles. Each article is a (title, link) tuple
    """
    soup = BeautifulSoup(text, "html.parser")
    articles = []

    for oneItem in soup.findAll('item'):
        try:
            title = oneItem.find('title').text
            link = oneItem.find('guid').text
        except AttributeError:
            title = "Error Value."
            link = "Title or Link not found."
        articles.append((title, link))

    return articles


if __name__ == '__main__':
    main()
