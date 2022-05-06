#!/usr/bin/env python3

import asyncio
from evdev import InputDevice, categorize, ecodes
from stdnum import isbn as std_isbn, ean

import isbn
import users
import food

INPUT_NFC = "/dev/input/by-id/usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd"
INPUT_BARCODE = "/dev/input/by-id/usb-USB_Adapter_USB_Device-event-kbd"

DEV_NFC = InputDevice(INPUT_NFC)
DEV_BARCODE = InputDevice(INPUT_BARCODE)

SCAN_CODES = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

CAPS_CODES = {
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

class DeviceReader:
  buffer = ""
  caps = False
  onLine = lambda line: None

  def __init__(self, device):
    self.device = device

  async def readDevice(self):
    async for ev in self.device.async_read_loop():
      if ev.type == ecodes.EV_KEY:
        data = categorize(ev)

        if data.scancode == ecodes.KEY_LEFTSHIFT:
          self.caps = data.keystate == 1

        if data.keystate == 1: # down
          lookup = CAPS_CODES if self.caps else SCAN_CODES
          key = u'{}'.format(lookup.get(data.scancode))
          if (data.scancode != ecodes.KEY_LEFTSHIFT) and (data.scancode != ecodes.KEY_ENTER):
            if key != None:
              self.buffer += key
          elif data.scancode == ecodes.KEY_ENTER:
            if self.onLine:
              line = self.buffer
              self.buffer = ""
              self.onLine(line)


if __name__ == "__main__":
  try:
    DEV_BARCODE.grab()
    DEV_NFC.grab()

    barcode = DeviceReader(DEV_BARCODE)
    nfc = DeviceReader(DEV_NFC)

    def onBarcode(line):
      print(f"Barcode scanned: {line}")

      if std_isbn.is_valid(line):
        try:
          book = isbn.lookupIsbn(line)
          print(f"Found book for isbn {line}:")
          print(repr(book))
        except Exception as e:
          print(f"ISBN lookup for {line} failed: {e}")
      elif ean.is_valid(line):
        # Both EAN-13 and EAN-8 are used on food.
        # Note than an ISBN is EAN-13, starting with 978 or 979
        try:
          product = food.lookupFood(line)
          print(f"Found food product for ean {line}:")
          print(repr(product))
        except Exception as e:
          print(f"Food lookup for {line} failed: {e}")

    barcode.onLine = onBarcode

    def onNfc(line):
      print(f"NFC scanned: {line}")
      user = users.findUser(line)
      if user:
        print(f"Found user {user} for UUID {line}")
      else:
        print(f"No user found for UUID {line}")

    nfc.onLine = onNfc

    asyncio.ensure_future(barcode.readDevice())
    asyncio.ensure_future(nfc.readDevice())

    barcode_loop = asyncio.get_event_loop()
    barcode_loop.run_forever()
  finally:
    DEV_BARCODE.ungrab()
    DEV_NFC.ungrab()
