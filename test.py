from lcd1602 import LCD

display = LCD(5, 4, 0, 2, 14, 12)
display.lcd_init()

if __name__ == '__main__':
    display.lcd_string("hello world", display.LCD_LINE_1)
    display.lcd_string("16X2 LCD TEST", display.LCD_LINE_2)
