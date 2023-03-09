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
            "1": lambda: self.adjustSpeed(0),
            "2": lambda: self.adjustSpeed(0),
            "3": lambda: self.adjustSpeed(0),
            "4": lambda: self.adjustSpeed(0),
            "5": lambda: self.adjustSpeed(0)
        }

        self.keyControls = {
            "1": lambda: self.adjustSpeed(20),
            "2": lambda: self.adjustSpeed(40),
            "3": lambda: self.adjustSpeed(60),
            "4": lambda: self.adjustSpeed(80),
            "5": lambda: self.adjustSpeed(100),
            "key.enter": lambda: self.setActive(True),
            "key.escape": lambda: self.setActive(False)
        }

        # Reset Throttle Value
        self.speed = 0
        self.readValues = ""

        # Start Serial Driver
        self.serialDriver = serialDriver(baud=115200, buffer=200)

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
                    # Clamp Speed Value to Int 0-100

                    # Write Speed Int To Arduino
                    print(f"Current Speed: {self.speed}")
                    self.serialDriver.sendValue(self.int2Bytes(20))

                    # os.system('cls')
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
            if finalKey is not None:
                self.keyControls[str(finalKey)]()

    def key_release(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.releaseControls.keys():
            if finalKey is not None:
                self.releaseControls[str(finalKey)]()

    @staticmethod
    def int2Bytes(x):
        return (x | 0).to_bytes(1, "big")


driver = ArduinoDriver()
