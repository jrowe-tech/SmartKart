import serial.tools.list_ports_windows as ports
import serial


class Driver:
    """
    Arduino Serial Port Driver

    Prompts for user's input to find serial port.
    Automatically takes care of buffer cleaning,
    data filtration, and time scaling.

    int baud: Baud rate of serial port (often 9600 / 115200)

    int buffer: Output buffer size. Buffer automatically
    clears after the max data is reached.
    """
    def __init__(self, baud: int = 115200, buffer: int = 200):
        self.comports = []
        print("\nOPEN COMPORTS:")
        for port in ports.comports():
            self.comports.append(str(port)[:4])
            print(port)

        self.portID = "COM" + input("\nCHOOSE A PORT: COM")
        if self.portID not in self.comports:
            raise AttributeError("Comport Number Not In Detected Comports!")

        self.serial = serial.Serial(timeout=0.0001)
        self.serial.baudrate = baud
        self.serial.port = self.portID
        self.serial.open()
        self.bufferSize = buffer
        self.buffer = 0
        self.maxReadLength = 5

    def sendValue(self, data):
        self.serial.write(data)
        if self.buffer >= self.bufferSize:
            self.serial.flush()
            self.buffer = 0
        self.buffer += 1

    def readValue(self):
        self.serial.flushInput()
        self.serial.flushOutput()
        self.serial.flush()
        return self.serial.read()

    def readLine(self):
        data = self.serial.readline()
        self.serial.flushInput()
        self.serial.flushOutput()
        self.serial.flush()
        return [byte for byte in data if len(data) <= 4 and
                data is not None]

    def startSend(self):
        self.serial.write(0xCC)

    def closePort(self):
        self.serial.flush()
        self.serial.cancel_read()
        self.serial.cancel_write()
        self.serial.close()

