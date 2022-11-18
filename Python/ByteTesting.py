from pynput import keyboard

def stringToBytes(data):
    print(bytearray(data.encode('utf-8'))[1])


def ints_to_bytes(x: int, y: int) -> bytes:
    return (x | y).to_bytes(1, 'big')
#SEND BYTE:
# Serial.write(int & 0xFF)
# byte = (throttle(int) | steering(int))
# steering = int('00000000', 2) OR 0
# throttle = int('00000000', 2) OR 0

def main():
    stringToBytes(input("Input String To Bytes:\n"))
    print(ints_to_bytes(int(input("Input INT (0-255) >>> ")), int(input("Input INT (0-255) >>> "))))

class ArduinoDriver:
    def __init__(self):
        # Open Arduino Firmata Firmware Object

        # Setup Keyboard Inputs:
        self.activeKey = None
        self.active = False
        self.connected = False
        self.steeringAngle = 0
        self.maxSteeringAngle = 45
        self.timeStep = 0.05
        self.releaseControls = {"a": lambda: self.AdjustSteering("D"),
                                "key.left": lambda: self.AdjustSteering("D"),
                                "d": lambda: self.AdjustSteering("D"),
                                "key.right": lambda: self.AdjustSteering("D"),
                                "w": lambda: self.AdjustThrottle("A"),
                                "key.up": lambda: self.AdjustThrottle("A"),
                                "s": lambda: self.AdjustThrottle("A"),
                                "key.down": lambda: self.AdjustThrottle("A")}

        self.keyControls = {"key.escape": lambda: self.SetActive(False),
                            "a": lambda: self.AdjustSteering("E"),
                            "key.left": lambda: self.AdjustSteering("E"),
                            "d": lambda: self.AdjustSteering("F"),
                            "key.right": lambda: self.AdjustSteering("F"),
                            "w": lambda: self.AdjustThrottle("B"),
                            "key.up": lambda: self.AdjustThrottle("B"),
                            "s": lambda: self.AdjustThrottle("C"),
                            "key.down": lambda: self.AdjustThrottle("C"),
                            "key.space": lambda: self.SetActive(),
                            "key.enter": lambda: self.SetActive()}

        # Reset Throttle and Steering
        self.throttle = "A"
        self.steering = "A"
        self.readValues = ""

        try:

            listener = keyboard.Listener(on_press=self.key_press, on_release=self.key_release)
            listener.start()
            loops = 0

            print(
                """Arduino Pipeline Successfully Formed!
                \nControls:
                A/D Keys For Steering 
                W/S Keys For Throttling
                Press C To Activate / Deactivate Camera
                Press Escape Or Enter To Terminate
                \nAlternative Keys:
                Left/Right Arrows For Steering
                Up/Down Arrows For Throttling""")

            self.active = False
            while True:
                if self.active:
                    # Write Bound Pins And Commands Here
                    # self.board.sp.write(loops.to_bytes(3, 'big'))
                    # board.digital[13].write(self.keyBind)
                    # print(f"Throttle: {self.throttle}\nSteering:{self.steering}")
                    # value = self.throttle + self.steering
                    value = input("Send String To Arduino >>> ")
                    print(value)
                    self.serialDriver.sendValue(value.encode('utf-8'))
                    # self.readValues = self.serialDriver.readValue()
                    # print(self.readValues)
                    # os.system('cls')
                    loops += 1
                # s(self.timeStep)

        except KeyboardInterrupt:
            print("Interrupted Arduino Stream")
            sys.exit()

    def sendString(self, data):
        msg = bytearray([pyfirmata.pyfirmata.START_SYSEX])
        msg.extend(pyfirmata.util.str_to_two_byte_iter(data))
        msg.append(pyfirmata.pyfirmata.END_SYSEX)
        self.board.sp.write(msg)

    def SetActive(self, state=None):
        self.throttle = "A"
        self.steering = "D"
        if state:
            if self.active == state:
                return
            self.active = state
        else:
            self.active = not self.active

    def AdjustSteering(self, v):
        self.steering = v

    def AdjustThrottle(self, v):

        # Might Apply Smoothing Gradient Depends On How Broken It Is
        self.throttle = v

    def key_press(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.keyControls.keys():
            self.keyControls[finalKey]()

    def key_release(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.releaseControls.keys():
            self.releaseControls[finalKey]()


driver = ArduinoDriver()
