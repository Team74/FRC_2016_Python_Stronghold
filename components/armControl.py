"""
File Author: Will Hescott, Will Lowry
File Creation Date: 1/28/2015
File Purpose: To control an arm
"""

import wpilib
from wpilib import CANTalon, Timer, DigitalInput, AnalogPotentiometer, PIDController, Compressor
from . import Component

class arm(Component):
    #set up variables
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.armMotor = CANTalon(4)
        self.wheelMotor = CANTalon(5)
        self.frontSwitch = DigitalInput(8)
        self.backSwitch = DigitalInput(9)
        self.comp = Compressor()
        self.comp.enabled()

        self.armMotor.enableBrakeMode(True)
        self.wheelMotor.enableBrakeMode(True)

        self.potentiometer = AnalogPotentiometer(3, 270, -193)
        #self.pidArm = PIDController(0.0, 0.0, 0.0, 0.0, self.potentiometer, self.armMotor, 0.02)

        self.position = 0

    def armAuto(self, upValue, downValue, target, rate=0.3):
        '''
        if self.getPOT() <= target:
            self.armMotor.set(0)
        '''
        if upValue == 1:
            self.armMotor.set(rate * -1)
        elif downValue == 1:
            self.armMotor.set(rate)
        else:
            self.armMotor.set(0)

    def armUpDown(self, left, right, controllerA, rate=0.3):
        rate2 = rate*1.75
        if(self.backSwitch.get() == False or self.frontSwitch.get() == False): #Checking limit switches
            self.armMotor.set(0)

        if(left >= 0.75):#if tripped, disallow further movement
#            if(controllerA == True):
#                self.armMotor.set(rate2)
#            else:
            self.armMotor.set(rate)
        elif(right >= 0.75):#if tripped, disallow further movement
#            if(controllerA == True):
#                self.armMotor.set(-rate2)
#            else:
            self.armMotor.set(rate * -1)
        elif(left < 0.75 and right < 0.75):
            self.armMotor.set(0)

    def wheelSpin(self, speed):
        currentSpeed = 0
        if (speed > 0.75):
            currentSpeed = -1
        elif(speed < -0.75):
            currentSpeed = 1
        self.wheelMotor.set(currentSpeed)

    def getPOT(self):
        return (self.potentiometer.get()*-1)

    def getBackSwitch(self):
        return self.backSwitch.get()

    def getFrontSwitch(self):
        return self.frontSwitch.get()
