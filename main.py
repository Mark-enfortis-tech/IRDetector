import usb.core
import usb.util
import sys
import usb.backend.libusb1
import time
from lac_driver import LACDriver

# Device
# Configuration
# Interface
# Alternate setting
# Endpoint


usb.core.find()

VENDOR_LAC = 0x04d8
PRODUCT_LAC = 0xfc5f

# lac = LACDriver(pid=0x04d9, vid=0xfc5f)
print('running main.py')

#
# device
#
dev = usb.core.find(idVendor=VENDOR_LAC, idProduct=PRODUCT_LAC)
# device = lac.find_device()


if dev is None:
    raise ValueError('LAC device is not found. ')
    sys.exit(1)
else:
    print('found device 0x%x, product 0x%x' % (VENDOR_LAC, PRODUCT_LAC))

#
# configuration
#
# configuration = device.get_active_configuration()
dev.set_configuration()
print('configuration set')

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

print('dev info:')
print('\tbLength \t\t\t0x%x' % dev.bLength)
print('\tbNumConfigurations \t0x%x' % dev.bNumConfigurations)
print('\tbDeviceClass \t\t0x%x' % dev.bDeviceClass)
print()

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match= \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

assert ep is not None

#print('endpoint info')
#print(ep)


'''
print('enumerating bEndpointAddresses')
dev1 = usb.core.find()
for cfg1 in dev1:
    for i in cfg1:
        for e in i:
            print('0x%x' % e.bEndpointAddress)
'''


#
# COMMANDS   protocol = command, lowB, highB

set_retract_limit_command = '\x02\x33\x00'        # 5mm   = 5*1024/100 = 51d  or 0x33
set_extend_limit_command = '\x03\xcc\x03'                       # 95mm  = 95*1024/ 100
pos_command_10 = '\x20\x10\x00'
pos_command_50 = '\x20\x10\x02'
get_pos_command = '\x10\x00\x00'

speed_command_50 = '\x21\x10\x02'

dev.write(1, speed_command_50, 100)
byteread = dev.read(0x81, 1000)

print(byteread)
for b in byteread:
    print('0x%x' % b)


dev.write(1, pos_command_50, 100)
byteread = dev.read(0x81, 1000)

time.sleep(5)
dev.write(1, get_pos_command, 100)
byteread = dev.read(0x81, 1000)
print('byteread 0x%x 0x%x 0x%x' % (byteread[0], byteread[1], byteread[2]))




