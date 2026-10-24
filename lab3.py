# ENME 441 - Lab 3: ESP32 Setup and MicroPython - Merrick Summers
#
# Fill in the function below, following the assignment handout.  Do not change
# the function name, and submit this file without renaming it.

import network

def get_ip():
    """Return the board's IP address on current Wi-Fi network as a string."""
    return network.WLAN(network.STA_IF).ifconfig()[0]


# The code below runs only when this file is executed directly (for example,
# by pressing "Run" in Thonny with your board connected).  It does not run
# when the autograder imports your function.  Leave it as-is.
if __name__ == '__main__':

    print('IP address:', get_ip())
