# ENME 441 Lab 5

from machine import Pin
import random
import time


class Shifter:
    def __init__(self, data, latch, clock):
        self.dataPin = Pin(data, Pin.OUT)
        self.latchPin = Pin(latch, Pin.OUT)
        self.clockPin = Pin(clock, Pin.OUT)

    def _ping(self, p):
        """Ping the clock (SRCLK) or latch (RCLK) pin."""
        p.value(1)
        time.sleep_us(10)
        p.value(0)

    def shift(self, data, num_bits=8):
        """Shift an arbitrary-length word into one or more 74HC595s."""
        for i in range(num_bits):
            self.dataPin.value(data & (1 << i))
            self._ping(self.clockPin)
        for i in range(-num_bits % 8):
            self.dataPin.value(0)
            self._ping(self.clockPin)
        self._ping(self.latchPin)


def debounced(callback, delay_ms=50):
    last = [time.ticks_ms() - delay_ms - 1]

    def handler(pin):
        now = time.ticks_ms()
        if time.ticks_diff(now, last[0]) > delay_ms:
            last[0] = now
            callback(pin)

    return handler


class Bug:
    def __init__(self, timestep=0.1, isOn=True, isWrapOn=False):
        self.timestep = timestep
        self.isOn = isOn
        self.isWrapOn = isWrapOn
        self.x = 3
        self.__shifter = Shifter(data=0, latch=1, clock=3)
        self.__shifter.shift(1 << self.x if self.isOn else 0)

    def start(self):
        self.isOn = True
        self.__shifter.shift(1 << self.x)

    def stop(self):
        self.isOn = False
        self.__shifter.shift(0)

    def step(self):
        if not self.isOn:
            return
        direction = 1 if random.getrandbits(1) else -1
        next_x = self.x + direction
        if self.isWrapOn:
            self.x = next_x % 8
        elif 0 <= next_x <= 7:
            self.x = next_x
        self.__shifter.shift(1 << self.x)


def main():
    bug = Bug()
    s1 = Pin(5, Pin.IN, Pin.PULL_DOWN)
    s2 = Pin(6, Pin.IN, Pin.PULL_DOWN)
    s3 = Pin(7, Pin.IN, Pin.PULL_DOWN)

    # Read the initial switch positions before enabling IRQs.
    bug.isOn = bool(s1.value())
    bug.timestep = 0.02 if s3.value() else 0.1
    def on_switch(pin):
        bug.isOn = bool(pin.value())

    def wrap_switch(pin):
        bug.isWrapOn = not bug.isWrapOn

    def speed_switch(pin):
        bug.timestep = 0.02 if pin.value() else 0.1

    both_edges = Pin.IRQ_RISING | Pin.IRQ_FALLING
    s1.irq(handler=on_switch, trigger=both_edges)
    s2.irq(handler=debounced(wrap_switch), trigger=both_edges)
    s3.irq(handler=speed_switch, trigger=both_edges)

    was_on = True  # Bug() initially lights the LED.
    last_step = time.ticks_ms()
    try:
        while True:
            if bug.isOn != was_on:
                if bug.isOn:
                    bug.start()
                    last_step = time.ticks_ms()
                else:
                    bug.stop()
                was_on = bug.isOn

            if bug.isOn and time.ticks_diff(time.ticks_ms(), last_step) >= int(bug.timestep * 1000):
                bug.step()
                last_step = time.ticks_ms()
            time.sleep_ms(5)
    finally:
        s1.irq(handler=None)
        s2.irq(handler=None)
        s3.irq(handler=None)
        bug.stop()


if __name__ == "__main__":
    main()
