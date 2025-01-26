button_a_pressed = False
button_b_pressed = False
button_ab_pressed = False

radio.set_group(1)

'''
Movement:
  AB - ParkingBrake (p_Brake)
  B  - Right
  A  - Left
  +60 deg  - Forwards
  -60 deg  - Backwards

Radio Signals:
  -1  - Backwards
  0   - Straight
  1   - Forwards
  2   - Left
  3   - Right
  10  - Parking Brake ON
'''

def on_forever():
    global button_a_pressed, button_b_pressed, button_ab_pressed

    # Button AB is released
    if not input.button_is_pressed(Button.AB) and button_ab_pressed:
        button_ab_pressed = False

    # Button AB is pressed
    if input.button_is_pressed(Button.AB) and not button_ab_pressed:
        radio.send_number(10)
        button_ab_pressed = True

    elif not button_ab_pressed:
        # Button A is pressed
        if button_a_pressed == False and input.button_is_pressed(Button.A) and button_b_pressed == False:
            radio.send_number(2)
            button_a_pressed = True

        # Button A is released
        if button_a_pressed and not input.button_is_pressed(Button.A) and button_b_pressed == False:
            radio.send_number(0)
            button_a_pressed = False

        # Button B is pressed
        if button_b_pressed == False and input.button_is_pressed(Button.B) and button_a_pressed == False:
            radio.send_number(3)
            button_b_pressed = True

        # Button B is released
        if button_b_pressed and not input.button_is_pressed(Button.B) and button_a_pressed == False:
            radio.send_number(0)
            button_b_pressed = False

    # Forwards
    if input.rotation(Rotation.PITCH) > 60:
        radio.send_number(1)
    
    # Backwards
    if input.rotation(Rotation.PITCH) < -60:
        radio.send_number(-1)
    
    basic.pause(150)

basic.forever(on_forever)
