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
        self.solenoid1 = Solenoid(6, 0)##NOT REAL VARIABLES, REPLACE LATER.
        self.solenoid2 = Solenoid(6, 1)
        self.ARM_STATUS = False
        self.BOTH_HELD = False

    def climbUpDown(self, leftButtonPressed, rightButtonPressed):
        '''
        if(rightButtonPressed == True):
            self.solenoid1.set(True)
            self.solenoid2.set(False)
        elif(leftButtonPressed == True):
            self.solenoid1.set(False)
            self.solenoid2.set(True)
        '''


        if(rightButtonPressed == True and leftButtonPressed == True and self.BOTH_HELD == False):
            self.BOTH_HELD = True
            if(self.ARM_STATUS == False):
                self.ARM_STATUS = True
            elif(self.ARM_STATUS == True):
                self.ARM_STATUS = False
            self.solenoid1.set(self.ARM_STATUS)
            self.solenoid2.set(not self.ARM_STATUS)
        elif(rightButtonPressed == False and leftButtonPressed == False):
            self.BOTH_HELD = False
