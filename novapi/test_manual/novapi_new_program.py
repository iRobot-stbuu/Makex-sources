import novapi
from mbuild import gamepad
from mbuild import power_expand_board
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild.smartservo import smartservo_class
from mbuild.encoder_motor import encoder_motor_class

# initialize the variables
auto_stage = 0
shoot = 0
invert = 0
feeddc = 1
lrmode = 0 # Differentiate between shoot and arm control mode

# Sensors
dual_rgb_sensor_1 = dual_rgb_sensor_class("PORT2", "INDEX1")
dual_rgb_sensor_2 = dual_rgb_sensor_class("PORT2", "INDEX2")

# Arm
smartservo_arm = smartservo_class("M6", "INDEX1")

# Turret
smartservo_updown = smartservo_class("M5", "INDEX1")

# Bot motors
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")


def AutoStart():
    global auto_stage
    pass


def Manual():
    global auto_stage
    global invert
    global lrmode
    global feeddc
    LoadMe()
    while True:
        time.sleep(0.001)
        JoyRes.MovingJoystick(invert)
        ManualRes.InvertLED(invert)
        ManualRes.ControlLED(lrmode)
        JoyRes.MultiControl(lrmode)

        if gamepad.is_key_pressed("Up"):
            ManualRes.MoveForward()

        if gamepad.is_key_pressed("Down"):
            ManualRes.MoveBackward()

        if gamepad.is_key_pressed("Left"):
            ManualRes.MoveLeft()

        if gamepad.is_key_pressed("Right"):
            ManualRes.MoveRight()

        if gamepad.is_key_pressed("N1"):
            smartservo_arm.move(10, 10)

        if gamepad.is_key_pressed("N2"):
            pass

        if gamepad.is_key_pressed("N3"):
            if feeddc == 0:
                feeddc = 1
            else:
                feeddc = 0
            while not not gamepad.is_key_pressed("N3"):
                pass
            pass

        if gamepad.is_key_pressed("N4"):
            smartservo_arm.move(-10, 10)

        # Switch shooting to arm control
        if gamepad.is_key_pressed("R2"):
            if lrmode == 0:
                lrmode = 1
            else:
                lrmode = 0
            while not not gamepad.is_key_pressed("R2"):
                pass
        # Invert control direction
        if gamepad.is_key_pressed("R_Thumb"):
            if invert == 0:
                invert = 1
            else:
                invert = 0
            while not not gamepad.is_key_pressed("R_Thumb"):
                pass

        # Dc feed
        if feeddc == 1:
            power_expand_board.set_power("DC2", -100)
        else:
            power_expand_board.stop("DC2")


def LoadMe():
    global auto_stage

    smartservo_arm.set_power(50)
    smartservo_arm.move(30, 10)
    power_expand_board.set_power("BL1", 50)
    power_expand_board.set_power("DC1", 50)
    power_expand_board.stop("BL1")
    power_expand_board.stop("DC1")


class JoyRes:
    def __init__(self):
        pass

    def MovingJoystick(invert):
        global auto_stage

        # Code for bot movement from left to right.
        # If the bot starts slipping to unwanted direction. Tune variables here
        Lx = gamepad.get_joystick("Lx")  # literally Lx variable
        Fl = 0   # Front left
        Fr = 0   # Front right
        Rl = 0   # Rear left
        Rr = 0   # Rear right

        # Adjust LR slide tuning here
        if gamepad.get_joystick("Lx") != 0:

            if gamepad.get_joystick("Lx") < 0:
                Fl = Lx + 10
            if gamepad.get_joystick("Lx") > 10:
                Fl = Lx - 10

            Fr = Lx + Fr
            Rl = Lx + Rl
            Rr = Lx + Rr
        # Encoder values. If the encoder motors config are changed even the slightest. change this one first then the inverted controls
        EFl = 1 * (gamepad.get_joystick("Ly")
                   + Fl - gamepad.get_joystick("Rx"))
        EFr = -1 * (gamepad.get_joystick("Ly") - Fr
                    + gamepad.get_joystick("Rx"))
        ERl = 1 * (gamepad.get_joystick("Ly") - Rl
                   - gamepad.get_joystick("Rx"))
        ERr = -1 * (gamepad.get_joystick("Ly") + Rr
                    + gamepad.get_joystick("Rx"))

        if invert == 1:  # If the controls are inverted The arms are now the bot's front
            ERr = 1 * (gamepad.get_joystick("Ly")
                       - Fl - gamepad.get_joystick("Rx"))
            ERl = -1 * (gamepad.get_joystick("Ly") + Fr
                        + gamepad.get_joystick("Rx"))
            EFr = 1 * (gamepad.get_joystick("Ly") + Rl
                       - gamepad.get_joystick("Rx"))
            EFl = -1 * (gamepad.get_joystick("Ly") - Rr
                        + gamepad.get_joystick("Rx"))
        encoder_motor_M1.set_power(EFl)
        encoder_motor_M2.set_power(EFr)
        encoder_motor_M3.set_power(ERl)
        encoder_motor_M4.set_power(ERr)

    def TurretControl():
        global auto_stage
        # > 40 < 60
        #if smartservo_updown.get_value("angle") > -43:
        #    smartservo_updown.move(-1, 10)

        #if smartservo_updown.get_value("angle") < -60:
        #    smartservo_updown.move(1, 10)
        #else:
        if smartservo_updown.get_value("angle") < -56:
            servo_value = smartservo_updown.get_value("angle")
            while servo_value < -56:
                smartservo_updown.move(3, 10)
                servo_value = smartservo_updown.get_value("angle")

        smartservo_updown.move(-gamepad.get_joystick("Ry"), 10)

    def FeedControl():
        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power("DC1", -100)
        elif gamepad.is_key_pressed("L2"):
            power_expand_board.set_power("DC1", 100)
        else:
            power_expand_board.stop("DC1")
            0

    def ShootControl():
        if gamepad.is_key_pressed("R1"):
            power_expand_board.set_power("DC3", -100)
        else:
            power_expand_board.stop("DC3")

    def GrabControl():
        # DC4 L1 release R1 grab
        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power("DC4", 50)

        elif gamepad.is_key_pressed("R1"):
            power_expand_board.set_power("DC4", -50)
        else:
            power_expand_board.stop("DC4")
        pass

    def HandControl():

        smartservo_arm.move(gamepad.get_joystick("Ry"), 10)
        pass

    def MultiControl(lc):
        if lc == 0:
            # Gun control mode
            JoyRes.TurretControl()
            JoyRes.ShootControl()
            JoyRes.FeedControl()
            power_expand_board.set_power("BL1", 20)
            power_expand_board.set_power("BL2", 20)
        else:
            # Hand control mode
            JoyRes.HandControl()
            JoyRes.GrabControl()
            power_expand_board.stop("BL1")
            power_expand_board.stop("BL2")


class ManualRes:
    def __init__(self):
        pass
    # Miscellaneous

    def InvertLED(i):
        if i != 0:
            dual_rgb_sensor_1.set_led_color("red")
        else:
            dual_rgb_sensor_1.set_led_color("green")

    def ControlLED(k):
        if k != 0:
            dual_rgb_sensor_2.set_led_color("red")
        else:
            dual_rgb_sensor_2.set_led_color("green")
    # Joystick Controls

    def MoveBackward():
        global auto_stage
        encoder_motor_M1.set_power(-50)
        encoder_motor_M2.set_power(50)
        encoder_motor_M3.set_power(-50)
        encoder_motor_M4.set_power(50)

    def MoveForward():
        global auto_stage
        encoder_motor_M1.set_power(50)
        encoder_motor_M2.set_power(-50)
        encoder_motor_M3.set_power(50)
        encoder_motor_M4.set_power(-50)

    def MoveRight():
        global auto_stage
        encoder_motor_M1.set_power(50)
        encoder_motor_M2.set_power(50)
        encoder_motor_M3.set_power(-50)
        encoder_motor_M4.set_power(-50)

    def MoveLeft():
        global auto_stage
        encoder_motor_M1.set_power(-50)
        encoder_motor_M2.set_power(-50)
        encoder_motor_M3.set_power(50)
        encoder_motor_M4.set_power(50)

    def StopMoving():
        global auto_stage
        encoder_motor_M1.set_power(0)
        encoder_motor_M2.set_power(0)
        encoder_motor_M3.set_power(0)
        encoder_motor_M4.set_power(0)


auto_stage = 1
while True:
    time.sleep(0.001)
    if auto_stage == 1:
        AutoStart()
        auto_stage = 0

    else:
        smartservo_arm.move_to(0, 10)
        Manual()