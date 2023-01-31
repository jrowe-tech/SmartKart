import network


def test_wireless():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    scan = wlan.scan()

    if scan:
        print(f"Wireless chip is working successfully and is detecting: \n{scan}")
    else:
        print("Wireless chip is not working successfully! Check connectivity!")
    

def grab_configurations():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    print(f"Channel: {wlan.config('channel')}")
    print(f"ESSID: {wlan.config('essid')}")
    print(f"TXPower: {wlan.config('txpower')}")
    

if __name__ == "__main__":
    grab_configurations()
    