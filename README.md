LCD1602 microPython driver for ESP8266
=====


how to use

**LCD1602 connect**

|LCD1602|ESP8266|
| ------ | ------ |
|VSS|+5V|
|VDD|GND|
|V0|GND|
|RS|GPIO5|
|RW|GND|
|E|GPIO4|
|D4|GPIO0|
|D5|GPIO2|
|D6|GPIO14|
|D7|GPIO12|
|A|+3.3v|
|K|GND|


**test code**
```python
from lcd1602 import LCD

display = LCD(5, 4, 0, 2, 14, 12)
display.lcd_init()

if __name__ == '__main__':
    display.lcd_string("hello world", display.LCD_LINE_1)
    display.lcd_string("16X2 LCD TEST", display.LCD_LINE_2)
```

