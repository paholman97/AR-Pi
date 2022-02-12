import datetime #To display current time
import digitalio #Contains classes to provide access to basic digital IO
import board #Contains constants for the pins on the board
import adafruit_rgb_display.ssd1351 as ssd1351 #SSD1351-based display - SSD1351 driver chip manages the display
from PIL import Image, ImageDraw, ImageFont #Python Imaging Library

#Configuration for CS and DC pins
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

#Set baud rate to 16MHz - SSD1351 driver limit
BAUDRATE = 1600000

#Set up SPI bus using hardware SPI
spi = board.SPI()

#1.27" display
disp = ssd1351.SSD1351(
    spi,
    height=96,
    y_offset=32,
    rotation=0,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE
)

#Determine if screen is landscape or portrait
if disp.rotation % 180 == 90:
    height = disp.width
    width = disp.height
else:
    width = disp.width
    height = disp.height
    
#Image with mode: 'RGB' for full colour
image = Image.new("RGB", (width, height))

#Drawing object to draw on image
draw = ImageDraw.Draw(image)

#Draw black box the full size of the screen
draw.rectangle((0, 0, width, height), outline="#000000", fill="#000000")
disp.image(image) #Show black box

font = ImageFont.truetype("/home/pi/Documents/OLEDTests/OpenSansBold.ttf", 20)
current_time = datetime.datetime.now().strftime("%H:%M")

text = current_time
(font_width, font_height) = font.getsize(text)
draw.text(
    (0, 0),
    text,
    font=font,
    fill=(0, 0, 0)
)
disp.image(image)