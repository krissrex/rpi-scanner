# Raspberry Pi Barcode and NFC Scanner

This uses raspbian 11 (bullseye).

The barcode scanner is an [Argox AS-8060](https://www.argox.com/products-detail/as-8060/) USB-HID device.  
The NFC scanner is a [SYCREADER R30C IC-USB Reader](https://www.sycreader.com/en/3880/).

Run `main.py` to start.  
It grabs exclusive control over the two scanners, based on their ID in `/dev/input/by-id/`.
Then it reads them concurrently using `asyncio`, and sends the strings to a callback when <kbd>enter</kbd> is pressed.


# Credits

The key code map was copied from [NoahNye on stack overflow](https://stackoverflow.com/a/65389539)
