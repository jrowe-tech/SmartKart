Jetson Nano Configuration Files:

User's Name: Jacob Rowe
Computer's Name: SmartyKarty

Pick a username: jacob
Choose a password: qwert123

Vino Password? connect / qwert123

Ipv4 VNC Address: 192.168.0.44
Mackey Address: 172.20.10.5
Jake's Guest Hotspot: 192.168.137.215
smartykartynet (Hotspot / AP): 10.42.0.1

Hardware Information:

USB\VID_0955&PID_7020&REV_0002&MI_02
USB\VID_0955&PID_7020&MI_02

MY HostAPD SSID IP (. __/ .) :

Static IP: 172.30.100.100 (ON ETH0 4 / Emulated IOT)
SSID: smartykarty_ap
PASSWORD: 6969420725

----- Jetson Nano Display Issues !YAY! -----

ATTEMPTED XRANDR FIX:

xrandr

xrandr --output DVI-0 --mode 1920x1080 
OR
xrandr --output HDMI-0 --mode 1920x1080

xrandr -q


ATTEMPTED NANO FIX:

sudo nano /sys/class/graphics/fbX/mode
NOTE: FIND THE GOD DAMN SETTINGS ):


MORE NANO FIXES:

sudo nano /etc/rc.local

EXAMPLE CODE:
#!/bin/bash

cat /sys/class/graphics/fb0/mode > home/jetson/boot.log
sudo echo "D:1920x1080p-60" > /sys/class/graphics/fb0/mode
cat /sys/class/graphics/fb0/mode >> /home/jetson/boot.log


SYSTEM CONTROL FIX:

sudo systemctl enable rc-local
sudo systemctl start rc-local
sudo systemctl status rc-local


GNOME FIX?

gnome-display-properties


FINALLY, REBOOT

sudo reboot now

THE FUCKING COMMAND WAS "startx" BECAUSE OF COURSE IT FUCKING WAS,
NO DOCUMENTATION OR ANYTHING

The command to fix gdm is:
sudo systemctl set-default graphical.target

---------------------------------------------------------------
INSTALL OPENSSH

sudo apt install openssh-server
sudo systemctl status ssh
sudo ufw allow ssh