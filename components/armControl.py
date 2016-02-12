"""
File Author: Will Hescott
File Creation Date: 1/28/2015
File Purpose: To control an arm
"""
import wpilib
from wpilib import CANTalon, Timer, AnalogPotentiometer
from . import Component

class arm(Component):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.armMotor = CANTalon(4)
        self.wheelMotor = CANTalon(5)
        self.potentiometer = AnalogPotentiometer(0, 90, 0)
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
        motorValue = left - right
#        if(self.potentiometer.get() == 85 or self.potentiometer == 5):
#            if(motorValue < 0):
#                motorValue = -0.1
#            if(motorValue > 0):
#                motorValue = 0.1
        self.armMotor.set(motorValue)

    def wheelSpin(self, value):
        self.wheelMotor.set(value)

    def sendPOT(self):
        return self.potentiometer.get()
