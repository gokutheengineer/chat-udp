import argparse, socket

MAX_SIZE_BYTES_UDP = 65535

def server(port):
    # Create a socket object for UDP connection with IPv4 addressing
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = '127.0.0.1'
    s.bind((hostname, port))
    print('Server is listening on port {}'.format(s.getsockname()))
    while True:
        # Receive data from client
        data, clientAddress = s.recvfrom(MAX_SIZE_BYTES_UDP)
        messageUpperCase = data.decode('ascii').upper()
        print('The client at {} says {!r}'.format(clientAddress, messageUpperCase))
        data = messageUpperCase.encode('ascii')
        # Send data to client
        s.sendto(data, clientAddress)
        
def server_chat(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = '127.0.0.1'
    s.bind((hostname, port))
    print('Server is listening on port {}'.format(s.getsockname()))
    while True:
        # Receive data from client
        data, clientAddress = s.recvfrom(MAX_SIZE_BYTES_UDP)
        message = data.decode('ascii')
        print('The client at {} says {!r}'.format(clientAddress, message))
        msg_to_client = input('input your message in lowercase to client: ')
        data = msg_to_client.encode('ascii')
        s.sendto(data, clientAddress)
        
def client_multi(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hosts = []
    while True:
        host = input('input host address: ')
        if host == 'q':
            break
        hosts.append((host, port))
        message = input('input your message in lowercase: ')
        data = message.encode('ascii')
        s.sendto(data, (host, port))
        print('The OS assigned the address {} to me'.format(s.getsockname())) 
        data, address = s.recvfrom(MAX_SIZE_BYTES_UDP)
        reply = data.decode('ascii')
        if address in hosts:
                print('The server {} replied with {!r}'.format(address, reply))
                hosts.remove(address)
        else:
            print('Message {!r} from unexpected host {!r}'.format(reply, address))
 
 
def client_chat(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = '127.0.0.1'
    while True:
        s.connect((host, port))
        print('The OS assigned the address {} to me'.format(s.getsockname())) 
        message = input('input your message in lowercase: ')
        data = message.encode('ascii')
        s.send(data)
        data = s.recv(MAX_SIZE_BYTES_UDP)
        reply = data.decode('ascii')
        print('The server replied with {!r}'.format(reply))
    
    
if __name__ == '__main__':
    funcs = {'client': client_chat, 'server': server_chat}
    parser = argparse.ArgumentParser(description='UDP client and server')
    parser.add_argument('functions', choices=funcs, help='client or server')
    parser.add_argument('-p', metavar='PORT', type=int, default=3000, help='UDP port (default 3000)')
    args = parser.parse_args()
    function = funcs[args.functions]
    function(args.p)