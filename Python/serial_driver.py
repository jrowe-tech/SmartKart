import serial.tools.list_ports_windows as ports
import serial

class Driver:
    def __init__(self, buffer):
        self.comports = []
        print("\nOPEN COMPORTS:")
        for port in ports.comports():
            self.comports.append(str(port)[:4])
            print(port)

        self.portID = "COM" + input("\nCHOOSE A PORT: COM")
        if self.portID not in self.comports:
            raise AttributeError

        self.serial = serial.Serial(timeout=0.01)
        self.serial.baudrate = 115200
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
        return self.serial.read()

    def readLine(self):
        self.serial.flushInput()
        self.serial.flushOutput()
        return [byte for byte in self.serial.readline() if
                len(self.serial.readline()) < self.maxReadLength]

    def startSend(self):
        self.serial.write(0xCC)

if __name__ == "main":
    driver = Driver()

