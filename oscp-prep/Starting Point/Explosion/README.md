## Explosion

1. Port enumeration

	![](./Screenshots/explosion-1.png)

2. Port 135, 139 & 445: SMB

3. Enumerate client using smbclient

	![](./Screenshots/explosion-2.png)
	
	Found nothing :(

3. Port 3389: Remote Desktop Access

4. Attempt to connect using rdesktop

	![](./Screenshots/explosion-3.png)
	
	[Use xfreerdp instead](https://www.linuxquestions.org/questions/linux-networking-3/failed-to-connect-credssp-required-by-server-4175611983/)
	
5. Attempt to connect using xfreerdp

	![](./Screenshots/explosion-4.1.png)

	![](./Screenshots/explosion-4.2.png)
	
	Use common default credentials (just try and try!)
	
6. Try with /cert:ignore /u:Administrator (syntax depends on version of xfreerdp used, order of flags should not matter)

	![](./Screenshots/explosion-5.1.png)
	
	![](./Screenshots/explosion-5.2.png)
	
	Grab flag :D