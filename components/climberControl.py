"""
File Author: Will Hescott
File Creation Date: 1/28/2015
File Purpose: To control an arm
"""
import wpilib
from wpilib import Solenoid, Timer
from . import Component

class lift(Component):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.cylinder1Up = Solenoid(6, 4)
        self.cylinder1Down = Solenoid(6, 5)
        self.cylinder2Up = Solenoid(6, 6)
        self.cylinder2Down = Solenoid(6, 7)
        self.ARM_STATUS = False
        self.BOTH_HELD = False

    def climbUpDown(self, leftButtonPressed, rightButtonPressed):
        if(rightButtonPressed == True and leftButtonPressed == True and self.BOTH_HELD == False):
            self.BOTH_HELD = True

            # Toggle arm status
            if(self.ARM_STATUS == False):
                self.ARM_STATUS = True
            elif(self.ARM_STATUS == True):
                self.ARM_STATUS = False

            # Set cylinder to up or down... Don't break plz!!!
            self.cylinder1Up.set(self.ARM_STATUS)
            self.cylinder1Down.set(not self.ARM_STATUS)
            self.cylinder2Up.set(self.ARM_STATUS)
            self.cylinder2Down.set(not self.ARM_STATUS)

        # Reset the button held flag
        elif(rightButtonPressed == False and leftButtonPressed == False):
            self.BOTH_HELD = False
