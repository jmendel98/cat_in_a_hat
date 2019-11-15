import time
import re

hold = 1

while hold == 1:
    pixel_data = open("img_data.txt","r").read()
    index = 0
    DATA_LENGTH = len(pixel_data)
    while index < DATA_LENGTH:
        key_pressed = input('Press ENTER to continue: ')
        print(key_pressed)
        temp_char = pixel_data[index]
        if temp_char in ['1']:
            print("High\n")
        else:
            print("Low\n")
        index = index + 1
    print("Done! and waiting for instructions")    
    INPUT_DATA = input('Enter info for next pixels or AAA if no input: ')  
    if INPUT_DATA != "AAA":
        open("img_data.txt","w").truncate(0)
        open("img_data.txt","w").write(INPUT_DATA)