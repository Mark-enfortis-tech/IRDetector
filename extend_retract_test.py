import lac_driver
import time

print('starting extend_retract_test.py')


class Test:
    def __init__(self):
        self.testNum = 0

    def increment(self):
        self.testNum += 1
        return self.testNum


FORWARD = 1
REVERSE = 0
START = 0
RUNNING = 1
STOP = 2
STROKE_LIMIT = 75
BEG_POSITION = 1
TRANSITION_DELAY = 5

# create new driver instance
lac = lac_driver.LACDriver(0, 100)

# set parameters
#lac.set_extend_limits_mm(STROKE_LIMIT)
#lac.set_extend_limits(1000)
time.sleep(.1)
#lac.set_retract_limits_mm(BEG_POSITION)
#lac.set_retract_limits(100)
time.sleep(.1)
#lac.set_speed(1024)
time.sleep(.1)
# lac.set_accuracy(6)
time.sleep(.1)
# lac.set_derivative_gain(2)
time.sleep(.1)
# lac.set_proportional_gain(6)
time.sleep(.1)

# always start at 0 position
#lac.set_position_mm(BEG_POSITION)
#position = lac.get_position_mm()
#print('position is %d (mm)' % position)
#while lac.get_position_mm() >= BEG_POSITION:
 #   #lac.set_position_mm(BEG_POSITION)
  #  position = lac.get_position_mm()
   # print('position is %d (mm)' % position)
   # time.sleep(.5)

# always start at begin position
lac.set_position_mm(BEG_POSITION)
isLooping = True
while isLooping:
    new_position = lac.get_position_mm()
    print('position is %d (mm)' % new_position)
    if abs(new_position - BEG_POSITION) < 1:
        isLooping = False

direction = FORWARD
mode = START
new_position = STROKE_LIMIT
print('stating main loop')
print('mode == START')

# main loop
while 1:
    if mode == START:
        lac.set_position_mm(new_position)
        mode = RUNNING
        print('mode == RUNNING')

    elif mode == RUNNING:
        time.sleep(1)
        current_position = lac.get_position_mm()
        print('current position is %d' % current_position)

        if direction == FORWARD:
            if current_position >= STROKE_LIMIT - 1:  # check limit
                print('at forward limit')
                mode = STOP
                direction = REVERSE
                new_position = BEG_POSITION

        elif direction == REVERSE:
            if current_position <= BEG_POSITION + 1:
                print('at reverse limit')
                mode = STOP
                direction = FORWARD
                new_position = STROKE_LIMIT

    elif mode == STOP:
        time.sleep(TRANSITION_DELAY)
        lac.set_position_mm(new_position)
        mode = RUNNING
