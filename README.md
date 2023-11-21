# SWAT - Savior When Absolutely Trashed
A tiny system rescue utility for Motorola devices

## Quickstart
Make sure your bootloader is unlocked, install fastboot, download `swat.py` and run it with Python 3.x to see usage.

## Motives
In short, I don't like Windows that much.

Technically speaking, I have Windows on my machine, but it's for my little brother who doesn't really understand how to get around Linux. On the day of this tool's creation, I had already had to reboot into his install twice to run LMSA (RSA now) to recover my stock firmware after bad GSI flashes.

I eventually got it working, but then unfortunately managed to somehow brick my phone using TrebleDroid's securize function.

I had been thinking about this since I started modding Motorola devices, and as good as RSD Lite is, it's very sketchy and hard to find a trustworthy download for. It's also *old.* It was still a heavy inspiration for this project though, and it's still a viable tool for what it does.\
So, it was 2AM, and I was sitting here with nothing but a bootlooping Moto G 5G that got into fastboot and not really much else. I couldn't be bothered to reboot to use LMSA at this point, and I especially couldn't be bothered to manually type out fastboot commands, so on a whim I made this utility, which it's goal was to be a Motorola stock flasher that works on multiple platforms and uses as few lines of code as possible.

I think it accomplishes that.

## Contributions wanted
- anything you would like to add! seriously. i want this to be as feature packed as possible, but remember, keep it small.
- general refactoring. while i do like the way the program's laid out, the way it's implemented is very odd. i will do this over time
- a consistent way to detect if the bootloader is unlocked/the phone can be flashed
- somebody to test/maintain flashing on Windows. I do not use Windows actively enough to consistently be able to fix issues with this, so if someone who is skilled in Python, uses Windows and isn't scared to reflash their device could help out i would be eternally grateful
- irix to comment this code because they started writing it at 2am and published it at 6am and only they can read it

## Dreams
- a direct method of ripping firmware from the LMSA download servers. i've already started reverse engineering it, but it does use a timed token and linked guid system that i've yet to figure out.\
  if we do end up doing this, it is almost certainly going to require login, which i'm not sure i'm for

## Licensing
This project is licensed under the MIT license. See the LICENSE file.

## Acknowledgements
- Motorola          - for creating the devices this was made for and for being a (mostly) open (enough) platform for modding
- mattlgroff        - for RSD Lite
- rootjunky         - for RSD Lite Mac/Linux
- lolinet (kaneawk) - for providing stock firmware for all these devices (and for rehosting the OTA downloader tool)
- erfanoabdi        - for creating the OTA downloader tool\
<sup>~~TrebleDroid     - for indirectly creating this tool by bricking my phone /j~~</sup>
