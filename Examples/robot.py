#!/usr/bin/env python3
import wpilib
from xbox import XboxController
from robotpy_ext.autonomous import AutonomousModeSelector
from wpilib.smartdashboard import SmartDashboard
import random
#from pyfrc.sim.pygame_joysticks import UsbJoysticks
#import pygame

# to stay in sync with our driver station
CONTROL_LOOP_WAIT_TIME = 0.025

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        self.controller = XboxController(0)

        self.lmotor = wpilib.CANTalon(0)
        self.rmotor = wpilib.CANTalon(1)

        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        #self.autonomous_modes = AutonomousModeSelector('autonomous')

        # Initialize the smart dashboard display elements
        self.sd = SmartDashboard()
        self.sd.putNumber("Random", 0)          # Send initialization packet

    def sendRandomData(self, upper, lower, step):
        self.sd.putNumber("Random", random.randrange(upper, lower, step))

    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(0.01)              # Wait for 0.01 seconds

    def autonomous(self):
        self.autonomous_modes.run()
        Timer.delay(CONTROL_LOOP_WAIT_TIME)

    def operatorControl(self):
        wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)

        while self.isOperatorControl() and self.isEnabled():

            self.lmotor.set(self.controller.getLeftY())
            self.rmotor.set(self.controller.getRightY())

            self.sendRandomData(-10,10,1)

    def test(self):
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
