import serial_driver as driver
from time import sleep as s

port = driver.Driver(200)

while True:
    rotationSpeed = int(input("Insert Rotation Speed For 1 Rotation Here (1-100) >>> "))
    speedByte = 0

    #Steps 0 - 255 Steps
    steps = abs(int(input("Insert Amount of Steps To Step (1-256) >>> ")))

    # Assign Negative Speed Identifier
    if abs(rotationSpeed) == rotationSpeed:
        speedByte |= 128
    speedByte |= abs(rotationSpeed)
    print(f"Speed Value Sent: {speedByte}")
    for _ in range(100):
        port.sendValue(100)
    port.sendValue(speedByte)
    port.sendValue(steps)

    data = port.readLine()
    print(f"Read Data: {data}")
    if len(data) > 20:
        print(f"Limit Switch State: {chr(data[0])}")
        currentSteps = (data[1] << 16) + (data[2] << 8) + data[3]
        print(f"Current Arduino Step Count: {currentSteps}")
    s(0.01)
