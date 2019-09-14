import selectors
import socket
import types
import conf as conf
import ClientCommunicator


def address_to_id(addr):
    return '{0}:{1}'.format(addr[0], addr[1])


def accept_wrapper(selector, sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    _data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    _events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn, _events, data=_data)
    return address_to_id(addr)


SELECTOR = selectors.DefaultSelector()
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((conf.HOST, conf.PORT))
lsock.listen()
print('listening on', (conf.HOST, conf.PORT))
lsock.setblocking(False)
SELECTOR.register(lsock, selectors.EVENT_READ, data=None)

clients = {}

while True:
    events = SELECTOR.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            client_id = accept_wrapper(SELECTOR, key.fileobj)
            clients[client_id] = ClientCommunicator.ClientCommunicator(SELECTOR, client_id)
            clients[client_id].addDataToSend('WELCOME')
            # exec a module on connect
            # clients[client_id].execModulesCommands("url=https://wiki.chaosdorf.de")
        else:
            #sock = key.fileobj
            data = key.data
            client_id = address_to_id(data.addr)

            if clients[client_id].is_connected and mask & selectors.EVENT_READ:
                clients[client_id].receive(key, mask)

            if clients[client_id].is_connected and mask & selectors.EVENT_WRITE:
                clients[client_id].send(key, mask)

            if not clients[client_id].is_connected:
                del clients[client_id]
