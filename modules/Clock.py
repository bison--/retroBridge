import modules.BaseModule
import time


class Clock(modules.BaseModule.BaseModule):

    def __init__(self):
        super().__init__()
        self.is_active = False
        self.tick_time = 1
        self.last_tick_time = 0
        self.start_time = time.time()

    def getRuntime(self) -> str:
        return str(time.time() - self.start_time)

    def tick(self):
        if not self.is_active:
            return

        if time.time() >= self.last_tick_time + self.tick_time:
            self.last_tick_time = time.time()
            self.writeLine(self.getRuntime())

    def command(self, user_command):
        commands = self.getDictFromCommand(user_command)
        #print(commands)
        if user_command == 'clock_reset':
            self.commandCatched()
            self.start_time = time.time()

        elif 'clock_help' in commands:
            self.commandCatched()
            self.writeLine('')
            self.writeLine('##################')
            self.writeLine('# CLOCK COMMANDS #')
            self.writeLine('##################')
            self.writeLine('')
            self.writeLine('clock_reset')
            self.writeLine('clock_time')
            self.writeLine('clock_runtime')
            self.writeLine('clock_active=1 / clock_active=0')

        elif 'clock_time' in commands:
            self.commandCatched()
            self.writeLine(str(time.time()))

        elif 'clock_runtime' in commands:
            self.commandCatched()
            self.writeLine(self.getRuntime())

        elif 'clock_active' in commands:
            self.commandCatched()
            self.is_active = bool(commands['clock_active'])
