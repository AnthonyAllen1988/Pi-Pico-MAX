from machine import Pin, I2C
from MAX6675 import MAX6675
import utime as time

# init so and sck pins. so = 1. sck = 0.
so = Pin(1, Pin.IN)
sck = Pin(0, Pin.OUT)


# init cs pins 2, 3, 4, 5, 6, 7, 8 and 9
m1cs = Pin(2, Pin.OUT)
m2cs = Pin(3, Pin.OUT)
m3cs = Pin(4, Pin.OUT)
m4cs = Pin(5, Pin.OUT)
m5cs = Pin(6, Pin.OUT)
m6cs = Pin(7, Pin.OUT)
m7cs = Pin(8, Pin.OUT)
m8cs = Pin(9, Pin.OUT)

# create instance of each thermocouple
max1 = MAX6675(sck, m1cs , so, 1)
max2 = MAX6675(sck, m2cs, so, 2)
max3 = MAX6675(sck, m3cs , so, 3)
max4 = MAX6675(sck, m4cs, so, 4)
max5 = MAX6675(sck, m5cs , so, 5)
max6 = MAX6675(sck, m6cs, so, 6)
max7 = MAX6675(sck, m7cs , so, 7)
max8 = MAX6675(sck, m8cs, so, 8)

# create thermocouple array
max_array = [max1, max2, max3, max4, max5, max6, max7, max8]

# create dictionary for output pins
pin_dict = {
        0:28,
        1:27,
        2:26,
        3:22,
        4:21,
        5:20,
        6:19,
        7:18
        }

# initialise output pins
for key in pin_dict.keys():
    Pin(pin_dict[key], Pin.OUT)
    Pin(pin_dict[key]).on()

# boot sequence turning each output on and off. loops 5 times.
timer = 0
while timer < 5:
    for key in pin_dict.keys():
        pin = Pin(pin_dict[key], Pin.OUT)
        pin.off()
        time.sleep(0.5)
        pin.on()
    timer = timer + 1

# begin main loop
while True:
    
    # create dictionary for 6 bits
    bin_dict = {
        5:None,
        4:None,
        3:None,
        2:None,
        1:None,
        0:None
        }
    
    # read each thermocouple in turn
    for couple in max_array:
        data = couple.read()
        
        # if the current thermocouple is the first, send bit 8
        if couple._cid == 1:
                Pin(pin_dict[7]).off()
        
        # if the temperature is 0 or below, set data to 0
        # this ensures no negative values
        if int(data) <= 0:
            data = 0
        
        # if the temperature is 250 or above, set data to 250
        if int(data) >= 250:
            data = 250
        
        # multiply data by 10, convert to integer then convert to binary string
        data = data * 10
        data = int(data)
        data = f'{data:08b}'
        
        # check the length of the string
        n = len(data)
            
        # if the binary string is less than 12 bits, add 0's to the beginning
        while n < 12:
            data = "0" + data
            n = len(data)
            
        # split binary string into two 6 bit strings, high byte and low byte
        high_byte = data[0:n//2]
        low_byte = data[n//2:]
        
        # initialise iterator
        i=5
        
        # iterate over each character in the high byte string
        # setting the value of the corresponding key in bin_dict
        # to the value of the character
        while i >= 0:
            for char in high_byte:
                bin_dict[i] = int(char)
                i = i-1
        
        # send high byte
        
        # iterate over each key in bin_dict
        # if the value of the key is 1, send a bit to corresponding output pin
        # if the value of the key is 0, do not send a bit to corresponding output pin
        for key in bin_dict.keys():
            if bin_dict[key] == 1:
                Pin(pin_dict[key]).off()
            else:
                Pin(pin_dict[key]).on()
        
        # sleep for 20ms
        time.sleep(0.02)
        
        # initialise the output pins
        for key in pin_dict.keys():
            Pin(pin_dict[key]).on()
        
        # initialise iterator
        i=5
        
        # iterate over each character in the low byte string
        # setting the value of the corresponding key in bin_dict
        # to the value of the character
        while i >= 0:
            for char in low_byte:
                bin_dict[i] = int(char)
                i = i-1
        
        # send low byte
        
        # iterate over each key in bin_dict
        # if the value of the key is 1, send a bit to corresponding output pin
        # if the value of the key is 0, do not send a bit to corresponding output pin
        for key in bin_dict.keys():
            if bin_dict[key] == 1:
                Pin(pin_dict[key]).off()
            else:
                Pin(pin_dict[key]).on()
        
        # sleep for 20ms
        time.sleep(0.02)
        
        # initialise the output pins
        for key in bin_dict.keys():
            Pin(pin_dict[key]).on()
        
        # sleep for 20ms
        time.sleep(0.02)
