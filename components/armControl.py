"""
File Author: Will Hescott
File Creation Date: 1/28/2015
File Purpose: To control an arm
"""
import wpilib
from wpilib import CANTalon, Timer, DigitalInput, AnalogPotentiometer, PIDController
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

        self.potentiometer = AnalogPotentiometer(0, 270, -11)
        self.pidArm = PIDController(0.0, 0.0, 0.0, 0.0, self.potentiometer, self.armMotor, 0.02)

        self.position = 0

    def armAuto(self, upValue=None , downValue=None, rate=0.3):
        if self.getPOT() <= 0 or self.getPOT() >= 90:
            self.armMotor.set(0)

        if upValue == 1:
            self.armMotor.set(rate * -1)
        if downValue == 1:
            self.armMotor.set(rate)

    def armUpDown(self, left, right, rate=0.3):
        if(self.backSwitch.get() == False or self.frontSwitch.get() == False): #Checking limit switches
            self.armMotor.set(0)

        if(self.backSwitch.get() == True and left >= 0.75):#if tripped, disallow further movement
            self.armMotor.set(rate)
        elif(self.frontSwitch.get() == True and right >= 0.75):#if tripped, disallow further movement
            self.armMotor.set(rate * -1)
        elif(left < 0.75 and right < 0.75):
            self.armMotor.set(0)

    '''
    # Arm movement function with using PID control
    def armUpDownPID(self, left, right, rate=0.03):
        if(self.backSwitch.get() == False or self.frontSwitch.get() == False):
            self.armMotor.set(0)

        #moves the arm up and down, as well as outputting potentiometer info to dashboard
        if(self.backSwitch.get() == True and left >= 0.75):
            self.position += rate
        elif(self.frontSwitch.get() == True and right >= 0.75):
            self.position -= rate

    '''
    
    def wheelSpin(self, speed = 1):
        self.wheelMotor.set(speed)

    def getPOT(self):
        return self.potentiometer.get()

    def getBackSwitch(self):
        return self.backSwitch.get()

    def getFrontSwitch(self):
        return self.frontSwitch.get()
