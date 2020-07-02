# Copyright (C) 2020 Mark L Saunders
#
# The following terms apply to all files associated
# with the software unless explicitly disclaimed in individual files.
#
# The authors hereby grant permission to use, copy, modify, distribute,
# and license this software and its documentation for any purpose, provided
# that existing copyright notices are retained in all copies and that this
# notice is included verbatim in any distributions. No written agreement,
# license, or royalty fee is required for any of the authorized uses.
# Modifications to this software may be copyrighted by their authors
# and need not follow the licensing terms described here, provided that
# the new terms are clearly indicated on the first page of each file where
# they apply.
#
# IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
# DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
# IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
# NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
# MODIFICATIONS.

from ctypes import *
import usb.util
import sys
import logging
from usb._debug import methodtrace
import usb._interop as _interop
import usb._objfinalizer as _objfinalizer
import errno
import math
from usb.core import USBError
import usb.libloader
import usb.core

__author__ = 'Mark L Saunders'


#import ctypes as ct

VENDOR_LAC = 0x04d8
PRODUCT_LAC = 0xfc5f
WRITE_DELAY = 100
READ_DELAY = 100

SET_ACCURACY = 0x01
SET_RETRACT_LIMIT = 0x02
SET_EXTEND_LIMIT = 0x03
GET_FEEDBACK = 0x10
SET_POSITION = 0x20
SET_SPEED = 0x21
SET_GAIN_P = 0x0c
SET_GAIN_D = 0x0d
RESET = 0xFF

'''
class Buffer(ct.Structure):
    _fields_ = [("0", ct.c_uint8),
                ("1", ct.c_uint8),
                ("2", ct.c_uint8)]
'''


class USBAPI:
    value = 0

    def __init__(self, instance):
        self.instance = instance
        self.dev = usb.core.find(idVendor=VENDOR_LAC, idProduct=PRODUCT_LAC)

        if self.dev is None:
            raise ValueError('LAC device is not found. ')
            sys.exit(1)
        else:
            print('found device 0x%x, product 0x%x' % (VENDOR_LAC, PRODUCT_LAC))

        self.dev.set_configuration()
        print('configuration set')

        # get an endpoint instance
        self.cfg = self.dev.get_active_configuration()
        self.intf = self.cfg[(0, 0)]

    def USBWrite(self, control, value):
        # Convert value into high & low bit
        low = value & 0xff
        high = (value & 0xff00) >> 8

        # Construct the Buffer
        write_buffer = bytearray(3)
        write_buffer[0] = control
        write_buffer[1] = low
        write_buffer[2] = high

        # print('USBWrite values 0x%x 0x%x 0x%x' %(write_buffer[0], write_buffer[1], write_buffer[2]))

        # write to the usb device
        self.dev.write(1, write_buffer, WRITE_DELAY)
        # bytes_read = self.dev.read(0x81, READ_DELAY)
        # print(bytes_read)

    def USBRead(self):
        # Construct buffer type
        #read_buffer_type = ct.c_uint8 * 64

        # create buffer instance
        # read_buffer = read_buffer_type()

        read_buffer = self.dev.read(0x81, 1000)
        # print('USBRead values 0x%x 0x%x 0x%x' % (read_buffer[0], read_buffer[1], read_buffer[2]))
        self.value = read_buffer[1] + (read_buffer[2] * 255)
        return self.value


class LACDriver:
    def __init__(self, instance, stroke):
        # set stroke length
        self.stroke = float(stroke)

        # create USBAPI instance
        self.lac = USBAPI(instance)

    def find_device(self):
        return usb.core.find(self.vendorID, self.productID)

    def set_speed(self, speed):
        if speed > 100:
            speed = 100
        if speed < 0:
            speed = 0

        # send command
        self.lac.USBWrite(SET_SPEED, speed)
        # get response
        # self.lac.USBRead()

    def set_position(self, position):
        # Convert position to register value
        set_value = int((position / self.stroke) * 1023)
        if set_value > 1023:
            set_value = 1023
        if set_value < 1:
            set_value = 1

        # send command
        self.lac.USBWrite(SET_POSITION, set_value)
        # get response
        response = self.lac.USBRead()

    def get_position(self):
        # send command
        self.lac.USBWrite(GET_FEEDBACK, 0)

        # get response
        response = self.lac.USBRead()
        return response

    def set_extend_limits_counts(self, limit):
        if limit > 1024:
            value = 1024
        elif limit < 0:
            value = 0
        else:
            value = limit

        # send command
        self.lac.USBWrite(SET_EXTEND_LIMIT, value)
        # get response
        # self.lac.USBRead()

    def set_retract_limits_counts(self, limit):
        if limit > 100:
            value = 100
        elif limit < 0:
            value = 0
        else:
            value = limit

        # send command
        self.lac.USBWrite(SET_RETRACT_LIMIT, value)
        # get response
        # self.lac.USBRead()

    def set_proportional_gain(self, gain):
        self.lac.USBWrite(SET_GAIN_P, gain)

    def set_derivative_gain(self, gain):
        self.lac.USBWrite(SET_GAIN_D, gain)

    def set_accuracy(self, accuracy):
        self.lac.USBWrite(SET_ACCURACY, accuracy)

    def reset_unit(self):
        # send command
        self.lac.USBWrite(RESET, 0)

        # get response
        # return self.lac.USBRead()


'''
ultimately I want these commands to exist within the LACDriver class:

set_speed()
set_position()
get_position()
set_extend_limits()
set_retract_limits()
and others as necessary.

#Open a FirgelliLAC instance: instance#: 0; stroke: 50mm
LAC = firgelli.FirgelliLAC(0, 50)

#Change some parameters
LAC.set_stall_time(1000) # [milliseconds]
LAC.set_accuracy(1) # [mm]
LAC.set_retract_limit(0) # [mm]

#Set a new position
LAC.set_position(0) # [mm]

#Close read and write handle
LAC.close()

'''
