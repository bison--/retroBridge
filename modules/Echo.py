import modules.BaseModule


class Echo(modules.BaseModule.BaseModule):

    def __init__(self):
        super().__init__()

    def command(self, user_command):
        if user_command:
            self.write('ECHO: ' + user_command + "\n")
