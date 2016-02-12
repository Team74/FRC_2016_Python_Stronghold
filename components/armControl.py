"""
File Author: Will Hescott
File Creation Date: 1/28/2015
File Purpose: To control an arm
"""
import wpilib
from wpilib import CANTalon, Timer
from . import Component

class arm(Component):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.armMotor = CANTalon(4)
        self.wheelMotor = CANTalon(5)
        while self.armMotor.isSafetyEnabled():
            self.armMotor.setSafetyEnabled(False)

    def armUpDown(self, zval, rate=0.3):
        self.armMotor.set(zval)
        '''
        if(abs(zval) >= 0.5):       #Activate only on sufficiently pressed-down trigger
            self.armMotor.set(abs(zval)/zval*rate)  #sign(zval)*rate
        else:
            self.armMotor.set(0)
        '''

    def armUpDown2(self, left, right, rate=0.3):
        self.armMotor.set((left - right))

    def wheelSpin(self, value):
        self.wheelMotor.set(value)
