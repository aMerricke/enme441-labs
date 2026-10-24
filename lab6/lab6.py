# shifter.py
#
# Shift register class
#
# ESP32-C3 SuperMini

from machine import Pin
import time
import random

class Shifter():

    def __init__(self, data=5, latch=6, clock=7): #init will allow us to call self.(variable) in the future
        self.dataPin = Pin(data, Pin.OUT) # Double Underscores are called dunders. Init is built-in and is a naming convention 
        self.latchPin = Pin(latch, Pin.OUT)
        self.clockPin = Pin(clock, Pin.OUT)

    def _ping(self, p): #Single underscore defines variable as private, function for internal use only
        """ping the clock (CLK) or latch (RCLK) pin"""
        p.value(1)
        time.sleep_us(10)
        p.value(0)
        
    def shift(self, data, num_bits=30):
        """
        Shift all bits in an arbitrary-length word, allowing
        multiple 8-bit shift registers to be chained (with overflow
        of SR<n> tied to input of SR<n+1>)

        The value of num_bits determines how many shift registers
        are present (num_bits = 8 --> 1 SR by default).
        (N-1)*8 < num_bits <= N*8 implies there are N chained
        shift registers
        """

        """
        Load bits short of a byte with 0.  The math works because
        the modulo operator returns the remainder, defined as:
            a % b = a - b * floor(a/b)
        So for example:
            -10 % 8 = -10 - 8 * floor(-10 / 8) 
                    = -10 - 8 * floor(-1.25)
                    = -10 - 8 * (-2)
                    = -10 - (-16)
                    = 6
        Python's modulo is non-negative, so this works even
        when a < b.
        """
        for i in range(-num_bits%8):
            self.dataPin.value(0)
            self._ping(self.clockPin) #Output to the shift register clock the time signal

        # Send the word
        for i in range(num_bits):
            self.dataPin.value(data & (1<<i))
            self._ping(self.clockPin)
    
        self._ping(self.latchPin)
        
class Bug():
    def __init__(self, timestep=0.1, isOn=True, isWrapOn= False):
        self.starttimestep = timestep
        self.timestep = timestep
        self.isOn = isOn
        self.isWrapOn = isWrapOn #Wrapping means from LED 0 to LED 7 and vice versa
        self.x= 3; #LED starting position
        
        # Double underscore tells us that the other function is internal 
        self.shifter = Shifter(data=5, latch=7, clock=6) #Defines which ESP32 pins correspond to what on the SR
    
    def update(self):
        
        if self.isOn:
            self.shifter.shift(1 << self.x, num_bits = 30) # will shift 1 to the left by pos (00001000 = 8)
        else:
            self.shifter.shift(0, num_bits=30) # Don't shift
    
    def start(self):
        if not self.isOn:
            self.update() # Turns everything off if its not supposed to be on
            return
        
        step = random.choice([-1, 1]) # Picks random number from -1 to 1
        
        if self.isWrapOn:
            self.x = (self.x+step)%30 # If pos is 8, it will reset back to 0 (the first index of the LED)
        else:
            if 0 <= (self.x+step) <= 29: #If new value is in between range 
                self.x = (self.x+step) # Now we can change position
                
        self.update() # run the function             

    def stop(self):
        self.isOn = False
        self.update() # This function will turn off LEDs


# Bug Instance

bug = Bug(timestep=0.1, isOn= False, isWrapOn=True)


def myCallback1(p1):
    
    bug.isOn = bool(p1.value())
    bug.update()

    
def myCallback2(p2):
    bug.isWrapOn = not bug.isWrapOn #Switches state
    
def myCallback3(p3):
    if p3.value() == 1:
        bug.timestep = bug.starttimestep / 5.0
    else:
        bug.timestep = bug.starttimestep
        
 
 
# Debouncing
def debounced(callback, delay_ms=50):
    last = [0] # list so the inner function can modify it
    def handler(p):
         now = time.ticks_ms()
         if time.ticks_diff(now, last[0]) > delay_ms:
             last[0] = now
             callback(p)
    return handler

# Define trigger pins
# Turn LED ON only when ON, and OFF when NOT
s1 = Pin(0, Pin.IN, Pin.PULL_DOWN) 
s1.irq(handler=debounced(myCallback1), trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

# Wrap/Unwrap whenever state switches
s2 = Pin(1, Pin.IN, Pin.PULL_DOWN)
s2.irq(handler=debounced(myCallback2), trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

# Increase the speed only when ON
s3 = Pin(3, Pin.IN, Pin.PULL_DOWN)
s3.irq(handler=debounced(myCallback3), trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)



if __name__ == "__main__":
    
    myCallback1(s1)
    myCallback3(s3)
    """  
    mask = 2**30-1
    alternate_bits = 0b101010101010101010101010101010
    alternate_bars = (2**10-1) | (2**10-1)<<20
    half_bars = (2**5-1) | (2**5-1)<<10 | (2**5-1)<<20
    print(f'{alternate_bits:030b}')
    print(f'{alternate_bits ^ mask:030b}')
    print(f'{alternate_bars:030b}')
    print(f'{alternate_bars ^ mask:030b}')
    print(f'{half_bars:030b}')
    print(f'{half_bars ^ mask:030b}')
    s = Shifter()
    s.shift(alternate_bits) # alternate bits on
    s.shift(alternate_bits ^ mask) # invert
    s.shift(alternate_bars) # alternate bars on
    s.shift(alternate_bars ^ mask) # invert
    s.shift(half_bars) # half-bars on
    s.shift(half_bars ^ mask) # invert
    """
    try:
        while True:
            bug.start()
            time.sleep(bug.timestep)
            
            

            
    except KeyboardInterrupt:
        bug.stop()
        print("Stopped Program.")
        
       
           


