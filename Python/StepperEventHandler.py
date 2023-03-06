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
        self.speed = 0
        self.timeStep = 0.01
        self.releaseControls = {"a": lambda: self.AdjustDirection("N", "L"),
                                "key.left": lambda: self.AdjustDirection("N", "L"),
                                "d": lambda: self.AdjustDirection("N", "R"),
                                "key.right": lambda: self.AdjustDirection("N", "R"),
                                "w": lambda: self.AdjustSpeed(0, 100),
                                "key.up": lambda: self.AdjustSpeed(0, 100),
                                "s": lambda: self.AdjustSpeed(0, -100),
                                "key.down": lambda: self.AdjustSpeed(0, -100)
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
        self.direction = 0
        self.speed = 0
        self.readValues = ""

        # Start Serial Driver
        self.serialDriver = serialDriver(200)

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
                    #Step 1: Update Spee

                    # Write 2 Bytes To Arduino

                    self.serialDriver.sendValue(self.int2Bytes(int(byteSpeed * 100)))
                    print(f"Int Value: {int.from_bytes(self.serialDriver.readValue(), 'big')}")
                    # self.serialDriver.sendValue(self.direction.encode('utf-8'))
                    os.system('cls')
                    loops += 1
                s(self.timeStep)
        except Exception as e:
            print(f"Exception Occurred: {e}")
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
        self.direction = 0
        self.speed = 0
        if state:
            if self.active == state:
                return
            self.active = state
        else:
            self.active = not self.active

    def AdjustSpeed(self, vOUT, vIN=None):

        # Fix Null-Overriding
        if vIN == self.speed or vIN is None:
            self.speed

    def AdjustDirection(self, vOUT, vIN=None):

        # Might Apply Smoothing Gradient Depends On How Broken It Is
        # #Fix Null-Overriding
        if vIN == self.direction or vIN is None:
            self.direction = vOUT

    def int2Bytes(self, x):
        return (x | 0).to_bytes(1, "big")

    def key_press(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.keyControls.keys():
            self.keyControls[finalKey]()

    def key_release(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.releaseControls.keys():
            self.releaseControls[finalKey]()


driver = ArduinoDriver()
