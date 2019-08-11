import conf as conf


class BaseModule:

    def __init__(self):
        self.catched_command = False
        self.output_buffer = ''

    def getDictFromCommand(self, command: str, separator_key_val='=', separator_fields=';', smart=True) -> dict:
        fields = []
        if separator_fields in command:
            fields = command.split(separator_fields)
        else:
            fields.append(command)

        ret = {}
        for kv in fields:
            if separator_key_val in kv:
                key_val = kv.split(separator_key_val)
                if smart:
                    if key_val[1].isdecimal():
                        key_val[1] = int(key_val[1])
                ret[key_val[0]] = key_val[1]
            else:
                ret[kv] = kv
        return ret

    def tick(self):
        pass

    def getOutputBuffer(self, clear=True) -> str:
        ret = self.output_buffer
        if clear:
            self.output_buffer = ''
        return ret

    def write(self, data: str, overwrite=False):
        if overwrite:
            self.output_buffer = data
        else:
            self.output_buffer += data

    def writeLine(self, data: str, overwrite=False):
        if overwrite:
            self.output_buffer = data + conf.NEW_LINE
        else:
            self.output_buffer += data + conf.NEW_LINE

    def commandCatched(self):
        self.catched_command = True

    def hasCommandBeenCatched(self, reset=False) -> bool:
        catched = self.catched_command
        if reset:
            self.catched_command = False
        return catched

    def command(self, user_command: str):
        pass
