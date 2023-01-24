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
        self.releaseControls = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0
        }

        self.keyControls = {
            "1": 20,
            "2": 40,
            "3": 60,
            "4": 80,
            "5": 100,
            "key.enter": self.setActive(True),
            "key.escape": self.setActive(False)
        }

        # Reset Throttle Value
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
                
                Controls:
                1-5 Keys For Throttling
                Press Escape Or Enter To Terminate
                """
            )

            self.active = False

            while True:

                if self.active:
                    # Write Speed Int To Arduino
                    self.serialDriver.sendValue(self.int2Bytes(self.speed))

                    os.system('cls')
                    loops += 1

                s(self.timeStep)

        except Exception as e:
            print(f"Exception Occurred: {e}")
            print("Interrupted Arduino Stream")

        finally:
            print("EXITING PYTHON APPLICATION")
            sys.exit()

    def setActive(self, state=None):
        self.speed = 0
        if state:
            if self.active == state:
                return
            self.active = state
        else:
            self.active = not self.active

    def adjustSpeed(self, vIN):

        # Fix Null-Overriding
        self.speed = max(min(vIN, 100), 0)

    def key_press(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.keyControls.keys():
            self.keyControls[finalKey]()

    def key_release(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.releaseControls.keys():
            self.releaseControls[finalKey]()

    @staticmethod
    def int2Bytes(x):
        return (x | 0).to_bytes(1, "big")


driver = ArduinoDriver()
