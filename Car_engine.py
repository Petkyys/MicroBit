
direction = 10
steering = 0

radio.set_group(1)

'''
Radio Signals:
  -1  - Backwards
  0   - Straight
  1   - Forwards
  2   - Left
  3   - Right
  10  - Parking brake on

  Made by: Daniel Peterka 5A6
'''

basic.show_leds("""
. . . . .
. . . . .
# # # # #
. . . . .
. . . . .
""")


# Vehicle control unit
def control_vehicle():
    global direction, steering

    # Movement control
    if direction == 1:            # Forwards
        if steering == 2:         # Turn left
            RingbitCar.turnleft()
        elif steering == 3:       # Turn right
            RingbitCar.turnright()
        else:
            RingbitCar.forward()  # Forwards

    elif direction == -1:         # Backwards
        if steering == 2:         # Turn left
            RingbitCar.turnleft()
        elif steering == 3:       # Turn right
            RingbitCar.turnright()
        else:
            RingbitCar.back()     # Backwards

    elif direction == 10:
        RingbitCar.brake()        # Stop


# Decode radio input
def on_received_number(receivedNumber):
    global direction, steering

    if receivedNumber in [-1, 10, 1]:
        if direction != receivedNumber:
            direction = receivedNumber
            control_vehicle()

    elif receivedNumber in [0, 2, 3]:
        if steering != receivedNumber:
            steering = receivedNumber
            control_vehicle()

radio.on_received_number(on_received_number)
