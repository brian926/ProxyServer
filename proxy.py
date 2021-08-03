#!/usr/bin/env python
import socket, sys, threading

try:
    listening_port = int(input("[*] Enter Listening Port Number: "))
except KeyboardInterrupt:
    print("\n[*] User Requested An Interrupt")
    print("[*] Application Exiting...")
    sys.exit()

# Max connections
max_conn = 5
# Max Socket buffer size
buffer_size = 8192

def start():
    try:
        # Initiate socket
        print("[*] Initializing Sockets")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind socket for listen
        sock.bind(('', listening_port))
        print("[*] Sockets Binded Successfully")
        # Start listening for incoming connections
        sock.listen(max_conn)
        print("[*] Server Started Successfully [ %d ] \n" % (listening_port))
    except Exception as e:
        print("[*] Unable to Initialize Socket")
        sys.exit(2)

    while 1:
        try:
            # Accept Connection from client browser
            conn, addr = sock.accept()
            # Receive client data
            data = conn.recv(buffer_size)
            # Start new thread
            print("test")
            print("Conn Data: " + str(conn))
            print("Data info: " + str(data))
            print("Addr info: " + str(addr))
            threading.Thread(target=conn_string, args=(conn, data, addr)).start()
        except KeyboardInterrupt:
            sock.clost()
            print("\n[*] Proxy Server Shutting down")
            sys.exit(1)
    
    sock.close()

def conn_string(conn, data, addr):
    # Client Browser request appears here
    try:
        first_line = data.split('\n')[0]

        url = first_line.split('')[1]

        # Find the position of ://
        http_pos = url.find("://")
        if(http_pos==-1):
            temp = url
        else:
            # Get the rest of the URL
            temp = url[(http_pos + 3):]

        # Find the pos of the port
        port_pos = temp.find(":")

        # Find the end of the web server
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        
        # Default port
        if(port_pos==-1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            # Specific port
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        proxy_server(webserver, port, conn, addr, data)
    except Exception as e:
        print("Failed to get browser request")

def proxy_server(webserver, port, conn, data, addr):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((webserver, port))
        sock.send(data)

        while 1:
            # Read reply or data to from end web server
            reply = sock.recv(buffer_size)

            if(len(reply) > 0):
                # Send reply back to client
                conn.send(reply)
                # Send notification to Proxy server
                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                print("[*] Request Done: %s => %s <=" % (str(addr[0]), str(dar)))
            else:
                break
        
        # Closing socket and connection
        sock.close()
        conn.close()

    except OSError as e:
        sock.close()
        conn.close()
        sys.exit(1)

start()