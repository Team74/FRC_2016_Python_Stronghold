"""
File Author: Will Hescott
File Creation Date: 1/28/2015
File Purpose: To control an arm
"""
import wpilib
from wpilib import CANTalon, Timer, DigitalInput, AnalogPotentiometer, PIDController
from . import Component

class arm(Component):

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
        armValue = (left - right)

        if(self.backSwitch == False or self.frontSwitch == False):
            self.armMotor.set(0)

        if(self.backSwitch == True and armValue < 0):
            self.armMotor.set(armValue)
        elif(self.frontSwitch == True and armValue > 0):
            self.armMotor.set(armValue)

    # Arm movement function with using PID control
    def armUpDownPID(self, left, right, rate=0.3):
        if(self.backSwitch == False or self.frontSwitch == False):
            self.pidArm.SetSetpoint(position)
            self.armMotor.set(0)

        if(self.backSwitch == True and armValue < 0):
            self.position += rate
            self.pidArm.SetSetpoint(position)
        elif(self.frontSwitch == True and armValue > 0):
            self.position -= rate
            self.pidArm.SetSetpoint(position)

    def wheelSpin(self, speed):
        self.wheelMotor.set(speed)

    def getPOT(self):
        return self.potentiometer.get()
