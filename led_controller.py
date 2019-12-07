from bluedot import BlueDot
from signal import pause
from gpiozero import LED
from gpiozero import PWMLED
import time
top_led = PWMLED(12)
bottom_led = PWMLED(20)
left_led = PWMLED(16)
right_led = PWMLED(21)
def dpad(pos):
    if pos.top:
        top_led.toggle()
    elif pos.bottom:
        bottom_led.toggle()
    elif pos.left:
        left_led.toggle()
    elif pos.right:
        right_led.toggle()
    elif pos.middle:
        top_led.toggle()
        bottom_led.toggle()
        left_led.toggle()
        right_led.toggle()
def swipe(pos):
    speed = pos.speed
    print(speed)
    if pos.up:
        top_led.blink(on_time=1/speed,off_time=1/speed)
    elif pos.down:
        bottom_led.blink(on_time=1/speed,off_time=1/speed)
    elif pos.left:
        left_led.blink(on_time=1/speed,off_time=1/speed)
    elif pos.right:
        right_led.blink(on_time=1/speed,off_time=1/speed)
def rotate(rotation):
    speed = 3
    print(speed)
    if(rotation.clockwise):
        
        for i in range(3):
            #top_led.blink(on_time=1/speed,off_time=1/speed)
            top_led.on()
            time.sleep(1/speed)
            top_led.off()
            #right_led.blink(on_time=3/speed,off_time=1/speed)
            right_led.on()
            time.sleep(1/speed)
            right_led.off()
            #bottom_led.blink(on_time=3/speed,off_time=1/speed)
            bottom_led.on()
            time.sleep(1/speed)
            bottom_led.off()
            #left_led.blink(on_time=3/speed,off_time=1/speed)
            left_led.on()
            time.sleep(1/speed)
            left_led.off()
    
    if(rotation.anti_clockwise):
        for i in range(3):
            #top_led.blink(on_time=1/speed,off_time=1/speed)
            top_led.on()
            time.sleep(1/speed)
            top_led.off()
            #right_led.blink(on_time=3/speed,off_time=1/speed)
            left_led.on()
            time.sleep(1/speed)
            left_led.off()
            #bottom_led.blink(on_time=3/speed,off_time=1/speed)
            bottom_led.on()
            time.sleep(1/speed)
            bottom_led.off()
            #left_led.blink(on_time=3/speed,off_time=1/speed)
            right_led.on()
            time.sleep(1/speed)
            right_led.off()
        
    
bd = BlueDot()
speed = 1
while True:
    bd.when_released = dpad
    bd.when_swiped = swipe
    #bd.when_rotated = rotate
    bd.set_when_rotated(rotate,background=True)