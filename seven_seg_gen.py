#!/usr/bin/env python
# https://hackaday.io/project/28833-microhacks/log/87292-oscilloscope-sing-along-rotating-cube
# this code is in the public domain

import wave  # FOr Wav Files
import struct
import math
import matplotlib.pyplot as plt
import time


def scale_shift(d_image, scale=1.0, x_shift=0.0, y_shift=0.0):
    output = []
    length = len(d_image)
    # First re-scale all the values and shift
    for x, y in d_image:
        output.append((scale*x + x_shift, scale*y + y_shift))

    # Then return the updated number
    return output


def get_digits(hours='00', minutes='00'):
    minutes = str(minutes)
    if len(minutes) == 1:
        minutes = "0" + minutes

    # print("Update minutes to: " + minutes)
    ver = 0.5
    hoz = 0.5
    scale = 0.35

    # Horizontal segments (A, D, G)
    A = [
        (-0.5, 0.9),
        (0.5, 0.9),
        (0.3, 0.7),
        (-0.3, 0.7),
        (-0.5, 0.9)
    ]
    B = [
        (0.3, 0.7),
        (0.3, 0.1),
        (0.5, 0.0),
        (0.5, 0.9),
        (0.3, 0.7)
    ]
    C = [
        (0.3, -0.1),
        (0.3, -0.7),
        (0.5, -0.9),
        (0.5, 0.0),
        (0.3, -0.1)
    ]
    D = [
        (-0.5, -0.9),
        (0.5, -0.9),
        (0.3, -0.7),
        (-0.3, -0.7),
        (-0.5, -0.9)
    ]
    E = [
        (-0.3, -0.1),
        (-0.3, -0.7),
        (-0.5, -0.9),
        (-0.5, 0.0),
        (-0.3, -0.1)
    ]
    F = [
        (-0.3, 0.7),
        (-0.3, 0.1),
        (-0.5, 0.0),
        (-0.5, 0.9),
        (-0.3, 0.7)
    ]
    G = [
        (-0.5, 0),
        (-0.3, 0.1),
        (0.3, 0.1),
        (0.5, 0.0),
        (0.3, -0.1),
        (-0.3, -0.1),
        (-0.5, 0)
    ]

    dots = [
        (-0.1, 0.1),
        (-0.1, -0.1),
        (0.1, -0.1),
        (0.1, 0.1),
        (-0.1, 0.1)
    ]

    digits = {
        "0": A + B + C + D + E + F,
        "1": B + C,
        "2": A + B + G + E + D,
        "3": A + B + G + C + D,
        "4": F + G + B + C,
        "5": A + F + G + C + D,
        "6": A + F + G + C + D + E,
        "7": A + B + C,
        "8": A + B + C + D + E + F + G,
        "9": A + B + C + D + F + G
    }

    # Setup the cordinates for all the numbers

    first_dig = scale_shift(digits[hours[0]], scale, -hoz, ver)
    second_dig = scale_shift(digits[hours[1]], scale, hoz, ver)

    third_dig = scale_shift(digits[minutes[0]], scale, -hoz, -ver)
    fourth_dig = scale_shift(digits[minutes[1]], scale, hoz, -ver)

    # Now draw the shapes
    complete_stamp = {
        "1st": first_dig,
        "2nd": second_dig,
        "3rd": third_dig,
        "4th": fourth_dig,
    }

    return complete_stamp


class ScopeDisplay():
    def __init__(self, sample_rate, filename):
        self.sample_rate = sample_rate
        self.wav = wave.open(filename, 'w')
        self.wav.setnchannels(2)
        # 1 byte per sample Unsigned 8-bit (0–255)
        self.wav.setsampwidth(1)
        self.wav.setframerate(sample_rate)
        self.wav.setnframes(1)
        self.data = []

    def point(self, x, y):
        # Generates it as a range from [0 255]
        left = int(min(max(128+127*x, 0), 255))
        right = int(min(max(128+127*y, 0), 255))
        # 128 is the center of the screen.
        # Raw bytes, not python, B => Usigned char, 1 byte
        self.data.append(struct.pack('B', left))
        self.data.append(struct.pack('B', right))

    # Interpolates many smallerpoints = no jagged lines
    # Step should increase resolution
    def line(self, x0, y0, x1, y1, step=1):
        # Length of the line
        d = math.sqrt((x0-x1)*(x0-x1) + (y0-y1)*(y0-y1))
        n_pts = max(2, int(step * d))
        for i in range(0, n_pts):
            x = x0 + (x1 - x0) * i / (n_pts-1)
            y = y0 + (y1 - y0) * i / (n_pts-1)
            self.point(x, y)

    # Write data to the file.

    def close(self):
        # self.wav.writeframes(''.join(self.data))
        # Updated for Python 3
        self.wav.writeframes(b''.join(self.data))
        self.wav.close()


period = 5
hours = "00"
for hour in range(0, 24):
    # Formatting
    if hour < 10:
        hours = "0" + str(hour)
    else:
        hours = str(hour)

    for minutes in range(0, 60):
        mins = "00"
        if minutes < 10:
            mins = "0" + str(minutes)
        else:
            mins = str(minutes)

        display = ScopeDisplay(48000, './time_files/t_' +
                               hours + '_'+mins+'.wav')
        print("Doing: " + str(minutes))
        # Square corners (normalized -1 to +1)
        # Width and height of a segment

        # Loop 59 times for the 59 minutes in a hour, after 59 it will tick over to next number
        for _ in range(period):
            complete_stamp = get_digits(hours, str(minutes))

            for current_num in complete_stamp:
                # print("current_num: " + current_num)
                cdata = complete_stamp[current_num]
                # print("number of lines:" + str(len(cdata)))

                for i in range(len(cdata) - 1):
                    x0, y0 = cdata[i]
                    x1, y1 = cdata[i + 1]
                    display.line(x0, y0, x1, y1, step=60)

        display.close()
