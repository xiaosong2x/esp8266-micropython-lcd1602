from time import sleep
from machine import Pin


class LCD:
    def __init__(self, rs, e, d4, d5, d6, d7):
        """
        Initialize the LCD object
        :param rs: int, Which GPIO is connected to the LCD_RS
        :param e:  int, Which GPIO is connected to the LCD_E
        :param d4: int, Which GPIO is connected to the LCD_D4
        :param d5: int, Which GPIO is connected to the LCD_D5
        :param d6: int, Which GPIO is connected to the LCD_D6
        :param d7: int, Which GPIO is connected to the LCD_D7
        """

        self.__LCD_WIDTH = 16  # Maximum characters per line
        self.LCD_CHR = True
        self.LCD_CMD = False
        self.LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
        self.__LCD_RS = Pin(rs, Pin.OUT)
        self.__LCD_E = Pin(e, Pin.OUT)
        self.__LCD_D4 = Pin(d4, Pin.OUT)
        self.__LCD_D5 = Pin(d5, Pin.OUT)
        self.__LCD_D6 = Pin(d6, Pin.OUT)
        self.__LCD_D7 = Pin(d7, Pin.OUT)
        self.__E_PULSE = 0.0005
        self.__E_DELAY = 0.0005

    def __lcd_toggle_enable(self):
        sleep(self.__E_DELAY)
        self.__LCD_E.on()
        sleep(self.__E_PULSE)
        self.__LCD_E.off()
        sleep(self.__E_DELAY)

    def lcd_byte(self, bits, mode):
        """
        Send data to LCD
        :param bits: data
        :param mode: self.LCD_CHR to send data or self.LCD_CMD to send command
        """
        if mode:
            self.__LCD_RS.on()
        else:
            self.__LCD_RS.off()

        def set0():
            self.__LCD_D4.off()
            self.__LCD_D5.off()
            self.__LCD_D6.off()
            self.__LCD_D7.off()
        # High bits
        set0()
        if bits & 0x10 == 0x10:
            self.__LCD_D4.on()
        if bits & 0x20 == 0x20:
            self.__LCD_D5.on()
        if bits & 0x40 == 0x40:
            self.__LCD_D6.on()
        if bits & 0x80 == 0x80:
            self.__LCD_D7.on()
        self.__lcd_toggle_enable()
        # Low bits
        set0()
        if bits & 0x01 == 0x01:
            self.__LCD_D4.on()
        if bits & 0x02 == 0x02:
            self.__LCD_D5.on()
        if bits & 0x04 == 0x04:
            self.__LCD_D6.on()
        if bits & 0x08 == 0x08:
            self.__LCD_D7.on()
        self.__lcd_toggle_enable()

    def lcd_init(self):
        """
        Initialise display
        """
        self.lcd_byte(0x33, self.LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, self.LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, self.LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.LCD_CMD)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.LCD_CMD)  # 000001 Clear display
        sleep(self.__E_DELAY + 0.1)

    def lcd_string(self, message, line):
        """
        Send string to display
        :param message: str, Which text you want to display
        :param line:  self.LCD_LINE_1 or self.LCD_LINE_2
        """
        message = "%-16s" % message
        self.lcd_byte(line, self.LCD_CMD)
        for i in range(self.__LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

    def lcd_clear(self):
        """
        Send 000001 Clear display
        """
        self.lcd_byte(0x01, self.LCD_CMD)

    def write_lcd_cg_ram(self, data, address):
        """
        Write customize character to CgRam
        :param data: list or tuple, customize character data
        :param address:bits, CgRam address
        """
        self.lcd_byte(address, self.LCD_CMD)
        for i in data:
            self.lcd_byte(i, self.LCD_CHR)

    def lcd_show(self, location, data):
        """
        display single character on lcd
        :param location: bits, LCD RAM address
        :param data: bits,
        """
        self.lcd_byte(location, self.LCD_CMD)
        self.lcd_byte(data, self.LCD_CHR)
