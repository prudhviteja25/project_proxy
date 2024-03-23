import socket
import http.server
import socketserver

def main():
    host = 'localhost'
    port = 8080

    client_s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_s1.connect((host, port))
    #give the desired url here
    http_request = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
    client_s1.send(http_request.encode())

    response = b""
    while True:
        part = client_s1.recv(4096)
        if not part:
            break
        response += part

    client_s1.close()

    # Find the index of the start of the HTML content
    html_index = response.find(b'<html')
    if html_index != -1:
        # Write only the HTML content to temp.html
        html_content = response[html_index:]
        with open('temp.html', 'wb') as f:
            f.write(html_content)
        
        # Start a simple HTTP server to serve the HTML file
        PORT = 8001
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("Serving at port", PORT)
            httpd.serve_forever()
    else:
        print("HTML content not found in response.")

if __name__ == "__main__":
    main()
