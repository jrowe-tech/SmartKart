import pyfirmata.pyfirmata
import pyfirmata

class Driver:
    def __init__(self):
        self.board = pyfirmata.ArduinoNano('COM' + str(input("INPUT COM NUMBER OF PORT >>> ")))
        self.ports = self.board.digital_ports
        print(self.ports)


    def sendValue(self, data):
        #Send Data In ByteArray If Necessary
        pass

    def digitalWrite(self, pin, value=False):
        try:
            self.board.digital[pin].write(int(value))
        except:
            print("PIN NOT WORKING CORRECTLY")
            return False

driver = Driver()