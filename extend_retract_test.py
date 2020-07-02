import lac_driver
import time
print('starting extend_retract_test.py')

FORWARD = 1
REVERSE = 0

# create new driver instance
lac = lac_driver.LACDriver(0, 100)

# set parameters
# lac.set_extend_limits_counts(100)
time.sleep(.1)
# lac.set_retract_limits_counts(5)
time.sleep(.1)
# lac.set_speed(1000)
time.sleep(.1)
# lac.set_accuracy(6)
time.sleep(.1)
# lac.set_derivative_gain(2)
time.sleep(.1)
# lac.set_proportional_gain(6)
time.sleep(.1)

# always start at 0 position
lac.set_position(0)
position = lac.get_position()
print('position is %d' % position)

direction = FORWARD
print('stating main loop')

# main loop
while 1:
    if direction == FORWARD:
        if lac.get_position() < STROKE_LIMIT:
            new_position += INCREMENT
        else:
            direction = REVERSE

    if direction == REVERSE:
        if new_position > INCREMENT:
            new_position -= INCREMENT
        else:
            direction = FORWARD

    print('position changed to %d' % new_position)
    lac.set_position(new_position)
    time.sleep(3)
    position = lac.get_position()
    print('actual position is %d' % position)
    time.sleep(1)
    print("test %d " % testVal.increment())