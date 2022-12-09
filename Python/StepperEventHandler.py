from serial_driver import Driver as serialDriver
import pyfirmata
import sys
import os
from time import sleep as s
from pynput import keyboard


class ArduinoDriver:
    def __init__(self):

        # Setup Keyboard Inputs:
        self.activeKey = None
        self.active = False
        self.speed = 0.00000
        self.maxSteeringAngle = 45
        self.deltaSpeed = 0.0500
        self.timeStep = 0.0
        self.releaseControls = {"a": lambda: self.AdjustDirection("N", "L"),
                                "key.left": lambda: self.AdjustDirection("N", "L"),
                                "d": lambda: self.AdjustDirection("N", "R"),
                                "key.right": lambda: self.AdjustDirection("N", "R"),
                                # "w": lambda: self.AdjustSpeed("A", "B"),
                                # "key.up": lambda: self.AdjustSpeed("A", "B"),
                                # "s": lambda: self.AdjustSpeed("A", "C"),
                                # "key.down": lambda: self.AdjustSpeed("A", "C")
                                }

        self.keyControls = {"key.escape": lambda: self.SetActive(False),
                            "a": lambda: self.AdjustDirection("L"),
                            "key.left": lambda: self.AdjustDirection("L"),
                            "d": lambda: self.AdjustDirection("R"),
                            "key.right": lambda: self.AdjustDirection("R"),
                            "w": lambda: self.AdjustSpeed(self.deltaSpeed),
                            "key.up": lambda: self.AdjustSpeed(self.deltaSpeed),
                            "s": lambda: self.AdjustSpeed(-self.deltaSpeed),
                            "key.down": lambda: self.AdjustSpeed(-self.deltaSpeed),
                            "key.space": lambda: self.SetActive(),
                            "key.enter": lambda: self.SetActive()}

        # Reset Throttle and Steering
        self.direction = "N"
        self.speed = 0.000000
        self.readValues = ""

        # Start Serial Driver
        # self.serialDriver = serialDriver(200)

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
                    # print(f"Throttle: {self.direction}\nSteering:{self.speed}")
                    # print(f"Throttle: {self.direction}\nSteering:{self.speed}")
                    print(f"Debug Speed: {self.speed}\nDebug Direction: {self.direction}")
                    # self.serialDriver.sendValue(self.direction.encode('utf-8'))
                    # self.serialDriver.sendValue(self.direction.encode('utf-8'))
                    # os.system('cls')
                    loops += 1
                s(self.timeStep)
        except KeyboardInterrupt:
            print("Interrupted Arduino Stream")
        finally:
            print("EXITING PYTHON APPLICATION")
            sys.exit()

    def sendString(self, data):
        msg = bytearray([pyfirmata.pyfirmata.START_SYSEX])
        msg.extend(pyfirmata.util.str_to_two_byte_iter(data))
        msg.append(pyfirmata.pyfirmata.END_SYSEX)
        self.board.sp.write(msg)

    def SetActive(self, state=None):
        self.direction = "N"
        self.speed = 0.00000000
        if state:
            if self.active == state:
                return
            self.active = state
        else:
            self.active = not self.active

    def AdjustSpeed(self, vOUT, vIN=None):

        # Fix Null-Overriding
        if vIN == self.speed or vIN is None:
            self.speed = max(0.0000, min(self.speed + vOUT, 1.0000))

    def AdjustDirection(self, vOUT, vIN=None):

        # Might Apply Smoothing Gradient Depends On How Broken It Is
        # #Fix Null-Overriding
        if vIN == self.direction or vIN is None:
            self.direction = vOUT

    def key_press(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.keyControls.keys():
            self.keyControls[finalKey]()

    def key_release(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.releaseControls.keys():
            self.releaseControls[finalKey]()


driver = ArduinoDriver()
