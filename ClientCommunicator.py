import conf as conf
import modules_active as mods


class ClientCommunicator:
    def __init__(self, selector, client_id):
        self.is_connected = True
        self.client_id = client_id
        self.selector = selector
        self.input_cache = ''
        self.output_cache = ''
        self.command_separator = conf.COMMAND_SEPARATOR

    def addDataToSend(self, data):
        self.output_cache += data

    def receive(self, key, mask):
        sock = key.fileobj
        data = key.data
        recv_data = sock.recv(1024)  # Should be ready to read
        #print('recv_data', recv_data)
        if recv_data:
            #data.outb += recv_data
            self.input_cache += recv_data.decode("utf-8")
            #print('input_cache', self.input_cache)
        else:
            self.disconnect(sock, data)

    def hasDataToSend(self):
        return self.output_cache != ''

    def hasParseableCommand(self):
        return self.command_separator in self.input_cache

    def getFirstCommand(self):
        parts = self.input_cache.split(self.command_separator)
        first_part = parts[0]
        self.input_cache = self.command_separator.join(parts[1:])
        return first_part

    def send(self, key, mask):
        sock = key.fileobj
        data = key.data

        if self.hasParseableCommand():
            #print('CACHE', self.input_cache)
            command = self.getFirstCommand()
            if command == 'quit':
                self.disconnect(sock, data)
                return
            else:
                #print('command', repr(command), 'from', data.addr)
                self.execModulesCommands(command)

        self.execModulesTick()

        if self.hasDataToSend():
            to_send = bytearray(self.output_cache, 'utf-8')
            while len(to_send) > 0:
                #sent = sock.sendall(to_send)  # Should be ready to write
                sent = sock.send(to_send)
                to_send = to_send[sent:]
                #print('send', sent)
            self.output_cache = ''

    def execModulesCommands(self, command):
        for module in mods.MODULES:
            try:
                module.command(command)
                if module.hasCommandBeenCatched(True):
                    #print(module, 'CATCHED', command)
                    break
            except Exception as ex:
                print('execModulesCommands', command, ex)
                if conf.USER_ERROR_MESSAGE:
                    self.addDataToSend(conf.USER_ERROR_MESSAGE)

    def execModulesTick(self):
        for module in mods.MODULES:
            try:
                module.tick()
                self.addDataToSend(module.getOutputBuffer())
            except Exception as ex:
                print('execModulesTick', ex)
                if conf.USER_ERROR_MESSAGE:
                    self.addDataToSend(conf.USER_ERROR_MESSAGE)

    def disconnect(self, sock, data):
        self.is_connected = False
        print('closing connection to', data.addr)
        self.selector.unregister(sock)
        sock.close()
        self.is_connected = False