import machine
from time import sleep

led = machine.Pin('LED', machine.Pin.OUT)

def toggle_led():
    led = machine.Pin('LED', machine.Pin.OUT)
    led.toggle()

def main():
    while True:
        toggle_led()
        sleep(0.2)
        
if __name__ == "__main__":
    main()
    