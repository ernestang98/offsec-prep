## Disclaimer:

All information and software available on this site are for educational purposes only. Use these at your own discretion, the site owners cannot be held responsible for any damages caused. The views expressed on this site are our own and do not necessarily reflect those of our employers.

Usage of all tools on this site for attacking targets without prior mutual consent is illegal. It is the end user’s responsibility to obey all applicable local, state and federal laws. We assume no liability and are not responsible for any misuse or damage caused by this site.

<!-- https://securityonline.info/disclaimer/ -->

## Additional Software to Install

- GoPass (Credential Management)

	- [Cheatsheet](https://woile.github.io/gopass-cheat-sheet/)

- Terminator

- Kali driver for wireless adapter (depending on your model)

	- [USB Wireless Adapter recognized by `lsusb` but not by `ifconfig` on Linux](https://superuser.com/questions/1279881/usb-wireless-adapter-recognized-by-lsusb-but-not-by-ifconfig-on-linux)
	
		- [rtl8812au driver](https://github.com/aircrack-ng/rtl8812au)
		
			- This one worked for me
			
			- Make sure to restart NetworkManager service and debug using lsusb
		
	- [USB Wifi Adapter connected to Kali Vbox but absent in ifconfig](https://superuser.com/questions/1570548/usb-wifi-adapter-connected-to-kali-vbox-but-absent-in-ifconfig)

		- [rtl8188fu driver](https://github.com/kelebek333/rtl8188fu)
		
	- Other stuff
	
		- [Getting RTL8188 to work with Kali in monitor mode](https://forums.kali.org/showthread.php?37911-Getting-RTL8188-to-work-with-Kali-in-monitor-mode)
		
		- [rtl8188eus driver](https://github.com/aircrack-ng/rtl8188eus)