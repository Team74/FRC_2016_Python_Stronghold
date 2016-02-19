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
        self.potentiometer = AnalogPotentiometer(0, 270, 0)
        self.pidArm = PIDController(0.0, 0.0, 0.0, 0.0, self.potentiometer, self.armMotor, 0.02)
        self.position = 0

    def armUpDown(self, left, right, rate=0.3):
        #if(left > 0.75= or right >= 0.75):
        #    armValue = (left - right)

        if(self.backSwitch.get() == False or self.frontSwitch.get() == False): #Checking limit switches
            self.armMotor.set(0)

        if(self.backSwitch.get() == True and left > 0.75):#if tripped, disallow further movement
            self.armMotor.set(rate * -1)
        elif(self.frontSwitch.get() == True and right > 0.75):#if tripped, disallow further movement
            self.armMotor.set(-rate)
        elif(left < 0.75 and right < 0.75):
            self.armMotor.set(0)

    # Arm movement function with using PID control
    def armUpDownPID(self, left, right, rate=0.3):
        if(self.backSwitch.get() == False or self.frontSwitch.get() == False):
            self.pidArm.SetSetpoint(position)
            self.armMotor.set(0)
                #moves the arm up and down, as well as outputting potentiometer info to dashboard
        if(self.backSwitch.get() == True and armValue < 0):
            self.position += rate
            self.pidArm.SetSetpoint(position)
        elif(self.frontSwitch.get() == True and armValue > 0):
            self.position -= rate
            self.pidArm.SetSetpoint(position)

    def wheelSpin(self, speed):
        self.wheelMotor.set(speed)

    def getPOT(self):
        return self.potentiometer.get()

    def getBackSwitch(self):
        return self.backSwitch.get()

    def getFrontSwitch(self):
        return self.frontSwitch.get()
