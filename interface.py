
class BaseInterface(object):
    def connect(self):
        raise NotImplementedError()

    def readline(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


class ArduinoInterface(BaseInterface):
    def __init__(self, port):
        self._port = port

    def connect(self):
        self._connection = serial.Serial(self._port)  # open serial port

    def readline(self):
        return self._connection.readline()

    def close(self):
        self._connection.close()


class FileInterface(BaseInterface):
    def __init__(self, path):
        self._filepath = path
    
    def connect(self):
        self._fh = open(self._filepath, 'rb')

    def readline(self):
        return self._fh.readline()

    def close(self):
        self._fh.close()
