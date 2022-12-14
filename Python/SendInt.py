# //------------------------------------------------//
# Pyserial Ping File -> Send Int, Receive Int

from serial_driver import Driver as serial
from time import sleep as s

tick = 0.01
sendInt = 255
port = serial(10)
while True:
    port.sendValue(sendInt.to_bytes(1, "big"))
    print(f"Value Sent To Arduino: {sendInt}\n "
          f"Values Received From Arduino: {port.readLine()}")
    s(tick)
