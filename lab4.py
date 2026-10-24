# ENME 441 - Lab 4: PWM and IRQs - Merrick Summers

from machine import Pin, PWM
from time import ticks_ms, ticks_diff
import math

DEBOUNCE_MS = 50     # ignore edges closer together than this

pin_nums = [5, 6, 7, 10, 20, 21]
leds = [PWM(Pin(num), freq=500) for num in pin_nums]

phase_shifts = []
phase_step = math.pi / 7
for i in range(0, len(leds)):
    phase_shifts.append(phase_step * i)


def get_duty_cycle(phi: float = 0) -> int:
    '''Use time, a sine-wave, and phase-shifts to return a 10-bit duty cycle value'''
    f = 0.2                     # pulse frequency in Hz
    T = 1 / f                   # pulse period in seconds
    t = ticks_ms() / 1000 % T   # cycle position in seconds
    return round(100 * ((math.sin(2 * math.pi * f * t - phi)) ** 2))


def switch_wave_direction(_):
    '''Change the led wave direction by inverting the signs of the phase-shifts'''
    global phase_shifts # To be honest the need for this may show that this code is structured poorly, but I will still accept it for the purposes of the completion of this assignment. Optimally I would learn a more healthy way to manage state in the future if I can, but perhaps for small files like this having a few stateful globals is ok, just as long as you keep a really good handle on them and don't let them make your life messy, complicated, and worse as the program grows.
    for i in range(len(phase_shifts)):
        phase_shifts[i] = -phase_shifts[i]


# How does delaying when the function is called debounce it? Can't you accidentally not call the function? Is this not what is happening here at all? Probably.
def debounced(callback, delay_ms=DEBOUNCE_MS):
    last = [0]        # list so the inner function can modify it
    def handler(p):
        now = ticks_ms()
        if ticks_diff(now, last[0]) > delay_ms:
            last[0] = now
            callback(p)
    return handler


interrupt_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)
interrupt_pin.irq(handler=debounced(switch_wave_direction), trigger=Pin.IRQ_RISING)

try:
    while True:
        for i, led in enumerate(leds):
            led.duty(get_duty_cycle(phase_shifts[i]))
except KeyboardInterrupt:
    for led in leds:
        led.deinit()
