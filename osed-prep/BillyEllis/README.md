# Exploit Challenges Set Up

### Set up (iPhone):

Step 1: Jailbreak iphone (make sure that it supports 32bit)

1. Preferably older models so that a jailbreak is available in the first place 

2. More on [jailbreak](https://osxdaily.com/tag/jailbreak/)

3. [Different types of jailbreak](https://www.youtube.com/watch?v=F_kxIatZpOE)

4. [checkra1n jailbreak](https://www.idownloadblog.com/2019/11/10/how-to-jailbreak-with-the-checkra1n-public-beta/) (ended up using this)

5. [chimera jailbreak](https://www.idownloadblog.com/2019/04/29/how-to-jailbreak-ios-12-0-12-1-2-with-chimera/) (failed for me, encountered many problems such as [this](https://www.reddit.com/r/jailbreak/comments/80mazr/question_getting_a_provisioncpp173_error_please/))

  - If you are using this method, you will need to use a downloader tool, popular ones are [impactor](http://www.cydiaimpactor.com/) and AltDeploy

  - [Resource for chimera jailbreak using impactor](https://www.idownloadblog.com/2019/04/29/how-to-jailbreak-ios-12-0-12-1-2-with-chimera/), however, impactor was not working for me as it kept crashing. Google and use any of such alternatives.

  - Used [AltDeploy](https://github.com/pixelomer/AltDeploy/releases) v1.0.1 as the latest version kept crashing

  - For any of these methods, if you are using a Mac, you need to make sure that the appleId of the account on the mac itself matches the appleId that you are using to install with as seen in this [tutorial](https://cybertips.io/how-to-install-ios-apps-with-altdeploy/#1_Download_AltDeploy). If not, you will encounter this [error](https://www.reddit.com/r/AltStore/comments/eqmpup/error_this_action_cannot_be_completed_at_this/)

Step 2: SSH into iphone

1. Install SSH Client from Cydia

2. Obtain IP of iphone before SSHing from your computer

3. Reference this [link](https://osxdaily.com/2011/08/04/ssh-to-iphone/) if needed

4. Username:Password credentials &#8594; root:alpine

Step 3: Install gdb on iphone

1. Follow tutorial [here](https://www.reddit.com/r/jailbreak/comments/ag3hrh/question_how_can_i_install_gdb_searching_it_wont/)

2. From cydia, go to data source and add http://cydia.radare.org

3. Search and install gdb

### Set up (Computer):

Alternatively, if you do not have an iPhone/do not want to go through the hassle of jailbreaking it, each challenge directory has a `src` subdirectory revealing the source code of each challenge. You can compile it yourself accordingly and try to reverse it on your computer.

You will need to compile the source code to the binaries with the appropriate security properties (e.g. ASLR, NX/DEP) enabled/disabled. Below are relevant links on how to do so:

1. Stack Alignment: `-mpreferred-stack-boundary=2` (ref [here](https://stackoverflow.com/questions/39737813/disabling-stack-protection-in-gcc-not-working))

2. Fortify: DON'T REALLY KNOW TOO MUCH ABOUT THIS PROPERTY YET (ref [here](https://resources.infosecinstitute.com/topic/gentoo-hardening-part-3-using-checksec-2/))

3. RELRO: `-Wl,-z,norelro` (ref [here](https://stackoverflow.com/questions/60493027/how-to-disable-relro-to-overwrite-fini-array-or-got-plt-element))

4. PIE: `-no-pie` (ref [here](https://askubuntu.com/questions/911538/disable-pie-and-pic-defaults-in-gcc-on-ubuntu-17-04))

5. ASLR: `echo 0 | sudo tee /proc/sys/kernel/randomize_va_space` (ref [here](https://askubuntu.com/questions/318315/how-can-i-temporarily-disable-aslr-address-space-layout-randomization))

6. Stack Canary: `-fno-stack-protector` (ref [here](https://stackoverflow.com/questions/2340259/how-to-turn-off-gcc-compiler-optimization-to-enable-buffer-overflow))

7. NX/DEP: `-z execstack` (ref [here](https://stackoverflow.com/questions/2340259/how-to-turn-off-gcc-compiler-optimization-to-enable-buffer-overflow))

8. Compile with 32 bit: `-m32`

### GDB Things

1. `set $esp=0x0000000` vs set `set {int}$esp=0x00000000` differences
