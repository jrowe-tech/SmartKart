from serial_driver import Driver as serialDriver
import pyfirmata
import sys, pygame
import os
from time import sleep as s
from pynput import keyboard


class ArduinoDriver:
    def __init__(self):
        # Open Arduino Firmata Firmware Object

        # self.board = Arduino('COM6')


        # Setup Keyboard Inputs:
        self.activeKey = None
        self.active = False
        self.connected = False
        self.steeringAngle = 0
        self.maxSteeringAngle = 45
        self.timeStep = 0.001
        self.releaseControls = {"a": lambda: self.AdjustSteering("D", "E"),
                                "key.left": lambda: self.AdjustSteering("D", "E"),
                                "d": lambda: self.AdjustSteering("D", "F"),
                                "key.right": lambda: self.AdjustSteering("D", "F"),
                                "w": lambda: self.AdjustThrottle("A", "B"),
                                "key.up": lambda: self.AdjustThrottle("A", "B"),
                                "s": lambda: self.AdjustThrottle("A", "C"),
                                "key.down": lambda: self.AdjustThrottle("A", "C")}

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
                    # Write Bound Pins And Commands Here
                    # self.board.sp.write(loops.to_bytes(3, 'big'))
                    # board.digital[13].write(self.keyBind)
                    # print(f"Throttle: {self.throttle}\nSteering:{self.steering}")
                    # print(f"Throttle: {self.throttle}\nSteering:{self.steering}")
                    self.serialDriver.sendValue(self.steering.encode('utf-8'))
                    self.serialDriver.sendValue(self.throttle.encode('utf-8'))
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
        self.throttle = "A"
        self.steering = "D"
        if state:
            if self.active == state:
                return
            self.active = state
        else:
            self.active = not self.active

    def AdjustSteering(self, vOUT, vIN=None):
        #Fix Null-Overriding
        if vIN == self.steering or vIN is None:
            self.steering = vOUT

    def AdjustThrottle(self, vOUT, vIN=None):

        # Might Apply Smoothing Gradient Depends On How Broken It Is
        # #Fix Null-Overriding
        if vIN == self.throttle or vIN is None:
            self.throttle = vOUT

    def key_press(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.keyControls.keys():
            self.keyControls[finalKey]()

    def key_release(self, key):
        finalKey = str(key).replace("'", "").lower()
        if finalKey in self.releaseControls.keys():
            self.releaseControls[finalKey]()


driver = ArduinoDriver()
