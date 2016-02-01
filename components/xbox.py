from wpilib import Joystick, Timer

class XboxController(object):
    """
        Allows usage of an Xbox controller, with sensible names for xbox
        specific buttons and axes.

    """

    def __init__(self, port):
        """
        :param port: The port on the driver station that the controller is
            plugged into.
        :type  port: int
        """
        self.joy = Joystick(port)
        self.debounce = DpadDebouncer()

    def getLeftX(self):
        """Get the left stick X axis

        :returns: -1 to 1
        :rtype: float
        """
        return self.joy.getRawAxis(0)

    def getLeftY(self):
        """Get the left stick Y axis

        :returns: -1 to 1
        :rtype: float
        """
        return self.joy.getRawAxis(1)

    #getX = self.getLeftX()
    #getY = self.getLeftY()

    def getLeftPressed(self):
        """Determines if the left stick is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawButton(9)

    def getPOV(self):
        """Get the state of the D-Pad
        :returns: The angle of the D-Pad in degrees, or -1 if the D-Pad is not pressed.
        :rtype: float
        """

        return self.debounce.get(self.joy.getPOV())

    def getRightX(self):
        """Get the right stick X axis

        :returns: -1 to 1
        :rtype: float
        """
        return self.joy.getRawAxis(4)

    def getRightY(self):
        """Get the right stick Y axis

        :returns: -1 to 1
        :rtype: float
        """
        return self.joy.getRawAxis(5)

    def getRightPressed(self):
        """Determines if the right stick is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawButton(10)

    def getButtonA(self):
        """Gets whether the A button is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawButton(1)

    def getButtonB(self):
        """Gets whether the B button is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawButton(2)

    def getButtonX(self):
        """Gets whether the X button is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawButton(3)

    def getButtonY(self):
        """Gets whether the X button is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawButton(4)

    def getStart(self):
        """Gets whether the Start button is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawButton(8)

    def getBack(self):
        """Gets whether the Back button is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawButton(7)

    def getLeftBumper(self):
        """Gets whether the left bumper is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawButton(5)

    def getRightBumper(self):
        """Gets whether the right bumper is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawButton(6)

    def getLeftTrigger(self):
        """Gets whether the left trigger is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawAxis(2) > 0

    def getRightTrigger(self):
        """Gets whether the right trigger is pressed

        :returns: True if pressed, False otherwise
        :rtype: bool
        """
        return self.joy.getRawAxis(3) > 0

    def rumble(self, left=None, right=None):
        """Sets the rumble amount on one/both side(s) of the controller"""
        if left is not None:
            self.joy.setRumble(Joystick.RumbleType.kLeftRumble_val, left)
        if right is not None:
            self.joy.setRumble(Joystick.RumbleType.kRightRumble_val, right)


class DpadDebouncer(object):
    def __init__(self):
        self.debounce_period = 0.5
        self.last_input = -1
        self.last_timestamp = Timer.getFPGATimestamp()

    def set_debounce_period(self, time):
        self.debounce_period = time

    def get(self, input):
        if input == self.last_input:
            time = Timer.getFPGATimestamp()
            if time - self.last_timestamp <= self.debounce_period:
                return -1
            else:
                self.last_timestamp = time
                return input
        else:
            self.last_input = input
            self.last_timestamp = Timer.getFPGATimestamp()
            return input
