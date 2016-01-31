import serial
import textwrap
import time


class LCDConnection:
    def __init__(self, serial_port, baud=9600, timeout=1, scroll_lines=1, chars=16, lines=2, delay=1):
        self.serialport = serial.Serial(serial_port, baud, timeout=timeout)
        self.scroll_lines = scroll_lines
        self.delay = delay
        self.chars = chars

    def clear(self):
        self.serialport.write(b'\xfe\x01')

    def on(self):
        self.serialport.write(b'\xfe\x0c')

    def off(self):
        self.serialport.write(b'\xfe\x01')

    def write(self, message):
        wrapped_msg = textwrap.wrap(message, width=self.chars)
        for line in wrapped_msg:
            line = (line + ' '*16)[:16]
            self.serialport.write(bytes(line, 'utf-8'))
            time.sleep(self.delay)

    def close(self):
        self.serialport.close()

    #def brightness(self, brightness):
    #    """brightness would be an integer between 0 and 30, 0 for backlight off and 30 for blinding"""
    #    self.serialport.write("\x7c\")

    def toggle_splash(self):
        self.serialport.write(b'\xfe\x09')
