import serial_driver as driver
from time import sleep as s

# We do a little threading
from threading import Thread


# DO NOT SEND 127 OR 255 STEPS

class Pipe:
    def __init__(self):
        self.port = driver.Driver(115200, 200)

        try:
            s(2)
            self.writeSerial(0.01)
            self.readingThread = Thread(target=self.readSerial, args=[0.01], daemon=True)
            self.readingThread.start()

        except KeyboardInterrupt:
            print("Interrupting Arduino Stream")
        except Exception as e:
            print(f"Other Exception Occurred: {e}")
        finally:
            # Send Custom Character Codes For Debugging
            # self.port.sendValue(self.processInt(127))
            # self.port.sendValue(self.processInt(0))
            # self.port.closePort()
            pass

        cw = True
        s(5)

    def processInt(self, x: int) -> bytes:
        return x.to_bytes(1, "big")

    def compileSpeedByte(self, rSpeed: int, cw: bool):
        speedByte = 0
        if cw:
            speedByte |= 128

        speedByte |= max(min(100, abs(rSpeed)), 0)

        return speedByte

    def readSerial(self, tick: float):
        while True:
            newData = self.port.readLine()
            if len(newData) > 0:
                data = newData
                print(f"New Data Received: {data}")
            s(tick)

    def writeSerial(self, tick: float):
        cw = True
        while True:
            speedInt = self.compileSpeedByte(50, True)

            steps = 1

            self.port.sendValue(self.processInt(speedInt))
            self.port.sendValue(self.processInt(steps))

            data = self.port.readLine()

            if len(data) > 3:
                print(f"Read Data: {data}")
                print(f"Limit Switch State: {chr(data[0])}")
                currentSteps = (data[1] << 16) + (data[2] << 8) + data[3]
                print(f"Current Arduino Step Count: {currentSteps}")

            s(0.2)


pipe = Pipe()
